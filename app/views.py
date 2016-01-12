from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from .forms import LoginForm
from .models import User
from . import models
from . import forms

import io
import csv

# before any request, define g.user to make it accessible anywhere
@app.before_request
def before_request():
	g.user = current_user

# we have to write a function that loads a user from the database.
# This function will be used by Flask-Login
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/index')
def index():

	return redirect(url_for('show_observations'))

	
@app.route('/demo')
@login_required
def demo():

	objects = models.Object.query.all()
	return render_template('demo.html', title='Demo', objects=objects)

@app.route('/demo2')
@login_required
def demo2():

	objects = models.Object.query.all()
	return render_template('demo2.html', title='Demo 2', objects=objects)


@app.route('/tsvcatalog/<catname>')
@login_required
def tsvcatalog(catname):
	"""Turns a catalog from the database into a D3.js-friendly tab-separated-values
	
	I guess that this can be done better, but it's a start.
	"""
	
	output = io.BytesIO()
	writer = csv.writer(output, delimiter="\t")
	
	if catname == "objects":
		objects = models.Object.query.all()
		writer.writerow(("name", "ra", "dec"))
		for object in objects:
			writer.writerow((object.name, object.ra, object.dec))
	
	elif catname == "stars":
		stars = models.Star.query.all()
		writer.writerow(("HD", "ra", "dec", "magV"))
		for star in stars:
			writer.writerow((star.HD, star.ra, star.dec, star.magV))	
	
	else:
		flash('Unkown catalog!')
		return redirect(url_for('index'))
	
	return output.getvalue()	
	#return render_template('catalog.tsv', objects=objects) # No, bad idea. Better use the dedicated csv module here!



@app.route('/login', methods=['GET', 'POST'])
def login():

	#if hasattr(g, "user"):
	#	return redirect(url_for('index'))
	if g.user is not None and g.user.is_authenticated:
		flash("You are already logged in!")
		return redirect(url_for('index'))	
	
	form = LoginForm()
	if form.validate_on_submit():
		
		# We try to find that user in the db:
		user = User.query.filter_by(username=form.username.data)

		if user.count() == 1: # The username was found in the db
			
			login_user(user.first(), remember = form.remember_me.data)
			#session['remember_me'] = form.remember_me.data
			
			flash('Welcome back, {0}!'.format(form.username.data))
	
			#next = request.args.get('next')
			# next_is_valid should check if the user has valid
			# permission to access the `next` url
			#if not next_is_valid(next):
			#	return flask.abort(400)
			#return redirect(next or url_for('index'))
			
			return redirect(url_for('index'))
			
		else: # the username was not found in the db
			
			flash('Invalid login')
			return redirect(url_for('login'))
		
		
	return render_template('login.html', title='Sign In', form=form)	


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Logged out!")
	return redirect(url_for('index'))
	
	
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if user == None:
		flash('User "%s" not found.' % username)
		return redirect(url_for('index'))
	else:
		return render_template('user.html', user=user)


###########
###	 Views from astronomr, slightly adapted

@app.route('/object/<int:object_id>')
def show_object(object_id):
	
	theobject = models.Object.query.get(object_id)
	if theobject is None:
		flash("Could not find that object!")
		return redirect(url_for('index'))

	observations = theobject.logged_observations.order_by(models.LoggedObservation.id.desc())[:10]
	
	return render_template('show_object.html', theobject = theobject,
						   observations = observations)

###

@app.route('/object/<int:object_id>/edit', methods=['GET','POST'])
@login_required
def edit_object(object_id):


	theobject = models.Object.query.get(object_id)
	if theobject is None:
		flash("Could not find that object!")
		return redirect(url_for('index'))

	edit_object_form = forms.EditObjectForm(obj = theobject)
	if edit_object_form.validate_on_submit():

		theobject.name = edit_object_form.name.data
		theobject.text = edit_object_form.text.data

		db.session.add(theobject)
		db.session.commit()

		flash('%s successfully updated' % theobject.name)
		return redirect(url_for('show_object', object_id = object_id))

	

	return render_template('edit_object.html', theobject = theobject,
						   edit_object_form = edit_object_form)

		

###

def get_newest_obs(nobs):

	observations = models.LoggedObservation.query.order_by(models.LoggedObservation.id.desc())[:nobs]

	return observations

###


@app.route('/')
@app.route('/add', methods=['GET', 'POST'])
def show_observations():

	new_obs_interface = do_add_observation()

	newest_obs = get_newest_obs(10)

	return render_template('show_entries.html', new_obs_interface = new_obs_interface, observations=newest_obs)



###
@login_required
def do_add_observation():
		

	new_obs_form = forms.LoggedObservationForm()
	if new_obs_form.validate_on_submit():

		new_obs = models.LoggedObservation(title = new_obs_form.title.data,
										  timestamp = new_obs_form.timestamp.data,
										  description = new_obs_form.description.data)
		db.session.add(new_obs)

		object_names = new_obs_form.objects.data.split(',')
		for object_name in object_names:
			theobject = models.Object.query.filter_by(name = object_name).first()
			if theobject is None:
				theobject = models.Object(name=object_name, text='')
			new_obs.objects.append(theobject)
			db.session.add(theobject)

		db.session.commit()

		flash('New entry was successfully posted')

		new_obs_form = forms.LoggedObservationForm(formdata = None)


	return render_template('add_observation.html', new_obs_form = new_obs_form)
	
###
	
