import regex as re
import json
import Levenshtein as le
import os
import pandas as pd
import time

import argparse


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def contextualize(m, s, start, end, context, size):
    return (m, s[max(start-size, 0):min(end+size, len(s))]) if context else m


def update_results(s, context, size, result, match):
    m = match[0]
    c = contextualize(m, s, match.start(), match.end(), context, size)
    result.append(c)


def apply_matcher(stopwords, article, matcher, abbrev, context, size):
    s = clear_stopwords(stopwords, article)
    result = []
    r = r"(?<=\W)("
    b = False
    for match in matcher.finditer(s):
        update_results(s, context, size, result, match)
        # if the binom starts with a capitalized letter,
        # add the possibility to match a binom with thid genus abreviated
        if abbrev:
            a = re.match(upper_case, match[0])
            if a and a[0] != 'M':
                b = True
                r += rf"{a[0]}\.\s{acword}|"
    # try to find all the abreviated binoms in the page
    r = r[:-1] + r")(?=\W)"
    # do the search only if there are geni that can be abreviated
    if b:
        for match in re.finditer(r, s):
            update_results(s, context, size, result, match)
    return result


def classify(article, classifier, stopwords, mode="Mm:A", expr="", adhoc=False):
    with open(article) as in_:
        text = in_.read()
    if classifier == "LATIN":
        finds = classify_latin(text, stopwords, context=True, mode=mode)
    elif classifier == "TAXREF":
        finds = classify_taxref(text, stopwords, context=True, mode=mode)
    elif classifier[:3] == "ABS":
        finds = classify_abstaxref(
            text, stopwords, context=True, classifier=classifier, mode=mode, adhoc=adhoc)
    elif classifier == "LINNAEUS":
        finds = handle_linnaeus(article)
    elif classifier == "INPUT":
        finds = handle_user_regex(
            text, stopwords, expr, context=True, mode=mode)
    else:
        exit("unexpected classifier")
    return finds


########################### LATIN BASED CLASSIFIER #####################################


lower_case = r"[a-zæœ-]"
upper_case = r"[A-ZŒÆ]"
any_case = f"({lower_case}|{upper_case})"
acword = any_case + lower_case + "+"
lcword = lower_case + "+"
ucword = upper_case + lcword

# leave the possibility for a subgenus
# binom = ucword + r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + lcword
# lbinom = lcword + r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + lcword
# min_maj = lcword + r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + ucword
#
# stopwords = r"\s€€\s"
# acbutstop = "(?!" + stopwords + ")" + acword
# binombutstop = "(?!" + stopwords + ")" + ucword + \
#                  "(?!" + stopwords + ")" + r"\s" + lcword

# Latin declension tables


# relaxed
def tables_relachee():
    nom_nominatif = [("us", 'M'), ("us", 'F'), ("a", 'F'), ("ma", 'N'),
                     ("er", 'M'), ("um", 'N'), ("ago", 'F'), ("is", 'F'),
                     ("ys", 'F'), ("ix", 'F'), ("oides", 'F'), ("e", 'F'),
                     ("dendron", 'N'), ("ma", 'N'), ("er", 'M'), ("er", 'N'),
                     ("es", 'M'), ("es", 'F'), ("es", 'N'), ("ex", 'M'),
                     ("ex", 'F'), ("on", 'M'), ("on", 'N'), ("io", 'M'),
                     ("ops", 'M'), ("ox", 'M'), ("as", 'F'), ("r", 'M'),
                     ("r", 'N'), ("s", 'M'), ("s", 'F'), ("s", 'N'),
                     ("o", 'N'), ("ax", 'F')]

    nom_genitif = ["i", "ii", "ae", "orum", "ium", "um", "is", "us", "ei"]

    adj_nominatif = [("us", 'M'), ("er", 'M'), ("a", 'F'), ("um", 'N'),
                     ("is", 'M'), ("is", 'F'), ("ior", 'M'), ("e", 'F'),
                     ("ior", 'F'), ("ius", 'N'), ("minor", 'M'),
                     ("minor", 'F'), ("minus", 'N'), ("major", 'M'),
                     ("major", 'F'), ("majus", 'N'), ("ans", 'M'),
                     ("ans", 'F'), ("ans", 'N'), ("ens", 'M'), ("ens", 'F'),
                     ("ens", 'N'), ("oides", 'M'), ("oides", 'F'),
                     ("oides", 'N')]
    return (nom_nominatif, nom_genitif, adj_nominatif)


