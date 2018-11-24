import json
from bson.json_util import dumps
from bson.raw_bson import RawBSONDocument
import bsonjs
import networkx as nx
import Tkinter as tk
import matplotlib.pyplot as plt
import networkx.drawing
from pymongo import MongoClient

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G = nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # show graph
    plt.show()
#banco
client = MongoClient('localhost', 27017,document_class=RawBSONDocument)
db = client["steam_api"]

user_id = "76561198004689792"

response = db[user_id].find({},{"friend_List.user_id":1,"_id":0})


responseFinal =  bsonjs.dumps(response)

print type(responseFinal)
print responseFinal
# graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
#          (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

# # you may name your edge labels
# labels = map(chr, range(65, 65+len(graph)))
# #draw_graph(graph, labels)

# # if edge labels is not specified, numeric labels (0, 1, 2...) will be used
# draw_graph(graph)