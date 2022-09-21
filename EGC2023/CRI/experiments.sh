#!/bin/bash

echo "première expérience TAXREF"
python3 Experiences/score_corpus.py -m 7 -v 0
echo "expérience LINNAEUS"
python3 Experiences/score_corpus.py -cl LINNAEUS

echo "expérience Table 1"
for mode in {"7", "7abs3", "7abs5", "7abs7"}; do
	echo "distance $mode"
	(time python3 Experiences/score_corpus.py -m $mode -v 0)
done

echo "expérience section 5"
python3 Experiences/score_corpus.py -m 6 -v 0 -s Experiences/empty.txt

echo "expériences figure 1" 
python3 Experiences/decision_bound_procedure.py -m CRI
echo "expériences figure 1" 
python3 Experiences/decision_bound_procedure.py -m TAXREF

echo "expériences table 2"
for mode in {"7", "3", "4", "6", "7abs3", "7abs5", "7abs7"}; do
	 (time python3 Experiences/score_corpus.py -m $mode -v 0)
done

