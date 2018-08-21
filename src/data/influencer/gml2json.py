#!/usr/bin/env python

# convert gml to json and add community grouping

# TODO: fix relative filepaths for file input and export

# import libraries
# import argparse
import json
import networkx as nx
from networkx.readwrite import json_graph
from modularity_maximization import partition
from modularity_maximization.utils import get_modularity


def gmltojson(gmlfile, jsonfile):
    """
    Converts GML file to json while adding communities/modularity groups
    using modularity_maximization. JSON output is usable with D3 force layout.
    Usage:
    python convert.py -i mygraph.graphml -o outfile.json
    Return data in node-link format that is suitable for JSON serialization and use in Javascript documents.
    """

    print('Reading file ', gmlfile)
    di_graph = nx.read_gml('../../../data/raw/' + gmlfile)
    comm_dict = partition(di_graph)
    for comm in set(comm_dict.values()):
        print("Community %d" % comm)
        print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))

    print('Modularity of such partition for network is %.3f' % \
          get_modularity(di_graph, comm_dict))

    # adds partition/community number as attribute named 'Modularity Class'
    print('Assigning Communities...')
    for n, d in di_graph.nodes(data=True):
        d['Modularity Class'] = comm_dict[n]

    # create a dictionary in a node-link format that is suitable for JSON serialization
    with open('../../../data/processed/' + jsonfile + '.json', 'w') as outfile1:
        outfile1.write(json.dumps(json_graph.node_link_data(G=di_graph, attrs=)))
    print('Complete!')

def gmltogexf(gmlfile, gexffile):
    """
    Converts GML file to gexf while adding communities/modularity groups
    using modularity_maximization. JSON output is usable with D3 force layout.
    Usage:
    python convert.py -i mygraph.graphml -o outfile.json
    """
    print('Reading file ', gmlfile)
    di_graph = nx.read_gml('../../../data/raw/' + gmlfile)
    comm_dict = partition(di_graph)
    for comm in set(comm_dict.values()):
        print("Community %d" % comm)
        print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))

    print('Modularity of such partition for network is %.3f' % \
          get_modularity(di_graph, comm_dict))

    # adds partition/community number as attribute named 'Modularity Class'
    print('Assigning Communities...')
    for n, d in di_graph.nodes(data=True):
        d['Modularity Class'] = comm_dict[n]

    # create a dictionary in a node-link format that is suitable for JSON serialization
    nx.write_gexf(di_graph, '../../../data/processed/' + gexffile + '.gexf')
    print('Complete!')


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Convert from GraphML to json. ')
#     parser.add_argument('-i', '--input', help='Input file name (gml)', required=True)
#     parser.add_argument('-o', '--output', help='Output file name/path', required=True)
#     args = parser.parse_args()
#     graphmltojson(args.input, args.output)

gmltogexf('TheDataFox.gml', 'TheDataFox')
gmltojson('TheDataFox.gml', 'TheDataFox')

