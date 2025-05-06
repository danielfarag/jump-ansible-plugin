import subprocess
import paramiko
import os

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(argument_spec=dict(
        pem_path=dict(type='str', required=True),
        ip=dict(type='list', required=True, elements='str'),
    ))

    pem_path = module.params['pem_path']
    ip_list = module.params['ip']

    private_path = os.path.expanduser("~/.ssh/id_rsa")

    if os.path.exists(private_path) == False:
        subprocess.run('ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""', shell=True, check=True)

    # # Run the shell script
    key = paramiko.RSAKey.from_private_key_file(pem_path)
    for ip in ip_list:
        ssh = paramiko.SSHClient()

        known_hosts = f"""
        if ! ssh-keygen -F "{ip}" > /dev/null; then
            ssh-keyscan -H "{ip}" >> {os.path.expanduser("~/.ssh/known_hosts")}
        fi
        """

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(hostname=ip, username='ubuntu', pkey=key)
            subprocess.run(known_hosts, shell=True, check=True)


            with open(os.path.expanduser(os.path.expanduser("~/.ssh/id_rsa.pub")), 'r') as f:
                public_key = f.read().strip()


            ssh.exec_command('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
            ssh.exec_command(f'grep -qxF "{public_key}" ~/.ssh/authorized_keys || echo "{public_key}" >> ~/.ssh/authorized_keys')
            ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
            
            ssh.close()
        except Exception as e:
            module.fail_json(msg=f"Failed to connect or configure {ip}: {str(e)}")


    module.exit_json(
        changed=True,
        message="Public key copied to all instances",
        hosts=ip_list
    )

if __name__ == '__main__':
    main()



