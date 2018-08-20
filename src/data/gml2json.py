#!/usr/bin/env python

# convert gml to json and add community

# import libraries
import argparse
import networkx as nx
from networkx.readwrite import json_graph
from modularity_maximization import partition
from modularity_maximization.utils import get_modularity

#def graphmltojson(graphfile, outfile):
    # """
    # Converts GraphML file to json while adding communities/modularity groups
    # using python-louvain. JSON output is usable with D3 force layout.
    # Usage:
    # python convert.py -i mygraph.graphml -o outfile.json
    # """

G = nx.read_gml('influencer\TheDataFox.gml')
print nx.info(G)
comm_dict = partition(G)
for comm in set(comm_dict.values()):
    print("Community %d"%comm)
    print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))

print('Modularity of such partition for network is %.3f' %\
      get_modularity(G, comm_dict))

# adds partition/community number as attribute named 'modularitygroup'
for n, d in G.nodes_iter(data=True):
    d['modularitygroup'] = comm_dict[n]

# create a dictionary in a node-link format that is suitable for JSON serialization
d = json_graph.node_link_data(g)
with open('dolphins.json', 'w') as fp:
    json.dump(d, fp)

node_link = json_graph.node_link_data(G)
json = json_graph.dumps(node_link)

#Write to file
fo = open('output.json', "w")
fo.write(json)
fo.close()

#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Convert from GraphML to json. ')
#     parser.add_argument('-i', '--input', help='Input file name (graphml)', required=True)
#     parser.add_argument('-o', '--output', help='Output file name/path', required=True)
#     args = parser.parse_args()
#     graphmltojson(args.input, args.output)

# graphmltojson('influencer\TheDataFox.gml', 'influencer\TheDataFox.json')


