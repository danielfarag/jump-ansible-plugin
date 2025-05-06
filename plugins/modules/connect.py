import os
from pathlib import Path
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(argument_spec=dict(
        bastion=dict(type='str', required=True),
        pem_path=dict(type='str', required=True),
        ip=dict(type='list', required=True, elements='str'),
    ))

    bastion = module.params['bastion']
    pem_path = module.params['pem_path']
    ip_list = module.params['ip']

    private_path = os.path.expanduser("~/.ssh/config")

    if os.path.exists(private_path) == False:
        Path(private_path).touch()

    lines =""
    with open(private_path, 'r') as file:
        lines = file.read().splitlines()

    content = ""

    if "Host bastion" not in lines:
        content=f"""
Host bastion
    HostName {bastion}
    User ubuntu
    IdentityFile {pem_path}

"""
    for ip in ip_list:
        
        if f"Host {ip}" not in lines:
            content += f"""
Host {ip}
    HostName {ip}
    User ubuntu
    IdentityFile {pem_path}
    ProxyJump bastion

"""

    with open(private_path, 'a') as f:
        f.write(content)

    module.exit_json(
        changed=True,
        message="Public key copied to all instances",
        hosts=ip_list
    )

if __name__ == '__main__':
    main()



