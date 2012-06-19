from flask import Flask, session, redirect, url_for, escape, request, render_template
from controllers import app, needLogin
import re
import controllers.login
import controllers.callback
from user import *
from arbre_action import *

@app.route('/players/all')
@needLogin
def getAllPlayers():

    meNum = session['joueur_num']

    body = '{"meIndex" : '+str(meNum)+', "users":['

    users = User.getUsersAndColors()
    body += makeJoueurBody(users[0][0], users[0][1], users[0][2])
    for user in users[1:]:
         body += ', '+makeJoueurBody(user[0],user[1], user[2])
    body += ']}'

    body = controllers.callback.addCallback(body,request)
    return body

def makeJoueurBody(username, jnum, color):
    return '{"username":"'+username + '", "number":'+str(jnum)+', "red":'+str(color[0])+', "blue":'+str(color[1])+', "green":'+str(color[2])+'}'
 
