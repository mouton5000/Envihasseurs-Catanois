from flask import Flask, session, redirect, url_for, escape, request, render_template
from controllers import app, needLogin
import re
import controllers.login
import controllers.callback
from Jeu import *
from joueurs import *
from plateau import *
from arbre_action import *

@app.route('/ressources/infos/<int:terreNum>')
@needLogin
def show_FirstRessource(terreNum):
    return show_ressourceOf(REDIS, terreNum)

@app.route('/ressources/infos/<int:actionNum>/<int:terreNum>')
@needLogin
def show_ressource(actionNum,terreNum):

    jnum = session['joueur_num']
    j1 = Joueur(jnum)
    
    action = Action.getAction(actionNum)
    bdd = j1.executerPartiel(action)

    return show_ressourceOf(bdd, terreNum)


def show_ressourceOf(bdd, terreNum):
    j = JoueurPossible(session['joueur_num'], bdd)
    terre = Plateau.getPlateau().ter(terreNum)
    cartes = j.getCartes(terre)
    wcartes = j.getAllCartes()
    aur = j.getOr(terre)
    waur = j.getAllOr(terre)

    body = '{'
    body += '"argile":'
    body += '{"landQtt":'+str(cartes.argile)+'.0,"worldQtt":'+str(wcartes.argile)+'.0},'
    body += '"ble":'
    body += '{"landQtt":'+str(cartes.ble)+'.0,"worldQtt":'+str(wcartes.ble)+'.0},'
    body += '"bois":'
    body += '{"landQtt":'+str(cartes.bois)+'.0,"worldQtt":'+str(wcartes.bois)+'.0},'
    body += '"caillou":'
    body += '{"landQtt":'+str(cartes.caillou)+'.0,"worldQtt":'+str(wcartes.caillou)+'.0},'
    body += '"mouton":'
    body += '{"landQtt":'+str(cartes.mouton)+'.0,"worldQtt":'+str(wcartes.mouton)+'.0},'
    body += '"or":'
    body += '{"landQtt":'+str(aur)+'.0,"worldQtt":'+str(waur)+'.0}'
    body += '}'   

    body = controllers.callback.addCallback(body, request)

    return body
