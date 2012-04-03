# -*- coding: utf8 -*-
from pions import *
from plateau import *
from cartes import *
from foret_action import *
import random
import functools
import redis
from errors import *


REDIS = redis.StrictRedis()

class Tarifs:
    COLONIE = CartesRessources(1,1,1,0,1)
    VILLE = CartesRessources(0,3,0,2,0)
    ROUTE = CartesRessources(1,0,1,0,0)
    BATEAU_TRANSPORT = CartesRessources(0,0,1,0,1)
    CARGO = CartesRessources(1,0,0,1,0)
    VOILIER = CartesRessources(1,0,0,0,2)
    DEVELOPPEMENT = CartesRessources(0,1,0,1,1)

def protection(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        peut_f = getattr(Jeu,'peut_' + f.__name__)
        if peut_f(*args,**kwargs):
            f(*args,**kwargs)
            return True
        else:
            return False

    return helper

def kallable(f):
    f.peut_etre_appellee = True
    return f

class Des:

    NB_LANCES = 4

    @staticmethod
    def roll():
        ''' Enregistre une liste de 4 lancés de dés dans la bdd '''
        dices = []
        for i in xrange(Des.NB_LANCES):
            dices.append(random.randint(2, 12))
        Des.save(dices)


    @staticmethod
    def getOrigin():
        ''' Renvoie le nombre de lancés de dés, correspond donc en jeu de plateau au nombres de joueurs qui ont lancé les dés et donc au numéro du joueur, modulo le nombre de joueurs, qui a effectué le premiers des 4 derniers lancés. '''
        return int(REDIS.get('dices:joueur_origine'))
    
    @staticmethod
    def setOrigin(num):
        ''' Enregistre le nombre de lancés de dés depuis le début de la partie '''
        REDIS.set('dices:joueur_origine',num)
    
    @staticmethod
    def incrOrigin():
        ''' Incrémente le nombre de lancé de dés '''
        REDIS.incr('dices:joueur_origine',Des.NB_LANCES)

    @staticmethod
    def save(dices):
        ''' Sauvegarde un lancé de 4 dés '''
        REDIS.delete('dices')
        REDIS.rpush('dices',*dices)
        Des.incrOrigin()

    @staticmethod
    def getDices():
        ''' Renvoie les 4 derniers lancés de dés '''
        a =  REDIS.lrange('dices',0,-1)
        dices = [int(i) for i in a]
        return dices

class Joueur:
    ''' Classe représentant un joueur, avec ses pions (construction, bateau), permettant de récupérer les informations relatives à ce joueur, voire d'en modifier.'''
    def __init__(self,num,bdd = REDIS):
        self.num = num
        self.bdd = bdd

    def setCartes(self,terre,cartes):
        ''' Associe à la main du joueur sur cette terre les cartes données en paramètre'''
        cartes.setTo('J'+str(self.num)+':T'+str(terre.num), self.bdd)

    def getCartes(self,terre):
        ''' Renvoie la main du joueur sur cette terre'''
        return CartesGeneral.get('J'+str(self.num)+':T'+str(terre.num), self.bdd)
    
    def payer(self,terre, cartes):
        ''' Déduis de la main du joueur sur cette terre les cartes données en paramètre'''
        self.setCartes(terre,self.getCartes(terre) - cartes)

    def recevoir(self,terre,cartes):
        ''' Ajoute à la main du joeuur sur cette terre les cartes données en paramètre'''
        self.payer(terre,cartes*(-1))

    def peut_payer(self,terre,cartes):
        ''' Vérifie si la main du joeuur sur cette terre peut payer la quantité donnée en paramètre'''
        return cartes <= self.getCartes(terre)
    
    def setCartesEnSommeil(self,terre,cartes):
        ''' Associe à la main du joueur sur cette terre les cartes données en paramètre, ces cartes sont en sommeil (non visibles pour le joueur qui les récupères, en particulier quand il achète une carte de développement, il doit attendre la nuit avant de pouvoir savoir ce qu'il a acheté, si l'arbre d'action a validé cette action)'''
        cartes.setTo('J'+str(self.num)+':T'+str(terre.num)+':sommeil')

    def getCartesEnSommeil(self,terre):
        ''' Renvoie la main du joueur sur cette terre, ces cartes sont en sommeil (non visibles pour le joueur qui les récupères, en particulier quand il achète une carte de développement, il doit attendre la nuit avant de pouvoir savoir ce qu'il a acheté, si l'arbre d'action a validé cette action)'''
        return CartesGeneral.get('J'+str(self.num)+':T'+str(terre.num)+':sommeil')
    
    def recevoirEnSommeil(self,terre,cartes):
        ''' Ajoute à la main du joeuur sur cette terre les cartes données en paramètre'''
        self.setCartesEnSommeil(terre,self.getCartesEnSommeil(terre) + cartes)
    
    def ressource_aleatoire(self,terre):
        ''' Ajoute à la main du joueur sur cette terre une carte de ressource aléatoire'''
        carte = CartesRessources.get_random_ressource()
        self.setCartes(terre,self.getCartes(terre) + carte)

    def getOr(self,terre):
        ''' Renvoie la quantité d'or du joueur présente sur cette terre'''
        return int(self.bdd.get('J'+str(self.num)+':T'+str(terre.num)+':or'))

    def setOr(self,terre, nb):
        ''' Définit la quantité d'or du joueur présente sur cette terre'''
        self.bdd.set('J'+str(self.num)+':T'+str(terre.num)+':or', nb)

    def addOr(self,terre,nb):
        ''' Ajoute au stock d'or du joeuur sur cette terre nb lingots d'or'''
        self.setOr(terre, self.getOr(terre) + nb)

    def payerOr(self,terre):
        ''' Déduis du stock d'or du joueur sur cette terre un lingot d'or'''
        self.addOr(terre,-1)

    def aColoniseTerre(self,terre):
        return self.bdd.sismember('J'+str(self.num)+':terres', terre.num)
    
    def addTerre(self,terre):
        ''' Ajoute une terre aux terres colonisées du joueur'''
        self.bdd.sadd('J'+str(self.num)+':terres',terre.num)
        self.setCartes(terre,Cartes.RIEN)
        self.setOr(terre,0)
        self.set_chevalliers(terre,0)
        self.set_route_la_plus_longue(terre,0)
        self.setStaticPoints(terre,0)
        terre.addJoueur(self)

    def getTerres(self):
        l = self.bdd.smembers('J'+str(self.num)+':terres')
        t = []
        for i in l:
            t.append(Plateau.getPlateau().ter(int(i)))
        return t

    def piocher_developpement(self, terre):
        ''' Ajoute à la main du joueur sur cette terre une carte de développement aléatoire'''
        i = random.Random().randint(1,5)
        if (i == 1):
            carte = Cartes.CHEVALLIER
        elif i == 2:
            carte = Cartes.MONOPOLE
        elif i == 3:
            carte = Cartes.POINT_VICTOIRE
        elif i == 4:
            carte = Cartes.DECOUVERTE
        elif i == 5:
            carte = Cartes.CONSTRUCTION_ROUTES
        self.recevoirEnSommeil(terre,carte)
        return carte

    def contient_commerce_utilisable(self,terre,comType):
        ''' Vérifie si le joueur contient sur cette terre un commerce de type comType'''
        for c in self.getBatiments():
            c = int(c)
            intersection = Plateau.getPlateau().it(c)
            ms = Voleur.marcheNonBrigande(intersection, self.bdd)
            ps = Voleur.portNonPirate(intersection, self.bdd)
            if ms != 0:
                for m in ms:
                    if m.commerceType == comType:
                        return True
            if ps != 0:
                for p in ps:
                    if p.commerceType == comType:
                        return True
        return False


    def recolter_ressources(self,des):
        ''' Récolte les ressources du joueur en fonction du lancé de dés, sur toutes les terres'''
        for c in self.getBatiments():
            c = int(c)
            it = Plateau.getPlateau().it(c)
            terre = it.getTerre()
            res = Colonie.getColonie(it,self.bdd).ressources_from_past(des,self.bdd)
            if (res != 0):
                self.addOr(terre,res[1])
                self.recevoir(terre,res[0]) 

    def getBateaux(self):
        ''' Renvoie les identifiants des bateaux du joueur, tout type confondu'''
        return self.getBateauxTransport().union(self.getCargos()).union(self.getVoiliers())
    
    def getBateauxTransport(self):
        return self.bdd.smembers('J'+str(self.num)+':transports')

    def getCargos(self):
        return self.bdd.smembers('J'+str(self.num)+':cargos')
    
    def getVoiliers(self):
        return self.bdd.smembers('J'+str(self.num)+':voiliers')
    
    
    def getBateauxTransportPositions(self):
        ''' Renvoie les arretes où se trouvent les bateaux du joueur, tout type confondu'''
        return self.bdd.smembers('J'+str(self.num)+':transports:positions')

    def getCargosPositions(self):
        return self.bdd.smembers('J'+str(self.num)+':cargos:positions')
    
    def getVoiliersPositions(self):
        return self.bdd.smembers('J'+str(self.num)+':voiliers:positions')
    
    def getBateauxPositions(self):
        ''' Renvoie les bateaux du joueur, tout type confondu'''
        return self.getBateauxTransportPositions().union(self.getCargosPositions()).union(self.getVoiliersPositions())

    def getColonies(self):
        ''' Renvoie tous les intersection où se trouvent les colonies du joueur'''
        return self.bdd.smembers('J'+str(self.num)+':colonies')

    def getVilles(self):
        ''' Renvoie tous les intersection où se trouvent les villes du joueur'''
        return self.bdd.smembers('J'+str(self.num)+':villes')
    
    def getRoutes(self):
        ''' Renvoie tous les arretes où se trouvent les routes du joueur'''
        return self.bdd.smembers('J'+str(self.num)+':routes')

    def getBatiments(self):
        ''' Renvoie toutes les intersection où se trouvent les batiments du joueur, tout type confondu'''
        return self.getColonies().union(self.getVilles())
    
    def set_chevalliers(self,terre, nb):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        self.bdd.set('J'+str(self.num)+':T'+str(terre.num)+':armee', nb)
                 
    def add_chevallier(self,terre):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        return int(self.bdd.incr('J'+str(self.num)+':T'+str(terre.num)+':armee'))
 
    def get_chevalliers(self,terre):
        ''' Renvoie l'armée du joueur sur cette terre'''
        if self.getEnRuine():
            return 0
        return int(self.bdd.get('J'+str(self.num)+':T'+str(terre.num)+':armee'))
   
    def set_deplacement_voleur(self,terre, dep):
        ''' Indique que sur cette terre, le joueur doit déplacer le voleur'''
        self.bdd.set('J'+str(self.num)+':T'+str(terre.num)+':deplacement_voleur', dep)
 
    def get_deplacement_voleur(self,terre):
        ''' Renvoie vrai si sur cette terre, le joueur doit déplacer le voleur'''
        return self.bdd.get('J'+str(self.num)+':T'+str(terre.num)+':deplacement_voleur') == 'True'
         
    def get_carte_armee_la_plus_grande(self,terre):
        ''' Renvoie vrai si le joueur a l'armée la plus grande sur cette terre'''
        u = Jeu.get_armee_la_plus_grande(terre, self.bdd)
        return u!=0 and u[0] == self.num
 
    def get_route_la_plus_longue(self,terre):
        ''' Renvoie la taille de la route la plus longue du joueur sur cette terre'''
        if self.getEnRuine():
            return 0
        return int(self.bdd.get('J'+str(self.num)+':T'+str(terre.num)+':rlpl'))
 
    def set_route_la_plus_longue(self,terre, l):
        ''' Définie la route la plus longue sur cette terre comme étant de taille l'''
        self.bdd.set('J'+str(self.num)+':T'+str(terre.num)+':rlpl',l)

    def recalcul_route_la_plus_longue(self,terre):
        ''' Calcule la route la plus longue de ce joueur sur cette terre. Si elle est déjà calculée alors renvoie juste la valeur déjà calculée '''
        if self.getEnRuine():
            self.set_route_la_plus_longue(terre,0)
            return
        if self.aColoniseTerre(terre):
                i = 0
                for arn in self.getRoutes():
                    ar = Plateau.getPlateau().ar(int(arn))
                    r = Route.getRoute(ar,self.bdd)
                    if ar.getTerre() == terre and r.est_extremite(self.bdd):
                        i = max(i, r.rlplfr(self.bdd))
                self.set_route_la_plus_longue(terre,i)
                       
    def get_carte_route_la_plus_longue(self,terre):
        ''' Vérifie si ce joueur a la carte de la route al plus longue sur cette terre'''
        u = Jeu.get_route_la_plus_longue(terre, self.bdd)
        return u!=0 and u[0]== self.num

    def addStaticPoints(self,terre,nb):
        ''' Ajoute nb points aux points statiques (ie batiments) de cette terre'''
        if self.getEnRuine():
            return 
        self.bdd.incr('J'+str(self.num)+':T'+str(terre.num)+':points',nb)

    def getStaticPoints(self,terre):
        if self.getEnRuine():
            return 0
        return int(self.bdd.get('J'+str(self.num)+':T'+str(terre.num)+':points'))
    
    def setStaticPoints(self,terre, nb):
        if self.getEnRuine():
            return 
        self.bdd.set('J'+str(self.num)+':T'+str(terre.num)+':points', nb)

    def getPoints(self,terre):
        ''' Calcule le nombre de points de ce joueur sur cette terre'''
        if self.getEnRuine() or not self.aColoniseTerre(terre):
            return 0
        return self.getVisiblePoints(terre) + self.getCartes(terre).get_cartes_de_type(Cartes.POINT_VICTOIRE)
    
    def getVisiblePoints(self,terre):
        ''' Calcule le nombre de points de ce joueur sur cette terre'''
        if self.getEnRuine() or not self.aColoniseTerre(terre):
            return 0
        p = 0
        if (self.get_carte_route_la_plus_longue(terre)):
            p += 2
        if (self.get_carte_armee_la_plus_grande(terre)):
            p += 2
        return self.getStaticPoints(terre) + p


    @staticmethod
    def setNbJoueurs(nb):
        REDIS.set('NombreJoueurs',nb)
        
    @staticmethod
    def getNbJoueurs():
        return int(REDIS.get('NombreJoueurs'))

    def setEnRuine(self,ruine):
        self.bdd.set('J'+str(self.num)+':ruine',ruine)
    
    def getEnRuine(self):
        return self.bdd.get('J'+str(self.num)+':ruine') == 'True'

    def ruiner(self):
        self.setEnRuine(True)
        for t in self.getTerres():
            self.setStaticPoints(t,0)
            Jeu.recalcul_route_la_plus_longue(t,self.bdd)
            Jeu.recalcul_armee_la_plus_grande(t,self.bdd)

class Jeu:

    @staticmethod
    def get_all_joueurs():
        i = Joueur.getNbJoueurs()
        joueurs = []
        for j in xrange(i):
            joueurs.append(Joueur(j+1))
        return joueurs

    # Renvoie le joueur qui possède la route la plus longue sur la terre terre et sa longueur.
    @staticmethod
    def get_route_la_plus_longue(terre, bdd = REDIS):
        jnum = bdd.get('T'+str(terre.num)+':carte_rlpl:joueur')
        l = bdd.get('T'+str(terre.num)+':carte_rlpl:longueur')
        if jnum != None and l != None:
            return (int(jnum),int(l))
        else:
            return 0

    @staticmethod
    def set_route_la_plus_longue(terre,jnum ,n, bdd = REDIS):
        bdd.set('T'+str(terre.num)+':carte_rlpl:joueur',jnum)
        bdd.set('T'+str(terre.num)+':carte_rlpl:longueur',n)
    
    @staticmethod
    def delete_route_la_plus_longue(terre, bdd = REDIS):
        bdd.delete('T'+str(terre.num)+':carte_rlpl:joueur')
        bdd.delete('T'+str(terre.num)+':carte_rlpl:longueur')

    # Vérifie si j a une route plus longue que la route la plus longue sur la terre terre. Si la route actuelle est nulle, alors vérifie si j a une route de plus de 5 troncons. Si c'est le cas, j prend la plus du joueur actuellement en position
    @staticmethod
    def challenge_route_la_plus_longue(j,terre):
            bdd = j.bdd
            n = j.get_route_la_plus_longue(terre)
            if n>=5:
                u = Jeu.get_route_la_plus_longue(terre,bdd)
                if u == 0 or  n > u[1]:
                    Jeu.set_route_la_plus_longue(terre,j.num,n,bdd)
                    
    # Recalcule qui parmi les colons de la terre a la carte de route la plus longue. Si il y a égalité, si la route la plus longue est identique à celle précédemment inscrite dans la base de données, alors elle est conservée, sinon, la carte est retirée du jeu jusqu'à ce que ait un montant plus important.
    @staticmethod
    def recalcul_route_la_plus_longue(terre, bdd = REDIS):
        jt = terre.getJoueurs(bdd)
        rlpl = 0
        jmax = []
        for jtn in jt:
            j = Joueur(int(jtn),bdd)
            rlplj = j.get_route_la_plus_longue(terre)
            if rlplj > rlpl:
                rlpl = rlplj
                jmax = [j.num]
            elif rlplj == rlpl:
                jmax.append(j.num)
        if len(jmax) == 1 and rlpl >= 5:
            Jeu.set_route_la_plus_longue(terre,jmax[0],rlpl,bdd)
        else:
            t = Jeu.get_route_la_plus_longue(terre,bdd)
            if t != 0  and (t[1] > rlpl or not t[0] in jmax):
                Jeu.delete_route_la_plus_longue(terre,bdd)
                


    # Renvoie le joueur qui possède l'armee la plus grande sur la terre terre et sa longueur.
    @staticmethod
    def get_armee_la_plus_grande(terre, bdd = REDIS):
        j = bdd.get('T'+str(terre.num)+':carte_alpg:joueur')
        s = bdd.get('T'+str(terre.num)+':carte_alpg:taille')
        if j != None and s != None:
            return (int(j),int(s))
        else:
            return 0

    @staticmethod
    def set_armee_la_plus_grande(terre,j,s, bdd = REDIS):
        bdd.set('T'+str(terre.num)+':carte_alpg:joueur',j)
        bdd.set('T'+str(terre.num)+':carte_alpg:taille',s)
    
    @staticmethod
    def delete_armee_la_plus_grande(terre, bdd = REDIS):
        bdd.delete('T'+str(terre.num)+':carte_alpg:joueur')
        bdd.delete('T'+str(terre.num)+':carte_alpg:taille')

                
    # Vérifie si j a une armee plus grande que la armee la plus grande sur la terre terre. Si l'armee actuelle est nulle, alors vérifie si j a une armee de plus de 3 chevalliers. Si c'est le cas, j prend la plus du joueur actuellement en position
    @staticmethod
    def challenge_armee_la_plus_grande(j,terre):
        bdd = j.bdd
        n = j.get_chevalliers(terre)
        if n>=3:
            u = Jeu.get_armee_la_plus_grande(terre,bdd)
            if u == 0 or  n > u[1]:
                Jeu.set_armee_la_plus_grande(terre,j.num,n,bdd)
    
    # Recalcule qui parmi les colons de la terre a la carte de route la plus longue. Si il y a égalité, si la route la plus longue est identique à celle précédemment inscrite dans la base de données, alors elle est conservée, sinon, la carte est retirée du jeu jusqu'à ce que ait un montant plus important.
    @staticmethod
    def recalcul_armee_la_plus_grande(terre, bdd = REDIS):
        jt = terre.getJoueurs(bdd)
        armee = 0
        jmax = []
        for jtn in jt:
            j = Joueur(int(jtn),bdd)
            armeej = j.get_chevalliers(terre)
            if armeej > armee:
                armee = armeej
                jmax = [j.num]
            elif armeej == armee:
                jmax.append(j.num)
        if len(jmax) == 1 and armee >= 3:
            Jeu.set_armee_la_plus_grande(terre,jmax[0],armee,bdd)
        else:
            t = Jeu.get_armee_la_plus_grande(terre,bdd)
            if t != 0  and (t[1] > armee or not t[0] in jmax):
                Jeu.delete_armee_la_plus_grande(terre,bdd)

# -----------------------------------------------------
#    Actions de la nuit
# -----------------------------------------------------

    @staticmethod
    def designer_deplaceur_de_voleur():
        p = Plateau.getPlateau()
        for terre in p.terres:
            js = terre.getJoueurs(REDIS)
            for jn in js:
                j = Joueur(int(jn))
                j.set_deplacement_voleur(terre,False)

        des = Des.getDices()
        origin = Des.getOrigin()
        for terre in p.terres:
            js = []
            for jns in terre.getJoueurs(REDIS):
                j = Joueur(int(jns))
                if(not j.getEnRuine()):
                    js.append(j)
            for i in range(0,Des.NB_LANCES):
                if des[i] == 7:
                    js[(i+origin)%len(js)].set_deplacement_voleur(terre,True)
    
    @staticmethod
    def peut_recolter_ressources(des):
        ''' On peut lancer la récolte des réssources si les dés sont entre 2 et 12'''
        if des < 2 or des == 7 or des > 12:
            return False
        else:
            return True

    @staticmethod
    @kallable
    @protection
    def recolter_ressources(des):
        ''' Effectue pour tous les joueurs sur toutes les terres la récolte des ressources sauf s'ils sont en ruine'''
        for j in Jeu.get_all_joueurs():
            if not j.getEnRuine(): 
                j.recolter_ressources(des)

# -----------------------------------------------------
#    Actions dans la journee
# -----------------------------------------------------
    
    @staticmethod
    def peut_construire_colonie(j,intersection):
        ''' Un joueur peut construire une colonie si il n'est aps en ruine, si il ne la construit pas a un emplacement voisin d'une autre colonie, si il la construit sur un emplacement voisin d'une de ses routes, si cet emplacement est sur terre et si il peut payer la construiction.'''
        bdd = j.bdd
        if j.getEnRuine():
            raise ColonieError(ColonieError.JOUEUR_EN_RUINE)
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

    @staticmethod
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
                Joueur(jrout,bdd).recalcul_route_la_plus_longue(terre)
        Jeu.recalcul_route_la_plus_longue(terre,bdd)

    @staticmethod
    def peut_construire_route(j, arrete, construction_route = False):
        ''' Un joueur j peut construire une route sur l'arrete si il n'est pas en ruine, si il n'existe pas déjà de route non en ruine sur cet emplacement, si cette arrete est terrestre, si il peut payer ou s'il a jouer une carte développement de construction de route, et s'il existe une colonie ou une route voiine à cette arrete.'''
        bdd = j.bdd
        if j.getEnRuine():
            raise RouteError(RouteError.JOUEUR_EN_RUINE)
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

    @staticmethod
    @kallable
    def construire_route(j,arrete, construction_route = False):
        ''' Pose, si c'est possible, une route du joueur j sur l'arrete et effectue le paiement.'''
        bdd = j.bdd
        if Jeu.peut_construire_route(j,arrete, construction_route):
            r = Route(j.num,arrete)
            terre = arrete.getTerre()
            if not construction_route:
                j.payer(terre,Tarifs.ROUTE)
            r.save(bdd)
            j.recalcul_route_la_plus_longue(terre)
            Jeu.challenge_route_la_plus_longue(j,terre)
            return True
        else:
            return False

    @staticmethod
    def peut_evoluer_colonie(j, intersection):
        ''' Un joueur j peut faire evoluer une colonie si il n'est pas en ruine, si elle est a lui et si il peyt payer le cout de l'évolution'''
        bdd = j.bdd
        if j.getEnRuine():
            raise ColonieError(ColonieError.JOUEUR_EN_RUINE)
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

    @staticmethod
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
    
    
    @staticmethod
    def peut_acheter_ressource(j,terre,carte):
        ''' Un joueur j sur cette terre peut acheter contre un lingot d'or une carte de type carte, si il n'est pas en ruien, si il possède au moins un lingot et si carte est une carte de ressource'''
        if j.getEnRuine():
            raise OrError(OrError.JOUEUR_EN_RUINE)
        if not j.aColoniseTerre(terre):
            raise OrError(OrError.TERRE_NON_COLONISEE)
        if not j.getOr(terre) > 0:
            raise OrError(OrError.RESSOURCES_INSUFFISANTES)
        if not (carte.est_ressource() and carte.size() == 1 and carte.est_physiquement_possible()):
            raise OrError(OrError.FLUX_IMPOSSIBLE)
        return True

    @staticmethod
    @kallable
    @protection
    def acheter_ressource(j,terre, carte):
        ''' Effectue via le joueur j sur cette terre l'achat de cette carte si il est possible'''
        j.payerOr(terre)
        j.recevoir(terre,carte)

# On suppose que chaque ile est separee d'au moins 2 arrete. Ca evite des ambiguites au niveau de la terre de construction.
    @staticmethod
    def peut_construire_bateau(j,arrete,construction_route = False):
        ''' Le joueur j peut poser un bateau sur l'arrete si il n'est pas en ruine, et s'il l'arrete est maritime et s'il peyt payer ou s'il a joué une carte de développement construction de route, et si il existe une colonie cotiere voisine de l'arrete.'''
        bdd = j.bdd
        terre = arrete.getTerre()
        # Si l'arrete n'a pas de terre, elle n'est surement pas reliée à la terre
        if terre == 0:
            raise BateauError(BateauError.ARRETE_NON_RELIEE)
        if j.getEnRuine():
            raise BateauError(BateauError.JOUEUR_EN_RUINE)
        if not arrete.isMaritimeOuCotier():
            raise BateauError(BateauError.ARRETE_NON_CONSTRUCTIBLE)
        if not (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.BATEAU_TRANSPORT)):
            raise BateauError(BateauError.RESSOURCES_INSUFFISANTES)

        col1 = Colonie.getColonie(arrete.int1,bdd)
        col2 = Colonie.getColonie(arrete.int2,bdd)
        if (col1 != 0 and col1.joueur == j.num) or (col2 != 0 and col2.joueur == j.num):
            return True
        raise BateauError(BateauError.ARRETE_NON_RELIEE)
    
    @staticmethod
    @kallable
    def construire_bateau(j,arrete, construction_route = False):
        ''' Pose, si c'est possible un bateau du joueur j sur l'arrete et effectue le paiement.'''
        bdd = j.bdd
        if Jeu.peut_construire_bateau(j,arrete, construction_route):
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
    

    @staticmethod
    def peut_deplacer_bateau(j,bateau,arrete):
        ''' Le joueur j peut déplacer un bateau sur une arrete, si il n'est pas en ruine, si le bateau appartient à ce joueur, si le bateau n'est pas abordé par un bateau pirate, si il souhaite se déplacer sur une arrete maritime, si cette arrete est voisine de la position actuelle du bateau ou a 2 déplacements pour un voillier, et si ce bateau n'a pas déjà bougé'''
        bdd = j.bdd
        if bateau == 0:
            raise BateauError(BateauError.BATEAU_INEXISTANT)
        if j.getEnRuine():
            raise BateauError(BateauError.JOUEUR_EN_RUINE)
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
    
    @staticmethod
    @kallable
    @protection
    def deplacer_bateau(j,bateau,arrete):
        ''' Déplace si c'est possible le bateau via le joueur j sur l'arrete'''
        bdd = j.bdd
        bateau.deplacer(arrete)
        bateau.aBouge = True
        bateau.save(bdd)

    @staticmethod
    def peut_echanger_bateau(j,bateau,ct,cb):
        ''' Le joueur j peut échanger avec ce bateau ct cartes de la terre où se trouve le bataeu vers le bateau et cb cartes du bateau vers la terre si il n'est pas en ruine, si le bateau appartient au joueur, si le bateau est sur une zone d'échange (colonie cotiere ou port), si il a assez de ressource sur la terre et dans le bateau et si les échanges sont des nombres entiers naturels.'''
        bdd = j.bdd
        if j.getEnRuine():
            raise BateauError(BateauError.JOUEUR_EN_RUINE)
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

    @staticmethod
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
    
    @staticmethod
    def peut_evoluer_bateau(j,bateau):
        ''' Le joueur j peut faire evoluer le bateau si il n'est pas en ruine, si le bateau est a lui, si le bateau est en zone d'échange, si le bateau n'est pas un voilier et si il peut payer l'évolution.'''
        bdd = j.bdd
        if j.getEnRuine():
            raise BateauError(BateauError.JOUEUR_EN_RUINE)
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

    
    @staticmethod
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

    @staticmethod
    def peut_acheter_carte_developpement(j,terre):
        ''' Un joueur j peut acheter une carte de développement sur la terre si il peut la payer'''
        if j.getEnRuine(): 
            raise DeveloppementError(DeveloppementError.JOUEUR_EN_RUINE)
        if not j.aColoniseTerre(terre):
            raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
        if not j.peut_payer(terre,Tarifs.DEVELOPPEMENT):
            raise DeveloppementError(DeveloppementError.RESSOURCES_INSUFFISANTES)
        return True
   
    @staticmethod
    @kallable
    @protection 
    def acheter_carte_developpement(j,terre):
        ''' Pioche pour le joueur j sur cette terre, une carte de développement si c'est possible, et effectue le paiement.'''
        j.payer(terre,Tarifs.DEVELOPPEMENT)
        return j.piocher_developpement(terre)

    @staticmethod
    def peut_coloniser(j,bateau,position,transfert):
        bdd = j.bdd
        if j.getEnRuine():
            raise BateauError(BateauError.JOUEUR_EN_RUINE)
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


    @staticmethod
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

    @staticmethod
    def peut_echanger(j1,j2num,terre,c1,c2):
        ''' Le joueur j1 peut echanger avec le joueur j2 sur la terre, des cartes c1 du joueur j1 vers j2 et c2 du joueur j2 vers j1 si aucun joueur n'est en ruine, si sur cette terre ils peuvent payer cette somme, si c1 et c2 sont des entiers naturels, et uniquement des ressources (pas carte de développement), '''
        j2 = Joueur(j2num,j1.bdd)
        return not j1.getEnRuine() and not j2.getEnRuine() and j1.aColoniseTerre(terre) and j2.aColoniseTerre(terre) and j1.peut_payer(terre,c1) and j2.peut_payer(terre,c2) and c1.est_ressource() and c2.est_ressource() and c1.est_physiquement_possible() and c2.est_physiquement_possible()

    @staticmethod
    @kallable
    @protection
    def echanger(j1,j2num,terre,c1,c2):
        ''' Effectue si il est possible un échange de cartes entre j1 et j2 sur cette terre, avec j1 donnant c1 cartes et j2 donnant c2 cartes.'''
        j2 = Joueur(j2num,j1.bdd)
        j1.payer(terre,c1)
        j1.recevoir(terre,c2)
        j2.payer(terre,c2)
        j2.recevoir(terre,c1)
    
    @staticmethod
    def peut_echanger_classique(j,terre,t1,t2):
        ''' Un joueur j peut effectuer un echange classique (4 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a colonisé la terre et si il peut payer 4 cartes de t1'''
        if j.getEnRuine():
            raise CommerceError(CommerceError.JOUEUR_EN_RUINE)
        if not (t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible()):
            raise CommerceError(CommerceError.FLUX_IMPOSSIBLE)
        if not j.aColoniseTerre(terre):
            raise CommerceError(CommerceError.TERRE_NON_COLONISEE)
        if not j.peut_payer(terre,t1*4):
            raise CommerceError(CommerceError.RESSOURCES_INSUFFISANTES)
        return True

    @staticmethod
    @kallable
    @protection
    def echanger_classique(j,terre,t1,t2):
        ''' Effectue s'il est possible un échange classique de cartes (4 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*4)
        j.recevoir(terre,t2)
    
    @staticmethod
    def peut_echanger_commerce_tous(j,terre,t1,t2):
        ''' Un joueur j peut effectuer un echange de commerce '?' (3 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce de type '?' et si il peut payer 3 cartes de t1'''

        if j.getEnRuine():
            raise CommerceError(CommerceError.JOUEUR_EN_RUINE)
        if not(t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible()):
            raise CommerceError(CommerceError.FLUX_IMPOSSIBLE)
        if not j.aColoniseTerre(terre):
            raise CommerceError(CommerceError.TERRE_NON_COLONISEE)
        if not j.peut_payer(terre,t1*3):
            raise CommerceError(CommerceError.RESSOURCES_INSUFFISANTES)
        if not j.contient_commerce_utilisable(terre,CommerceType.TOUS):
            raise CommerceError(CommerceError.COMMERCE_NON_UTILISABLE)
        return True
    
    @staticmethod
    @kallable
    @protection
    def echanger_commerce_tous(j,terre,t1,t2):
        ''' Effectue s'il est possible un échange commerce '?' de cartes (3 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*3)
        j.recevoir(terre,t2)
    
    @staticmethod
    def peut_echanger_commerce(j,terre,t1,t2):
        ''' Un joueur j peut effectuer un echange de commerce spécialisé (2 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce spécialisé en le type t1 et si il peut payer 2 cartes de t1'''
        if j.getEnRuine():
            raise CommerceError(CommerceError.JOUEUR_EN_RUINE)
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
    
    @staticmethod
    @kallable
    @protection
    def echanger_commerce(j,terre,t1,t2):
        ''' Effectue s'il est possible un échange de commerce spécialisé de cartes (2 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*2)
        j.recevoir(terre,t2)


    @staticmethod
    def peut_jouer_decouverte(joueur,terre,cartes):
        if joueur.getEnRuine():
            raise DeveloppementError(DeveloppementError.JOUEUR_EN_RUINE)
        if not joueur.aColoniseTerre(terre):
            raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
        if not Cartes.DECOUVERTE <= joueur.getCartes(terre):
            raise DeveloppementError(DeveloppementError.CARTE_NON_POSSEDEE)
        if not(cartes.size() == 2 and cartes.est_ressource() and cartes.est_physiquement_possible()):
            raise DeveloppementError(DeveloppementError.DECOUVERTE_FLUX_IMPOSSIBLE)
        return True

    @staticmethod
    @kallable
    @protection
    def jouer_decouverte(joueur,terre,cartes):
            joueur.recevoir(terre,cartes)
            joueur.payer(terre,Cartes.DECOUVERTE)

    @staticmethod
    def peut_jouer_monopole(joueur,terre,t1, jvols):
        if joueur.getEnRuine():
            raise DeveloppementError(DeveloppementError.JOUEUR_EN_RUINE)
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

        for j in jvols:
            j = Joueur(j,joueur.bdd)
            if j.getEnRuine():
                raise DeveloppementError(DeveloppementError.MONOPOLE_JOUEUR_EN_RUINE)
            if not j.aColoniseTerre(terre):
                raise DeveloppementError(DeveloppementError.MONOPOLE_TERRE_NON_COLONISEE)
        return True

    @staticmethod
    @kallable
    @protection
    def jouer_monopole(joueur,terre,t1,jvols):
        i = 0
        for j in jvols:
            j = Joueur(j,joueur.bdd)
            r =  j.getCartes(terre).get_cartes_de_type(t1)
            i += r
            j.payer(terre,t1*r)
        joueur.recevoir(terre,t1*i)


    @staticmethod
    def peut_jouer_construction_routes(joueur,terre,isFirstRoute,a1,isSecondRoute,a2):
        if joueur.getEnRuine():
            raise DeveloppementError(DeveloppementError.JOUEUR_EN_RUINE)
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
            b = Jeu.peut_construire_route(joueur,a1,True)
        else:
            b = Jeu.peut_construire_bateau(joueur,a1,True)
        if isSecondRoute:
            b = b and Jeu.peut_construire_route(joueur,a2,True) 
        else:
            b = b and Jeu.peut_construire_bateau(joueur,a2,True)
        return b

    @staticmethod
    @kallable
    @protection
    def jouer_construction_routes(joueur,terre,isFirstRoute,a1,isSecondRoute,a2):
        joueur.payer(terre,Cartes.CONSTRUCTION_ROUTES)
        if isFirstRoute:
            Jeu.construire_route(joueur,a1,True)
        else:
            Jeu.construire_bateau(joueur,a1,True)
        if isSecondRoute:
            Jeu.construire_route(joueur,a2,True)
        else:
            Jeu.construire_bateau(joueur,a2,True)

    @staticmethod
    def peut_defausser(joueur,terre,cartes):
        bdd = joueur.bdd
        if not joueur.getEnRuine() and 7 in Des.getDices() and joueur.aColoniseTerre(terre):
            c = joueur.getCartes(terre)
            rs = c.ressources_size()


            bs = []
            for bn in joueur.getBateaux():
                b = Bateau.getBateau(int(bn),bdd)
                if b.est_proche(terre):
                    bs.append(b.num)
                    rs += b.cargaison.ressources_size()
            if rs <= 7:
                return cartes == (Cartes.RIEN,[])
            
            res = cartes[0]
            cargs = cartes[1]

            ds = rs/2 + rs%2 # ressource arrondi au superieur
            rs2 = rs - ds

            while rs2 > 7:
                ds += rs2/2 + rs2%2 # ressource arrondi au superieur
                rs2 = rs - ds
            if res <= c and res.est_ressource() and res.est_physiquement_possible():
                ss = res.ressources_size()
                for cb in cargs:
                    if cb[0].num in bs and cb[1] <= cb[0].cargaison and cb[1].est_physiquement_possible() and cb[1].est_ressource():
                        ss += cb[1].ressources_size()
                    else:
                        return False
                return ss == ds
        return False

    @staticmethod
    @kallable
    @protection
    def defausser(joueur,terre,cartes):
        joueur.payer(terre,cartes[0])
        bdd = joueur.bdd
        for cb in cartes[1]:
            cb[0].remove(cb[1])
            cb[0].save(bdd)

    
    @staticmethod
    def positions_possibles_voleur(joueur,terre,voleur):
        bdd = joueur.bdd
        if voleur == 0:
            return []
        b = voleur.etat == Voleur.VoleurType.PIRATE
        if not b:
            hexs = terre.hexagones[:]
        else:
            hexs = terre.espaceMarin[:]
        if voleur.position != 0:
            hexs.remove(voleur.position)
        possibilite = []
        if b:
            for h in hexs:
                if h.commerceType!= 0:
                    for i in h.ints:
                        col = Colonie.getColonie(i,bdd)
                        if (col != 0) and (col.joueur != joueur.num):
                            possibilite.append((h,col.joueur))
                for a in h.liens:
                    for bat in Bateau.getBateaux(a,bdd):
                        if (bat != 0) and (bat.joueur != joueur.num):
                            possibilite.append((h,bat.joueur))
            if possibilite == []:
                return [(0,0)]
        else:
            for h in hexs:
                for i in h.ints:
                    col = Colonie.getColonie(i,bdd)
                    if (col != 0) and (col.joueur != joueur.num):
                            possibilite.append((h,col.joueur))
            if possibilite == []:
                for h in voleur.position.terre.hexagones:
                    if h.etat == HexaType.DESERT and h.commerceType == 0:
                        possibilite.append((h,0))
        return possibilite 



    @staticmethod
    def peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,chevallier = False):
        bdd = joueur.bdd
        if not joueur.getEnRuine() and (joueur.get_deplacement_voleur(terre) or chevallier) and (hex == 0 or hex.terre == terre):
            if voleurType == Voleur.VoleurType.BRIGAND:
                voleur = Voleur.getBrigand(terre,bdd)
            else:
                voleur = Voleur.getPirate(terre,bdd)
            if jvol == 0:
                t = (hex, 0)
            else:
                t = (hex, jvol)
            return joueur.aColoniseTerre(terre) and t in Jeu.positions_possibles_voleur(joueur,terre,voleur)
        return False

    @staticmethod
    def voler(j1,terre,j2num):
        bdd = j1.bdd
        j2 = Joueur(j2num,bdd)
        ressources_terrestres = j2.getCartes(terre)
        nc = ressources_terrestres.ressources_size()
        ressources_bateaux = []
        s = nc
        for bn in j2.getBateaux():
            b = Bateau.getBateau(int(bn),bdd)
            if b.en_position_echange(bdd) and b.position.getTerre() == terre:
                n = b.cargaison.size()
                ressources_bateaux.append((n,b))
                s+=n
        if s == 0:
            return
        u = random.randint(1,s)
        if u <= nc:
            c = ressources_terrestres.carte(u)
            j2.payer(terre,c)
            j1.recevoir(terre,c)
        else:
            u-=nc
            for rb in ressources_bateaux:
                if u <= rb[0]:
                    c = rb[1].cargaison.carte(u)
                    rb[1].remove(c)
                    rb[1].save(bdd)
                    j1.recevoir(terre,c)
                    return
                else:
                    u -= rb[0]

    @staticmethod
    @kallable
    def deplacer_voleur(joueur,terre,voleurType,hex,jvol, chevallier = False):
        bdd = joueur.bdd
        if Jeu.peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,chevallier):
            if voleurType == Voleur.VoleurType.BRIGAND:
                voleur = Voleur.getBrigand(terre,bdd)
            else:
                voleur = Voleur.getPirate(terre,bdd)
            voleur.deplacer(hex)
            voleur.save(bdd)
            Jeu.voler(joueur,terre,jvol)
            if not chevallier:
                joueur.set_deplacement_voleur(terre,False)
            return True
        else:
            return False
                
    @staticmethod
    def peut_jouer_chevallier(joueur,terre,voleurType, hex,jvol):
        if joueur.getEnRuine():
            raise DeveloppementError(DeveloppementError.JOUEUR_EN_RUINE)
        if not joueur.aColoniseTerre(terre):
            raise DeveloppementError(DeveloppementError.TERRE_NON_COLONISEE)
        if not Cartes.CHEVALLIER <= joueur.getCartes(terre):
            raise DeveloppementError(DeveloppementError.CARTE_NON_POSSEDEE)
        return Jeu.peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,True)

    @staticmethod
    @kallable
    @protection
    def jouer_chevallier(joueur,terre,voleurType, hex,jvol):
            joueur.add_chevallier(terre)
            joueur.payer(terre,Cartes.CHEVALLIER)
            Jeu.challenge_armee_la_plus_grande(joueur,terre)
            Jeu.deplacer_voleur(joueur,terre,voleurType,hex,jvol,True)


if __name__ == '__main__':
    j = Joueur("1")
