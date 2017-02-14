#FindIt!

An app for finding things in your house.

## Deployed site
Find-it is deployed on Heroku at https://rts-find-it.herokuapp.com/.

## Technologies used

This website is powered by Django.
The css is compiled from SASS.

## Approach

This is my first (non-tutorial) Django app. I relied heavily on the
book [Django Unleashed](https://django-unleashed.com/) by Andrew Pinkham
for my general app set-up and development approach.

## Limitations

The most glaring thing that's missing from this app is testing. I consider
tesing to be an essential part of web development. However, the tutorial I
used as a basis for this app's development did not include testing, and in
the interests of time, I have overlooked it here. It is definitely the next
thing on my list to learn in Django.

## Next steps

Beyond testing, most ideas for features are listed in the Github issues and
organized into release milestones.

## Development

This app was developed using Django 10.3 and Python 3

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
  1. Set the dev environment: `export DJANGO_SETTINGS_MODULE=findIt.settings.dev`
  1. You can now run a local server! `./manage.py runserver`


When editing scss, use `sass --watch templates/styles/index.scss:static/site/index.css` to
auto-update css files.

When editing all other files, `./manage.py runserver` will run a local
server and watch for file changes.
