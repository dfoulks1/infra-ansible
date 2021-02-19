# infra-ansible
A proof of concept for Ansible at the Apache Software Foundation

## To Do:

* Hetzner needs an API key for the hetzner script to work
    * Once that's done we can extract names from the output and do the name based sorting.

* Leaseweb can use cloudmonkey(?) to list the instances in our private cloud.

## Inventory

* The inventory is entirely dynamic, relying on python scripts to query each of our cloud providers.
* In order to run the inventory scripts, the modules in requirements.txt _must_ be installed.
* Once a list of names is retrieved from a cloud provider, each script populates groups using name regex matching.
* Each inventory script can be run, on its own, with --list or --host <HOSTNAME>

### Inventory variables

In the root of the inventory directory there are two directories: host_vars and group_vars, that contain all of the variables defined outside of a
role. Inside of the variables directories I've organized the vars files by datacenter. These are automagically associated when the inventory is built.


### Meta-grouping

Each cloud provider having its own directory simplifies organizing meta-grouping files relevant to that specific DC. The metagroups file is prefixed with `zz_` 
because ansible processes each file in an inventory directory in alphabetical order. The script must populate the base groups before they can then be organized
into meta-groups.

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


