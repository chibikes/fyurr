#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
import logging
from logging import Formatter, FileHandler
from datetime import datetime
from forms import ArtistForm, ShowForm, VenueForm
from models import app,db,City,Show,Venue,Artist
  
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  shows = Show.query.all()
  venues = Venue.query.all()
  cities = City.query.all()
  real_data = []
  for c in cities:
    cdict = {}
    slists = []
    cdict['city'] = c.name
    cdict['state'] = c.state
    for v in venues:
      shows = Show.query.filter_by(venue_id=v.id).count()
      if v.city == c.name:
        slists.append({'id': v.id, 'name': v.name, 'num_incoming_shows' : shows})
    cdict['venues'] = slists
    real_data.append(cdict)

  return render_template('pages/venues.html', areas=real_data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  name = request.form.get('search_term')

  sql = 'SELECT * FROM venues WHERE name LIKE \'%' + name + '%\''
  
  result = db.engine.execute(db.text(sql))
  
  venues = result.fetchall()
  
  
  res_dict = {}
  res_dict['count'] = len(venues)
  res_dict['data'] = []
  for venue in venues:
    upcoming_shows = Show.query.filter_by(venue_id=venue[0]).count()
    ven = {'id': venue[0], 'name': venue[1], 'num_upcoming_shows': upcoming_shows}
    res_dict['data'].append(ven)

  return render_template('pages/search_venues.html', results=res_dict, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
  past_shows = []
  upcoming_shows = []
  v = Venue.query.get(venue_id)
  

  num_past_shows = len(past_shows_query)
  num_upcoming_shows = len(upcoming_shows_query)
  for show in past_shows_query:
    past_shows.append({
      'artist_id' : show.artist_id,
      'artist_name' : Artist.query.get(show.artist_id).name,
      'artist_image_link' : Artist.query.get(show.artist_id).image_link,
      'start_time' : show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })

    for show in upcoming_shows_query:
        upcoming_shows.append({
      'artist_id' : show.artist_id,
      'artist_name' : Artist.query.get(show.artist_id).name,
      'artist_image_link' : Artist.query.get(show.artist_id).image_link,
      'start_time' : show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })


  data={
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city,
    "state": v.state,
    "phone": v.phone,
    "website": v.website_link,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description,
    "image_link": v.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------



@app.route('/venues/create', methods=['GET','POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = VenueForm()
    if form.validate_on_submit():
      try:
        try:
          request.form['seeking_talent']
          isSeekingTalent = True
        except:
          isSeekingTalent = False
        city = City(name=request.form['city'],state=request.form['state'])
        dcity = City.query.filter(City.name==request.form['city']).first()
        if dcity:
          print()
        else:
          db.session.add(city)

        ven = Venue(name=request.form['name'],city=request.form['city'],state=request.form['state'],
        address= request.form['address'],phone=request.form['phone'],
        image_link=request.form['image_link'], facebook_link=request.form['facebook_link'],
        website_link=request.form['website_link'],seeking_talent=isSeekingTalent,
        seeking_description=request.form['seeking_description'],genres=request.form.getlist('genres'))
        db.session.add(ven)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
      except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed')
        print(sys.exc_info())
      finally:
        db.session.close()
    else:
      for field, message in form.errors.items():
          flash(field + ' - ' + str(message), 'danger')
  
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)
    venues = Venue.query.filter_by(city=venue.city)
    if venues.count() <= 1:
      city = City.query.filter_by(name=venue.city).one()
      db.session.delete(city)
    db.session.delete(venue)
    db.session.commit()
    flash('Deleted successfully')
  except:
    print(sys.exc_info())
    flash('Delete was unsuccessful')
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  name = request.form.get('search_term')

  sql = 'SELECT * FROM artists WHERE name LIKE \'%' + name + '%\''
  
  result = db.engine.execute(db.text(sql))
  
  artists = result.fetchall()
  
  
  res_dict = {}
  res_dict['count'] = len(artists)
  res_dict['data'] = []
  for artist in artists:
    upcoming_shows = Show.query.filter_by(artist_id=artist[0]).count()
    ven = {'id': artist[0], 'name': artist[1], 'num_upcoming_shows': upcoming_shows}
    res_dict['data'].append(ven)
  
  return render_template('pages/search_artists.html', results=res_dict, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
  past_shows = []
  upcoming_shows = []
  a = Artist.query.get(artist_id)
  

  num_past_shows = len(past_shows_query)
  num_upcoming_shows = len(upcoming_shows_query)
  for show in past_shows_query:
    past_shows.append({
      'venue_id' : show.venue_id,
      'venue_name' : Venue.query.get(show.venue_id).name,
      'venue_image_link' : Venue.query.get(show.venue_id).image_link,
      'start_time' : show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })

    for show in upcoming_shows_query:
        upcoming_shows.append({
      'venue_id' : show.venue_id,
      'venue_name' : Venue.query.get(show.venue_id).name,
      'venue_image_link' : Venue.query.get(show.venue_id).image_link,
      'start_time' : show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })


  data={
    "id": a.id,
    "name": a.name,
    "genres": a.genres,
    "city": a.city,
    "state": a.state,
    "phone": a.phone,
    "website": a.website_link,
    "facebook_link": a.facebook_link,
    "seeking_venue": a.seeking_venue,
    "seeking_description": a.seeking_description,
    "image_link": a.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,

  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
# def edit_artist(artist_id):
#   form = ArtistForm()

#   data = Artist.query.get(artist_id)
  
#   # TODO: populate form with fields from artist with ID <artist_id>
  
#   return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  form.populate_obj(artist)

  if form.validate_on_submit():
    try:
      db.session.add(artist)
      db.session.commit()
      flash('Edit successfully')
    except:
      flash('An error occured')
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
    
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/venues/<int:venue_id>/edit', methods=['GET','POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  form.populate_obj(venue)

  if form.validate_on_submit():
    try:
      del_cities()
      # add city if it does not exist in the city database
      cities = City.query.filter_by(name=venue.city)
      if cities.count() < 1:
        new_city = City(name=venue.city, state=venue.state)
        db.session.add(new_city)
 
      db.session.add(venue)
      db.session.commit()
      flash('Edited successfully')
    except:
      print(sys.exc_info())
      flash('An error occured')
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET','POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  if form.validate_on_submit():
    try:
      isSeekingVenue = False
      try:
        y = request.form['seeking_venue']
        isSeekingVenue = True
      except:
        isSeekingVenue = False
      musician = Artist(name=request.form['name'],city=request.form['city'],state=request.form['state'],
      phone=request.form['phone'],
      image_link=request.form['image_link'], facebook_link=request.form['facebook_link'],
      website_link=request.form['website_link'],seeking_venue=isSeekingVenue,
      seeking_description=request.form['seeking_description'],genres=request.form.getlist('genres'))
      db.session.add(musician)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed')
    finally:
      db.session.close()
  else:
      for field, message in form.errors.items():
          flash(field + ' - ' + str(message), 'danger')
  return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  lshows = []
  try:
    for show in shows:
      show_dict = {}
      venue = Venue.query.get(show.venue_id)
      artist = Artist.query.get(show.artist_id)
      show_dict['venue_id'] = venue.id
      show_dict['venue_name'] = venue.name
      show_dict['artist_id'] = show.artist_id
      show_dict['artist_name'] = artist.name
      show_dict['artist_image_link'] = artist.image_link
      show_dict['start_time'] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    
      lshows.append(show_dict)
  except:
    print(sys.exc_info())
    
  
  return render_template('pages/shows.html', shows=lshows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # TODO: insert form data as a new Show record in the db, instead
  try:
    show = Show(venue_id=request.form['venue_id'],artist_id=request.form['artist_id'],start_time=request.form['start_time'])
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed. Make sure date is of the right format and try again')
  finally:
    db.session.close()
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

# method to delete redundant/duplicate cities
def del_cities():
  cities = City.query.all()
  for city in cities:
    venue = Venue.query.filter_by(city=city.name)
    if venue.count() < 1:
      city = City.query.get(city.id)
      db.session.delete(city)
  db.session.commit()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
