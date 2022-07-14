# Intro

Solution for Backend task #1
https://mvpmatch.notion.site/Backend-1-9a5476e6cb7848ec9f620ce8a64c0d06

Programing language: Python 3.8
Framework: Django 4.0

Code Style Guidelines:
https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

Mostly follows the well known Python style guide PEP8. 
One big exception is the line length, where up to 119 characters are allowed.

```pip install flake8```
```flake8```
To check for rule exceptions - E501 (line length is ignored in `.flake8` config).
If existing codding style issues exist the command will list their error code and location.
If the code is clean, the command will exit with no input successfully.

##  Instructions

```shell
pip install -r requirements.txt

cd src
./manage.py migrate
./manage.py loaddata fixtures/auth.json
./manage.py runserver
```

By default the local server will run on port 8000.
Specify a different port if needed:
```./manage.py runserver 0.0.0.0:8001```

## After running a local server:

Go to `http://localhost:8000/api/users/`

Create User with Role - `seller`
POST:
```json
{
    "username": "test_seller",
    "password": "pa55_se!!er",
    "password_repeat": "pa55_se!!er",
    "role": ["seller"]
}
```

Create User with Role - `buyer`
POST:
```json
{
    "username": "test_buyer",
    "password": "pa55_buy3r",
    "password_repeat": "pa55_buy3r",
    "role": ["buyer"]
}
```

Go to `http://localhost:8000/api-auth/login`

Login as Seller
POST:
```json
{
    "username": "test_seller",
    "password": "pa55_se!!er"
}
```

Login as Buyer
POST:
```json
{
    "username": "test_buyer",
    "password": "pa55_buy3r"
}
```

Go to `http://localhost:8000/api/users/deposit/`

POST:
```json
{
    "amount": 100
}
```

Go to `http://localhost:8000/api/users/reset/`

GET:
no data

Go to `http://localhost:8000/api/products/`

POST:
```json
{
    "name": "product name",
    "seller_id": "seller id",
    "cost": 10,
    "amount_available": 10
}
```

Go to `http://localhost:8000/api/products/buy/`

POST:
```json
{
    "product": 1,
    "amount": 1
}
```

## Alternatively the prepared pytest TestCases can be run:

```shell
cd src
pip install -r test_requirements.txt
pytest --cov=apps                    # terminal output
pytest --cov-report html --cov=apps  # html output results will be generated in htmlcov/
```


## Auto generated documatation is provided:
http://localhost:8000/api/schema/redoc/
http://localhost:8000/api/schema/swagger-ui/