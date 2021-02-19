#!/usr/bin/python3

import boto3
import json
import pprint
import argparse
import re

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

client = boto3.client('ec2')
pp = pprint.PrettyPrinter(depth=4)
data = [ item['Instances'][0] for item in client.describe_instances()['Reservations'] ]

# pp.pprint(data)

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
if len(tlps) > 0: inventory['aws_tlp'] = tlps
if len(mails) > 0: inventory['aws_mail'] = mails
if len(bbs) > 0: inventory['aws_bb'] = bbs
if len(msqls) > 0: inventory['aws_mysql'] = msqls
if len(psqls) > 0: inventory['aws_psql'] = psqls
if len(jenkinss) > 0: inventory['aws_jenkins'] = jenkinss
if len(atls) > 0: inventory['aws_atlassian'] = atls

if len(infras) > 0: 
    if len(atls) > 0:
        inventory['aws_infra'] = {} 
        inventory['aws_infra']['children'] = ["aws_atlassian"]
        inventory['aws_infra']['hosts'] = infras
    else:
        inventory['aws_infra'] = infras
if len(projs) > 0: inventory['aws_proj'] = projs

if args.list:
    print(json.dumps(inventory))
elif args.host in inventory['aws']:
    print(json.dumps(inventory['vars']))
else:
    print(json.dumps(inventory))
