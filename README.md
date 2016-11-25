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

Setup:
  1. I recommend developing in a virtualenv
  1. You must install django, postgresSQL and psychopg2
  1. Create the database (in bash: `psql`, in postgreSQL: `CREATE DATABASE findit;`)
  1. Give a user permissions to the `findit` database: `GRANT ALL PRIVILEGES ON DATABASE findit TO <user>;`
  1. Add your postgress password (PASSWORD) and (SECRET_TOKEN) as environment variables.
      In bash: `export $PASSWORD='<your_password>'`
  1. Run the migrations: `./manage.py migrate`
  1. Run `make css ` to generate site's css file.
  1. You can now run a local server! `./manage.py runserver`


When editing scss, use `sass --watch templates/styles/index.scss:static/site/index.css` to
auto-update css files.

When editing all other files, `./manage.py runserver` will run a local
server and watch for file changes.
