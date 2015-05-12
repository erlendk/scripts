#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlpretty import prettify

import difflib

def diff(filename1, filename2):
    import lxml
    
    try:
        text1 = prettify(filename1)
        text2 = prettify(filename2)
    except lxml.etree.XMLSyntaxError:
        return ''

    difflist = list(difflib.unified_diff(text1.splitlines(True), text2.splitlines(True), filename1, filename2))
    return ''.join(difflist)


def diffdir(dir1, dir2):
    import os
    import os.path
    import random

    difflist = []
    dirlist = os.listdir(dir1)

    print 'Vil nå diffe %i par med filer...' % len(dirlist)

    for filename in dirlist:
        diffres = diff(os.path.join(dir1, filename), os.path.join(dir2, filename))
        if diffres:
            difflist.append((filename, diffres))

    for filename, diffres in difflist:
        print filename

    print 'Antall mismatches: %i' % len(difflist)

    if len(difflist) > 0:
        diff_prompt = raw_input('Vis differ (j/n)? ').lower()

        if diff_prompt != 'n':
            for filename, diffres in difflist:
                print filename
                print diffres
                print ''


if __name__ == '__main__':
    import sys
    from os.path import *

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    if isdir(filename1) and isdir(filename2):
        diffdir(filename1, filename2)
    else:
        print diff(filename1, filename2)
