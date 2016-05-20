#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  

reload(sys)  
sys.setdefaultencoding('utf-8')

import os
import os.path
import codecs
import chardet

target_encoding = 'utf-8'
#extensions = ['.java', '.xml']
extensions = ['.xml']
ignore_dirs = ['target']
converted = []
not_converted = []

def detect(file_path):
    return chardet.detect(open(file_path, 'r').read())

def detect_encoding(file_path):
    result = detect(file_path)
    return (result['encoding'], result['confidence'])

def convert(file_path, encoding):
    source_data = None

    try:
        with codecs.open(file_path, 'rb', encoding) as source_file:
        #with codecs.open(file_path, 'r', 'utf-8') as source_file:
            #source_data = source_file.read()
            #source_data = source_file.read().decode('utf-8')
            source_data = source_file.read().decode(encoding)
    except UnicodeDecodeError, e:
        print str(e)
        return

    with codecs.open(file_path, 'wb', target_encoding) as target_file:
        target_file.write(source_data.encode(target_encoding))
        #target_file.write(source_data)

    converted.append((file_path, encoding))

def filter_dirs(dirs):
    for dir in ignore_dirs:
        if dir in dirs:
            dirs.remove(dir)

for root, dirs, filenames in os.walk('.'):
    print 'Entering ' + root

    filter_dirs(dirs)

    for filename in [f for f in filenames if os.path.splitext(f)[1] in extensions]:
        file_path = os.path.join(root, filename)
        (encoding, confidence) = detect_encoding(file_path)

        if encoding != target_encoding:
            if confidence > 0.5:
                convert(file_path, encoding)
            else:
                not_converted.append((file_path, encoding, confidence))


print "\nConverted:"

for file_path, encoding in converted:
    print file_path + '(' + encoding + ')'

print "\nNot converted:"

for file_path, encoding, confidence in not_converted:
    print file_path + '(' + encoding + ', ' + str(confidence) + ')'
