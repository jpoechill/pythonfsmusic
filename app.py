#!/usr/bin/env python
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask import make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Artist, User
from urlparse import urlparse
import httplib2
import httplib
import requests
import psycopg2
import json
import string
import random
import validators
import re


engine = create_engine('sqlite:///fsmusic.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

DBNAME = "fsmusic"

app = Flask(__name__, static_url_path='/static')
app.secret_key = "pns07bL1ON6AC6BqHT6Pe5OG"
app.config['SESSION_TYPE'] = 'filesystem'


# Main functions
@app.route('/')
def showRoot():
    return render_template(    
        'index.html', genres=getGenres(),
        artists=getAllArtists(), loggedIn=loggedIn())


# Show Login
@app.route('/login', methods=['GET'])
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))

    login_session['state'] = state
    return render_template('login.html', STATE=state, login_session=login_session, genres=getGenres())


# Show Categories
@app.route('/<categoryname>', strict_slashes=False)
def showCategory(categoryname):
    # Get all categories
    theCategory = filter(
        lambda x: categoryname == x.name.lower().replace(' ', ''),
        session.query(Category).all())

    artists = filter(
        lambda x: theCategory[0].name ==
        x.category.name, session.query(Artist).all())

    return render_template(
        'category.html', genres=getGenres(), categoryshortname=categoryname,
        category=theCategory[0], artists=artists)


# Show Add
@app.route('/<categoryname>/add',  methods=['GET'], strict_slashes=False)
def showAdd(categoryname):
    if not loggedIn():
        return redirect('/login')

    return render_template(
        'add.html', genres=getGenres(), category=categoryname)


# Execute Add
@app.route('/<categoryname>/add', methods=['POST'])
def makeAdd(categoryname):
    if not loggedIn():
        return redirect('/login')

    user_id = getUserID(login_session['email'])

    if validators.url(request.form['image']):
        validIMG = request.form['image']
    else:
        validIMG = '/static/male-avatar.png'

    theCategory = filter(
        lambda x: x.name == request.form['genre'],
        session.query(Category).all())

    newArtist = Artist(
        name=request.form['name'],
        image=validIMG,
        shortname=createUniqShortname(request.form['name']),
        description=request.form['description'],
        category=theCategory[0],
        user_id=user_id)

    session.add(newArtist)
    session.commit()

    return redirect(
        url_for(
            'showCategory', categoryname=categoryname))


# Show Artist
@app.route('/<categoryname>/<artist>', strict_slashes=False)
def showArtist(categoryname, artist):
    shortname = artist

    theseArtists = filter(
        lambda x: x.shortname ==
        shortname, session.query(Artist).all())

    return render_template(
        'artist.html', genres=getGenres(), category=categoryname,
        artist=theseArtists[0], shortname=shortname)


# Show Edit
@app.route('/<categoryname>/<artist>/edit', methods=['GET'])
def showEdit(categoryname, artist):
    if not loggedIn():
        return redirect('/login')

    shortname = artist

    theArtist = filter(
        lambda x: artist == x.shortname,
        session.query(Artist).all())

    return render_template(
        'edit.html', genres=getGenres(), category=categoryname,
        artists=theArtist, shortname=shortname)


# Execute Edit
@app.route('/<categoryname>/<artist>/edit', methods=['POST'])
def makeEdit(categoryname, artist):
    if not loggedIn():
        return redirect('/login')

    shortname = artist

    # Find Artist
    theArtist = filter(
        lambda x: shortname == x.shortname,
        session.query(Artist).all())

    # Check authorization
    currentID = getUserID(login_session['email'])

    if currentID != theArtist[0].user_id:
        print "User not authorized"
        return redirect('/?noautho')

    # Fetch new values
    new_genre = request.form['genre']
    new_genre_shortname = request.form['genre'].lower().replace(" ", "")
    new_name_shortname = request.form['name'].lower().replace(" ", "")

    # Find Category
    theCategory = filter(
        lambda x: x.name == new_genre, session.query(Category).all())

    theArtist[0].name = request.form['name']
    theArtist[0].image = request.form['image']
    theArtist[0].description = request.form['description'].replace("'", r"''")
    theArtist[0].category = theCategory[0]

    # Update DB
    session.add(theArtist[0])
    session.commit()

    return redirect(
        url_for(
            'showArtist', categoryname=new_genre_shortname,
            artist=shortname))


# Show Delete
@app.route('/<categoryname>/<artist>/delete', methods=['GET'])
def showDelete(categoryname, artist):
    if not loggedIn():
        return redirect('/login')

    return render_template(
        'delete.html', genres=getGenres(), category=categoryname)


# Execute Delete
@app.route('/<categoryname>/<artist>/delete', methods=['POST'])
def makeDelete(categoryname, artist):
    if not loggedIn():
        return redirect('/login')

    shortname = artist

    # Find Artist
    theArtist = filter(
        lambda x: shortname == x.shortname,
        session.query(Artist).all())

    # Check authorization
    currentID = getUserID(login_session['email'])

    if currentID != theArtist[0].user_id:
        print "User not authorized"
        return redirect('/?noautho')

    # Make delete
    session.delete(theArtist[0])
    session.commit()

    return redirect(url_for('showCategory', categoryname=categoryname))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'

        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()


    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data["email"]

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = login_session['username']
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        # return response
        loggedInStatus = False
        return redirect('/')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# API Endpoints
@app.route('/JSON')
def allArtistsJSON():
    artists = session.query(Artist).all()
    return jsonify(Artists=[i.serialize for i in artists])


@app.route('/<categoryname>/<artist>/JSON')
def singleArtistJSON(categoryname, artist):
    singleArtist = session.query(Artist).filter_by(shortname=artist).one()
    return jsonify(Artist=singleArtist.serialize)
#
#
@app.route('/<categoryname>/JSON')
def categoryJSON(categoryname):
    category = session.query(Category).filter_by(shortname=categoryname).one()
    artists = session.query(Artist).filter_by(
        category=category).all()
    return jsonify(allCategoryArtists=[r.serialize for r in artists])


# App functions
def createUniqShortname(name):
    # Attempt to create new shortname
    name = name.lower().replace(' ', '')

    # Check if already exist
    searchNames = filter(
        lambda x: name == x.name.lower().replace(' ', ''),
        session.query(Artist).all())

    if searchNames:
        # Name exists, query tail
        sorted(searchNames, key=lambda x: x.shortname)
        endString = re.sub('.*?([0-9]*)$', r'\1', searchNames[-1].shortname)

        # Test and modify, if needed
        if endString == '':
            name = name + '1'
        else:
            name = name + str(int(endString) + 1)
    else:
        return name


def getGenres():
    return session.query(Category).all()


def getAllArtists():
    return session.query(Artist).all()


def loggedIn():
    if 'username' not in login_session:
        login_session['email'] = ''
        login_session['gplus_id'] = ''
        login_session['access_token'] = ''
        return False
    else:
        return True


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def uri_validator(x):
    try:
        result = urlparse(x)
        return True if [result.scheme, result.netloc, result.path] else False
    except:
        return False


# Main subroutine
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.globals.update(loggedIn=loggedIn)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
