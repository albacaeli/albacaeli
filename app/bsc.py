#-*- coding: utf-8 -*-
"""
Quite custom stuff to read the Bright Star Catalog (BSC) files taken from Stellarium...
"""


alphabet={'alf  ':'α','alf01':'α¹','alf02':'α²',\
  'bet  ':'β','bet01':'β¹','bet02':'β²','bet03':'β³',\
  'gam  ':'γ','gam01':'γ¹','gam02':'γ²','gam03':'γ³',\
  'del  ':'δ','del01':'δ¹','del02':'δ²','del03':'δ³',\
  'eps  ':'ε','eps01':'ε¹','eps02':'ε²','eps03':'ε³',\
  'zet  ':'ζ','zet01':'ζ¹','zet02':'ζ²','zet03':'ζ³',\
  'eta  ':'η','eta01':'η¹','eta02':'η²','eta03':'η³',\
	  'the  ':'θ','the01':'θ¹','the02':'θ²','the03':'θ³',\
  'iot  ':'ι','iot01':'ι¹','iot02':'ι²',\
  'kap  ':'κ','kap01':'κ¹','kap02':'κ²',\
  'lam  ':'λ','lam01':'λ¹','lam02':'λ²','lam03':'λ³',\
  'mu.  ':'μ','mu.01':'μ¹','mu.02':'μ²','mu.03':'μ³',\
	  'nu.  ':'ν','nu.01':'ν¹','nu.02':'ν²','nu.03':'ν³',\
  'ksi  ':'ξ','ksi01':'ξ¹','ksi02':'ξ²','ksi03':'ξ³',\
	  'omi  ':'ο','omi01':'ο¹','omi02':'ο²','omi03':'ο³',\
  'pi.  ':'π','pi.01':'π¹','pi.02':'π²','pi.03':'π³','pi.04':'π⁴','pi.05':'π⁵','pi.06':'π⁶',\
  'rho  ':'ρ','rho01':'ρ¹','rho02':'ρ²','rho03':'ρ³',\
  'sig  ':'σ','sig01':'σ¹','sig02':'σ²','sig03':'σ³',\
  'tau  ':'τ','tau01':'τ¹','tau02':'τ²','tau03':'τ³','tau04':'τ⁴','tau05':'τ⁵','tau06':'τ⁶','tau07':'τ⁷','tau08':'τ⁸','tau09':'τ⁹',\
  'ups  ':'υ','ups01':'υ¹','ups02':'υ²','ups03':'υ³',\
  'phi  ':'φ','phi01':'φ¹','phi02':'φ²','phi03':'φ³','phi04':'φ⁴',\
  'chi  ':'χ','chi01':'χ¹','chi02':'χ²','chi03':'χ³',\
  'psi  ':'ψ','psi01':'ψ¹','psi02':'ψ²','psi03':'ψ³','psi04':'ψ⁴','psi05':'ψ⁵','psi06':'ψ⁶','psi07':'ψ⁷','psi08':'ψ⁸','psi09':'ψ⁹',\
  'ome  ':'ω','ome01':'ω¹','ome02':'ω²','ome03':'ω³'}
	

class Star():
	"""
	Coords are in degrees, J2000
	ra beteen 0 and 360
	dec between -90 and 90
	
	"""
	def __init__(self, HD, ra, dec, magV, Bay, const, HIP):
		self.HD = HD
		self.ra = ra
		self.dec = dec
		self.magV = magV
		self.Bay = Bay
		self.const = const
		self.HIP = HIP
	
	def __str__(self):
		return "%8s : %10.4f, %10.4f, V = %5.2f, Bay = %s" % (self.HD, self.ra, self.dec, self.magV, self.Bay)
			

def readstars(filepath, n=None):

	catfile = open(filepath, "r")
	lines = catfile.readlines()
	catfile.close()
	stars = []

	if n != None:
		lines = lines[:n]
	for line in lines:
		line.rstrip()
		assert len(line) == 78
		
		try:
			HD = int(line[0:6])
		except:
			HD = 0
		try:
			magV = float(line[58:63])
		except:
			magV = 10.0	
		Bay = line[68:73]
		try:
			Bay = alphabet[Bay]
		except:
			Bay = ""
		try:
			HIP = int(line[31:37])
		except:
			HIP = None	
			
		const = line[74:77]
		
		rah = float(line[38:40])
		ram = float(line[40:42])
		ras = float(line[42:47])
		ra = (rah + ram/60.0 + ras/3600.0) * 15.0
		
		decg = line[48:49]
		decd = float(line[49:51])
		decm = float(line[51:53])
		decs = float(line[53:57])
		
		dec = (decd + decm/60.0 + decs/3600.0)
		if decg == "-":
			dec *= -1.0
		
		star = Star(HD=HD, ra=ra, dec=dec, magV=magV, Bay=Bay, const=const, HIP=HIP)
		stars.append(star)
		
	return stars


# def findstar(stars, val, name="HIP"):
# 	vals = [getattr(star, name) for star in stars]
# 	try:
# 		index = vals.index(val)
# 		return stars[index]
# 	except:
# 		print "Cannot find HIP %i" % (val)
# 		return None
# 	
	
	
# def readconsts(filepath = "data/constellations.txt"):
# 	"""
# 	Build a dictionnarry containing the HIP number pairs of lines to draw
# 	"""
# 	consts = {}
# 	constfile = open(filepath, "r")
# 	lines = constfile.readlines()
# 	constfile.close()
# 	for line in lines:
# 		if len(line) < 10:
# 			continue
# 		elements = line.split()
# 		name = elements[0]
# 		n = int(elements[1])
# 		hipcouples = []
# 		for i in range(n):
# 			hipcouples.append((int(elements[2+2*i]), int(elements[3+2*i])))
# 		consts[name] = hipcouples
# 	return consts
# 		
# 
# def idconsts(stars, consts):
# 	"""
# 	Replaces HIP numbers by Stars
# 	"""
# 	out = {}
# 	for (name, couplelist) in consts.iteritems():
# 		out[name] = []
# 		print name
# 		for couple in couplelist:
# 			out[name].append((findstar(stars, val=couple[0], name="HIP"), findstar(stars, val=couple[1], name="HIP")))
# 	return out
# 			
		
	

	

