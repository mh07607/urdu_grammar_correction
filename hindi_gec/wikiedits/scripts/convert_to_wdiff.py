#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from difflib import SequenceMatcher

import string


def comment_skip(file):
    for line in file:
        if not line.startswith('###'):
            yield line

def pairwise_sent(file):
    prev = None
    for line in file:
        line=line.strip()
        if line == '' or line =='\n':
            continue
        if prev is None:
            prev = line
        else:
            yield prev,line
            prev = None

def wdiff(err_toks, cor_toks):
    result = []
    matcher = SequenceMatcher(None, err_toks, cor_toks)
    ispunct = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        err = ' '.join(err_toks[i1:i2])
        cor = ' '.join(cor_toks[j1:j2])
        if tag == 'replace':
            result.append("[-{}-] {{+{}+}}".format(err, cor))
        elif tag == 'insert':
            result.append("{{+{}+}}".format(cor))
        elif tag == 'delete':
            result.append("[-{}-]".format(err))
        else:
            result.append(err)
    return ' '.join(result)


if __name__ == '__main__':
    import sys
    for err,cor in pairwise_sent(comment_skip(sys.stdin)):
        text = wdiff(err.split(), cor.split())
        print(text)
