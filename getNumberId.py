#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sys, unicodedata
import multiprocessing as mtp
import networkx as nx
import Tkinter as tk
import matplotlib.pyplot as plt
import networkx.drawing
from joblib import Parallel, delayed

api_key = "7CA772628D17EB61985E3FBF61D124B6"
name = "vnc10"


def requester(url,user_id):
    global api_key
    urlFinal = url.format(api_key,user_id)
    resp = requests.get(urlFinal)
    respFormated = resp.json()
    aux = {}
    aux[user_id] = respFormated
    return aux



# url = "https://steamidfinder.com/lookup/{}".format(name)
urlId = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}".format(api_key,name)

response = requests.get(urlId)

responseId = response.json()

user_idResponse = responseId.get("response")
user_id = user_idResponse.get("steamid")


urlfriend = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend"
friends = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(api_key,user_id)
urlGames = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(api_key,user_id)

G = nx.Graph()

G.add_node(user_id)




responseFriends = requests.get(friends)

userFriendList = []

userId_ListAux = responseFriends.json()

userId_ListAuxNv1 = userId_ListAux.get("friendslist")
userId_ListAuxNv2 = userId_ListAuxNv1.get("friends")

userId_List = list(userId_ListAuxNv2)


responseGames = requests.get(urlGames)

# print responseGames.json()
#petris -> friends
for friend in userId_List:
    id = friend.get("steamid")
    G.add_node(id)
    G.add_edge(user_id, id)
    userFriendList.append(id)


# nx.draw(G, with_labels=True, font_weight='bold')
# nx.draw_shell(G, with_labels=False, font_weight='bold')
# plt.show()
# print len(userFriendList)
urlList = Parallel(n_jobs=mtp.cpu_count())(delayed(requester)(urlfriend,x)for x in userFriendList)

# arq = open("retornFriends.txt","w")

#petris -> friends -> friends
for x in urlList:
    pai = x.keys()[0]
    friends = x.get(pai)

    print len(friends)
    # arq.write(("{}:{}\n".format(pai,friends)))


