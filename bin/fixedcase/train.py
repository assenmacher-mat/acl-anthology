#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import collections
import sys
from common import *

falselist = set([w for w in nltk.corpus.words.words() if w.islower()])
# Note: this is only a list of lemmas, so words like "frames" don't appear

if __name__ == "__main__":
    c = collections.defaultdict(collections.Counter)
    for xmlfile in sys.argv[1:]:
        tree = ET.parse(xmlfile)
        for paper in tree.getroot().findall(".//paper"):
            for abstract in paper.findall("abstract"):
                for w in tokenize(get_text(abstract)):
                    c[w.lower()][w] += 1
    truelist = []
    for w_lower in c:
        if w_lower in falselist:
            continue
        if w_lower != max(c[w_lower], key=c[w_lower].get):
            for w in c[w_lower]:
                if fixedcase_word(w) is None:
                    truelist.append(w)
    truelist.sort()

    with open("truelist-auto", "w") as outfile:
        print("# Automatically generated by train.py", file=outfile)
        for w in truelist:
            print(w, file=outfile)
