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
    global user_id
    final = db[user_id].find({"user_id":user_id},{"friend_List":{"$elemMatch":{"user_id": id}}})

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

user_id = "76561198101080649"

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

sort = sorted_x[-11:-1]

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
    if aux != None:
        games = []
        for game in aux:
            x = game.get("appid")
            games.append(x)
        gamesP[id] = games


gameList = []
gameFreq = {}

for id in gamesP.keys():
    user_list_games = gamesP.get(id)
    for game_user in user_list_games:
        if game_user in gameList:
            gameFreq[game_user] = gameFreq[game_user]+1
        else:
            gameFreq[game_user] = 1
            gameList.append(game_user)

user_gamesAux = db[user_id].find({"user_id":user_id},{"game_List":1,"_id":0})

user_gamesAuxNV1 = dumps(user_gamesAux)
user_gamesAuxNV2 = loads(user_gamesAuxNV1)

user_gamesAuxNV2 = byteify(user_gamesAuxNV2)[0]

user_gamesAuxNV2 = user_gamesAuxNV2.get("game_List")

games_user = []
for game in user_gamesAuxNV2:
    x = game.get("appid")
    games_user.append(x)

gameFreqAux = []
for k in gameList:
    if gameFreq[k] > 1:
        gameFreqAux.append(k)

for gameFreq in gameFreqAux:
    if gameFreq not in games_user:
        print gameFreq

