# Taskly
> Pet project

Django project for management different tasks in the IT sphere and planing your time.

## Check it out!

[Taskly deployed to Render](https://task-manager-acs0.onrender.com/)


## Installation

Python3 must be installed:

```shell
git clone https://github.com/Sergi0bbb/Task-Manager.git
cd task_manager
python -m venv env
source env/bin/activate  # For Windows: `env\Scripts\activate`
pip install -r requirements.txt
```

Then you need to migrate db:
```shell
python manage.py makemigrations
python manage.py migrate
```
And finally create superuser and start server
```shell
python manage.py createsuperuser
python manage.py runserver
```


## Features

* Creation user
* Change profile pictures
* Create your own task and mark as completed
* Check your tasks in calendar and plan your time
* Check other users tasks 


## User credentials for testing

| login | password  |
|-------|-----------|
| test  | user12345 |


## Demo
![Project diagram](demo.png)
