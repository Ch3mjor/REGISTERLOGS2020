# Request Log

A request logger with (unauthenticated) API exposure

# Requirements
1. Python 3.6
2. Memcached
3. See [Pipfile](Pipfile)

# Getting Started
1. Install requirements:
```bash
python3 -m pip install pipenv

pipenv shell

pipenv install --system --deploy --ignore-pipfile
```

2. Install memcached
```bash
sudo apt-get update

sudo apt-get install memcached

sudo systemctl start memcached
```

3. Create a settings.ini file using the [sample](settings.ini.sample)
```bash
mv settings.ini.sample settings.ini

vi settings.ini
```

4. Run some updates
```bash
python manage.py migrate
python manage.py collectstatic
```

5. Run the server
```bash
# for development
python manage.py runserver

# for deployment
waitress-serve --threads 4 --host 0.0.0.0 --port 5000 requestlog.wsgi:application
```
6.Paths
'''
/log
#To see previous logs stored in the DB.
'''
