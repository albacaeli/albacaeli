"""Models for the Flask-SQLAlchemy database

We follow http://flask-sqlalchemy.pocoo.org/2.1/models/
"""

from app import db
from flask.ext.login import UserMixin

class User(db.Model, UserMixin):
	"""A user
	
	"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)

	def __init__(self, username, email=None):
		self.username = username
		self.email = email
		

	def __repr__(self):
		return '<User %r>' % (self.username)

# Do not use these, apparently versions of flask-login have changed them from functions to attributes...
# Instead, we inherit from UserMixin.
"""
	# We add the stuff below to make it Flask-Login friendly:
	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)	 # python 2
		except NameError:
			return str(self.id)	 # python 3
"""





# We define a helper table to create a many-to-many relationship
# An Object will get a "cats" attribute which is a list of Catalogs.
catalogs = db.Table('catalogs',
	db.Column('object_id', db.Integer, db.ForeignKey('object.id')),
	db.Column('catalog_id', db.Integer, db.ForeignKey('catalog.id'))
)

# idem for the observations (not sure why this is many to many!)
objects_observed = db.Table('objects_observed',
	db.Column('logged_observation_id', db.Integer, db.ForeignKey('logged_observation.id')),
	db.Column('object_id', db.Integer, db.ForeignKey('object.id'))
)
 
 
class Object(db.Model):
	"""A celestial object
	
	One object can be in many catalogs.
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	text = db.Column(db.Text) # We should specify for what this is for
	type = db.Column(db.String(64))
	ra = db.Column(db.Float)
	dec = db.Column(db.Float)

	cats = db.relationship('Catalog', secondary=catalogs, backref=db.backref('objects', lazy='dynamic'))

	def __init__(self, name, text, type="Star", ra=0.0, dec=0.0):
		self.name = name
		self.text = text
		self.type = type
		self.ra = ra
		self.dec = dec

	def __repr__(self):
		return '<Object %r>' % (self.name)
		


class LoggedObservation(db.Model):
	"""A log for one object.
	
	"""
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(80))
	timestamp = db.Column(db.DateTime)
	description = db.Column(db.Text)
	objects = db.relationship('Object', secondary=objects_observed, backref=db.backref('logged_observations', lazy='dynamic'))
	# Why is this plural ? Only one object per LoggedObservation, no ?

	def __repr__(self):
		return '<LoggedObservation %r: %r>' % (self.id, self.title)
    


class Catalog(db.Model):
	"""A catalog of celestial objects
	
	A catalog can have many objects. 
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Catalog %r>' % self.name
	
	
class Star(db.Model):
	"""A dedicated database for "foreground" stars to be drawn in charts
	
	"""
	id = db.Column(db.Integer, primary_key=True)
	
	HD = db.Column(db.Integer)
	ra = db.Column(db.Float)
	dec = db.Column(db.Float)
	magV = db.Column(db.Float)
	#Bay = db.Column(db.String(64)) Would need unicode in the SQLalchemy... fix this later.
	const = db.Column(db.String(64))
	HIP = db.Column(db.Integer)
	
	def __init__(self, HD, ra, dec, magV, Bay, const, HIP):
		
		self.HD = HD
		self.ra = ra
		self.dec = dec
		self.magV = magV
		#self.Bay = Bay
		self.const = const
		self.HIP = HIP

	def __repr__(self):
		return '<Star HD %r>' % (self.HD)
	





	