# strict
def tables_restreintes():
    nom_nominatif = [("us", 'M'), ("us", 'F'), ("a", 'F'), ("ma", 'N'),
                     ("er", 'M'), ("um", 'N'), ("ago", 'F'), ("is", 'F'),
                     ("ys", 'F'), ("oides", 'F'),
                     ("dendron", 'N'), ("ma", 'N'), ("er", 'M'), ("er", 'N'),
                     ("or", 'M'), ("or", 'N'),
                     ("on", 'M'), ("on", 'N'), ("o", 'M'),
                     ("ps", 'M'), ("ex", 'M'), ("ex", 'F'), ("ex", 'N'),
                     ("ox", 'M'), ("ox", 'F'), ("ox", 'N'),
                     # ("ix", 'M'), ("ix", 'F'), ("ix", 'N'),
                     ("ax", 'M'), ("ax", 'F'), ("ax", 'N'),
                     ("yx", 'M'), ("yx", 'F'), ("yx", 'N')]

    nom_genitif = ["i", "ii", "ae", "orum", "ium", "um", "is", "us", "ei"]

    adj_nominatif = [("us", 'M'), ("er", 'M'), ("a", 'F'), ("um", 'N'),
                     ("is", 'M'), ("is", 'F'), ("ior", 'M'),
                     ("ior", 'F'), ("ius", 'N'), ("minor", 'M'),
                     ("minor", 'F'), ("minus", 'N'), ("major", 'M'),
                     ("major", 'F'), ("majus", 'N'), ("ans", 'M'),
                     ("ans", 'F'), ("ans", 'N'), ("ens", 'M'), ("ens", 'F'),
                     ("ens", 'N'), ("oides", 'M'), ("oides", 'F'),
                     ("oides", 'N')]
    return (nom_nominatif, nom_genitif, adj_nominatif)


# returns a regex that matches binoms
# (with upper_case letters at arbitrary positions) in latin form
# according to the tables inputed
def get_latin_expr(tables, case_genus, case_species):
    before_latin_build = time.time()
    nom_nominatif, nom_genitif, adj_nominatif = tables
    latin_binom = r""
    # leave the possibility of a subgenus in parentheses
    # between the genus and the species name
    mid = r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + case_species
    # mid = rf"\s{case_species}"
    for t, g in nom_nominatif:
        genre_name = case_genus + t
        for tp, _ in nom_nominatif:
            species_names = mid + tp
            latin_binom += f"({genre_name}{species_names})|"
        for tp in nom_genitif:
            species_names = mid + tp
            latin_binom += f"({genre_name}{species_names})|"
        for tp, gp in adj_nominatif:
            if g == gp:
                species_names = mid + tp
                latin_binom += f"({genre_name}{species_names})|"

    after_latin_build = time.time()
    latin_build_time_min = (after_latin_build - before_latin_build)/60
    print(f"{latin_build_time_min = }")

    # remplacer le dernier | par la parenthèse qui ferme le groupe
    return latin_binom[:-1]


# returns the pattern for recognising binoms preceding a famous naturalist
def get_names():
    linn = r"(L|l)inn(aeus)?"
    buffon = r"(B|b)uffon"
    lamarck = r"(L|l)amarck"
    humboldt = r"(H|h)umboldt"
    prec = rf"{acword}\s{acword}"
    names = rf"(?=\s({linn}|{buffon}|{lamarck}|{humboldt}))"
    return prec + names


# print(f"{latin_binom = }")
# re_latin = re.compile(latin_binom)


t = tables_restreintes()
# re_latin_focused = re.compile(latin_focused_maj_maj)

pattern_name = get_names()

# Mm = re.compile(rf"(?<=\W)({latin_binom})(?!-)(?=\W)")

# MmMM = re.compile(rf"(?<=\W)({latin_binom}|{latin_focused_maj_maj})(?!-)(?=\W)")

