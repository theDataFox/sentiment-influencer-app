#!/usr/bin/env python

#  import libraries
import numpy as np
import json
import networkx as nx
from modularity_maximization import partition
from modularity_maximization.utils import get_modularity
import matplotlib.pyplot as plt
import re


def analyze_convert(gmlfile, outputfile, outputfile_format='json'):

    """
    Converts GML file to json or gexf while adding statistics and community information,
    node and edge coloring and alpha, node size and edge weight

    # see: https://cambridge-intelligence.com/keylines-faqs-social-network-analysis/
    """
    print('Starting conversion to JSON\n')
    print(outputfile_format.upper(), 'output file selected')
    print('\nReading GML file:', gmlfile)
    di_graph = nx.read_gml('../../data/interim/' + gmlfile, label='id')

    # re-assign node id as attr
    node_id_dict = {}
    for id in di_graph.node:
        node_id_dict[id] = int(id)
    nx.set_node_attributes(di_graph, name='id', values=node_id_dict)

    # find communities and assign
    print('Identifying communities...')
    comm_dict = partition(di_graph)

    print('\nModularity of such partition for network is %.3f' % \
          get_modularity(di_graph, comm_dict))

    print('\nAssigning Communities...')

    # get unique set of communities
    comm_unique_set = set()
    for n, d in di_graph.nodes(data=True):
        d['mc'] = comm_dict[n]
        comm_unique_set.add(d['mc'])

    # create colormap
    cmap = plt.get_cmap('cool')
    colors = (cmap(np.linspace(0, 1, len(comm_unique_set)))) * 255
    colors = np.round(colors, decimals=0)

    # assign colors to each community group
    color_mapping = {}
    counter = 0
    for i in list(comm_unique_set):
        color_mapping[i] = colors[counter]
        counter += 1

    # applying colors to nodes iteratively
    for n, d in di_graph.nodes(data=True):
        for group in color_mapping.keys():
            if d['mc'] == group:
                d['color'] = re.sub(r'\s+', '', np.array2string(color_mapping[group], separator=','))
                d['color'] = str.replace(d['color'], '255.]', '1)')
                d['color'] = str.replace(d['color'], '[', 'rgba(')
                d['color'] = str.replace(d['color'], '.', '')

    # loop through nodes and edges, if edge source == node id then color same
    for n, node_d in di_graph.nodes(data=True):
        for source, target, edge_d in di_graph.edges(data=True):
            if source == n:
                edge_d['color'] = node_d['color']
                edge_d['color'] = edge_d['color'].replace(',1)', ',0.1)')

    # set positions of nodes using layout algorithm
    print('\nCreating layout...')

    pos = nx.spring_layout(G=di_graph, iterations=50, weight='weight', scale=5, k=1)

    # positions from layout applied to node attributes
    for node, (x, y) in pos.items():
        di_graph.node[node]['x'] = float(x)
        di_graph.node[node]['y'] = float(y)

    print('\nCalculating network statistics...')

    # betweeness centrality
    bc = nx.betweenness_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='bc', values=bc)

    # degree centrality
    size = nx.degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='size', values=size)

    idc = nx.in_degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='idc', values=idc)

    odc = nx.out_degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='odc', values=odc)

    # eigen-vector centrality
    edc = nx.eigenvector_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='edc', values=edc)

    # closeness centrality
    cc = nx.closeness_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='cc', values=cc)

    # page rank
    pr = nx.pagerank(di_graph)
    nx.set_node_attributes(di_graph, name='pr', values=pr)

    # choose which output file to write
    if outputfile_format.upper() == 'JSON':

        print('\nExporting ' + outputfile + '.json')

        # create a dictionary in a node-link format that is suitable for JSON serialization
        with open('../../data/processed/' + outputfile + '.json', 'w') as outfile1:
            outfile1.write(json.dumps(nx.readwrite.json_graph.
                                      node_link_data(G=di_graph,
                                                     attrs={'link': 'edges',
                                                            'name': 'id',
                                                            'source': 'source',
                                                            'target': 'target'})))
        print('Complete!')

    elif outputfile_format.upper() == 'GEXF':
        print('\nExporting GEXF file...', outputfile, '.gexf')
        nx.write_gexf(di_graph, '../../data/processed/' + outputfile + '.gexf')
        print('\nComplete!')

    else:
        print('Please enter a valid output file format: JSON or GEXF')


analyze_convert('TheDataFox.gml', 'TheDataFox', outputfile_format='json')

