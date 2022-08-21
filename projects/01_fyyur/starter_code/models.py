#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from unicodedata import name
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class City(db.Model):
  __tablename__ = 'cities'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  state = db.Column(db.String)

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    venues = db.relationship('Venue', secondary='shows', backref='artists', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# show = db.Table('shows', 
# db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
# db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
# db.Column('start_time', db.DateTime, nullable=False))

class Show(db.Model):
  __tablename__ = 'shows'
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), primary_key=True)
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
  start_time = db.Column('start_time', db.DateTime, nullable=False)
  is_done = db.Column(db.Boolean)