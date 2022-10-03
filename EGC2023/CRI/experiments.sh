#!/bin/bash

# echo "première expérience TAXREF (avec abbréviations)"
# python3 Experiences/score_corpus.py -cl TAXREF  -m A -s Experiences/empty.txt
# echo "première expérience TAXREF (sans abbréviations)"
# python3 Experiences/score_corpus.py -cl TAXREF -s Experiences/empty.txt

# echo "expérience LINNAEUS"
# python3 Experiences/score_corpus.py -cl LINNAEUS

# echo "expérience Table 1"
# # besoin du script

# echo "expériences section 4.2"
# for classifier in {"ABS7", "ABS5", "ABS3"}; do
#     python3 Experiences/score_corpus.py -cl $classifier -s Experiences/empty.txt
# done

# echo "expérience amélioration ad-hoc"
# python3  Experiences/score_corpus.py -cl ABS3 -s Experiences/empty.txt -a 1

# echo "expérience section 5"
# python3 Experiences/score_corpus.py -cl LATIN -m A:MM:mm -s Experiences/empty.txt

# echo "expériences figure 1 LATIN"
# python3 Experiences/decision_bound_procedure.py -m CRI
echo "expériences figure 1 TAXREF"
python3 Experiences/decision_bound_procedure.py -m TAXREF

# echo "expériences table 2"
# # à modifier
# for classifier in {"TAXREF", "LATIN", "ABS3"}; do
    # for mode in {"A", "A:MM", "A:mm:MM"}; do
    # 	 (time python3 Experiences/score_corpus.py -cl $classifier -m $mode -vs test)
    # done
# done