# Mmmm = re.compile(rf"(?<=\W)({latin_binom}|{latin_focused_min_min})(?!-)(?=\W)")

# MmMMmm = re.compile(rf"(?<=\W)({latin_binom}|{latin_focused_maj_maj}|{latin_focused_min_min})(?!-)(?=\W)")


def compile_stopwords(stopwords_path):
    # get the list of frequent words to remove and compile it to a regex
    with open(stopwords_path, "r") as stops:
        words = stops.readline()
        stopwords = re.compile(
            rf"(?<=\W){words.strip()}(?=\W)", flags=re.IGNORECASE)
        return stopwords


def clear_stopwords(stopwords, article):
    return stopwords.sub(r"€\g<mid_word>€", article)


def compile_latin(latin_expr):
    before_latin_compile = time.time()
    matcher = re.compile(rf"(?<=\W)({latin_expr})(?!-)(?=\W)")
    after_latin_compile = time.time()
    latin_compile_time_min = (after_latin_compile - before_latin_compile)/60
    print(f"{latin_compile_time_min = }")
    return matcher


latin_matcher = False


# evaluates the article according with the asked mode
def classify_latin(article, stopwords, context=False, size=30, mode=""):
    abbrev = re.search(r"A", mode)

    global latin_matcher
    if not latin_matcher:
        latin_binom = get_latin_expr(tables_relachee(), ucword, lcword)
        latin_expr = f"{latin_binom}"  # else ""
        if re.search(r"MM", mode):
            latin_focused_maj_maj = get_latin_expr(
                tables_restreintes(), ucword, ucword)
            latin_expr = latin_expr + f"|{latin_focused_maj_maj}"  # else ""
        if re.search(r"mm", mode):
            latin_focused_min_min = get_latin_expr(
                tables_restreintes(), lcword, lcword)
            latin_expr = latin_expr + f"|{latin_focused_min_min}"  # else ""
        # re.compile(rf"(?<=\W)(latin_expr)(?!-)(?=\W)")
        latin_matcher = compile_latin(latin_expr)

    matcher = latin_matcher
    return apply_matcher(stopwords, article, matcher, abbrev, context, size)


######################### TAXREF BASED CLASSIFIER ##########################

datapath = re.split(r'/', __file__)[:-3]
datapath.append("DATA")

taxref_path = "/".join(datapath)


def is_article(s):
    return s in {"du", "Du", "le", "Le", "d"}

# returns a regex that matches binoms of the TAXREF base
def get_taxref_expr(abbrev=False):
    print(f"{abbrev = }")
    
    before_taxref_build = time.time()

    taxref = open(f"{taxref_path}/taxref.out").read()
    taxref_raw_lines = re.split( r'\n', re.sub(r"\[.*\]|\(.*\)|\?|\"", "", taxref) )

    # build a Genus -> species dictionnary
    taxref_dic = {}
    for line in taxref_raw_lines:
        # print(f"{line = }")

        # a few paticuliar cases
        if line == "" or line[0] == "+" or " x " in line or " " not in line: continue
        line_split = re.split(r' +', line)
        gen = line_split[0]
        spe = line_split[1]
        if gen == "" or spe == "": continue
        if is_article(spe):
            if len(line_split) > 2:
                spe = " ".join([spe, line_split[2]])
            else: continue

        # Genius species litterally extracted from TAXREF
        if gen not in taxref_dic:
            taxref_dic[gen] = {spe}
        else:
            taxref_dic[gen].add(spe)

        # G. species extracted from TAXREF only if abbrev
        if abbrev:
            g = gen[0] + r"\."
            if g not in taxref_dic:
                taxref_dic[g] = {spe}
            else:
                taxref_dic[g].add(spe)

    # computes statistics on the Genus -> species dictionary
    print(
        f"taxref_dic size ({'abbrev' if abbrev else 'strict'}) = {len(taxref_dic)}")
    print(
        f"taxref_dic # species / gen = {sum([len(taxref_dic[gen]) for gen in taxref_dic]) / len(taxref_dic)}")

    # a function for summing (regex operator |) the species of a given genius
    spe_sum = (lambda gen: (("" if len(taxref_dic[gen]) == 1 else "(")
                            + "|".join(taxref_dic[gen])
                            + ("" if len(taxref_dic[gen]) == 1 else ")")))

    taxref_expr = "(" + \
        "|".join(
                        [f"({gen} {spe_sum(gen)})" for gen in taxref_dic]) + ")"
    # print(f"{taxref_expr = }")

    after_taxref_build = time.time()
    taxref_build_time_min = (after_taxref_build - before_taxref_build)/60
    print(f"{taxref_build_time_min = }")
    return taxref_expr


