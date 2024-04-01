#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from difflib import SequenceMatcher

from wikiedits.urdu_sentence_tokenizer import UrduSentenceTokenizer

punct = set(UrduSentenceTokenizer.NUMBERS + UrduSentenceTokenizer.ALLOWED_PUNCTUATION+' ')
hindi_dictionary = {line.strip():i for i,line in enumerate(open('dict'))}


def comment_skip(file):
    for line in file:
        if not line.startswith('###'):
            yield line


def diff(err, cor):
    matcher = SequenceMatcher(None, err, cor)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        er = err[i1:i2]
        co = cor[j1:j2]
        yield " ".join(er), " ".join(co), tag

diacrit={'़','ँ','्','ु','ू','ॉ','म ्','न ्','ण्','ः'}
def all_punct(err_tok, cor_tok):
    di=len(set(err_tok).symmetric_difference(set(cor_tok)))
    l=list(zip(*diff(err_tok,cor_tok)))
    t=set(l[0]+l[1])
    chars_err=set(err_tok)
    chars_cor=set(cor_tok)
    return punct.issuperset(chars_err) or punct.issuperset(chars_cor) or (len(diacrit.intersection(t))!=0) or di>6

def filter_edits(err, cor):
    err_out = []
    for err_tok, cor_tok, tag in diff(err.split(), cor.split()):
        a=hindi_dictionary.get(err_tok)
        b=hindi_dictionary.get(cor_tok)      
        if tag == 'replace' and not all_punct(err_tok, cor_tok) and a is not None and b is not None and abs(b-a)<800:
            err_out.append(err_tok)
        else:
            err_out.append(cor_tok)
    return " ".join(err_out), " ".join(cor.split())


def pairwise_sent(file):
    prev = None
    for line in file:
        if line[0]=="#":
            continue
        line = line.strip()
        if not line or line.isspace():
            continue
        if prev is None:
            prev = line
        else:
            yield prev, line
            prev = None


def print_edits(err, cor, file):
    print(err, cor, sep='\n', end='\n\n', file=file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Cleanup Edits File')
    args = parser.parse_args()

    for err, cor in pairwise_sent(sys.stdin):
        err, cor=filter_edits(err, cor)
        err=' '.join(err.split())
        cor=' '.join(cor.split())
        if err!=cor:
            sys.stdout.write(f"{err}\n{cor}\n\n")
