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
        body += '{"position":'+str(colonies[0].position)+', "joueur":'+str(colonies[0].joueur)+'}'
        for col in colonies[1:]:
            body += ', {"position":'+str(col.position)+', "joueur":'+str(col.joueur)+'}' 
    body += '],'

    body += '"villes":'
    body += '['
    if len(villes)>0:
        body += '{"position":'+str(villes[0].position)+', "joueur":'+str(villes[0].joueur)+'}'
        for vil in villes[1:]:
            body += ', {"position":'+str(vil.position)+', "joueur":'+str(vil.joueur)+'}' 
    body += '],'
    

    routes = []
    bateaux_transport = []
    cargos = []
    voilliers = []
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
                voilliers.append(t) 
        

    body += '"routes":'
    body += '['
    if len(routes)>0:
        body += '{"position1":'+str(routes[0][0].int1)+', "position2":'+str(routes[0][0].int2)+', "joueur":'+str(routes[0][1])+'}'
        for route in routes[1:]:
            body += ', {"position1":'+str(route[0].int1)+', "position2":'+str(route[0].int2)+', "joueur":'+str(route[1])+'}'
    body += '],'

    body += '"bateaux_transports":'
    body += '['
    if len(bateaux_transport)>0:
        body += '{"position1":'+str(bateaux_transport[0][0].int1)+', "position2":'+str(bateaux_transport[0][0].int2)+', "joueur":'+str(bateaux_transport[0][1])+'}'
        for bateau in bateaux_transport[1:]:
            body += ', {"position1":'+str(bateau[0].int1)+', "position2":'+str(bateau[0].int2)+', "joueur":'+str(bateau[1])+'}'
    body += '],'

    body += '"cargos":'
    body += '['
    if len(cargos)>0:
        body += '{"position1":'+str(cargos[0][0].int1)+', "position2":'+str(cargos[0][0].int2)+', "joueur":'+str(cargos[0][1])+'}'
        for cargo in cargos[1:]:
            body += ', {"position1":'+str(cargo[0].int1)+', "position2":'+str(cargo[0].int2)+', "joueur":'+str(cargo[1])+'}'
    body += '],'

    body += '"voilliers":'
    body += '['
    if len(voilliers)>0:
        body += '{"position1":'+str(voilliers[0][0].int1)+', "position2":'+str(voilliers[0][0].int2)+', "joueur":'+str(voilliers[0][1])+'}'
        for voillier in voilliers[1:]:
            body += ', {"position1":'+str(voillier[0].int1)+', "position2":'+str(voillier[0].int2)+', "joueur":'+str(voillier[1])+'}'
    body += ']'

    body += '}'

    body = controllers.callback.addCallback(body,request)
    return body
