# -*- coding: utf8 -*-
# Module de jeu


import redis
import functools
import random
from pions import *
from joueurs import *
from plateau import *
from cartes import *
from errors import *
from ActionNight import *

REDIS = redis.StrictRedis()



def predefausse(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        j = args[0]
        if not j.doit_defausser_general():
            f(*args,**kwargs)
            return True
        else:
            raise ActionError(ActionError.DOIT_DEFAUSSER)

    return helper


def preruine(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        import joueurs
        j = joueurs.JoueurPossible(args[0].num)
        if not j.getEnRuine():
            f(*args,**kwargs)
            return True
        else:
            raise ActionError(ActionError.JOUEUR_EN_RUINE)

    return helper

def protection(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        peut_f = globals()['peut_' + f.__name__]
        if peut_f(*args,**kwargs):
            f(*args,**kwargs)
            return True
        else:
            return False

    return helper

def kallable(f):
    f.peut_etre_appelee = True
    return f

# Renvoie le joueur qui possède la route la plus longue sur la terre terre et sa longueur.

def get_route_la_plus_longue(terre, bdd = REDIS):
    jnum = bdd.get('T'+str(terre.num)+':carte_rlpl:joueur')
    l = bdd.get('T'+str(terre.num)+':carte_rlpl:longueur')
    if jnum != None and l != None:
        return (int(jnum),int(l))
    else:
        return 0


def set_route_la_plus_longue(terre,jnum ,n, bdd = REDIS):
    bdd.set('T'+str(terre.num)+':carte_rlpl:joueur',jnum)
    bdd.set('T'+str(terre.num)+':carte_rlpl:longueur',n)


def delete_route_la_plus_longue(terre, bdd = REDIS):
    bdd.delete('T'+str(terre.num)+':carte_rlpl:joueur')
    bdd.delete('T'+str(terre.num)+':carte_rlpl:longueur')

# Vérifie si j a une route plus longue que la route la plus longue sur la terre terre. Si la route actuelle est nulle, alors vérifie si j a une route de plus de 5 troncons. Si c'est le cas, j prend la plus du joueur actuellement en position

def challenge_route_la_plus_longue(j,terre):
        bdd = j.bdd
        n = j.get_route_la_plus_longue(terre)
        if n>=5:
            u = get_route_la_plus_longue(terre,bdd)
            if u == 0 or  n > u[1]:
                set_route_la_plus_longue(terre,j.num,n,bdd)
                
# Recalcule qui parmi les colons de la terre a la carte de route la plus longue. Si il y a égalité, si la route la plus longue est identique à celle précédemment inscrite dans la base de données, alors elle est conservée, sinon, la carte est retirée du jeu jusqu'à ce que ait un montant plus important.

def recalcul_route_la_plus_longue(terre, bdd = REDIS):
    jt = terre.getJoueurs(bdd)
    rlpl = 0
    jmax = []
    for jtn in jt:
        j = JoueurPossible(int(jtn),bdd)
        rlplj = j.get_route_la_plus_longue(terre)
        if rlplj > rlpl:
            rlpl = rlplj
            jmax = [j.num]
        elif rlplj == rlpl:
            jmax.append(j.num)
    if len(jmax) == 1 and rlpl >= 5:
        set_route_la_plus_longue(terre,jmax[0],rlpl,bdd)
    else:
        t = get_route_la_plus_longue(terre,bdd)
        if t != 0  and (t[1] > rlpl or not t[0] in jmax):
            delete_route_la_plus_longue(terre,bdd)
            


# Renvoie le joueur qui possède l'armee la plus grande sur la terre terre et sa longueur.

def get_armee_la_plus_grande(terre, bdd = REDIS):
    j = bdd.get('T'+str(terre.num)+':carte_alpg:joueur')
    s = bdd.get('T'+str(terre.num)+':carte_alpg:taille')
    if j != None and s != None:
        return (int(j),int(s))
    else:
        return 0


def set_armee_la_plus_grande(terre,j,s, bdd = REDIS):
    bdd.set('T'+str(terre.num)+':carte_alpg:joueur',j)
    bdd.set('T'+str(terre.num)+':carte_alpg:taille',s)


def delete_armee_la_plus_grande(terre, bdd = REDIS):
    bdd.delete('T'+str(terre.num)+':carte_alpg:joueur')
    bdd.delete('T'+str(terre.num)+':carte_alpg:taille')

            
# Vérifie si j a une armee plus grande que la armee la plus grande sur la terre terre. Si l'armee actuelle est nulle, alors vérifie si j a une armee de plus de 3 chevalliers. Si c'est le cas, j prend la plus du joueur actuellement en position

def challenge_armee_la_plus_grande(j,terre):
    bdd = j.bdd
    n = j.get_chevalliers(terre)
    if n>=3:
        u = get_armee_la_plus_grande(terre,bdd)
        if u == 0 or  n > u[1]:
            set_armee_la_plus_grande(terre,j.num,n,bdd)

# Recalcule qui parmi les colons de la terre a la carte de route la plus longue. Si il y a égalité, si la route la plus longue est identique à celle précédemment inscrite dans la base de données, alors elle est conservée, sinon, la carte est retirée du jeu jusqu'à ce que ait un montant plus important.

def recalcul_armee_la_plus_grande(terre, bdd = REDIS):
    jt = terre.getJoueurs(bdd)
    armee = 0
    jmax = []
    for jtn in jt:
        j = JoueurPossible(int(jtn),bdd)
        armeej = j.get_chevalliers(terre)
        if armeej > armee:
            armee = armeej
            jmax = [j.num]
        elif armeej == armee:
            jmax.append(j.num)
    if len(jmax) == 1 and armee >= 3:
        set_armee_la_plus_grande(terre,jmax[0],armee,bdd)
    else:
        t = get_armee_la_plus_grande(terre,bdd)
        if t != 0  and (t[1] > armee or not t[0] in jmax):
            delete_armee_la_plus_grande(terre,bdd)


# -----------------------------------------------------
#Actions dans la journee
# -----------------------------------------------------

def translate_construire_colonie(j, intersection_num_str):
    ''' L'action comporte pour parametre le numéro d'une intersection. '''
    try:
        num = int(intersection_num_str)
        it = Plateau.getPlateau().it(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [it]

@preruine
@predefausse
def peut_construire_colonie(j,intersection):
    ''' Un joueur peut construire une colonie si il n'est aps en ruine, si il ne la construit pas a un emplacement voisin d'une autre colonie, si il la construit sur un emplacement voisin d'une de ses routes, si cet emplacement est sur terre et si il peut payer la construiction.'''
    bdd = j.bdd
    if intersection.isMaritime():
        raise ColonieError(ColonieError.EMPLACEMENT_MARITIME)
    if not j.peut_payer(intersection.getTerre(), Tarifs.COLONIE):
        raise ColonieError(ColonieError.RESSOURCES_INSUFFISANTES)
    col = Colonie.hasColonie(intersection, bdd)
    if col:
        raise ColonieError(ColonieError.EMPLACEMENT_OCCUPE)

    for i in intersection.neigh:
        if Colonie.hasColonie(i,bdd):
            raise ColonieError(ColonieError.EMPLACEMENTS_VOISINS_OCCUPES)
            return False
    for a in intersection.liens:
        jrout = Route.getRouteJoueur(a,bdd)
        if jrout == j.num:
            return True
    raise ColonieError(ColonieError.EMPLACEMENT_NON_RELIE)


@kallable
@protection
def construire_colonie(j, intersection):
    ''' Pose une nouvelle colonie du joueur j sur l'intersection si il en a la possibilité, et effectue le paiement.'''
    bdd = j.bdd
    c = Colonie(j.num, intersection)
    terre = intersection.getTerre()
    j.payer(terre, Tarifs.COLONIE)
    j.addStaticPoints(terre,1)

    c.save(bdd)
    for a in intersection.liens:
        jrout = Route.getRouteJoueur(a,bdd)
        if jrout != 0 and jrout != j.num:
            JoueurPossible(jrout,bdd).recalcul_route_la_plus_longue(terre)
    recalcul_route_la_plus_longue(terre,bdd)

def translate_construire_route(j,arrete_num_str):
    ''' L'action comporte pour parametre le numéro d'une arrete, et. '''
    try:
        num = int(arrete_num_str)
        ar = Plateau.getPlateau().ar(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [ar]

@preruine
@predefausse
def peut_construire_route(j, arrete, construction_route = False):
    ''' Un joueur j peut construire une route sur l'arrete si il n'est pas en ruine, si il n'existe pas déjà de route non en ruine sur cet emplacement, si cette arrete est terrestre, si il peut payer ou s'il a jouer une carte développement de construction de route, et s'il existe une colonie ou une route voiine à cette arrete.'''
    bdd = j.bdd
    if arrete.isMaritime():
        raise RouteError(RouteError.ARRETE_MARITIME)
    if (not construction_route and not j.peut_payer(arrete.getTerre(), Tarifs.ROUTE)):
        raise RouteError(RouteError.RESSOURCES_INSUFFISANTES)
    rout = Route.hasRoute(arrete,bdd)
    if rout:
        raise RouteError(RouteError.ARRETE_OCCUPEE)
     
    jcol1 = Colonie.getColonieJoueur(arrete.int1,bdd)
    jcol2 = Colonie.getColonieJoueur(arrete.int2,bdd)
    if (jcol1 == j.num) or (jcol2 == j.num):
        return True
    for a in arrete.neighb():
        jrout = Route.getRouteJoueur(a,bdd)
        if (jrout == j.num):
            return True
    raise RouteError(RouteError.ARRETE_NON_RELIEE)


@kallable
def construire_route(j,arrete, construction_route = False):
    ''' Pose, si c'est possible, une route du joueur j sur l'arrete et effectue le paiement.'''
    bdd = j.bdd
    if peut_construire_route(j,arrete, construction_route):
        r = Route(j.num,arrete)
        terre = arrete.getTerre()
        if not construction_route:
            j.payer(terre,Tarifs.ROUTE)
        r.save(bdd)
        j.recalcul_route_la_plus_longue(terre)
        challenge_route_la_plus_longue(j,terre)
        return True
    else:
        return False

def translate_evoluer_colonie(j,intersection_num_str):
    ''' L'action comporte pour parametre le numéro d'une intersection. '''
    try:
        num = int(intersection_num_str)
        it = Plateau.getPlateau().it(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [it]

@preruine
@predefausse
def peut_evoluer_colonie(j, intersection):
    ''' Un joueur j peut faire evoluer une colonie si il n'est pas en ruine, si elle est a lui et si il peyt payer le cout de l'évolution'''
    bdd = j.bdd
    colonie = Colonie.getColonie(intersection,bdd)
    if colonie == 0:
        raise ColonieError(ColonieError.COLONIE_INEXISTANTE)
    if colonie.isVille:
        raise ColonieError(ColonieError.COLONIE_DEJA_EVOLUEE)
    if colonie.joueur != j.num:
        raise ColonieError(ColonieError.NON_PROPRIETAIRE)
    if not j.peut_payer(intersection.getTerre(), Tarifs.VILLE):
        raise ColonieError(ColonieError.RESSOURCES_INSUFFISANTES)
    return True


@kallable
@protection
def evoluer_colonie(j,intersection):
    ''' Evolue si c'est possible la colonie, via le joueur j et effectue le paiement'''
    bdd = j.bdd
    colonie = Colonie.getColonie(intersection,bdd)
    colonie.evolue()
    terre = intersection.getTerre()
    j.payer(terre,Tarifs.VILLE)
    j.addStaticPoints(terre,1)
    colonie.save(bdd)

def translate_acheter_ressource(j,terre_num_str, carte_name):
    try:
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)

    carte = CartesGeneral.getFromName(carte_name)
    if carte == 0:
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)

    return [terre, carte]

@preruine
@predefausse
def peut_acheter_ressource(j,terre,carte):
    ''' Un joueur j sur cette terre peut acheter contre un lingot d'or une carte de type carte, si il n'est pas en ruine, si il possède au moins un lingot et si carte est une carte de ressource'''
    if not j.aColoniseTerre(terre):
        raise OrError(OrError.TERRE_NON_COLONISEE)
    if not j.getOr(terre) > 0:
        raise OrError(OrError.RESSOURCES_INSUFFISANTES)
    if not (carte.est_ressource() and carte.size() == 1 and carte.est_physiquement_possible()):
        raise OrError(OrError.FLUX_IMPOSSIBLE)
    return True


@kallable
@protection
def acheter_ressource(j,terre, carte):
    ''' Effectue via le joueur j sur cette terre l'achat de cette carte si il est possible'''
    j.payerOr(terre)
    j.recevoir(terre,carte)

# On suppose que chaque ile est separee d'au moins 2 arrete. Ca evite des ambiguites au niveau de la terre de construction.

def translate_construire_bateau(j,arrete_num_str):
    try:
        num = int(arrete_num_str)
        arrete = Plateau.getPlateau().ar(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)

    return [arrete]

@preruine
@predefausse
def peut_construire_bateau(j,arrete,construction_route = False):
    ''' Le joueur j peut poser un bateau sur l'arrete si il n'est pas en ruine, et s'il l'arrete est maritime et s'il peyt payer ou s'il a joué une carte de développement construction de route, et si il existe une colonie cotiere voisine de l'arrete.'''
    bdd = j.bdd
    terre = arrete.getTerre()
    # Si l'arrete n'a pas de terre, elle n'est surement pas reliée à la terre
    if terre == 0:
        raise BateauError(BateauError.ARRETE_NON_RELIEE)
    if not arrete.isMaritimeOuCotier():
        raise BateauError(BateauError.ARRETE_NON_CONSTRUCTIBLE)
    if not (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.BATEAU_TRANSPORT)):
        raise BateauError(BateauError.RESSOURCES_INSUFFISANTES)

    col1 = Colonie.getColonie(arrete.int1,bdd)
    col2 = Colonie.getColonie(arrete.int2,bdd)
    if (col1 != 0 and col1.joueur == j.num) or (col2 != 0 and col2.joueur == j.num):
        return True
    raise BateauError(BateauError.ARRETE_NON_RELIEE)


@kallable
def construire_bateau(j,arrete, construction_route = False):
    ''' Pose, si c'est possible un bateau du joueur j sur l'arrete et effectue le paiement.'''
    bdd = j.bdd
    if peut_construire_bateau(j,arrete, construction_route):
        i = bdd.get('lastBateauId')
        if i == None:
            i = 1
            bdd.set('lastBateauId',1)
        b = Bateau(i,j.num,arrete,Cartes.RIEN,Bateau.BateauType.TRANSPORT,False)
        if not construction_route:
            j.payer(arrete.getTerre(),Tarifs.BATEAU_TRANSPORT)

        b.save(bdd)
        bdd.incr('lastBateauId')
        return True
    else:
        return False


def translate_deplacer_bateau(j,bateau_num_str, arrete_num_str):
    try:
        num = int(bateau_num_str)
        bateau = Bateau.getBateau(num, j.bdd)
        if bateau == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
        num = int(arrete_num_str)
        arrete = Plateau.getPlateau().ar(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)

    return [bateau, arrete]

@preruine
@predefausse
def peut_deplacer_bateau(j,bateau,arrete):
    ''' Le joueur j peut déplacer un bateau sur une arrete, si il n'est pas en ruine, si le bateau appartient à ce joueur, si le bateau n'est pas abordé par un bateau pirate, si il souhaite se déplacer sur une arrete maritime, si cette arrete est voisine de la position actuelle du bateau ou a 2 déplacements pour un voillier, et si ce bateau n'a pas déjà bougé'''
    bdd = j.bdd
    if bateau == 0:
        raise BateauError(BateauError.BATEAU_INEXISTANT)
    if bateau.joueur != j.num:
        raise BateauError(BateauError.NON_PROPRIETAIRE)
    if Voleur.est_pirate(bateau.position,bdd):
        raise BateauError(BateauError.BATEAU_PIRATE)
    if not arrete.isMaritimeOuCotier(): 
        raise BateauError(BateauError.ARRETE_TERRESTRE)
    if not (arrete in bateau.position.neighb() or (bateau.etat == Bateau.BateauType.VOILIER and arrete in bateau.position.doubleNeighb() )):
        raise BateauError(BateauError.ARRETE_INATTEIGNABLE)
    if bateau.aBouge:
        raise BateauError(BateauError.BATEAU_DEJA_DEPLACE)
    return True


@kallable
@protection
def deplacer_bateau(j,bateau,arrete):
    ''' Déplace si c'est possible le bateau via le joueur j sur l'arrete'''
    bdd = j.bdd
    bateau.deplacer(arrete)
    bateau.aBouge = True
    bateau.save(bdd)

def translate_echanger_bateau(j,bateau_num_str, key_ct, key_cb):
    try:
        bdd = j.bdd
        num = int(bateau_num_str)
        bateau = Bateau.getBateau(num, bdd)
        if bateau == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
        ct = Cartes.get(key_ct)
        cb = Cartes.get(key_cb)
        if ct == 0 or cb == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [bateau, ct, cb]

@preruine
@predefausse
def peut_echanger_bateau(j,bateau,ct,cb):
    ''' Le joueur j peut échanger avec ce bateau ct cartes de la terre où se trouve le bataeu vers le bateau et cb cartes du bateau vers la terre si il n'est pas en ruine, si le bateau appartient au joueur, si le bateau est sur une zone d'échange (colonie cotiere ou port), si il a assez de ressource sur la terre et dans le bateau et si les échanges sont des nombres entiers naturels.'''
    bdd = j.bdd
    if j.num != bateau.joueur:
        raise BateauError(BateauError.NON_PROPRIETAIRE)
    if not bateau.en_position_echange(bdd):
        raise BateauError(BateauError.PAS_EMPLACEMENT_ECHANGE)
    if not j.peut_payer(bateau.position.getTerre(), ct):
        raise BateauError(BateauError.FLUX_TROP_ELEVE)
    if not bateau.peut_recevoir_et_payer(ct,cb):
        raise BateauError(BateauError.FLUX_TROP_ELEVE)
    if not ct.est_physiquement_possible():
        raise BateauError(BateauError.FLUX_IMPOSSIBLE)
    if not cb.est_physiquement_possible():
        raise BateauError(BateauError.FLUX_IMPOSSIBLE)
    return True


@kallable
@protection
def echanger_bateau(j,bateau,ct,cb):
    ''' Echange si c'est possible des cartes entre la cargaison du bateau et la main de j sur la terre où se trouve le bateau, ct cartes depuis la terre vers le bateau et cb depuis le bateau'''
    bdd = j.bdd
    terre = bateau.position.getTerre()
    j.payer(terre,ct)
    j.recevoir(terre,cb)
    bateau.remove(cb)
    bateau.append(ct)
    bateau.save(bdd)

def translate_evoluer_bateau(j,bateau_num_str):
    try:
        bdd = j.bdd
        num = int(bateau_num_str)
        bateau = Bateau.getBateau(num, bdd)
        if bateau == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [bateau]

@preruine
@predefausse
def peut_evoluer_bateau(j,bateau):
    ''' Le joueur j peut faire evoluer le bateau si il n'est pas en ruine, si le bateau est a lui, si le bateau est en zone d'échange, si le bateau n'est pas un voilier et si il peut payer l'évolution.'''
    bdd = j.bdd

    if j.num != bateau.joueur:
        raise BateauError(BateauError.NON_PROPRIETAIRE)
    if not bateau.en_position_echange(bdd):
        raise BateauError(BateauError.PAS_EMPLACEMENT_ECHANGE)
    if bateau.etat == Bateau.BateauType.TRANSPORT: 
        if not j.peut_payer(bateau.position.getTerre(), Tarifs.CARGO):
            raise BateauError(BateauError.RESSOURCES_INSUFFISANTES)
        return True
    if bateau.etat == Bateau.BateauType.CARGO:
        if not j.peut_payer(bateau.position.getTerre(), Tarifs.VOILIER):
            raise BateauError(BateauError.RESSOURCES_INSUFFISANTES)
        return True
    raise BateauError(BateauError.DEJA_EVOLUE)



@kallable
@protection
def evoluer_bateau(j,bateau):
    ''' Evolue, si c'est possible le bateau via le joueur j et effectue le paiement'''
    bdd = j.bdd
    terre = bateau.position.getTerre()
    if(bateau.etat == Bateau.BateauType.TRANSPORT):
        bateau.evolue()
        j.payer(terre,Tarifs.CARGO)
        bateau.save(bdd)
    elif bateau.etat == Bateau.BateauType.CARGO :
        bateau.evolue()
        j.payer(terre,Tarifs.VOILIER)
        bateau.save(bdd)
    else:
        return False

def translate_acheter_carte_developpement(j, terre_num_str):
    try:
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre]


@preruine
@predefausse
def peut_acheter_carte_developpement(j,terre):
    ''' Un joueur j peut acheter une carte de développement sur la terre si il peut la payer'''
    if not j.aColoniseTerre(terre):
        raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
    if not j.peut_payer(terre,Tarifs.DEVELOPPEMENT):
        raise DeveloppementError(DeveloppementError.RESSOURCES_INSUFFISANTES)
    return True
   

@kallable
@protection 
def acheter_carte_developpement(j,terre):
    ''' Pioche pour le joueur j sur cette terre, une carte de développement si c'est possible, et effectue le paiement.'''
    j.payer(terre,Tarifs.DEVELOPPEMENT)
    return j.piocher_developpement(terre)

def translate_coloniser(j,bateau_num_str, it_num_str, key_transfert):
    try:
        bdd = j.bdd
        num = int(bateau_num_str)
        bateau = Bateau.getBateau(num, bdd)
        transfert = Cartes.getTransfert(key_transfert)

        if bateau == 0 or transfert == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
        num = int(it_num_str)
        position = Plateau.getPlateau().it(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [bateau, position, transfert]

@preruine
@predefausse
def peut_coloniser(j,bateau,position,transfert):
    bdd = j.bdd
    if j.num != bateau.joueur:
        raise BateauError(BateauError.NON_PROPRIETAIRE)
    if not transfert.est_physiquement_possible():
        raise BateauError(BateauError.FLUX_IMPOSSIBLE)
    if not Tarifs.COLONIE <= bateau.cargaison:
        raise ColonieError(ColonieError.RESSOURCES_INSUFFISANTES)
    if not transfert <= (bateau.cargaison-Tarifs.COLONIE):
        raise BateauError(BateauError.FLUX_TROP_ELEVE)
    if not position.isTerrestreOuCotier():
        raise ColonieError(ColonieError.EMPLACEMENT_MARITIME)
    if j.aColoniseTerre(position.getTerre()):
        raise BateauError(BateauError.TERRE_DEJA_COLONISEE)
    
   
    col = Colonie.getColonie(position,bdd)
    if col != 0:
        raise ColonieError(ColonieError.EMPLACEMENT_OCCUPE)

    for i in position.neighb():
        col = Colonie.getColonie(i,bdd)
        if col != 0:
            raise ColonieError(ColonieError.EMPLACEMENTS_VOISINS_OCCUPES)

    if not position in bateau.positions_colonisables():
        raise BateauError(BateauError.EMPLACEMENT_INATTEIGNABLE)
    
    return True



@kallable
@protection
def coloniser(j,bateau,position,transfert):
    bdd = j.bdd
    Colonie(j.num,position).save(bdd)
    terre = position.getTerre()
    j.addTerre(terre)
    j.addStaticPoints(terre,1)
    j.recevoir(terre,transfert)
    bateau.remove(Tarifs.COLONIE + transfert)
    bateau.save(bdd)


def translate_echanger_classique(j,terre_num_str, carte_name1, carte_name2):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        c1 = Cartes.getFromName(carte_name1)
        c2 = Cartes.getFromName(carte_name2)
        if c1 == 0 or c2 == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,c1,c2]


@preruine
@predefausse
def peut_echanger_classique(j,terre,t1,t2):
    ''' Un joueur j peut effectuer un echange classique (4 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a colonisé la terre et si il peut payer 4 cartes de t1'''
    if not (t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible()):
        raise CommerceError(CommerceError.FLUX_IMPOSSIBLE)
    if not j.aColoniseTerre(terre):
        raise CommerceError(CommerceError.TERRE_NON_COLONISEE)
    if not j.peut_payer(terre,t1*4):
        raise CommerceError(CommerceError.RESSOURCES_INSUFFISANTES)
    return True


@kallable
@protection
def echanger_classique(j,terre,t1,t2):
    ''' Effectue s'il est possible un échange classique de cartes (4 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
    j.payer(terre,t1*4)
    j.recevoir(terre,t2)


def translate_echanger_commerce_tous(j,terre_num_str, carte_name1, carte_name2):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        c1 = Cartes.getFromName(carte_name1)
        c2 = Cartes.getFromName(carte_name2)
        if c1 == 0 or c2 == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,c1,c2]


@preruine
@predefausse
def peut_echanger_commerce_tous(j,terre,t1,t2):
    ''' Un joueur j peut effectuer un echange de commerce '?' (3 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce de type '?' et si il peut payer 3 cartes de t1'''

    if not(t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible()):
        raise CommerceError(CommerceError.FLUX_IMPOSSIBLE)
    if not j.aColoniseTerre(terre):
        raise CommerceError(CommerceError.TERRE_NON_COLONISEE)
    if not j.peut_payer(terre,t1*3):
        raise CommerceError(CommerceError.RESSOURCES_INSUFFISANTES)
    if not j.contient_commerce_utilisable(terre,CommerceType.TOUS):
        raise CommerceError(CommerceError.COMMERCE_NON_UTILISABLE)
    return True


@kallable
@protection
def echanger_commerce_tous(j,terre,t1,t2):
    ''' Effectue s'il est possible un échange commerce '?' de cartes (3 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
    j.payer(terre,t1*3)
    j.recevoir(terre,t2)


def translate_echanger_commerce(j,terre_num_str, carte_name1, carte_name2):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        c1 = Cartes.getFromName(carte_name1)
        c2 = Cartes.getFromName(carte_name2)
        if c1 == 0 or c2 == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,c1,c2]


@preruine
@predefausse
def peut_echanger_commerce(j,terre,t1,t2):
    ''' Un joueur j peut effectuer un echange de commerce spécialisé (2 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce spécialisé en le type t1 et si il peut payer 2 cartes de t1'''
    if not(t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible()):
        raise CommerceError(CommerceError.FLUX_IMPOSSIBLE)
    if not j.aColoniseTerre(terre):
        raise CommerceError(CommerceError.TERRE_NON_COLONISEE)
    if not j.peut_payer(terre,t1*2):
        raise CommerceError(CommerceError.RESSOURCES_INSUFFISANTES)

    if t1 == Cartes.ARGILE:
        comType = CommerceType.ARGILE
    elif t1 == Cartes.BOIS:
        comType = CommerceType.BOIS
    elif t1 == Cartes.BLE:
        comType = CommerceType.BLE
    elif t1 == Cartes.CAILLOU:
        comType = CommerceType.CAILLOU
    elif t1 == Cartes.MOUTON:
        comType = CommerceType.MOUTON
    else:
        comType = 0
        
    if not j.contient_commerce_utilisable(terre,comType):
        raise CommerceError(CommerceError.COMMERCE_NON_UTILISABLE)
        
    return True


@kallable
@protection
def echanger_commerce(j,terre,t1,t2):
    ''' Effectue s'il est possible un échange de commerce spécialisé de cartes (2 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
    j.payer(terre,t1*2)
    j.recevoir(terre,t2)


def translate_jouer_decouverte(j,terre_num_str, key_cartes):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        cartes = Cartes.get(key_cartes)
        if cartes == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,cartes]


@preruine
@predefausse
def peut_jouer_decouverte(joueur,terre,cartes):
    if not joueur.aColoniseTerre(terre):
        raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
    if not Cartes.DECOUVERTE <= joueur.getCartes(terre):
        raise DeveloppementError(DeveloppementError.CARTE_NON_POSSEDEE)
    if not(cartes.size() == 2 and cartes.est_ressource() and cartes.est_physiquement_possible()):
        raise DeveloppementError(DeveloppementError.DECOUVERTE_FLUX_IMPOSSIBLE)
    return True


@kallable
@protection
def jouer_decouverte(joueur,terre,cartes):
        joueur.recevoir(terre,cartes)
        joueur.payer(terre,Cartes.DECOUVERTE)


def translate_jouer_monopole(j,terre_num_str, carte_name, *jnums_str):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        c = Cartes.getFromName(carte_name)
        if c == 0:
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
        jnums = []
        for jnum_str in jnums_str:
            jnums.add(int(jnum_str))
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,c] + jnums


@preruine
@predefausse
def peut_jouer_monopole(joueur,terre,t1, jvols):
    if not joueur.aColoniseTerre(terre):
        raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
    if not Cartes.MONOPOLE <= joueur.getCartes(terre):
        raise DeveloppementError(DeveloppementError.CARTE_NON_POSSEDEE)
    if not (t1.est_ressource() and t1.size() == 1 and t1.est_physiquement_possible()):
        raise DeveloppementError(DeveloppementError.MONOPOLE_FLUX_IMPOSSIBLE)
    if not len(jvols) > 0:
        raise DeveloppementError(DeveloppementError.MONOPOLE_NBJOUEURS_TROP_FAIBLE)
    if not len(jvols) <= 3:
        raise DeveloppementError(DeveloppementError.MONOPOLE_NBJOUEURS_TROP_ELEVE)
    if joueur.num in jvols:
        raise DeveloppementError(DeveloppementError.MONOPOLE_AUTO_ATTAQUE)

    for jnum in jvols:
        if jnum > JoueurPossible.getNbJoueurs() or jnum < 1:
            raise DeveloppementError(DeveloppementError.MONOPOLE_JOUEUR_INEXISTANT)
        j = JoueurPossible(jnum,joueur.bdd)
        if j.getEnRuine():
            raise DeveloppementError(DeveloppementError.MONOPOLE_JOUEUR_EN_RUINE)
        if not j.aColoniseTerre(terre):
            raise DeveloppementError(DeveloppementError.MONOPOLE_TERRE_NON_COLONISEE)
    return True


@kallable
@protection
def jouer_monopole(joueur,terre,t1,jvols):
    Monopole(0,joueur,jvols,terre,t1).save(joueur.bdd)


def translate_jouer_construction_routes(j,terre_num_str, isFirstRoute_str, a1_num_str, isSecondRoute_str, a2_num_str):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        num = int(a1_num_str)
        a1 = Plateau.getPlateau().ter(num)
        num = int(a2_num_str)
        a2 = Plateau.getPlateau().ter(num)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,isFirstRoute_str == 'True', a1, isSecondRoute_str == 'False', a2]

@preruine
@predefausse
def peut_jouer_construction_routes(joueur,terre,isFirstRoute,a1,isSecondRoute,a2):
    if a1 == a2 and isFirstRoute and isSecondRoute:
        raise DeveloppementError(DeveloppementError.CONSTRUCTION_ROUTES_IDENTIQUES)
    if not joueur.aColoniseTerre(terre):
        raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
    if not Cartes.CONSTRUCTION_ROUTES <= joueur.getCartes(terre):
        raise DeveloppementError(DeveloppementError.CARTE_NON_POSSEDEE)
    if not (a1.getTerre() == terre or a1.int1.getTerre() == terre or a1.int2.getTerre() == terre):
        raise DeveloppementError(DeveloppementError.CONSTRUCTION_EMPLACEMENT_INCORRECT)
    if not (a2.getTerre() == terre or a2.int1.getTerre() == terre or a2.int2.getTerre() == terre):
        raise DeveloppementError(DeveloppementError.CONSTRUCTION_EMPLACEMENT_INCORRECT)
    if isFirstRoute:
        b = peut_construire_route(joueur,a1,True)
    else:
        b = peut_construire_bateau(joueur,a1,True)
    if isSecondRoute:
        b = b and peut_construire_route(joueur,a2,True) 
    else:
        b = b and peut_construire_bateau(joueur,a2,True)
    return b


@kallable
@protection
def jouer_construction_routes(joueur,terre,isFirstRoute,a1,isSecondRoute,a2):
    joueur.payer(terre,Cartes.CONSTRUCTION_ROUTES)
    if isFirstRoute:
        construire_route(joueur,a1,True)
    else:
        construire_bateau(joueur,a1,True)
    if isSecondRoute:
        construire_route(joueur,a2,True)
    else:
        construire_bateau(joueur,a2,True)


@preruine
@predefausse
def peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol):
    bdd = joueur.bdd
    if not joueur.aColoniseTerre(terre):
        raise VoleurError(VoleurError.TERRE_NON_COLONISEE)
    if not (hex == 0 or hex.terre == terre):
        raise VoleurError(VoleurError.EMPLACEMENT_INTERDIT)
    if jvol > JoueurPossible.getNbJoueurs() or jvol < 0: # jvol = 0 est toléré pour les îles où le voleur n'est pas déplaceable.
        raise VoleurError(VoleurError.JOUEUR_VOLE_INEXISTANT)

    if voleurType == Voleur.VoleurType.BRIGAND:
        voleur = Voleur.getBrigand(terre,bdd)
    else:
        voleur = Voleur.getPirate(terre,bdd)
    if jvol == 0:
        t = (hex, 0)
    else:
        t = (hex, jvol)
    if not t in joueur.positions_possibles_voleur(terre,voleur):
        raise VoleurError(VoleurError.EMPLACEMENT_INTERDIT)

    return True


def deplacer_voleur(joueur,terre,voleurType,hex,jvol):
    DeplacementVoleur(0,joueur,terre,voleurType,hex,jvol,True).save(joueur.bdd) 


def translate_jouer_chevallier(j,terre_num_str, voleur_type, hex_num_str, jnum_str):
    try:
        bdd = j.bdd
        num = int(terre_num_str)
        terre = Plateau.getPlateau().ter(num)
        num = int(hex_num_str)
        hex = Plateau.getPlateau().hexa(num)
        jnum = int(jnum_str)
    except (ValueError, IndexError):
        raise ActionError(ActionError.MAUVAIS_PARAMETRES)
    return [terre,voleur_type, hex, jnum]



@preruine
@predefausse
def peut_jouer_chevallier(joueur,terre,voleurType, hex,jvol):
    if not joueur.aColoniseTerre(terre):
        raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
    if not Cartes.CHEVALLIER <= joueur.getCartes(terre):
        raise DeveloppementError(DeveloppementError.CARTE_NON_POSSEDEE)
    return peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol)


@kallable
@protection
def jouer_chevallier(joueur,terre,voleurType, hex,jvol):
    joueur.add_chevallier(terre)
    joueur.payer(terre,Cartes.CHEVALLIER)
    challenge_armee_la_plus_grande(joueur,terre)
    deplacer_voleur(joueur,terre,voleurType,hex,jvol)
