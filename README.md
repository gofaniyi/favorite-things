## Favorite Things App

[![Maintainability](https://api.codeclimate.com/v1/badges/7513939bf4da89be4919/maintainability)](https://codeclimate.com/github/gofaniyi/favorite-things/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7513939bf4da89be4919/test_coverage)](https://codeclimate.com/github/gofaniyi/favorite-things/test_coverage)
[![Build Status](https://travis-ci.org/gofaniyi/favorite-things.svg?branch=master)](https://travis-ci.org/azu/travis-badge)


## Description

The **favorite-things-app** is an application that allows the user to track their favorite things. The project is divided into two parts. The Frontend build on **VueJs - Javascript** and the Backend built on **Flask - Python**.


- Key Application features

2. Favorite Management
    - Creation of Favorites
    - Updating different Favorites
    - Removing different Favorites from the system
    - Viewing all Favorites and those under a particular category

2. Category Management
    - Creation of Categories
    - Updating different Categories
    - Removing different Categories from the system

- FrontEnd

The FrontEnd is a VueJs application that I am serving as static pages through the Flask application. Due to the size of the frontend, it is hosted in a [separate repository](https://github.com/gofaniyi/favorite-things-web). Only the static files are hosted in this repository. See [static files](https://github.com/gofaniyi/favorite-things/tree/master/dist)


- BackEnd

The api built on Flask Rest API Framework, provides resources, i.e. Collection of endpoints to track a user's favorite things.

## Development Approach

Making the assumption that a Risk is created under a Risk Type category. Risk Type object have the ability to store 
the custom attributes that will be defined when creating these risks.

- Database Setup & Entity Relationship
The following tables were designed to manage the concept of these solution.

1. Categories
2. Favorites
3. Audit logs

The relationship between these tables is explained in the entity relation diagram below

* Entity Relationship Diagram

![alt text](https://image.prntscr.com/image/sl4JJUqvRc21vlvPdrHHHg.png)


* Here is a link [ORM Classes](https://github.com/gofaniyi/favorite-things/tree/master/api/models.py) to the folder that contains the ORM classes for these tables. 


## Technology Stack - BackEnd

- Flask
- Flask RestPlus
- SQLAlchemy
- Marshmallow
- JSON Web Token
- Pytest
- Flask S3
- MySQL

###  Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.7.0
    ```

-   Install pipenv:

    ```
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.10.13
    ```
-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
    ```

-   Clone the insurance-app repo and cd into it:

    ```
    git clone https://github.com/favorite-things.git
    ```

-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```

-   Make a copy of the .env.sample file and rename it to .env and update the variables accordingly:

    ```
    FLASK_ENV=development # Takes either development, testing, staging or production
    API_BASE_URL_V1=/api/v1 # The base url for version 1 of the API
    FLASK_APP=manage.py
    DATABASE_URI = "mysql+pymysql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_DATABASE_NAME" #Development and production db uri
    TEST_DATABASE_URI = "mysql+pymysql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_TEST_DATABASE_NAME"
    JWT_SECRET_KEY="" # Generate your secret key. You can use this code snippet below to generate it
    ```

-   How to generate a Secret Key
    ```
    import os
    secret_key = os.urandom(24)
    print(secret_key)
    ```

-   Activate a virtual environment:

    ```
    pipenv shell
    ```

-   Apply migrations:

    ```
    flask db upgrade
    ```

-   If you'd like to seed initial data to the database:

    ```
    flask seed
    ```

*   Run the application with either commands:

    ```
    flask run
    ```

*   Should you make changes to the database models, run migrations as follows

    -   Migrate database:

        ```
        flask db migrate
        ```

    -   Upgrade to new structure:
        ```
        flask db upgrade
        ```

*   Deactivate the virtual environment once you're done:
    ```
    exit
    ```

## Running tests and generating report

On command line run:

```
pytest
```

To further view the lines not tested or covered if there is any,

An `htmlcov` directory will be created, get the `index.html` file by entering the directory and view it in your browser.

## Set Up Development With Docker

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account to download Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

-   `cd <project dir>` to check into the dir
-   `docker-compose build` or `make build` to build the application images
-   `docker-compose up -d` or `make start` or `make start_verbose` to start the api after the previous command is successful

The `docker-compose build` or `make build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

The `docker-compose up -d` or `make start` command starts the application while ensuring that the postgres database is seeded before the api starts.

The `make start_verbose` command starts the api verbosely to show processes as the container spins up providing for the visualization of errors that may arise.

To stop the running containers run the command `docker-compose down` or `make stop`

## Local Deployment to AWS Lambda using Zappa

-   Install zappa inside virtual environment:

    ```
    pip install zappa
    ```

-   Initialize project with zappa

    ```
    zappa init
    ```

-   Deploy project with zappa

    ```
    zappa deploy dev
    ```

-   Redeploy updates/changes with zappa

    ```
    zappa update dev
    ```

##  Continuous Deployments with Travis CI

    You must have initialized and performed initial deployment using zappa locally. My project uses Travis CI and deploys to AWS Lambda after CI passes.

-   Include the command below under the `after_success` block in the `.travis.yml` file

    ```
    zappa update dev

    ```

    Ensure you remove the `profile_name` key from the `zappa_settings.json` file before pushing 
    to remote


- Here is a link to the deployed version of the project: 

https://skudz1hazf.execute-api.us-east-2.amazonaws.com/dev

* Landing Page

![alt text](https://image.prntscr.com/image/8BHnRsncR8yIqRRLV1z6bQ.png)


## Demo

Find below a guide on how to use the app.
1. [User Authentication](https://github.com/gofaniyi/insurance-app/blob/master/documentation/user_authentication.md)
2. [Create Risk Types](https://github.com/gofaniyi/insurance-app/blob/master/documentation/create_risk_types.md)
3. [View Risk Types](https://github.com/gofaniyi/insurance-app/blob/master/documentation/view_risk_types.md)
3. [Edit Risk Types](https://github.com/gofaniyi/insurance-app/blob/master/documentation/edit_risk_types.md)
4. [Delete Risk Types](https://github.com/gofaniyi/insurance-app/blob/master/documentation/delete_risk_types.md)
5. [Create Risks under a Risk Type](https://github.com/gofaniyi/insurance-app/blob/master/documentation/create_risks.md)
6. [View Risks under a Risk Type](https://github.com/gofaniyi/insurance-app/blob/master/documentation/view_risks.md)


## Other deliverables

1. Link to the debugging quiz is [here](https://github.com/gofaniyi/favorite-things/blob/master/quiz.py)


I hope you find my concept of solving this problem helpful. :)