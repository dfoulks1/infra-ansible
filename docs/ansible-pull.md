# Ansible as config management / enforcement tool

[Ansible-pull][https://docs.ansible.com/ansible/latest/cli/ansible-pull.html] allows administrators to have managed nodes pull the configuration that relates to them from a github (or other) VCSrepo and apply it.

While this is useful, it does not do the same thing as puppet's agent. ansible-pull is done on a cron basis and is only capable of running a job named local.yaml in the root of the repository.

We can leverage local.yaml and ansible's var fetching where FQDN == {{ inventory_hostname }} in order to dynamically enforce configuration management.

