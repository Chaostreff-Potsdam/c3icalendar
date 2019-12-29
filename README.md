c3icalendar
===========

[![Build Status](https://travis-ci.org/Chaostreff-Potsdam/c3icalendar.svg?branch=master)](https://travis-ci.org/Chaostreff-Potsdam/c3icalendar)

ICalendar adapter for the [36C3 schedule].
You can subscribe to the ICS file:

> **https://c3icalendar.herokuapp.com/36c3.ics**

[36C3 schedule]: https://events.ccc.de/congress/2019/wiki/index.php/Static:Schedule#Merged_schedules_.28XML_.2F_JSON.29

Deployment
----------

You can deploy the app using Heroku.
There is a free plan.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Heroku uses [gunicorn](http://flask.pocoo.org/docs/dev/deploying/wsgi-standalone/#gunicorn)
to run the server, see the [Procfile](Procfile).


Software Components
-------------------

- Python3 and the packages in requirements.txt
  - [Flask](http://flask.pocoo.org/)
- [icalendar](https://icalendar.readthedocs.io/)


Development
-----------

1. Optional: Install virtualenv and Python3 and create a virtual environment.
    ```
    virtualenv -p python3 ENV
    source ENV/bin/activate
    ```
2. Install the packages.
    ```
    pip install -r requirements.txt test-requirements.txt
    ```
3. Start the app.
    ```
    python3 app.py
    ```
4. Test the app.
    ```
    pytest
    ```


For the configuration of the app through environment variables,
see the [app.json] file.

[app.json]: app.json
