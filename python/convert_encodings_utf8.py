#!/usr/bin/env python3

import os
import os.path
import codecs
import chardet

target_encoding = 'utf-8'
extensions = ['.java', '.xml', '.txt']
ignore_dirs = ['target']
converted = []
not_converted = []

def detect(file_path):
    with open(file_path, 'rb') as source_file:
        return chardet.detect(source_file.read())

def detect_encoding(file_path):
    result = detect(file_path)
    return (result['encoding'], result['confidence'])

def convert(file_path, encoding, confidence):
    try:
        with open(file_path, 'rb') as source_file:
            source_data = source_file.read().decode(encoding)
    except UnicodeDecodeError as e:
        print(str(e))
        return

    with open(file_path, 'wb') as target_file:
        target_file.write(source_data.encode(target_encoding))

    converted.append((file_path, encoding, confidence))

def filter_dirs(dirs):
    for dir in ignore_dirs:
        if dir in dirs:
            dirs.remove(dir)

for root, dirs, filenames in os.walk('.'):
    print('Entering ' + root)

    filter_dirs(dirs)

    for filename in [f for f in filenames if os.path.splitext(f)[1] in extensions]:
        file_path = os.path.join(root, filename)
        encoding, confidence = detect_encoding(file_path)

        if encoding != target_encoding:
            if confidence > 0.5:
                convert(file_path, encoding, confidence)
            else:
                not_converted.append((file_path, encoding, confidence))


print("\nConverted:")

for file_path, encoding, confidence in converted:
    print(file_path + ' (' + encoding + ', ' + str(confidence) +')')

print("\nNot converted:")

for file_path, encoding, confidence in not_converted:
    print(file_path + ' (' + encoding + ', ' + str(confidence) + ')')
