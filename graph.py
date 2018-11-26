import json
from bson.json_util import dumps, loads
from bson.raw_bson import RawBSONDocument
import bsonjs
import networkx as nx
from networkx.algorithms.approximation import clique
import Tkinter as tk
import matplotlib.pyplot as plt
import networkx.drawing
import operator
from pymongo import MongoClient

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

# d = nx.coloring.greedy_color(G, strategy='largest_first')
# d = clique.max_clique(G)
# d = clique.enumerate_all_cliques(G)
aux = {}
for (node, val) in G.degree():
    aux[node] = val


sorted_x = sorted(aux.items(), key=operator.itemgetter(1))

sort = sorted_x[-10:-1]

sort_aux  = []
for item in sort:
    sort_aux.append(item[0])

# nx.draw(G, with_labels=False, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
# plt.show()
#nx.draw(G, with_labels=False, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
#plt.show()

x = sort_aux

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