def compile_taxref(taxref_expr):
    before_taxref_compile = time.time()
    matcher = re.compile(rf"(?<=\W)({taxref_expr})(?!-)(?=\W)")
    after_taxref_compile = time.time()
    taxref_compile_time_min = (after_taxref_compile - before_taxref_compile)/60
    print(f"{taxref_compile_time_min = }")
    return matcher

taxref_matcher = False


# evaluates the article according with the asked mode
def classify_taxref(article, stopwords, context=False, size=30, mode="raw"):
    abbrev = True if re.search(r"A", mode) else False
    # print(f"{abbrev = }")
    global taxref_matcher
    if not taxref_matcher:
        print(f"Compute matcher {abbrev}")
        taxref_expr = get_taxref_expr(abbrev)
        # taxref_matcher = compile_taxref(rf"(?<=\W)({taxref_expr})(?!-)(?=\W)")
        taxref_matcher = compile_taxref(rf"{taxref_expr}")
    matcher = taxref_matcher
    # abbreviation are disabled in apply_matcher
    return apply_matcher(stopwords, article, matcher, False, context, size)


######################### TAXREF BASED RELAXED CLASSIFIER ##########################


low_c = "[éèêæœüöa-z]"
high_c = "[ÆŒA-Z]"

# truncate starting from the end
# replace the truncated part with @
def etacnurt(word, width):  
    return (word if len(word) <= width else ("@" + word[-width:]))


def regex_of_spe(spe, adhoc=False, uc=False):
    if adhoc and (spe[-1] == "i" or spe[-3:-1] == "sis"):
        # is a genitive, possibly capitalized
        return re.sub(rf"@", "{high_c}{low_c}*(-{low_c}+)?", spe)
    else:
      s = f"{low_c}+(-{low_c})?"
      if uc:
        s = "(" + s + f"|{upper_case}{low_c}*)"
      return re.sub(r"@", s, spe)


def regex_of_gen(gen, lc=False):
    s = f"{high_c}{low_c}*"
    if lc:
      s = "(" + s + f"|{low_c}+)"  
    return re.sub(r"@", s, gen)


# returns a regex that matches abstracted binoms of the TAXREF base
def get_abstaxref_expr(abs_width=3, abbrev=False, MM=False, mm=False, adhoc=False):
    before_taxref_build = time.time()

    taxref = open(f"{taxref_path}/taxref.out").read()
    taxref_raw_lines = re.split(r'\n', re.sub(
        r"\[.*\]|\(.*\)|\?|\"", "", taxref))
    taxref_dic = {}
    for line in taxref_raw_lines:
        if line == "" or " x " in line or line[0] == "+" or " " not in line:
            continue
        line_split = re.split(r' +', line)
        gen = line_split[0]
        spe = line_split[1]
        if gen == "" or spe == "":
            continue
        # handle species with particle
        if is_article(spe):
            if len(line_split) > 2:
                spe = " ".join([spe, line_split[2]])
            else:
                continue
        g = gen[0] + r"\."
        spe_suff = etacnurt(spe, abs_width)
        gen_suff = etacnurt(gen, abs_width)
        # G. species extracted from TAXREF only if $abbrev
        if abbrev:
            if g not in taxref_dic:
                taxref_dic[g] = {spe_suff}
            elif spe_suff not in taxref_dic[g]:
                taxref_dic[g].add(spe_suff)
        if gen_suff not in taxref_dic:
            taxref_dic[gen_suff] = {spe_suff}
        elif spe_suff not in taxref_dic[gen_suff]:
            taxref_dic[gen_suff].add(spe_suff)
    print(
        f"taxref_dic size ({'abbrev' if abbrev else 'strict'}) = {len(taxref_dic)}")
    print(
        f"taxref_dic # species / gen = {sum([len(taxref_dic[gen]) for gen in taxref_dic]) / len(taxref_dic)}")

    spe_sum = (lambda gen: (("" if len(taxref_dic[gen]) == 1 else "(")
                            + "|".join(map((lambda s: regex_of_spe(s, adhoc=adhoc, uc=MM)), taxref_dic[gen]))
                            + ("" if len(taxref_dic[gen]) == 1 else ")")))
    prefix = r"(?!(nous|Nous|Plus|Mais|\w+tion|(\w+|[A-Z]\.) (\w+tion|\w+tions|\w+enne|\w+ennes|\w+elle|\w+elles|dans|nous|sous|sans|plus|sera|vers|puis)))" if adhoc else ""
    taxref_expr = prefix + \
        "(" + "|".join([f"({regex_of_gen(gen, lc=mm)} {spe_sum(gen)})" for gen in taxref_dic]) + ")"
    after_taxref_build = time.time()
    taxref_build_time_min = (after_taxref_build - before_taxref_build)/60
    print(f"{taxref_build_time_min = }")
    return taxref_expr


