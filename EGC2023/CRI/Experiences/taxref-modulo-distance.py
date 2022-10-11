
import regex as re
import time

datapath = re.split(r'/', __file__)[:-3]
datapath.append("DATA")
datapath = "/".join(datapath)
print(f"{datapath = }")

def depouilleSondage29juillet():
# lecture du fichier sondage
# mise sous forme d'une liste de binômes
	sondage = open(f"{datapath}/sondage 12 mai 22 - positifs.txt").read()
	# print(sondage)
	sondageLines = re.split(r'\n', sondage)
	sondageList = []
	sondageListAbbrev = []
	for l in sondageLines:
		if re.search(r'in:',l):
			lWords = re.split(r' ', l)
			g = lWords[0] ; e = lWords[1]
			if len(g) == 2 and g[1] == '.':
				sondageListAbbrev.append((g[0], lWords[1]))
			else:	
				sondageList.append(f"{lWords[0]} {lWords[1]}")
	# print(sondageList)
	# print(sondageListAbbrev)
	nb_long_taxons = len(sondageList)
	nb_short_taxons = len(sondageListAbbrev)
	print(f"Nombre d'éléments de forme longue du sondage = {nb_long_taxons}")
	print(f"Nombre d'éléments de forme abrégée du sondage = {nb_short_taxons}")

# lecture du fichier TAXREF
# mise sous forme d'une chaîne de binômes
	taxref = open(f"{datapath}/taxref.out").read()
	taxreflines = re.split(r'\n', taxref)

	taxreflst = []
	for trl in taxreflines:
		ge = re.split(r'\s', trl)
		g = ge[0] ; es = ge[1:]      # g = genre, es = espèceS (une liste, parfois vide)
		# print("%s --- %s" % (g, str(e)))
		for e in es:
			taxreflst.append(f"{g} {e}")
	print("#taxreflst = ", len(taxreflst))
	taxreflst.sort()
	taxreflstuniq = []
	prev = ""
	for i in range(len(taxreflst)):
		if not (taxreflst[i] == prev):
			taxreflstuniq.append(taxreflst[i])
		prev = taxreflst[i]

	print("#taxreflstuniq = ", len(taxreflstuniq))
	# print("taxreflst ", taxreflst)

	fsondage = open("sondage29juilletXtaxref.txt", "w")
	cptge = 0
	cptgea = 0
	ttot = {}
	for d in range(0,5):
		print("distance = ", d)
		tstart = time.time()
		nextsondageList = []
		cptge_prev = cptge
		for gesondage in sondageList:
			# print("gesondage = ", gesondage)
			gere = r"({}){{e<={}}}".format(gesondage, d)
			gerecmp = re.compile(gere)
			# print("gere = ", gere)
			found = False
			for getaxref in taxreflstuniq:
				res = gerecmp.fullmatch(getaxref)
				if (res != None):
					cptge += 1
					# print(f"{cptge}: getaxref = ", gesondage, " = ", getaxref, f" mod {d}")
					found = True
					break
			if not found:
				nextsondageList.append(gesondage)
		print("# reste sondageList = ", len(sondageList), file=fsondage, flush=True)
		tend = time.time()
		ttot[d] = (tend-tstart)/60
		print(f"durée mod {d} = ", ttot[d]/ttot[0], file=fsondage, flush=True)
		print(f"cptge mod {d} = ", (cptge-cptge_prev)/nb_long_taxons, file=fsondage, flush=True)
		sondageList = nextsondageList
		# print(sondageList)

	
	for d in range(0,5):
		print("distance = ", d)
		tstart = time.time()
		nextsondageListAbbrev = []
		cptgea_prev = cptgea
		for gesondage in sondageListAbbrev:
			# print("gesondage = ", gesondage)
			gere = r"{}[a-z]+ ({}){{e<={}}}".format(gesondage[0], gesondage[1], d)
			gerecmp = re.compile(gere)
			# print("gere = ", gere)
			found = False
			for getaxref in taxreflstuniq:
				res = gerecmp.fullmatch(getaxref)
				if (res != None):
					cptgea += 1
					# print(f"{cptgea}: getaxref = ", gesondage, " = ", getaxref, f" mod {d}")
					found = True
					break
			if not found:
				nextsondageListAbbrev.append(gesondage)
		print("# reste sondageListAbbrev = ", len(sondageListAbbrev), file=fsondage, flush=True)
		tend = time.time()
		ttot[d] = (tend-tstart)/60
		print(f"durée mod {d} = ", ttot[d]/ttot[0], file=fsondage, flush=True)
		print(f"cptge mod {d} = ", (cptgea-cptgea_prev)/nb_short_taxons, file=fsondage, flush=True)
		sondageListAbbrev = nextsondageListAbbrev
		# print(sondageListAbbrev)	


depouilleSondage29juillet()

