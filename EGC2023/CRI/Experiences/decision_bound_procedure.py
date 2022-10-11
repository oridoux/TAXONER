import re
import os
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(
    description="evaluates all of the articles \
    in the Corpus and prints the results")
parser.add_argument("-m", "--mode",
                    help="chosen mode",
                    choices=["LATIN", "TAXREF"])
parser.add_argument(
    "-o", "--output",
    help="if providied, the results will be printed in this file")
args = parser.parse_args()


def compute_volume():
    resultfile = "results/results_1.txt"
    difffile = "results/diff_1.txt"

    os.system("mkdir -p results")
    digits = re.compile(r"\d+")

    reference = "results/results_500.txt"

    cmd_test_volume = "python3 Experiences/test_volume.py 14 latin_bin_and_names -o"

    for i in range(500, 10000, 500):
        stri = str(i)
        resultfile = digits.sub(stri, resultfile)
        difffile = digits.sub(stri, difffile)
        cmd_stopwords = f"python3 Experiences/compute_stopwords.py -n {i} Experiences/stopwords.txt"
        with open(resultfile, "w") as res:
            os.system(cmd_stopwords)
            os.system(cmd_test_volume + resultfile)

        os.system(f"diff -y {reference} {resultfile} > {difffile}")
        reference = resultfile


def print_curves(x, pr, re, fm):
    plt.plot(x, pr, 'o-', color="blue", label="précision")
    plt.plot(x, re, 'o--', color="red", label="rappel")
    plt.plot(x, fm, 'o-', color="green", label="f-mesure")
    plt.xlabel('Nombre de mots supprimés')
    plt.title(
        'Évolution de la qualité de reconaissance en fonction du nombre de mots supprimés')
    plt.legend()
    plt.savefig('decision_bound_curves.png')
    plt.show()


def find_bound():
    prec = []
    rec = []
    fme = []
    x = []
    a = r"overall scores on the whole corpus:.*"
    b = r"precision = (?P<p>\d+\.\d+) %.*"
    c = r"recall = (?P<r>\d+\.\d+) %.*"
    d = r"F-measure = (?P<fm>\d+\.\d+)"
    results = re.compile(a+b+c+d, flags=re.DOTALL)
    stops_path = "Experiences/tmp_stopwords.txt"
    if args.mode == "LATIN":
        classifier = "LATIN"
        file_name = "analyses/evolution_latin.csv"
    elif args.mode == "TAXREF":
        classifier = "ABS3"
        file_name = "analyses/evolution_TAXREF.csv"
    else:
        exit("unexpected mode")
    cmd = f"python3 Experiences/score_corpus.py -o tmp -cl {classifier} -m A -s {stops_path} -vs calibration"
    best_prec = (.0, "0")
    best_rec = (.0, "0")
    best_fm = (.0, "0")
    with open(file_name, "w") as data:
        data.write("i,precision,recall,fmeasure\n")
        for i in range(500, 45000, 5000):
            print(f"starting the evaluation with {i} words removed")
            stri = str(i)
            cmd_stopwords = f"python3 Experiences/compute_stopwords.py -n {i} {stops_path}"
            os.system(cmd_stopwords)
            os.system(cmd)
            with open("tmp", "r") as results_file:
                text = "".join(results_file)
                match = results.search(text)
                p = float(match.group("p"))
                r = float(match.group("r"))
                fm = float(match.group("fm"))
                x.append(i)
                prec.append(p)
                rec.append(r)
                fme.append(fm)
                print(
                    f"i = {stri}, precision = {p}, recall = {r}, F-measure = {fm}")
                data.write(
                    f"{i},{match.group('p')},{match.group('r')},{match.group('fm')}\n")
                if r > best_rec[0]:
                    best_rec = (r, stri)
                if fm > best_fm[0]:
                    best_fm = (fm, stri)
                if p > best_prec[0]:
                    best_prec = (p, stri)
                if fm < .9 * best_fm[0]:
                    print_curves(x, prec, rec, fme)
                    os.system("rm tmp")
                    os.system(f"rm {stops_path}")
                    return(stri, best_prec, best_rec, best_fm)
            os.system(f"rm {stops_path}")
            os.system("rm tmp")
    # print_curves(x, prec, rec, fme)
    return(stri, best_prec, best_rec, best_fm)


i, prec, rec, fm = find_bound()
results = f"stopped at {i} because the F-measure was too low\nbest precision : {prec}\nbest recall : {rec}\nbest fm-measure : {fm}"

if args.output:
    with open(args.output, "a") as out:
        out.write(results)
    else:
        print(results)
