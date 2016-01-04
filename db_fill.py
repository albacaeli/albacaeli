from app import db, models
import csv

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

with open('data/H400.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	for row in reader:
		#print row
		db.session.add(models.Object(name=row["Name"], type=row["Type"], ra=0.0, dec=0.0))



db.session.commit()
