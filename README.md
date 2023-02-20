# Online gift shop

An online gift shop is planning to launch a campaign in different regions. In order for the sales strategy to be effective, market analysis is necessary. The store has a supplier who regularly sends (for example, by email) data exports with information about residents.

For this purpose, a REST API service has been developed in Python that analyzes the provided data and identifies demand for gifts among residents of different age groups in different cities by month.

The service implements the following handlers:

`POST /imports` - Adds a new data export;  
`GET /imports/$import_id/citizens` - Returns residents of the specified data export;  
`PATCH /imports/$import_id/citizens/$citizen_id` - Modifies information about a resident (and their relatives) in the specified data export;  
`GET /imports/$import_id/citizens/birthdays` - Calculates the number of gifts that each resident of the data export will purchase for their first-order relatives, grouped by month;  
`GET /imports/$import_id/towns/stat/percentile/age` - Calculates the 50th, 75th, and 99th percentiles of the ages (in full years) of residents by city in the specified sample.  

What is inside?
===========
The application is packaged in a Docker container.

Project Structure
=================
```
.
├── Dockerfile - is a text document containing all the commands for building the image
├── README.md - a text file that is distributed with the software and contains information about it.
├── app.py 
├── citizens - application directory
│ ├── __init__.py
│ ├── app.py - application description
│ └── handlers
│      ├── __init__.py
│      └── imports.py
├── db - database directory
│ ├── __init__.py
│ └── models.py - description of the database schema
├── docker-compose.tests.yml
├── docker-compose.yml
├── requirements.tests.txt - list of external dependencies
├── requirements.txt - list of external dependencies
├── run_app.sh - server startup script
├── run_tests.sh - test run script
├── tests - tests directory
│ ├── __init__.py
│ ├── api
│ │   ├── __init__.py
│ │   ├── conftest.py
│ │   ├── test_imports_get.py
│ │   └── test_imports_post.py
│ ├── conftest.py
│ └── data
│      └── citizens.json
└── utils
    ├── __init__.py
    ├── request_schema.py
    └── validate.py
```
How to use?
=================

How to run REST API service locally on port 8080:
* We give permission to execute the script `chmod +x run_app.sh`
* Run the command `./run_app.sh`
* After running the commands, the application will start listening for requests at `0.0.0.0:8080`.

How to run tests?
-----------------------------
* We give permission to execute the script `chmod +x run_test.sh`
* Run the command `./run_test.sh`

Technology stack:
-----------------
* Docker - is a platform designed to help developers build, share, and run modern applications.
* Flask - API web framework
* SQLAlchemy - The Database Toolkit for Python
* Marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.
* Python-dateutil - the dateutil module provides powerful extensions to the standard datetime module, available in Python. Installation.
* Werkzeug is a comprehensive WSGI web application library.
* Psycopg2-binary - Python-PostgreSQL Database Adapter
 
Test:
-----
* Coverage is a tool for measuring code coverage of Python programs.
* Pytest - the pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.
* Pylama - code audit tool for python.
* Pytest-flask is a plugin for pytest that provides a set of useful tools to test Flask applications and extensions
* Pytest-cov - this plugin produces coverage reports

Logs:
-----
* Logs are collected and stored using docker logs

