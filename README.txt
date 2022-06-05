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