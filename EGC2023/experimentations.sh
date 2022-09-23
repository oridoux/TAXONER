cd CRI
echo "**********************************************************************"
echo "LATIN strict"
time python3 Experiences/score_corpus.py -cl LATIN -m raw
echo "**********************************************************************"
echo "LATIN strict + abbrev"
time python3 Experiences/score_corpus.py -cl LATIN -m A
echo "**********************************************************************"
echo "TAXREF strict"
time python3 Experiences/score_corpus.py -cl TAXREF -m raw
echo "**********************************************************************"
echo "TAXREF strict + A"
time python3 Experiences/score_corpus.py -cl TAXREF -m A

