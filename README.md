# Full Stack Music

An artist catalog for musician and singers.

Made with Python (Flask), PostgreSQL, and HTML/CSS (Bootstrap).

Oauth API by Google.


Enjoy!

## Screenshot

![Screenshot](/static/pythonfsmusic-ss.png)

## Steps to install and run:

  1. Setup and run vagrant (virtual server)

    `vagrant up`

    `vagrant ssh`

  2. Install packages

    `pip install validators`

  3. Populate database

    `python lotsOfArtists.py`

## Run app

  1. Run python app on local server

    `python app.py`

  2. Open page in browser

    `localhost:5000`

## JSON Endpoints

  1. All artists

      `location:5000/JSON`

  2. All artists per category

      `location:5000/<category>/JSON`

      ex. `location:5000/rock/JSON`

  3. Single artist detail

      `location:5000/<category>/<artist>/JSON`

      ex. `location:5000/rock/redhotchilipeppers/JSON`
