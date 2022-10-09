
import regex as re
import time
import argparse

TaxRef = "../../../TAXREF_v15_2021/TAXREFv15.txt"
taxref = "taxtref.out"

argparser = argparse.ArgumentParser(
	description = "Condensates the TAXREF reference file into a \\-separated list of taxons")

argparser.add_argument("input", nargs = "?", default = TaxRef, help = "Path to a TAXREF file")
argparser.add_argument("-i", "--input", help = "Path to a TAXREF file")

argparser.add_argument("output", nargs = "?", default = taxref, help = "Name for saving condensed file")
argparser.add_argument("-o", "--output", help = "Name for saving condensed file")


args = argparser.parse_args()
print(args)

def prepare(input = TaxRef, output = taxref):
# Prepare input file as a list of lines
	f = open(input)
	file = f.read()
	lines = re.split(r'\n', file)
#	print(len(lines))
#	print(lines[1000])

# Get position of field LB_NOM
	headings = re.split(r'\t', lines[0])
	print(headings)
	lb_nom = headings.index('"LB_NOM"')
#	print(tuples[3333][lb_nom])

# Prepare output file
	gef = open("taxref.out", "w") 

	for l in lines:
		l_splitted = re.split(r'\t', l)
		ge = l_splitted[lb_nom][1:-1]
		print(ge, file=gef, flush=True)

	

prepare()