matcher_taxref_abs = [False, False, False, False, False, False, False, False]


# evaluates the article according with the asked mode
def classify_abstaxref(article, stopwords, context=False, size=30, classifier="ABS3", mode="", adhoc=False):
    abbrev = re.search(r"A", mode)
    MM = re.search(r"MM", mode)
    mm = re.search("mm", mode)
    if classifier[:3] == "ABS" and (i := int(classifier[3])) <= 7:  # TAXREF abstrait suffixes de taille i
        global matcher_taxref_abs
        if not matcher_taxref_abs[i]:
            taxref_expr = get_abstaxref_expr(i, abbrev, MM, mm, adhoc)
            matcher_taxref_abs[i] = compile_taxref(rf"{taxref_expr}")
        matcher = matcher_taxref_abs[i]
    else:
        # should not arrive but if the modes change will allow to see it quickly
        exit("unexpected mode")
    return apply_matcher(stopwords, article, matcher, False, context, size)


################### OTHER MATCHERS ##########################################@

def handle_linnaeus(article):
    os.system(
        f"java -jar linnaeus/bin/linnaeus-2.0.jar --text {article} --out tmp")
    df = pd.read_csv('tmp', delimiter='\t')
    res = df["text"].tolist()
    os.system("rm -f tmp")
    return res


user_regex = False


def handle_user_regex(article, stopwords, expr, context=True, mode="raw", size=30):
    abbrev = re.search(r"A", mode)
    global user_regex
    if not user_regex:
        with open(expr) as e:
            raw_expr = e.readline()
            user_regex = re.compile(raw_expr)
    matcher = user_regex
    return apply_matcher(stopwords, article, matcher, abbrev, context, size)


################### MEASUREMENT TOOLS ##########################################@


def f_measure(precision, recall):
    if(precision == 0 and recall == 0):
        return -1
    return 2 * precision * recall / (precision + recall)


# given an article, the chosen mode of recognition and
# the expected results for this article
# returns the false positives, false negatives and true positives
# when recognisiong with the mode mode
def check(article, expected, classifier, stopwords, mode="raw", expr="", adhoc=False):
    with open(article) as in_:
        text = in_.read()
    finds = classify(article, classifier, stopwords,
                     mode=mode, expr=expr, adhoc=adhoc)
    fps = []
    fns = []
    tps = []
    # get the positions in the original article of all matches
    matches = []
    prec_pos = 0
    for n, _ in finds:
        # escape the pattern so that Genus (subgenus) species is
        # correctly recognized et the parentheses
        p = re.escape(n)
        m = re.search(p, text, pos=prec_pos)
        # if the match is not in the rest of the article
        # it must be that we are looking at the abreviated binoms
        # so we have to start again from the beginning of the file
        if not m:
            m = re.search(p, text)
        matches.append((m[0], m.start(), m.end()))
        prec_pos = m.end()
    # score using the positions of the matches
    # and no more using exact matches
    for (n, b, e) in matches:
        # if there exists an expected binom in wich the current match is included
        if len(list(filter((lambda x: b >= x[1] and e <= x[2]), expected))) > 0:
            tps.append((n, b, e))
        else:
            fps.append((n, b, e))
    for (m, b, e) in expected:
        # if there does not exist a match that in included in the current expected binom
        if len(list(filter((lambda x: x[1] >= b and x[2] <= e), matches))) == 0:
            fns.append((m, b, e))
    # for tp in expected:
    #     if tp in finds:
    #         tps.append(tp)
    #     else:
    #         fns.append(tp)
    # for f in finds:
    #     if f not in tps:
    #         fps.append(f)
    return (fps, fns, tps)


