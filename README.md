# Movie database


## Description
Simple website that allows browsing / searching movie database provided by `http://www.omdbapi.com/`. Only logged in users are capable to use this feature (standard-login or Facebook/Google). API results should be viewable on a website with basic layout, with pagination and a possibility to save favourites into local database.


## Technology

Python, Flask, Bootstrap, JQuery, Docker


## Requirements

Entire project should be available as an open source project on GitHub. Please commit your work on a regular basis (rather than one huge commit). The project should contain README file with information how to install application in local environment.


## Windows -- debugging

`env FLASK_APP=moviedb.py FLASK_DEBUG=1 flask run`


## Deploy

Configuration is based on `docker-compose.yml`.
You may change your api-key for `omdbapi` in config.py

### Linux

`docker-compose build --no-cache`

`docker-compose up`


