#!/usr/bin/env python

# TODO: make relative file paths and integrate into main converter file


import sys
import json

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
    for s in ['id', 'label', 'source', 'target', 'value']:
        blob = blob.replace(s, '"%s":' % s)
    blob = blob.replace('\n"', ', "')
    blob = blob.replace('\n}', '}')
    return blob.strip('\n')

def main(graphfile):

    with open(graphfile, 'r') as f:
        blob = f.read()
    blob = ''.join(blob.split('node')[1:])
    nodes = blob.split('edge')[0]
    edges = ''.join(blob.split('edge')[1:]).strip().rstrip(']')

    nodes = gml_sub(nodes)
    edges = gml_sub(edges)
    with open('out.txt', 'w') as fn:
       # print('Filename:', filename, file=fn)  # Python 3.x
        print('{\n  "nodes":[', file = fn)
        print(nodes.rstrip(','), file = fn)
        print('  ],\n  "edges":[',  file = fn)
        print('    ' + edges.rstrip(),  file = fn)
        print('  ]\n}\n', file=fn)


main('Untitled.gml')