[![Build Status](https://travis-ci.org/peterwade153/flybob.svg?branch=master)](https://travis-ci.org/peterwade153/flybob)
[![Coverage Status](https://coveralls.io/repos/github/peterwade153/flybob/badge.svg?branch=master)](https://coveralls.io/github/peterwade153/flybob?branch=master)
# Flybob-API
---
## Description
Flybob provides a platform which enables users book flights in a quick and efficient way.

###  Built with
python 3.7 and the Flask mirco-framework and uses a postgres database.

---
### Installation
Create a virtual environment and activate it.
<pre>
$ python3 -m venv fly-env
</pre>
Change directory into fly-env and clone the repository.
<pre>
git clone https://github.com/peterwade153/flybob.git
</pre>
To activate the environment.
<pre>
$ source bin/activate
</pre>
### Create Database
Create a database with a `flybobdb`. Assuming postgresql is already installed with `your-user-name` being the user-name created on installation.
<pre>
psql postgres -U your-user-name
</pre>
<pre>
CREATE DATABASE flybobdb;
</pre>

### Environment variables
Set up cloudinary account, its the service used for hosting the user images.
Add these variables replacing then with actual values.
<pre>
$ export SECRET_KEY='to something secret'
$ export APP_SETTINGS='development'
$ export DATABASE_URL='postgresql://your-username:your-password@localhost/flybobdb'
$ export CLOUDINARY_CLOUD_NAME = 'cloud-name'
$ export CLOUDINARY_API_KEY = 'api-key'
$ export CLOUDINARY_API_SECRET = 'api-secret'
</pre>
Alterbatively these variables can be placed in a `.env` file which can be added to the root folder.

### Install all the dependencies
<pre>
$ pip install -r requirements.txt
</pre>

### Migrations
<pre>
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
</pre>

### Testing
Nosetests is used for running tests.
<pre>
$ nosetests
</pre>

### Running application
<pre>
$ python run.py
</pre>
The use a tool like postman to access the endpoints below.
### Endpoints

Request |       Endpoints                 |       Functionality
--------|---------------------------------|--------------------------------
POST    |  api/v1/auth/register           |        Register user
POST    |  api/v1/auth/login              |        Login user
POST    |  api/v1/auth/logout             |        Logout user
POST    |  api/v1/auth/upload             |        Upload passport photo
POST    |  api/v1/flights                 |        Register a flight (Admin-only)
GET     |  api/v1/flights                 |        Returns all flights
PUT     |  api/v1/flights/<id>            |        Update flight data (Admin-only)
DELETE  |  api/v1/flights/<id>            |        Delete a flight (Admin-only)
GET     |  api/v1/flights/<id>            |        Return a flight
