#!/usr/bin/env python3

import argparse
import json
import boto3
import datetime
import paramiko
import botocore
import os
import time
from tabulate import tabulate
from rich.progress import track
from rich.console import Console

import rich

from botocore.exceptions import ClientError

console = Console()

ec2 = boto3.client('ec2', region_name='us-east-1')


def setup_directory_structure():
    home_dir = os.path.expanduser('~')

    axiom_dir = f"{home_dir}/.axiom"
    if not os.path.exists(axiom_dir):
        print("Welcome to Axiom!")
        print(f"- Creating directory for configuration {axiom_dir}...")
        os.mkdir(axiom_dir)
        os.mkdir(f"{axiom_dir}/keys")
        print("Writing default configuration...")
        default_config = {
            'profile':'work',
        }

        with open(f"{axiom_dir}/config.json") as f:
            f.write(json.dumps(default_config, indent=4))
            f.close()
        

def create_security_group(name):
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=name, Description=f'{name} security group', VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
        return security_group_id
    except ClientError as e:
        response = ec2.describe_security_groups(
            Filters=[
            dict(Name='group-name', Values=[name])
            ]
        )
        group_id = response['SecurityGroups'][0]['GroupId']
        return group_id

def create_key_pair(keypair_name):
    try:
        key_pair = ec2.create_key_pair(KeyName=keypair_name)

        private_key = key_pair["KeyMaterial"]
        key_path = f"keys/{keypair_name}.pem"
        with os.fdopen(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)
    except:
        pass

    return keypair_name

def create_instance(instance_name, instance_type, image_id, security_group_id, keypair_name, profile):
    response = ec2.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {

                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                },
            },
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name','Value': instance_name}, {'Key':'Profile', 'Value':profile}],
            }
        ],
        ImageId=image_id,
        KeyName=keypair_name,
        InstanceType=instance_type,
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroupIds=[
            security_group_id
        ],
    )

    return response

def create_base_instance(instance_name, instance_type, profile_name, build_name):

    security_group_id = create_security_group(profile_name)
    keypair_name = create_key_pair(profile_name)
    
    console.print(f"Creating instance {instance_name}")
    resp = create_instance(instance_name, instance_type, "ami-07d9b9ddc6cd8dd30", security_group_id, keypair_name, profile_name)

    with rich.progress.Progress(rich.progress.SpinnerColumn(), transient=True) as progress:
        task_id = progress.add_task("Waiting for instance to run...", total=100)
        
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[resp['Instances'][0]['InstanceId']])
        
        progress.update(task_id, completed=100)

    code = """sudo apt update
sudo apt-get upgrade -y
sudo apt-get install -y zsh
sudo chsh -s $(which zsh) ubuntu
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add -
sudo sh -c "echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list.d/kali.list"
sudo sh -c "echo 'Package: *' > /etc/apt/preferences.d/kali.pref; echo 'Pin: release a=kali-rolling' >> /etc/apt/preferences.d/kali.pref; echo 'Pin-Priority: 50' >> /etc/apt/preferences.d/kali.pref"
wget http://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb
sudo dpkg -i kali-archive-keyring_2022.1_all.deb
rm kali-archive-keyring_2022.1_all.deb
sudo apt update
sudo apt update --fix-missing
sudo apt install -f
sudo apt --fix-broken install
sudo apt -y upgrade
sudo apt -y install ffuf nmap subfinder httpx-toolkit nuclei wordlists amass gobuster
    """

    with rich.progress.Progress(rich.progress.SpinnerColumn(), transient=True) as progress:
        task_id = progress.add_task("Configuring instance...", total=len(code.split("\n")))
        time.sleep(15)
        
        for idx, line in enumerate(code.split("\n")):
            ssh_exec(instance_name, line)  
            progress.update(task_id, advance=1)

        time.sleep(15)

    resp = ec2.create_image(InstanceId=resp['Instances'][0]['InstanceId'], Name=build_name, NoReboot=True)
    time.sleep(15)
    
    delete_instances(instance_names=[instance_name])
    return resp

def snapshot(instance_id, build_name):
    resp = ec2.create_image(InstanceId=instance_id, Name=build_name, NoReboot=True)
    print(resp)


def init_instance(instance_name, instance_type, profile_name, source_image_id):
    security_group_id = create_security_group(profile_name)
    keypair_name = create_key_pair(profile_name)
    resp = create_instance(instance_name, instance_type, source_image_id, security_group_id, keypair_name, profile_name)
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[resp['Instances'][0]['InstanceId']])



