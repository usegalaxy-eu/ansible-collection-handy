usegalaxy_eu.handy.powertools
=======

Ansible role for enabling PowerTools repository in a RedHat/CentOS system.

Requirements
------------
Ansible >= 2.11

Role Variables
--------------
See [defaults/main.yml](defaults/main.yml).

Playbook usage example
-------------
```
- hosts: localhost
  become: true
  collections:
    - usegalaxy_eu.handy
  roles:
    - powertools
```
     
License
-------
GPLv3

Author Information
------------------
[Galaxy Europe](https://galaxyproject.eu)
