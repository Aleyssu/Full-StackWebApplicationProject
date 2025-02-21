# Full Stack Web Application
This is the repo for a group project I've done in school for creating a full stack web application from scratch. I (Alex) created most of the framework, from the foundations of the front-end to the setting up and integration of the backend database. 

## Contributions
Alex Sun - Aleyssu

Nick Axani - NickAxani

Ewan Peterson - Ewan-Peterson

## To run
Make sure you have the required python packages installed. To do this, use
~~~bash
pip install -r requirements.txt
~~~
Once the requirements are installed, simply run `app.py` and go to the link shown in the console.

## Testing
Make sure you have pytest installed. To do this, use:
~~~bash
pip install pytest
~~~
Once you have pytest, simply use:
~~~bash
pytest test_app.py
~~~
to run the tests.

To run just the integration tests, use:
~~~bash
pytest test_app.py -m integration
~~~

## Coverage
Make sure you have Coverage installed.
~~~bash
pip install coverage
~~~
Once coverage is installed, run the coverage tool with
~~~bash
coverage run -m pytest
coverage report
~~~

## End to End Test
Make sure you have selenium, and webdriver-manager installed
~~~bash
pip install selenium
pip install webdriver-manager
~~~
Once you have the tools installed, start the app
~~~bash
python app.py testing
~~~
Finally, in a new terminal, run the end to end test script
~~~bash
python test_e2e.py
~~~
