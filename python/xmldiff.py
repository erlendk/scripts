from xmlpretty import prettify

import difflib

def diff(filename1, filename2):
    text1 = prettify(filename1)
    text2 = prettify(filename2)
    difflist = list(difflib.unified_diff(text1.splitlines(True), text2.splitlines(True), filename1, filename2))
    return ''.join(difflist)

def diffdir(dir1, dir2):
    import os
    import os.path
    import random

    dirlist = os.listdir(dir1)
    random.shuffle(dirlist)

    difflist = []

    for filename in dirlist:
        diffres = diff(os.path.join(dir1, filename), os.path.join(dir2, filename))
        if diffres:
            difflist.append((filename, diffres))

    for filename, diffres in difflist:
        print filename

    print 'Antall mismatches: %i' % len(difflist)


if __name__ == '__main__':
    import sys
    from os.path import *

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    if isdir(filename1) and isdir(filename2):
        diffdir(filename1, filename2)
    else:
        print diff(filename1, filename2)
