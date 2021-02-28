# FAKE CSV GENERATOR


# SETUP

Create a virtual environment to install dependencies in and activate it:
```shell
$ virtualenv venv -p python3.8
$ source venv/bin/activate
```

Install the dependencies:
```shell
$ pip install -r requirements.txt
```

Create local settings
```shell
$ cd core/settings
$ cp local.example.py local.py
```

Create a database:
```shell
$ sudo -u postgres psql
$ create database fake_csv_db encoding 'UTF-8';
$ \q
```

Pass your settings to local.py

Do migrate:
```shell
$ python manage.py migrate
```

Create superuser:
```shell
$ python manage.py createsuperuser
```


Install redis:
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04

Run app:

```shell
$ python manage.py runserver
$  celery -A core worker -B --loglevel=info
```


Go to browser and open:
http://locahost:8000

**DONE**


## For Production:
Environment variables

| Key    | Description   | 
| :---         |     :---      |
| `SECRET_KEY`  | secret key  | 
| `DEBUG`  | Debug mode True or False  |
| `ALLOWED_HOSTS`| Allowed host |
| `DB_NAME`| Database name |
| `DB_USER`| Database user | 
| `USER_PASSWORD`  | Database user password |
| `BROKER_URL`  | Broker url
| `CELERY_RESULT_BACKEND`  | Celery result backend

