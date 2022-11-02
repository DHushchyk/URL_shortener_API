# URL Shortener API

API service for shortening url written on DRF

## Check it out!

[URL Shortener API project deployed to Heroku](https://short-a.herokuapp.com/api/)

## Installation

Python3 must be already installed

Install SQLite and create db

```shell
git clone https://github.com/DHushchyk/URL_shortener_API.git
cd URL_shortener_API
python3 -m venv venv
source venv\Scripts\activate (on Windows)
source venv\bin\activate (on Mac)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Getting access
* all guests get access to API


## Features
* Admin panel /admin/ (user: superuser, password: 0pHLx8GK)
* Creating short urls and getting lisl of them via API /api/links/
* Setting link's expiration date (1 day - 1 year, default: 90 days)
* Short link redirect
