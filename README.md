## CROWDSOURCE

This is an API project called CROWDSOURCE built with Django Rest Framework.

## How to run the project locally

- Install Python
- Git clone the project with `https://github.com/Aderinmola/crowdsource.git`
- change directory with `cd crowdsource`
- Create your virtualenv with `py -m venv venv` and activate it.
- Install the requirements with `pip install -r requirements.txt`
- Finally run the API, in another terminal
  `python manage.py runserver`
- Go ahead to test the endpoints listed in the table below with postman, using the base url ` http://127.0.0.1:8000/swagger/`


## ROUTES TO IMPLEMENTED

| METHOD   | ROUTE               | FUNCTIONALITY       | ACCESS          |
| -------- | ------------------- | ------------------- | --------------- |
| _User_   |
| _GET_    | `/register/`   | _Create a User_     | _Register user_ |
| _POST_   | `/login/`           | _Login a User_      | _Login user_    |
| _POST_   | `/profile/`    | _View User Profile_ | _View Profile_  |
