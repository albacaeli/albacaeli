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
		assert len(row["RA"]) == 9
		assert len(row["Decl"]) in [9, 10]
		
		decd = float(row["Decl"][-9:-7])
		decm = float(row["Decl"][-6:-4])
		decs = float(row["Decl"][-3:-1])
		dec = (decd + decm/60.0 + decs/3600.0)
		if row["Decl"][0] == "-":
			dec *= -1.0
		
		rah = float(row["RA"][-9:-7])
		ram = float(row["RA"][-6:-4])
		ras = float(row["RA"][-3:-1])
		ra = (rah + ram/60.0 + ras/3600.0) * 15.0
		
		db.session.add(models.Object(name=row["Name"], type=row["Type"], text="Imported from H400.csv", ra=ra, dec=dec))

# We add the stars
stars = bsc.readstars("data/IV_27A/catalog.dat", n=None)
for s in stars:
	if s.magV < 8.0:
		db.session.add(models.Star(s.HD, s.ra, s.dec, s.magV, s.Bay, s.const, s.HIP))

db.session.commit()
