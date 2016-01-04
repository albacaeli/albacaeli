from app import db, models, bsc
import csv
import numpy as np

# We erase the db:
users = models.User.query.all()
for e in users:
	db.session.delete(e)
objects = models.Object.query.all()
for e in objects:
	db.session.delete(e)
catalogs = models.Catalog.query.all()
for e in catalogs:
	db.session.delete(e)

db.session.commit()


db.session.add(models.User(username='user', email='user@gmail.com'))
db.session.add(models.User(username='test', email='test@test.com'))

with open("data/H400.csv") as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	for row in reader:
		#print row
		db.session.add(models.Object(name=row["Name"], type=row["Type"], ra=np.random.uniform(0.0, 360.0), dec=np.random.uniform(-90.0, 90.0)))


# We add the stars
stars = bsc.readstars("data/IV_27A/catalog.dat", n=None)
for s in stars:
	if s.magV < 8.0:
		db.session.add(models.Star(s.HD, s.ra, s.dec, s.magV, s.Bay, s.const, s.HIP))

db.session.commit()
