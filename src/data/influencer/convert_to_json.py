#!/usr/bin/env python

# working
# TODO: x,y coordinates, layout, stats,
import sys
import re

def gml_sub(blob):

    lines = []
    for line in blob.split('\n'):
        line = line.strip()
        lines.append(line)
    blob = "\n".join(lines)

    blob = blob.replace('\n\n', '\n')
    blob = blob.replace(']\n', '},\n')
    blob = blob.replace('[\n', '{')
    blob = blob.replace('\n{', '\n    {')
    for s in ['id', 'label', 'source', 'target', 'value', 'file', 'user_id', 'ffr', 'lfr', 'image', 'type', 'friends',
              'statuses', 'followers', 'listed', 'shape', 'weight']:
            blob = re.sub(r'\b%s\b' % s, '"%s":' % s, blob )

    blob = blob.replace('\n"', ', "')
    blob = blob.replace('\n}', '}')
    return blob.strip('\n')

def main(graphfile):
    """
    Converts GraphML file to json
    """

    with open(graphfile, 'r') as f:
        blob = f.read()
    blob = ''.join(blob.split('node')[1:])
    nodes = blob.split('edge')[0]
    edges = ''.join(blob.split('edge')[1:]).strip().rstrip(']')

    nodes = gml_sub(nodes)
    edges = gml_sub(edges)

    print ('{\n  "nodes":[')
    print (nodes.rstrip(','))
    print ('  ],\n  "edges":[')
    print ('    ' + edges.rstrip(','))
    print ('  ]\n}\n')


main('TheDataFox.gml')


#This will get you a list of exact matches.
#
# matches = [c for c in checklist if c in words]
#
# Which is the same as:
#
# matches = []
# for c in checklist:
#   if c in words:
#     matches.append(c)