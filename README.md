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
Patch: Bug fixes
The versioning is mainly for developmental purpose. Since the versioning starting from 1.x.x, the urls starts with 'api'.


## Prerequisites:
I am using VSCode for my development and its integrated terminal. Any IDE and command prompt is enough.
I have enabled 'autosave features'. So, 'save' won't be mentioned in the follwing instructions.

## Initial setup
In terminal:

mkdir Remedy_v2_backend
cd Remedy_v2_backend
pipenv install django
pipenv shell
django-admin startproject backend .

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

Migrate the model to the database
```
python manage.py makemigrations
```
```
python manage.py migrate
```

