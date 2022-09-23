#!/bin/bash

echo "première expérience TAXREF (avec abbréviations)"
python3 Experiences/score_corpus.py -cl TAXREF  -m A -s Experiences/empty.txt
echo "première expérience TAXREF (sans abbréviations)"
python3 Experiences/score_corpus.py -cl TAXREF -s Experiences/empty.txt
echo "expérience LINNAEUS"
python3 Experiences/score_corpus.py -cl LINNAEUS

echo "expérience Table 1"
# besoin du script


echo "expérience section 5"
python3 Experiences/score_corpus.py -cl LATIN -m A:MM:mm -s Experiences/empty.txt

echo "expériences figure 1 LATIN"
python3 Experiences/decision_bound_procedure.py -m CRI
echo "expériences figure 1 TAXREF"
python3 Experiences/decision_bound_procedure.py -m TAXREF

echo "expériences table 2"
# à modifier
for mode in {"7", "3", "4", "6", "7abs3", "7abs5", "7abs7"}; do
	 (time python3 Experiences/score_corpus.py -m $mode -vs test)
done
