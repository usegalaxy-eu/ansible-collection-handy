usegalaxy_eu.handy.os_setup
=======


This role provides numerous useful setup for a Galaxy Server running into a RedHat/CentOS system.
Requirements
------------
ansible-core >= 2.11
[community.general](https://galaxy.ansible.com/community/general) >= 4.0.2

Role Variables
--------------
See [defaults/main.yml](defaults/main.yml).

Tasks
-----
* hostname: set a hostname
* powertools: enables PowerTools repository
* remap_user: rearranges the 999:999 user:group so that is free for the galaxy user
* create_user: adds a group nad user
* exclude_packages: exclude package inside a custom repo file
* kernel_5: install kernel-{lt, ml} package from ELRepo repo
* pam_limits: prevent user from creating files larger than n TB
* grub: add a grub option needed to visualize VM's logs into the OpenStack dashboard
* cgroups: install and enable cgroups ⚠️ cgroupsv2 are default in Rocky 9 so this is not used
* journald: configure journald
* install_software: install software from a list of groups
* ansible_root_cron: install cron tasks as root

Playbook usage example
-------------
By default, all tasks are disabled
```
- hosts: localhost
  become: true
  vars:
    hostname: full_hostname

  roles:
    - role: usegalaxy_eu.handy.os_setup
      vars:
        enable_hostname: true
        enable_powertool: true
        enable_remap_user: false
        enable_exclude_packages: false
        enable_kernel_5: false
```
     
License
-------
GPLv3

Author Information
------------------
[Galaxy Europe](https://galaxyproject.eu)
