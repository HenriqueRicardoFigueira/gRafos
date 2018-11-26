import json
from bson.json_util import dumps, loads
from bson.raw_bson import RawBSONDocument
import bsonjs
import networkx as nx
from networkx.algorithms.approximation import clique
import Tkinter as tk
import matplotlib.pyplot as plt
import networkx.drawing
from pymongo import MongoClient

def draw_graph(G, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # # create networkx graph
    # G = nx.Graph()

    # # add edges
    # for edge in graph:
    #     G.add_edge(edge[0], edge[1])

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
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,font_family=text_font)

    if labels is None:
        labels = range(400)

    # edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, label_pos=edge_text_pos)

    # show graph
    plt.show()
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def getbffList(id):
    final = db[user_id].aggregate([
        {"$match": {"friend_List.user_id": id}},
        {"$addFields" : {"friend_List":{"$filter":{
            "input": "$friend_List",
            "as": "friend_List",
            "cond": {"$eq": ["$$friend_List.user_id", id]}
        }}}}
    ])

    bookingfinal = dumps(final)
    bookingfinal2 = loads(bookingfinal)

    userlistFriend = bookingfinal2[0].get("friend_List")[0].get("friend_List")
    return userlistFriend

def getgameList(id):
    final = db[user_id].aggregate([
        {"$match": {"friend_List.user_id": id}},
        {"$addFields" : {"game_List":{"$filter":{
            "input": "$game_List",
            "as": "game_List",
            "cond": {"$eq": ["$$game_List.user_id", id]}
        }}}}
    ])

    bookingfinal = dumps(final)
    bookingfinal2 = loads(bookingfinal)
    try:
        userlistFriend = bookingfinal2[0].get("friend_List")[0].get("game_List")
    except IndexError:
        userlistFriend = []
        pass
    return userlistFriend

#banco
client = MongoClient('localhost', 27017)
db = client["steam_api"]

user_id = "76561198004689792"

G = nx.Graph()

#cria pai
G.add_node(user_id)


booking = dumps(db[user_id].find({},{"friend_List.user_id":1,"_id":0}))
booking2 = loads(booking)
friendsnv1 = booking2[0].get("friend_List")

cleanFriends = []
for node in friendsnv1:
    id = node.get("user_id")
    cleanFriends.append(id)

for node in cleanFriends:
    G.add_node(node)
    G.add_edge(user_id, node)

# print len(cleanFriends)

x = 0
for id in cleanFriends:

    userlistFriend = getbffList(id)

    #for node in userlistFriend:
        #G.add_node(node)

    # print userlistFriend
    for node in userlistFriend:
         if node in cleanFriends:
             G.add_edge(id, node)


# arq = open("agregationReturn.json","w")
# arq.write("{}".format(list(final)))

#nx.draw(G, with_labels=False, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
#plt.show()
d = clique.max_clique(G)
x = list(d)
x = byteify(x)

gamesP = {}

for id in x:
    aux = getgameList(id)
    games = []
    for game in aux:
        x = game.get("appid")
        games.append(x)
    gamesP[id] = games

print gamesP

# graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
#          (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

# # you may name your edge labels
# labels = map(chr, range(65, 65+len(graph)))

# # if edge labels is not specified, numeric labels (0, 1, 2...) will be used
# draw_graph(graph)
