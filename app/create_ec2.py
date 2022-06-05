import boto3
from botocore.config import Config


### /START/ CREATE NEW EC2 Instance & with new keypair and store file locally###

#Python Program for creating a connection
ec2Instances = boto3.resource('ec2')
# create a file to store the key locally
outfile = open('ec2-keypair.pem','w')

# boto ec2 funktion aufrufen um ein key pair zu erstellen
key_pair = ec2Instances.create_key_pair(KeyName='ec2-keypair')

# key holen und in einem file speichern
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)

# neue EC2 instance erstellen
conn=instances = ec2Instances.create_instances(
     ImageId='ami-015c25ad8763b2f11',   ##BEISPIEL SERVER: ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20220420###
     MinCount=1,
     MaxCount=1,                        ##Anzahl Instances definieren, die erstellt werden sollten
     InstanceType='t2.micro',
     KeyName='ec2-keypair'              #name des keys eingeben
 )
print(conn)
### /END/ CREATE NEW EC2 Instance & with new keypair and store file locally###

""" 
### /START/ 2. Variante: erstellt instance ohne keypair###
#Function um mit EC2 instance zu verbinden / mit meinen AWS-Account-Daten
ec2 = boto3.client('ec2',
                   'eu-central-1',
                   aws_access_key_id='', 
                   aws_secret_access_key='')

#This function will describe all the instances
#with their current state 
response = ec2.describe_instances()
print(response)

#Function for running instances
conn = ec2.run_instances(InstanceType="t2.micro",
                         MaxCount=1,
                         MinCount=1,
                         ImageId="ami-015c25ad8763b2f11")
print(conn)
### /END/ Erstellt instance ohne keypair###
"""