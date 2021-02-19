# infra-ansible
A proof of concept for Ansible at the Apache Software Foundation

## Inventory

* The inventory is entirely dynamic, relying on python scripts to query each of our cloud providers.
* Once a list of names is retrieved from a cloud provider, each script populated groups using name regex matching.
* Each inventory script can be run, on its own, with --list or --host <HOSTNAME>

### Inventory variables and meta-grouping

Each cloud provider having its own directory simplifies organizing meta-grouping files as well as variable files relevant to that specific DC.

NOTE:
the metagroups file is prefixed with `zz_` because ansible processes each file in an inventory directory in alphabetical order. The script must populate
the base groups before they can then be organized into meta-groups.

### Required Python Packages:
| *Provider* | *API Package* |
| AWS | boto3 |
| Hetzner | hcloud |
| LeaseWeb | cloudmonkey |
| Azure | |

## Ansible as config management / enforcement tool

[Ansible-pull][https://docs.ansible.com/ansible/latest/cli/ansible-pull.html] allows administrators to have managed nodes pull the configuration that relates to them from a github (or other) VCSrepo and apply it.

While this is useful, it does not do the same thing as puppet's agent. ansible-pull is done on a cron basis and is only capable of running a job named local.yaml in the root of the repository.

We can leverage local.yaml and ansible's var fetching where FQDN == {{ inventory_hostname }} in order to dynamically enforce configuration management.


