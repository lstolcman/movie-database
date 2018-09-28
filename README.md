# Movie database


## Description
Simple website that allows browsing / searching movie database provided by `http://www.omdbapi.com/`. Only logged in users are capable to use this feature (standard-login or Facebook/Google). API results should be viewable on a website with basic layout, with pagination and a possibility to save favourites into local database.


## Technology

Any


## Requirements

Entire project should be available as an open source project on GitHub. Please commit your work on a regular basis (rather than one huge commit). The project should contain README file with information how to install application in local environment.


## Deploy

Use `docker-compose`


### Windows

`env FLASK_APP=moviedb.py flask run`

### Linux

`export FLASK_APP=moviedb.py flask run`


