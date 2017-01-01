#FindIt!

An app for finding things in your house.

## Technologies used

This website is powered by Django.
The css is compiled from SASS.

## Approach

This is my first (non-tutorial) Django app. I relied heavily on the
book [Django Unleashed](https://django-unleashed.com/) by Andrew Pinkham
for my general app set-up and development approach.

## Development

This app was developed using Django 10.3

Setup:
  1. I recommend developing in a virtualenv
  1. Install requirements and dev requirements:
     `pip install -r requirements.txt`
     `pip install -r dev_requirements.txt`
  1. Create the database (in bash: `psql`, in postgreSQL: `CREATE DATABASE findit;`)
  1. Give a user permissions to the `findit` database: `GRANT ALL PRIVILEGES ON DATABASE findit TO <user>;`
  1. Add your postgres password (PASSWORD) and (SECRET_TOKEN) as environment variables.
      In bash: `export $PASSWORD='<your_password>'`
  1. Run the migrations: `./manage.py migrate`.
  1. Run `make css` to generate site's css file.
  1. Set the dev environment: `export DJANGO_SETTINGS_MODULE=findIt.settings.dev`
  1. You can now run a local server! `./manage.py runserver`


When editing scss, use `sass --watch templates/styles/index.scss:static/site/index.css` to
auto-update css files.

When editing all other files, `./manage.py runserver` will run a local
server and watch for file changes.
