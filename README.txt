First run in terminal:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

then activate the environment:
venv/Scripts/activate

install inside of venv:
py -m pip install -r requirements.txt
or python3 -m pip install -r requirements.txt

OR install only one:
py -m pip install matplotlib
or python3 -m pip install matplotlib

python3 -m pip install awscli boto3

run web app:
python app\app.py
or python3 app\app.py

exit env:
deactivate

To run create_ec2.py / manage_ec2.py / show_ec2.py and

Create IAM-User, that has FULL ACESS TO CREATE EC2 INSTANCES:
https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/users
and safe the Acess ID & Acess Key to your desktop.

enter git bash and run: aws configure, enter the ID and the Key, chose the aws region: z.B. eu-central-1 and format: json.
after this configuration you're able to start the ec2 instances remotly.

if not understood, follow this instructions:

https://www.ipswitch.com/blog/how-to-create-an-ec2-instance-with-python
