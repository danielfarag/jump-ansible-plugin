# 📦 iti.jump Ansible Plugin ([Sample -> Terraform + Ansible + Jenkins ](https://github.com/DanielFarag/aws-bastion-ssh-setup))

This Ansible plugin simplifies the process of connecting to private EC2 instances through a bastion host. It automates SSH config generation and public key distribution, allowing seamless SSH access from a bastion to private instances.

## 🧩 Plugin Components

### 1. `iti.jump.connect`

* Creates entries in `~/.ssh/config` to enable SSH ProxyJump through a bastion host.
* Ensures SSH config file exists and appends required entries only if missing.

#### Parameters:

* `bastion`: Public IP or hostname of the bastion.
* `pem_path`: Path to the bastion’s `.pem` key file.
* `ip`: List of private instance IPs.

---

### 2. `iti.jump.setup`

* Ensures an RSA key exists locally.
* Uses `paramiko` to connect to each private EC2 and appends the local public key to `~/.ssh/authorized_keys` on the instances.
* Ensures idempotent setup (avoids duplicating the key).

#### Parameters:

* `pem_path`: Path to the `.pem` file used to connect to private instances.
* `ip`: List of private IPs of the instances.

---

## 📁 Sample Ansible Playbook

```yaml
- name: connection bastion to private service via ssh
  hosts: bastion
  become: true
  gather_facts: false
  tasks:
    - name: Install pip3
      apt:
        name: python3-pip
        state: present
        update_cache: yes

    - name: Install paramiko using pip3
      pip:
        name: paramiko
        executable: pip3
        state: present

- name: configure bastion with private ec2
  hosts: bastion
  gather_facts: false
  vars_files:
    - vars.yaml
  tasks:
    - name: copy pem file into bastion server
      copy:
        src: "{{ pem_file }}" 
        dest:  "{{ pem_path_dest }}"
        mode: "0400"

    - name: allow seamless connection between bastion server & private ec2s
      iti.jump.setup:
        pem_path: "{{ pem_path_dest }}"
        ip: "{{ private_ips }}"

    - name: configure ssh config
      delegate_to: localhost
      iti.jump.connect:
        bastion: "{{ bastion }}"
        pem_path: "{{ pem_file }}"
        ip: "{{ private_ips }}"
```

---

## 📄 Example `vars.yaml`

```yaml
pem_file: /path/to/bastion-key.pem
pem_path_dest: /home/ubuntu/bastion-key.pem
bastion: 54.12.34.56
private_ips:
  - 10.0.1.10
  - 10.0.1.11
```

---

## 🔧 Requirements

* Python 3
* Ansible
* `paramiko` (auto-installed via pip)
* A Linux host with SSH access
---

## ✅ Summary

This plugin automates:

* Secure copying of SSH keys
* Bastion-to-private instance SSH access using ProxyJump
* Safe and minimal edits to SSH config