# calculates the precision, recall and f_measure considering the numbers
# of false positives, false negatives and true positives given
def score(fps, fns, tps):
    if(tps == 0 and fps == 0 and fns == 0):
        precision = 1
        recall = 1
    elif(tps == 0 and fps == 0):
        precision = 1
        recall = 0
    elif(tps == 0 and fns == 0):
        precision = 0
        recall = 1
    else:
        precision = tps / (tps + fps)
        recall = tps / (tps + fns)
    fm = f_measure(precision, recall)
    return (precision, recall, fm)


# takes an article, its name, the expected matches
#  and the chosen mode of recognition
#  and return the effective matches the number of
# true positives, false negatives and false positives
def evaluate(article, name, expected, classifier, stopwords, mode, expr="", adhoc=False):
    (fps, fns, tps) = check(article, expected,
                            classifier, stopwords, mode, expr, adhoc=adhoc)
    (precision, recall, fm) = score(len(fps), len(fns), len(tps))
    prec = "{:.2f}".format(precision*100)
    rec = "{:.2f}".format(recall*100)
    fmes = "{:.2f}".format(fm*100)
    res = "Evaluation of the article : " + name + " :\n"
    res += f"\ttrue positives : {json.dumps(tps)} \n"
    res += f"\tfalse positives : {json.dumps(fps)} \n"
    res += f"\tfalse negatives : {json.dumps(fns)} \n"
    res += f"\tprecision = {prec} %\n"
    res += f"\trecall = {rec} %\n"
    res += f"\tF-measure = {fmes} %\n"
    return res, len(tps), len(fns), len(fps)


# prints the results or writes it in the file output if provided
def print_res(output, result):
    if output:
        with open(output, "a") as out:
            out.write(result)
    else:
        print(result)





# list of common things used in each application
# to be able to modify them in one place
stopwords_path = "Experiences/stopwords.txt"
help_stopwords = f"if provided, the path to the stopwords file, else {stopwords_path}"
corpus_path = "Processed_corpus"
expected_results_path = "Experiences/Expected_results_position"
default_mode = "A"
mode_choices = ["raw", "A", "Mm", "MM", "mm"] 
help_mode = '''R|\
the chosen mode should be either 'raw' or  a ':'-separated string of the chosen modes from {mode_choices}
if the argument is not provided, it is assumed that mode is {default_mode}
- raw does not search for abbreviations
- A searches for abbreviations
- MM searches binoms where the species name can be capitalized
- mm searches binoms where the genre name can be not capitalized'''
volumes_path = "archives_pretraitees/"
help_regex = "input a regex (path to a file with the regex on the first line) to be used as classifier"
default_regex = ""
missing_regex_message = "user chose classifier INPUT and did not input a regex"
help_classifier = "the classifier used, if INPUT is chosen, it is expected that the regex option is also used"
classifier_choices = ["LATIN", "TAXREF",
                      "ABS1", "ABS2", "ABS3", "ABS4", "ABS5", "ABS6", "ABS7", "LINNAEUS", "INPUT"]
default_classifier = "LATIN"

mode_opt = "|".join(mode_choices)
re_modes = re.compile(rf"{mode_choices}(:{mode_choices})*")

def check_mode(mode):
	if not (re_modes.match(mode) or mode == "raw"):
		exit(f"error : wrong mode selection. \n{help_mode}")

def match_dist(pattern, word):
    # taux d'erreur de 10 %
    return le.distance(pattern, word) < 1 + len(pattern)//10
