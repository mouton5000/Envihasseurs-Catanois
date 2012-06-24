from flask import Flask, session, redirect, url_for, escape, request, render_template
from controllers import app, needLogin
import re
import controllers.login
import controllers.callback
from Jeu import *
from joueurs import *
from plateau import *
from arbre_action import *

@app.route('/map/infos')
@needLogin
def displayFirstMap():
    return displayMapOf(REDIS)

@app.route('/map/infos/<int:actionNum>')
@needLogin
def displayMap(actionNum):
    jnum = session['joueur_num']
    j1 = Joueur(jnum)

    action = Action.getAction(actionNum)
    bdd = j1.executerPartiel(action)

    return displayMapOf(bdd)

def displayMapOf(bdd):
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

    body += '"voiliers":'
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

def makePionBody(name, tab, func):
    body = '"'+name+'":'
    body += '['
    if len(tab)>0:
        body += func(tab[0])
        for elem in tab[1:]:
            body += ', '+ func(elem) 
    body += ']'
    return body

@app.route('/map/diff/<int:actionNumDown>')
@needLogin
def diffFirst(actionNumDown):
    jnum = session['joueur_num']
    j1 = Joueur(jnum)

    actionDown = Action.getAction(actionNumDown)
    bdd = REDIS
    bdd2 = j1.executerPartiel(actionDown)
    
    return diffOf(bdd,bdd2)

@app.route('/map/diffD/<int:actionNumUp>')
@needLogin
def diffDFirst(actionNumUp):
    jnum = session['joueur_num']
    j1 = Joueur(jnum)

    actionUp = Action.getAction(actionNumUp)
    bdd2 = REDIS
    bdd = j1.executerPartiel(actionUp)
    
    return diffOf(bdd,bdd2)

@app.route('/map/diff/<int:actionNumUp>/<int:actionNumDown>')
@needLogin
def diff(actionNumUp, actionNumDown):
    jnum = session['joueur_num']
    j1 = Joueur(jnum)

    actionUp = Action.getAction(actionNumUp)
    actionDown = Action.getAction(actionNumDown)
    bdd = j1.executerPartiel(actionUp)
    bdd2 = j1.executerPartiel(actionDown)

    return diffOf(bdd,bdd2)

def diffOf(bdd,bdd2):
    j = JoueurPossible(session['joueur_num'],bdd)
    j2 = JoueurPossible(session['joueur_num'],bdd2)

    body = '{'

    p = Plateau.getPlateau()

    colonies = []
    coloniesD = []
    colNum2 = j2.getColonies()
    colNum1 = j.getColonies()
    for cNum in colNum2:
        if not cNum in colNum1:
            colonies.append(Colonie.getColonie(p.it(int(cNum)),bdd2))
    for cNum in colNum1:
        if not cNum in colNum2:
            coloniesD.append(Colonie.getColonie(p.it(int(cNum)),bdd))



    villes = []
    villesD = []
    vilNum2 = j2.getVilles()
    vilNum1 = j.getVilles()
    for vNum in vilNum2:
        if not vNum in vilNum1:
            villes.append(Colonie.getColonie(p.it(int(vNum)),bdd2))
    for vNum in vilNum1:
        if not vNum in vilNum2:
            villesD.append(Colonie.getColonie(p.it(int(vNum)),bdd))

    body += makePionBody("colonies", colonies, makeBatimentBody)
    body += ','
    
    body += makePionBody("coloniesD", coloniesD, makeBatimentBody)
    body += ','
    
    body += makePionBody("villes", villes, makeBatimentBody)
    body += ','

    body += makePionBody("villesD", villesD, makeBatimentBody)
    body += ','

    routes = []
    routesD = []
    routNum2 = j2.getRoutes()
    routNum1 = j.getRoutes()
    for rNum in routNum2:
        if not rNum in routNum1:
            routes.append([p.ar(int(rNum)),j.num])
    for rNum in routNum1:
        if not rNum in routNum2:
            routesD.append([p.ar(int(rNum)),j.num])
    
    body += makePionBody("routes", routes, makeRouteBody)
    body += ','
    
    body += makePionBody("routesD", routesD, makeRouteBody)
    body += ','

    bateaux_transport = []
    bateaux_transportD = []
    btNum2 = j2.getBateauxTransport()
    btNum1 = j.getBateauxTransport()
    for btNum in btNum2:
        bateau = Bateau.getBateau(btNum,bdd2)
        if not btNum in btNum1:
            bateaux_transport.append([bateau.position,j.num])
        else:
            bateauD = Bateau.getBateau(btNum,bdd)
            if(bateau.position != bateauD.position):
                bateaux_transport.append([bateau.position,j.num])
                bateaux_transportD.append([bateauD.position,j.num])

    for btNum in btNum1:
        if not btNum in btNum2:
            bateau = Bateau.getBateau(btNum,bdd)
            bateaux_transportD.append([bateau.position,j.num])
    
    
    cargos = []
    cargosD = []
    crNum2 = j2.getCargos()
    crNum1 = j.getCargos()
    for crNum in crNum2:
        if not crNum in crNum1:
            bateau = Bateau.getBateau(crNum,bdd2)
            cargos.append([bateau.position,j.num])
    for crNum in crNum1:
        if not crNum in crNum2:
            bateau = Bateau.getBateau(crNum,bdd)
            cargosD.append([bateau.position,j.num])
    
    voiliers = []
    voiliersD = []
    vlNum2 = j2.getVoiliers()
    vlNum1 = j.getVoiliers()
    for vlNum in vlNum2:
        if not vlNum in vlNum1:
            bateau = Bateau.getBateau(vlNum,bdd2)
            voiliers.append([bateau.position,j.num])
    for vlNum in vlNum1:
        if not vlNum in vlNum2:
            bateau = Bateau.getBateau(vlNum,bdd)
            voiliersD.append([bateau.position,j.num])
    
    body += makePionBody("bateaux_transports", bateaux_transport, makeBateauBody)
    body += ','
    body += makePionBody("bateaux_transportsD", bateaux_transportD, makeBateauBody)
    body += ','
    
    body += makePionBody("cargos", cargos, makeBateauBody)
    body += ','
    body += makePionBody("cargosD", cargosD, makeBateauBody)
    body += ','

    body += makePionBody("voiliers", voiliers, makeBateauBody)
    body += ','
    body += makePionBody("voiliersD", voiliersD, makeBateauBody)

    body += '}'

    body = controllers.callback.addCallback(body,request)

    return body
