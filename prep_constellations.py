"""
We prepare a static TSV file containing the constellation stick figures in a format suitable for D3

"""

from app import bsc
import csv

consts_HIP = bsc.readconsts("data/constellations.txt") # Those are just HIP numbers
stars = bsc.readstars("data/IV_27A/catalog.dat", n=None)

consts = bsc.idconsts(stars, consts_HIP)

# This is a dict with entries like
# 'Cru': [(<app.bsc.Star instance at 0x102915098>, <app.bsc.Star instance at 0x102910b00>), (<app.bsc.Star instance at 0x102915d88>, <app.bsc.Star instance at 0x102910128>)]


outfile = open("app/static/consts.tsv", "w")
writer = csv.writer(outfile, delimiter="\t")
writer.writerow(("ara", "adec", "bra", "bdec", "constname"))

#print consts in 

for (constname, starpairs) in consts.iteritems():
	for (stara, starb) in starpairs:
		if stara is None or starb is None:
			continue
		
		#print (stara, starb)
		
		writer.writerow((stara.ra, stara.dec, starb.ra, starb.dec, constname))
		
		#writer.writerow((object.name, object.ra, object.dec))

outfile.close()

#for const in consts



#print consts


