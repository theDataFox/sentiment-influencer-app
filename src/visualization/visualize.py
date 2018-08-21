# script to take edgelist from twecoll.py and run into sigma js for output

# TODO: read in edgelist file
# TODO: convert from gml to gexf
# TODO: load server

import networkx as nx

# load gml and convert to gexf
G = nx.read_gml('../data/influencer/TheDataFox.json.gml')
gexf_file = nx.write_gexf(G, '../data/influencer/TheDataFox.json.gexf')
json_file = nx.json


# load a simple server to serve files on local system
# TODO: Write if block here

# If Python version returned above is 3.X
from http.server import 
# If Python version returned above is 2.X
#import SimpleHTTPServer

PORT = 8000

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

import http.server
import socketserver


# alternative
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


