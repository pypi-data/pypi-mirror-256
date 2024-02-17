from echobox.tool import system
from echobox.tool import template

SYSTEMD_FOLDER = '/etc/systemd/system'


def reinstall_systemd_service(service_name, template_path, payload=None):
    service_fpath = _build_service_fpath(service_name=service_name)

    template_payload = {'payload': payload}
    template.render_to_file(template_path, template_payload, service_fpath)

    cmd_list = [
        f'chmod 664 {service_fpath}',
        'systemctl daemon-reload',
        f'systemctl enable {service_name} --now',
        f'systemctl status {service_name} --no-pager'
    ]
    system.shell_run(cmd_list)


def remove_systemd_service(service_name):
    cmd_list = [
        f'systemctl disable {service_name}',
        f'systemctl stop {service_name}',
        f'systemctl status {service_name} --no-pager',
        f'unlink {_build_service_fpath(service_name)}',
    ]
    system.shell_run(cmd_list)


def _build_service_fpath(service_name):
    return f'{SYSTEMD_FOLDER}/{service_name}.service'
