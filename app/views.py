from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from .forms import LoginForm
from .models import User
from . import models

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


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/demo')
@login_required
def demo():

	objects = models.Object.query.all()
	return render_template('demo.html', title='Demo', objects=objects)

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
	