def extract_info(reservation):


    clean = {
        'instanceId': reservation['Instances'][0]['InstanceId'],
        'instanceType': reservation['Instances'][0]['InstanceType'],
        'architecture': reservation['Instances'][0]['Architecture'],
        'currentStatus': reservation['Instances'][0]['State']['Name'],
        'name':None
    }

    try:
        clean['tags'] = reservation['Instances'][0]['Tags']
        clean['privateIpAddress'] = reservation['Instances'][0]['PrivateIpAddress']
        clean['publicIpAddress'] = reservation['Instances'][0]['PublicIpAddress']
        clean['publicDnsName'] = reservation['Instances'][0]['PublicDnsName']
        clean['privateDnsName'] = reservation['Instances'][0]['PrivateDnsName']

        name_tag = [tag['Value'] for tag in clean['tags'] if tag['Key'] == 'Name']
        profile_tag = [tag['Value'] for tag in clean['tags'] if tag['Key'] == 'Profile']
        clean['name'] = name_tag[0]
        clean['profile'] = profile_tag[0]
    except:
        pass

    return clean

def get_images():
    images = ec2.describe_images(Owners=['self'])
    
    return images

def print_images():
    images = get_images()['Images']

    images_minimal = []
    for image in images:
        image_meta = [
            image['ImageId'],
            image['ImageLocation'],
            image['CreationDate']
        ]

        images_minimal.append(image_meta)
    
    print(tabulate(images_minimal, headers=["ID", "Location", "Date"], tablefmt='grid'))

def get_instances(instance_ids=[]):
    if len(instance_ids) > 0:
        return(ec2.describe_instances(InstanceIds=instance_ids))
    else:
        return(ec2.describe_instances())

def get_instances_minimal(instance_ids=[]):
    instances = get_instances(instance_ids)

    clean_instances = []
    for res in instances["Reservations"]:
        clean = extract_info(res)
        if clean['currentStatus'] != 'terminated':
            clean_instances.append(clean)

    return clean_instances


def format_table(data):
    headers = ['Name', 'Instance ID', 'Instance Type', 'Status', 'Private IP', 'Public IP', 'Public DNS']
    
    # Extract the values for tags and name from the data
    tags_column = [format_tags_and_name(instance['tags'], instance['name']) for instance in data]
    

    # Re-format the data to include the tags and name columns
    reformatted_data = [[tags_column[i][1],
        instance['instanceId'],
        instance['instanceType'], 
                    instance['currentStatus'],
                    instance.get('privateIpAddress', 'N/A'),
                    instance.get('publicIpAddress', 'N/A'),
                    instance.get('publicDnsName', 'N/A')] 
                    for i, instance in enumerate(data)]
    
    return tabulate(reformatted_data, headers, tablefmt='grid')

# Define a function to format the tags and instance name
def format_tags_and_name(tags, name):
    if tags:
        tag_str = ', '.join(['{}: {}'.format(tag['Key'], tag['Value']) for tag in tags])
    else:
        tag_str = 'N/A'

    if name:
        name_str = name
    else:
        name_str = 'None'

    return tag_str, name_str

def print_instances():
    instances = get_instances_minimal()

    print(format_table(instances))

def ssh_to_instance(instance_name):
    for instance in get_instances_minimal():
        if instance['name'] == instance_name:
            public_ip = instance['publicIpAddress']
            profile = instance['profile']

            os.system(f"ssh -i keys/{profile}.pem ubuntu@{public_ip}")

def ssh_exec(instance_name, code):
    print(code)
    output = ""

    for instance in get_instances_minimal():
        if instance['name'] == instance_name:
            public_ip = instance['publicIpAddress']
            profile = instance['profile']
            pkey = paramiko.RSAKey.from_private_key_file(f"keys/{profile}.pem")

            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(public_ip, username="ubuntu", pkey=pkey)
            _stdin, _stdout,_stderr = client.exec_command(code)
            print(_stdout.read().decode())
            client.close()



def delete_instances(instance_names=[]):
    instances = get_instances_minimal()
    ids_to_be_deleted = []

    for instance_name in instance_names:
        for instance in instances:
            if instance['name'] == instance_name:
                ids_to_be_deleted.append(instance['instanceId'])

    resp = ec2.terminate_instances(
        InstanceIds = ids_to_be_deleted,
        DryRun=False
    )


parser = argparse.ArgumentParser(description='axiom Instance Orchestration')

