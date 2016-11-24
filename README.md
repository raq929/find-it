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

When editing scss, use `sass --watch templates/styles:static/site/` to
auto-update css files.

When editing all other files, `./manage.py runserver` will run a local
server and watch for file changes.
