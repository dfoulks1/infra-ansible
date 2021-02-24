# Ansible as config management / enforcement tool

[Ansible-pull][https://docs.ansible.com/ansible/latest/cli/ansible-pull.html] allows administrators to have managed nodes pull the configuration that relates to them from a github (or other) VCSrepo and apply it.

While this is useful, _**it does not do the same thing as puppet's agent**_. ansible-pull is done on a cron basis and is only capable of running a job named local.yaml in the root of the repository.

We can however, leverage local.yaml and ansible's var fetching where FQDN == {{ inventory_hostname }} in order to dynamically enforce configuration management in much the same way that puppet agent does.

In theory we could even go so far as to have a pubsub mechanism watching the ansible repository to use ansible to force everything that it is aware of to perform and ansible-pull action.

Those two mechanisms, together would get us pretty close to where puppet has us right now.