# Instance Management
parser.add_argument('--build', action='store_true',
                    help='Build a new base AWS instance')
parser.add_argument('instance_name', nargs='?',
                    help='Name of the instance to perform an operation for')

parser.add_argument('--instance-type', default='t3.micro',
                    help='Type of the instance (default: t3.micro)')
parser.add_argument('--profile', default='work',
                    help='Profile of the instance (default: work)')
parser.add_argument('--prefix', 
                    help='Prefix of the fleet')

# Fleet Initialization
parser.add_argument('--init', 
                    help='Initialize a new fleet of instances')
parser.add_argument('-n', type=int, default=1,
                    help='Number of nodes to initialize (default: 1)')

parser.add_argument('--images', action='store_true',
                    help='Print a table of images')

parser.add_argument('--image-id', 
                    help='Image ID to use as the base image')

parser.add_argument('--snapshot', 
                    help='Snapshot an instance by name to create an iamge')

# Instance Interaction
parser.add_argument('--instances', action='store_true',
                    help='Print a table of instance information')
parser.add_argument('--ssh',
                    help='Interactively SSH into an instance')

parser.add_argument('--exec',
                    help='Execute a single command over SSH')
parser.add_argument('--rm', nargs='+', 
                    help='List of instance names to delete')

def main():

    intro = """
 ██████  ██▓███   ██▓ ██▀███   ▒█████  
▒██    ▒ ▓██░  ██▒▓██▒▓██ ▒ ██▒▒██▒  ██▒
░ ▓██▄   ▓██░ ██▓▒▒██▒▓██ ░▄█ ▒▒██░  ██▒
  ▒   ██▒▒██▄█▓▒ ▒░██░▒██▀▀█▄  ▒██   ██░
▒██████▒▒▒██▒ ░  ░░██░░██▓ ▒██▒░ ████▓▒░
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░▓  ░ ▒▓ ░▒▓░░ ▒░▒░▒░ 
░ ░▒  ░ ░░▒ ░      ▒ ░  ░▒ ░ ▒░  ░ ▒ ▒░ 
░  ░  ░  ░░        ▒ ░  ░░   ░ ░ ░ ░ ▒  
      ░            ░     ░         ░ ░  

    author: pry0cc

    """

    print(intro)

    args = parser.parse_args()
    # Validate arguments for exclusivity
    if (args.build and args.rm) or \
        (args.init and args.rm) or \
        (args.init and args.build) or \
        (args.ssh and args.rm) or \
        (args.ssh and args.instances):
        parser.error("Invalid combination of arguments. "
                 "Choose only one of: --build, --init, --rm, --ssh, --instances.")

    # Build instance
    if args.build:
        build_name = ""
        if args.instance_name:
            build_name = args.instance_name
        else:
            build_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

        create_base_instance(f'{args.profile}-{build_name}', args.instance_type, args.profile, build_name)
        print(f'Built instance: {build_name}')


    from concurrent.futures import ThreadPoolExecutor
    import threading 

    # Initialize fleet
    if args.init:
        num_nodes = args.n
        prefix = args.init

        print(f'Initializing a fleet with {num_nodes} node/s.')

        # Function to run in thread
        def init_instance_threaded(i):
            instance_name = f'{prefix}{i}'
            instance_type = 't3.micro' 
            profile_name = args.profile
            source_image_id = args.image_id
            init_instance(instance_name, instance_type, profile_name, source_image_id)

        # Use ThreadPoolExecutor to run threads
        with ThreadPoolExecutor(max_workers=num_nodes) as executor:
            futures = [executor.submit(init_instance_threaded, i) for i in range(num_nodes)]
        
        # Wait for threads to complete
        for future in futures:
            future.result() 

        print("All instances initialized")

    if args.snapshot:
        instance_id = args.snapshot
        base_image = args.image_id
        snapshot(instance_id, base_image)

    # Print instances
    if args.instances:
        print_instances()

    if args.images:
        print_images()

    # SSH into instance
    if args.ssh:
        ssh_to_instance(args.ssh)

    if args.exec:
        ssh_exec(args.instance_name, args.exec)

    if args.rm:
        if args.prefix:
            print(f'Deleting instances with prefix: {args.prefix}')
            instances = []
            for instance in get_instances_minimal():
                if instance["name"].startswith(args.prefix):
                    instances.append(instance["name"])
            delete_instances(instances)
        else:
            print(f'Deleting specific instances: {", ".join(args.rm)}')
            delete_instances(args.rm)


if __name__ == "__main__":
    main()
