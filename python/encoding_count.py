#!/usr/bin/env python3

import os
import os.path
import chardet

extensions = ['.java', '.xml']
ignore_dirs = ['target']
encoding_counts = dict()

def detect(file_path):
    with open(file_path, 'rb') as source_file:
        return chardet.detect(source_file.read())

def detect_encoding(file_path):
    result = detect(file_path)
    return (result['encoding'], result['confidence'])

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

        if encoding in encoding_counts:
            encoding_count, confidence_sum = encoding_counts[encoding]
            encoding_counts[encoding] = (encoding_count + 1, confidence_sum + confidence)
        else:
            encoding_counts[encoding] = (1, confidence)

print("\nEncoding counts:")

for key, value in encoding_counts.items():
    print(key + ' (' + str(value[0]) + ', ' + str(value[1]/value[0]) + ')')
