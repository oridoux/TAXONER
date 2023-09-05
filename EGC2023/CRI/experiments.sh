#!/bin/bash

output_file="results/experiments_results.md"


echo "expérience LINNAEUS"
echo "# expérience LINNAEUS" >> $output_file
## python3 Experiences/score_corpus.py -o $output_file -cl LINNAEUS


echo "Table 1"
echo "# première expérience TAXREF (avec abbréviations)" >> $output_file
## python3 Experiences/score_corpus.py -o $output_file -cl TAXREF  -m A -s Experiences/empty.txt

echo "première expérience TAXREF (sans abbréviations)"
echo "# première expérience TAXREF (sans abbréviations)" >> $output_file
## python3 Experiences/score_corpus.py -o $output_file -cl TAXREF -m raw -s Experiences/empty.txt


echo "expérience Table 2 (results in analyses/sondage29juilletXtaxref.txt)"
## python3 Experiences/taxref-modulo-distance


echo "expériences Table 3"
echo "# expériences Table 3" >> $output_file
## for classifier in "ABS7" "ABS5" "ABS4" "ABS3" "ABS2" 
## do
##     echo $classifier
##     python3 Experiences/score_corpus.py -o $output_file -cl $classifier -s Experiences/empty.txt
## done

echo "expérience amélioration ad-hoc"
echo "expérience amélioration ad-hoc" >> $output_file
## python3  Experiences/score_corpus.py -o $output_file -cl ABS3 -s Experiences/empty.txt -a 1

echo "expérience section 5"
echo "expérience section 5" >> $output_file
## python3 Experiences/score_corpus.py -o $output_file -cl LATIN -m A:MM:mm -s Experiences/empty.txt


echo "expériences figure 1 LATIN"
echo "# expériences figure 1 LATIN" >> $output_file
## python3 Experiences/decision_bound_procedure.py -m CRI -o $output_file

echo "expériences figure 1 TAXREF rang 2"
echo "# expériences figure 1 TAXREF rang 2" >> $output_file
## python3 Experiences/decision_bound_procedure.py -m TAXREF2 -o $output_file

echo "expériences figure 1 TAXREF rang 3"
echo "# expériences figure 1 TAXREF rang 3" >> $output_file
## python3 Experiences/decision_bound_procedure.py -m TAXREF3 -o $output_file
echo "you can find the csv for the experiments in the analyses folder at evolution_latin.csv and evolution_TAXREF.csv" 

echo "expériences table 4"
echo "# expériences table 4" >> $output_file
for classifier in 'MIXi' 'MIXu' 'ABS3' 'LATIN'
do
    for mode in 'A' 'A:MM' 'A:mm:MM' 
    do
      echo "running $classifier with mode $mode"
    	(time python3 Experiences/score_corpus.py -o $output_file -cl $classifier -m $mode -vs test)
    done
done

echo "tous les résultats ont étés écrits dans le fichier $output_file"
