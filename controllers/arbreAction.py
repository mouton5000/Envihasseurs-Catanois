from flask import Flask, session, redirect, url_for, escape, request, render_template
from controllers import app, needLogin
import re
import controllers.login
import controllers.callback
from user import *
from arbre_action import *

@app.route('/arbre_actions')
@needLogin
def getTree():

    meNum = session['joueur_num']
    j = Joueur(meNum)

    # Parcours en profondeur prefixe de l'arbre
    nodes = j.getNodes()

    bodies = []
    for node in nodes:
        bodies.append(makeNodeBody(node))
    body = '[' + ', '.join(bodies) + ']'

    body = controllers.callback.addCallback(body,request)
    return body

def makeNodeBody(node):
    body = '{ "num":'+str(node.num)+', "father":'+str(node.getFatherNode().num)+', "first_child":'+str(node.getFirstChild().num)+', "sibling":'+str(node.getSiblingNode().num)+', "pSibling":'+str(node.getPSiblingNode().num)+', "actions":['
    actions = []
    for num in node.getActionsNum():
        action = Action.getAction(num)
        params = action.params
        strParams = '['+', '.join(['"'+str(p)+'"' for p in params])+']'
        actions.append('{"num":'+action.num+', "func":"'+action.func+'", "params":'+strParams+'}')
    body +=', '.join(actions)+']}'
    return body
