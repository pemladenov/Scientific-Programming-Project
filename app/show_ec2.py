import boto3
from botocore.config import Config


### DISPLAY Instances & Instance Status ###
#Python Program for creating a connection
ec2Instances = boto3.resource('ec2')

# ID der instance printen
for instance in ec2Instances.instances.all():
    print(instance.id)
# print different infos about instances including ID & Status
for status in ec2Instances.meta.client.describe_instance_status()['InstanceStatuses']:
    print(status)