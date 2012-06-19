from flask import Flask, session, redirect, url_for, escape, request, render_template
from controllers import app, needLogin
import re
import controllers.login
import controllers.callback
from Jeu import *
from joueurs import *
from plateau import *
from arbre_action import *

@app.route('/map/infos/<int:nodeNum>/<int:actionIndex>')
@needLogin
def displayMap(nodeNum,actionIndex):
    jnum = session['joueur_num']
    j1 = Joueur(jnum)

    node = Node(nodeNum)
    action = Action.getAction(int(node.getActionsNum()[actionIndex]))
    bdd = j1.executerPartiel(node,action)

    j = JoueurPossible(session['joueur_num'],bdd)

    brigands = []
    pirates = []

    p = Plateau.getPlateau()

    for terre in p.terres:
        brigands.append(Voleur.getBrigand(terre,bdd).position.num)
        pirates.append(Voleur.getPirate(terre,bdd).position.num)
   


    body = '{'
    body += '"brigands":'
    body += '['+str(brigands[0])
    for br in brigands[1:]:
        body += ', ' + str(br)
    body += '],'

    body += '"pirates":'
    body += '['+ str(pirates[0])
    for pr in pirates[1:]:
        body += ', '+ str(pr)
    body += '],'
    

    colonies = []
    villes = []
    for intersection in p.intersections:
        col = Colonie.getColonie(intersection, bdd)
        if col != 0:
            if col.isVille:
                villes.append(col)
            else:
                colonies.append(col)


    body += '"colonies":'
    body += '['
    if len(colonies)>0:
        body += makeBatimentBody(colonies[0])
        for col in colonies[1:]:
            body += ', '+ makeBatimentBody(col) 
    body += '],'

    body += '"villes":'
    body += '['
    if len(villes)>0:
        body += makeBatimentBody(villes[0])
        for vil in villes[1:]:
            body += ', '+makeBatimentBody(vil) 
    body += '],'
    

    routes = []
    bateaux_transport = []
    cargos = []
    voiliers = []
    for arrete in p.arretes:
        route = Route.getRoute(arrete,bdd)
        if route != 0:
            routes.append([arrete,route.joueur])
        bateaux = Bateau.getBateaux(arrete,bdd)
        for bateau in bateaux:
            t = [arrete,bateau.joueur]
            if bateau.etat == Bateau.BateauType.TRANSPORT:
                bateaux_transport.append(t)
            elif bateau.etat == Bateau.BateauType.CARGO:
                cargos.append(t)
            else:
                voiliers.append(t) 
        

    body += '"routes":'
    body += '['
    if len(routes)>0:
        body += makeRouteBody(routes[0]) 
        for route in routes[1:]:
            body += ', '+makeRouteBody(route)
    body += '],'

    body += '"bateaux_transports":'
    body += '['
    if len(bateaux_transport)>0:
        body += makeBateauBody(bateaux_transport[0])
        for bateau in bateaux_transport[1:]:
            body += ', '+makeBateauBody(bateau)
    body += '],'

    body += '"cargos":'
    body += '['
    if len(cargos)>0:
        body += makeBateauBody(cargos[0])
        for cargo in cargos[1:]:
            body += ', '+makeBateauBody(cargo)
    body += '],'

    body += '"voilliers":'
    body += '['
    if len(voiliers)>0:
        body += makeBateauBody(voiliers[0])
        for voilier in voiliers[1:]:
            body += ', '+makeBateauBody(voilier)
    body += ']'

    body += '}'

    body = controllers.callback.addCallback(body,request)
    return body

def makeBatimentBody(bat):
    jnum = bat.joueur
    return '{"position":'+str(bat.position)+', "joueur":'+str(jnum)+'}'

def makeRouteBody(route):
    jnum = route[1]
    return '{"position1":'+str(route[0].int1)+', "position2":'+str(route[0].int2)+', "joueur":'+str(jnum)+'}'

def makeBateauBody(bat):
    jnum = bat[1]
    return '{"position1":'+str(bat[0].int1)+', "position2":'+str(bat[0].int2)+', "joueur":'+str(jnum)+'}'
