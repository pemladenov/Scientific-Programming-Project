First run in terminal:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

then activate the environment:
venv/Scripts/activate

install inside of venv:
py -m pip install -r requirements.txt

OR install only one:
py -m pip install matplotlib

run web app:
python app\app.py

exit env:
deactivate