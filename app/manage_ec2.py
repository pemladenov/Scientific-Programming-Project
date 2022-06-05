import boto3
from botocore.config import Config


### ACCESS Instances and choose to run,stop or reboot Instance(s)###
region = 'eu-central-1'
#declare the config.
config = Config( 
             region_name = region,
             signature_version = 'v4',
             retries = {
                 'max_attempts': 10,
                 'mode': 'standard'
             }
         )
#initialize boto3 client for ec2 with the config object.
ec2 = boto3.client('ec2', config = config)
instances = ["i-0f54acdd2e9f1523b"] # or ["<instance-id-1>","<instance-id-2>",...,"<instance-id-n>"]


#start the instance
ec2.start_instances(InstanceIds=instances)
print("started")
"""
#stop the instance
ec2.stop_instances(InstanceIds=instances)
print("stopped")

#reboot the instance
ec2.reboot_instances(InstanceIds=instances)
print("reboted")
"""