usegalaxy_eu.handy.os_setup
=======


This role provides numerous useful setup for a Galaxy Server running into a RedHat/CentOS system.
Requirements
------------
Ansible >= 2.11

Role Variables
--------------
See [defaults/main.yml](defaults/main.yml).

Tasks
-----
* powertools: enables PowerTools repository
* remap_user: rearranges the 999:999 user:group so that is free for the galaxy user

Playbook usage example
-------------
By default, all tasks are disabled
```
- hosts: localhost
  become: true
  roles:
    - role: usegalaxy_eu.handy.os_setup
      vars:
        enable_powertool: True
        enable_remap_user: True
```
     
License
-------
GPLv3

Author Information
------------------
[Galaxy Europe](https://galaxyproject.eu)
