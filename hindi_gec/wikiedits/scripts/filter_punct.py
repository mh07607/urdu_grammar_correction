#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from difflib import SequenceMatcher

from wikiedits.indic_sentence_tokenizer import IndicSentenceTokenizer

punct = set(IndicSentenceTokenizer.NUMBERS + IndicSentenceTokenizer.ALLOWED_PUNCTUATION)
hindi_dictionary = {"सज्ञा"}


def comment_skip(file):
    for line in file:
        if not line.startswith('###'):
            yield line


def diff(err, cor):
    err = err.split()
    cor = cor.split()
    matcher = SequenceMatcher(None, err, cor)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        er = err[i1:i2]
        co = cor[j1:j2]
        yield " ".join(er), " ".join(co), tag


def all_punct(err_tok, cor_tok):
    chars = set(err_tok)
    chars.update(set(cor_tok))
    return punct.issuperset(chars)


def filter_edits(err, cor):
    err_out = []
    for err_tok, cor_tok, tag in diff(err, cor):
        if tag == 'replace' and not all_punct(err_tok, cor_tok) and err_tok in hindi_dictionary:
            err_out.append(err_tok)
        else:
            err_out.append(cor_tok)
    return " ".join(err_out), cor


def pairwise_sent(file):
    prev = None
    for line in file:
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
        err,cor=filter_edits(err, cor)
        if err!=cor:
            sys.stdout.write(f"{err}\n{cor}\n\n")
