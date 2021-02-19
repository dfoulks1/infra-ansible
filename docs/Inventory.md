# Inventory

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
