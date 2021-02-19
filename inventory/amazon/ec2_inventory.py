#!/usr/bin/python3

import json
import argparse
import re

import boto3

# NAME REGEXES
# tlp
tlpr = re.compile('^tlp*')
tlps = []
# mail
mailr = re.compile('^mail*|^mx*')
mails = []
# buildbot
bbr = re.compile('^bb*')
bbs = []
# mysql
msqlr = re.compile('^mysql*')
msqls = []
# psql
psqlr = re.compile('^psql*')
psqls = []
# jenkins
jenkinsr = re.compile('^jenkins*')
jenkinss = []
# ldap
ldapr = re.compile('^ldap*')
ldaps = []
#atlassian
atlr = re.compile('^jira*|^cwiki*|^crowd*')
atls = []
#infra
infrar = re.compile('^git*|^tools*')
infras = []
# Project VMs
projs = []

parser = argparse.ArgumentParser("Ansible EC2 inventory script")
parser.add_argument(
    "--list",
    action="store_true",
)
parser.add_argument(
    "--host",
    action="store",
)

args = parser.parse_args()


##################################################
### THE CUSTOM BIT, CHANGES WITH THE PLATFORM  ###
##################################################

client = boto3.client('ec2')
data = [ item['Instances'][0] for item in client.describe_instances()['Reservations'] ]

######################
### END CUSTOM BIT ###
######################

instances = []
for instance in data:
    try:
        if instance.get('Tags')[0]['Key'] == "Name":
            name = instance.get('Tags')[0]['Value']
            instances.append(name)
            if tlpr.match(name):
                tlps.append(name)
                continue
            elif mailr.match(name):
                mails.append(name)
                continue
            elif bbr.match(name):
                bbs.append(name)
                continue
            elif msqlr.match(name):
                msqls.append(name)
                continue
            elif psqlr.match(name):
                psqls.append(name)
                continue
            elif ldapr.match(name):
                ldaps.append(name)
                continue
            elif jenkinsr.match(name):
                jenkinss.append(name)
                continue
            elif infrar.match(name):
                infras.append(name)
                continue
            elif atlr.match(name):
                atls.append(name)
                continue
            else:
                projs.append(name)               
    except TypeError:
        continue

inventory = {
    "aws": {
        "hosts": instances,
    }
}
if len(tlps) > 0: inventory['aws_tlp'] = {'hosts': tlps}
if len(mails) > 0: inventory['aws_mail'] = {'hosts': mails}
if len(bbs) > 0: inventory['aws_bb'] = {'hosts': bbs}
if len(msqls) > 0: inventory['aws_mysql'] = {'hosts': msqls}
if len(msqls) > 0: inventory['aws_psql'] =  {'hosts': psqls}
if len(jenkinss) > 0: inventory['aws_jenkins'] = {'hosts': jenkinss}
if len(atls) > 0: inventory['aws_atlas'] = {'hosts': atls}
if len(infras) > 0: inventory['aws_infra'] = {'hosts': infras}
if len(projs) > 0: inventory['aws_proj'] = {'hosts': projs}

if args.list:
    print(json.dumps(inventory))
elif args.host in inventory['aws']:
    print(json.dumps(inventory['vars']))
else:
    print(json.dumps(inventory))
