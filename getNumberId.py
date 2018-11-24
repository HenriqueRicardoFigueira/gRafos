#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import sys, unicodedata
import multiprocessing as mtp
import networkx as nx
import Tkinter as tk
import matplotlib.pyplot as plt
import networkx.drawing
from itertools import chain
from pymongo import MongoClient
from joblib import Parallel, delayed


#steam api config
api_key = "7CA772628D17EB61985E3FBF61D124B6"
name = "vnc10"

#banco config
client = MongoClient('localhost', 27017)
db = client["steam_api"]

#funcao request
def requester(url,user_id):
    global api_key
    urlFinal = url.format(api_key,user_id)
    resp = requests.get(urlFinal)
    respFormated = resp.json()
    aux = {}
    aux[user_id] = respFormated
    return aux

#funcao inserir no banco
def insertFriends(user_id,friend_list,cursor):
    for friend in friend_list:
        pai = x.keys()[0]
        friends = x.get(pai)
        cursor.update({"user_id":user_id},{"$push":{"friend_List":{"user_id":friend,"friend_List":"","game_List":""}}})

#funcao inserir no banco nv2
def insertFriendsNV2(user_id,friend_list,cursor,friendsNV2,gamelist):
    for friend in friend_list:
        friendClean = byteify(friend)
        try:
            friendsaux = friendsNV2[friendClean]
            gamelistaux = gamelist[friendClean]
        except KeyError, x:
            continue
        cursor.update({"user_id":user_id},{"$push":{"friend_List":{"user_id":friendClean,"friend_List":friendsaux,"game_List":gamelistaux}}})

#limpar json
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

#urls api steam
# url = "https://steamidfinder.com/lookup/{}".format(name)
urlId = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}".format(api_key,name)
urlfriend = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend"
urlGame =   "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json"

response = requests.get(urlId)
responseId = response.json()
user_idResponse = responseId.get("response")
user_id = user_idResponse.get("steamid")

friends = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(api_key,user_id)
urlGames = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(api_key,user_id)

#criacao de banco
cursor = db[user_id]
cursor.insert_one({"user_id":user_id})

# G = nx.Graph()
# G.add_node(user_id)


responseFriends = requests.get(friends)
userFriendList = []

#trata retorno de friends da steam pq tem 3 nvs
userId_ListAux = responseFriends.json()
userId_ListAuxNv1 = userId_ListAux.get("friendslist")
userId_ListAuxNv2 = userId_ListAuxNv1.get("friends")
userId_List = list(userId_ListAuxNv2)


responseGames = requests.get(urlGames)
response = responseGames.json()

usergames_ListAuxNv1 = response.get("response")
usergames_ListAuxNv2 = usergames_ListAuxNv1.get("games")
usergames_List = usergames_ListAuxNv2


for i in usergames_List:
    cursor.update({"user_id":user_id},{"$push":{"game_List":{"user_id":i}}})

# print responseGames
# cursor.update({"user_id":user_id},{"$push":{"game_List":responseGames.json()}})

#petris -> friends
for friend in userId_List:
    id = friend.get("steamid")
    # G.add_node(id)
    # G.add_edge(user_id, id)
    userFriendList.append(id)

# nx.draw(G, with_labels=True, font_weight='bold')
# nx.draw_shell(G, with_labels=False, font_weight='bold')
# plt.show()

urlList = Parallel(n_jobs=mtp.cpu_count())(delayed(requester)(urlfriend,x)for x in userFriendList)

#petris -> friends -> friends
cleanFriendList = {}

for x in urlList:
    pai = x.keys()[0]
    try:
        friends = x.get(pai)
    except AttributeError, x:
        # print "key vazia {}".format(x)
        continue

    
    userId_friendsListNv1 = friends.get("friendslist")
    friendsFinalList = []
    try:
        userId_friendsListNv2 = userId_friendsListNv1.get("friends")
        userId_friendsList = list(userId_friendsListNv2)
        
        for friends in userId_friendsList:
            friendsFinalList.append(friends.get("steamid"))
    except AttributeError, x:
        # print "key vazia {}".format(x)
        continue
    
    cleanFriendList[pai] = friendsFinalList

#Limpa u'
cleanFriendList = byteify(cleanFriendList)
FriendGameList = Parallel(n_jobs=mtp.cpu_count())(delayed(requester)(urlGame,x)for x in userFriendList)
gamedict = {}


for games in FriendGameList:
    key = games.keys()[0]
    element = games[key]
    game_List = []
    try:
        game_ListAuxNv1 = element.get("response")
        game_ListAuxNv2 = game_ListAuxNv1.get("games")
        game_List = game_ListAuxNv2
    except TypeError:
        continue
    gamedict[key] = game_List


gamedict = byteify(gamedict)
insertFriendsNV2(user_id,userFriendList,cursor,cleanFriendList,gamedict)

# arq = open("gamesList.json","w")
# arq.write("{}".format(gamedict))


