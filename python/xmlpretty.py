#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

def prettify(filename):
    try:
        with open(filename) as f:
            return etree.tostring(etree.parse(f, etree.XMLParser(remove_blank_text=True, strip_cdata=False)), pretty_print=True)
    except etree.XMLSyntaxError as ex:
        print filename
        print ex.msg
        raise ex

if __name__ == "__main__":
    import sys
    print prettify(sys.argv[1]) 
