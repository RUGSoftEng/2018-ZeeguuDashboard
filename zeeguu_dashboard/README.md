# How to Install


#Create virtual env
This is the dashboard-web. 
To install you need to setup a python virtual environment.
To do this, make sure you have python3.6 installed.
'python3.6 -m {{venv_name}} venv'


#Activate your venv
Go to your venv folder.
'source bin/activate'

#Install packages into your venv.
'pip install {{package_name}}'
You will need to install the separate packages: 
 1. Flask-bootstrap
 2. Flask
 3. Flask-WTF


#Run with main.py
'export FLASK_APP=main.py'
'flask run'


Done!

