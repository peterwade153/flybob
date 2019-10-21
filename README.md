[![Build Status](https://travis-ci.org/peterwade153/flybob.svg?branch=master)](https://travis-ci.org/peterwade153/flybob)
[![Coverage Status](https://coveralls.io/repos/github/peterwade153/flybob/badge.svg?branch=master)](https://coveralls.io/github/peterwade153/flybob?branch=master)
# Flybob-API
---
## Description
Flybob provides a platform which enables users book flights in a quick and efficient way.

###  Built with
python 3.7 and the Flask mirco-framework and uses a postgres database.

### API Documentation
These Docs ease usage of the Flybob API. https://documenter.getpostman.com/view/3447977/S1EJWfp4

---
### Prerequisites
A cloudinary account, this will allow the saving images remotely. Please go ahead and create one.

### Installation with Docker.
- This will require Docker to be already Installed. And its a shorter process compared to the second option.

Clone the repository
<pre>
git clone https://github.com/peterwade153/flybob.git
</pre>

- Start the Docker deamon on the machine if its not running already. 

- Change directory to the folder where the project is cloned and run the command below.

- Updates Environment variable. Create a `.env` file from the `.env-sample` and replace thm with actual varibles.

<pre>
docker-compose up
</pre>

Docker will spin up containers and after the API endpoints can be accessed. Via http://localhost:5000/


### Installation and API usage without Docker.

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
Ensure redis is installed locally.

Create a `.env` and copy variables in the `.env-sample` and replace them with the actual values


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
$ python application.py
</pre>

API endpoints can be accessed. Via http://localhost:5000/

#### Running the flight remainder task via email functionlity 
To start redis
<pre>
$ redis-server
</pre>
To run the celery beat
<pre>
celery -A app.celery beat -l info
</pre>
To run the celery worker
<pre>
celery -A app.celery worker -l info
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
PUT     |  api/v1/flights/id              |        Update flight data (Admin-only)
DELETE  |  api/v1/flights/id              |        Delete a flight (Admin-only)
GET     |  api/v1/flights/id              |        Return a flight
POST    |  api/v1/reservations            |        Reserve a seat on a flight 
GET     |  api/v1/reservations            |        View reserved seats on a flight
GET     |  api/v1/reservations/id         |        Return a reservation
PUT     |  api/v1/reservations/id         |        Update a reservation details

Developer -- @peterwade153@gmail.com