# Remedy
### An integrated software solution for superspeciality clinics to connect between patients, doctors, and labs.

## Modules
### Module 1: Authentication
The authentication module deals with the admin, patient, doctor, and lab’s account creation, password reset, login, and logout.
### Module 2: Patients
The Patients module contains their pages, functionalities, and other basic data models.
### Module 3: Doctors and Labs
This module deals with Doctors, and Laboratories. Contains their pages, functionalities, and other basic data models.
### Module 4: Executives
The executives module deals with the management of the system, and approval of doctors and laboratories.
### Module 5: Appointments
The appointments module deals with management of appointments. It also supplies real-time information on time-slot availability
### Module 6: Payments
The payments module deals with the processing of payments for appointments. It stores required information related to payments as well.
### Module 7: Reports
The reports module deals with the generation of reports, especially creating lab reports, prescriptions, other relevant data storage as well.
### Module 8: Video call
This module deals with all video call related APIs, settings, keys, etc.
### Module 9: Chat
This module deals with all chat related APIs, settings, keys, etc.

Versioning:
I am planning to use semantic versioning for the application backend as well as for the frontend. The structure is as follows:
<major>.<minor>.<patch>
Major: Major changes in the code which is incompatible with previous code.
Minor: Adding new features or changes
Patch: Bug fixes, 'b' represents backend and 'f' represent forntend
The versioning is mainly for developmental purpose. Since the versioning starting from 1.x.x, the urls starts with 'api'.

1.0.0:
Working code (Not all features are tested)

1.0.1b:
* Executives can initiate chat with Staff, Doctors, and Labs.
* Doctor, Lab, Executive models changed to accommodate document url.
* Documents will be stored in S3 bucket, inside 'docs' library.
* Doctor, Lab, and Executive accounts require Approval from an existing Executive account.

1.0.2b:
* Time and time zone added to the generic API window.

1.0.3b:
* Changes made according to bugs raised by project partner in boarding week.
* Minor changes in the asgi.py file, now the server is running with 'daphne backend.asgi:application' command.
* Installed new package for http2 and tls support.

1.0.5b
* Patients now can cancel appointments. The amount will be refunded to the source.

1.0.6b
* Executives cannot block themselves from the platform. No executives can block superuser from platform


## Prerequisites:
I am using VSCode for my development and its integrated terminal. Any IDE and command prompt is enough.
I have enabled 'autosave features'. So, 'save' won't be mentioned in the follwing instructions.

## Initial setup
In terminal:
```
mkdir Remedy_v2_backend
cd Remedy_v2_backend
pipenv shell
pipenv install django
django-admin startproject backend .
```

Initialize a new git repository
```
git init
```

Create two file named '.env' and .gitignore
```
touch .env
```
```
touch .gitignore
```

Add .env to the gitignore file

Install 'Python-decouple' package
```
pip install python-decouple
```

Now copy the 'secret key from settings.py to .env file.
In the .env file it should be something like the following:
```
SECRET_KEY = 'the_secret_key'
```
In the settings.py file, add the following lines:
```
from decouple import config
SECRET_KEY = config("SECRET_KEY")
```

If having any issue with decouple, Select the proper interpreter in VS Code

Start new app for all modules
```
python manage.py startapp authentication; \
python manage.py startapp patients; \
python manage.py startapp doctors_and_labs; \
python manage.py startapp executives; \
python manage.py startapp appointments; \
python manage.py startapp payments; \
python manage.py startapp reports; \
python manage.py startapp video_call; \
python manage.py startapp chat;
```

Install psycopg to interact with PostgreSQL
```
pipenv install psycopg
```

Create a new db in PSQL
add the credentials into the settings.

Add the following lines into settings.py to make the custom usermodel to be used for authentication.
```
AUTH_USER_MODEL = 'authentication.Account
```
Install REST and CORS for django
```
pipenv install djangorestframework django-cors-headers 
```
Install Python magic to validate files
```
pipenv install python-magic
```
Install simple JWT for access and refresh tokens
```
pipenv install djangorestframework-simplejwt
```
Install Razorpay for payment integration
```
pipenv install razorpay
```
Install pusher for chatting
```
pipenv install pusher
```
Install boto3 for AWS S3
```
pipenv install boto3
```
Install django-storages
```
pipenv install django-storages
```
Install pytz for Indian time zone
```
pipenv install pytz
```
Install uvicorn for ASGI server along with Gunicorn
```
pipenv install uvicorn
```
Install http2 and tls packages
```
pipenv install 'Twisted[http2,tls]'
```

Migrate the model to the database
```
python manage.py makemigrations
```
```
python manage.py migrate
```

