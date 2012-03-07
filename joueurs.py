# *-* coding: iso-8859-1 *-*
from constructions import *
from plateau import *
from cartes import *
from foret_action import *
import random
import functools
import redis

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

class Joueur:
    ''' Classe représentant un joueur, avec ses pions (construction, bateau), permettant de récupérer les informations relatives à ce joueur, voire d'en modifier.'''
    def __init__(self,num):
        self.num = num
        self.deplacement_voleur = []
        self.routes_les_plus_longues = []
        self.enRuine = False

    def setCartes(self,terre,cartes):
        ''' Associe à la main du joueur sur cette terre les cartes données en paramètre'''
        cartes.setTo('I'+str(self.num)+':T'+str(terre.num))

    def getCartes(self,terre):
        ''' Renvoie la main du joueur sur cette terre'''
        return CartesGeneral.get('I'+str(self.num)+':T'+str(terre.num))
    
    def payer(self,terre, cartes):
        ''' Déduis de la main du joueur sur cette terre les cartes données en paramètre'''
        self.setCartes(terre,self.getCartes(terre) - cartes)

    def recevoir(self,terre,cartes):
        ''' Ajoute à la main du joeuur sur cette terre les cartes données en paramètre'''
        self.payer(terre,cartes*(-1))

    def peut_payer(self,terre,cartes):
        ''' Vérifie si la main du joeuur sur cette terre peut payer la quantité donnée en paramètre'''
        return cartes <= self.getCartes(terre)
    
    def ressource_aleatoire(self,terre):
        ''' Ajoute à la main du joueur sur cette terre une carte de ressource aléatoire'''
        carte = CartesRessources.get_random_ressource()
        self.setCartes(terre,self.getCartes(terre) + carte)

    def getOr(self,terre):
        ''' Renvoie la quantité d'or du joueur présente sur cette terre'''
        return int(REDIS.get(self.num+':'+terre+':or'))

    def setOr(self,terre, nb):
        ''' Définit la quantité d'or du joueur présente sur cette terre'''
        REDIS.set(self.num+':'+terre+':or', nb)

    def addOr(self,terre,nb):
        ''' Ajoute au stock d'or du joeuur sur cette terre nb lingots d'or'''
        self.setOr(terre, self.getOr(terre) + nb)

    def payerOr(self,terre):
        ''' Déduis du stock d'or du joueur sur cette terre un lingot d'or'''
        self.addOr(terre,-1)
    
    def addTerre(self,terre):
        ''' Ajoute une terre aux terres colonisées du joueur'''
        REDIS.sadd(self.num+':terres',terre)
        self.setCartes(terre,Cartes.RIEN)
        self.setOr(terre,0)



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
            carte = Cartes.CONSTRUCTION_ROUTE
        self.recevoir(terre,carte)
        return carte

    def contient_commerce_utilisable(self,terre,comType):
        ''' Vérifie si le joueur contient sur cette terre un commerce de type comType'''
        for c in self.getBatiments():
            c = int(c)
            intersection = Plateau.getPlateau.it(c)
            ms = intersection.marcheNonBrigande()
            ps = intersection.portNonPirate()
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
            terre = Plateau.getPlateau().it(c).getTerre()
            res = Colonie.getColonie(c).ressources_from_past(des)
            if (res != 0):
                self.addOr(terre,res[1])
                self.recevoir(terre,res[0]) 

    def getBateauxTransport(self):
        return REDIS.smembers('J'+str(self.num)+':transports')

    def getCargos(self):
        return REDIS.smembers('J'+str(self.num)+':cargos')
    
    def getVoiliers(self):
        return REDIS.smembers('J'+str(self.num)+':voiliers')
    
    def getBateaux(self):
        ''' Renvoie les bateaux du joueur, tout type confondu'''
        return self.getBateauxTransport() + self.getCargos() + self.getVoiliers()
    
    def getBateauxTransportPositions(self):
        return REDIS.smembers('J'+str(self.num)+':transports:positions')

    def getCargosPositions(self):
        return REDIS.smembers('J'+str(self.num)+':cargos:positions')
    
    def getVoiliersPositions(self):
        return REDIS.smembers('J'+str(self.num)+':voiliers:positions')
    
    def getBateauxPositions(self):
        ''' Renvoie les bateaux du joueur, tout type confondu'''
        return self.getBateauxTransportPositions() + self.getCargosPositions() + self.getVoiliersPositions()

    def getColonies(self):
        ''' Renvoie tous les intersection où se trouvent les colonies du joueur'''
        return REDIS.smembers('J'+str(self.num)+':colonies')

    def getVilles(self):
        ''' Renvoie tous les intersection où se trouvent les villes du joueur'''
        return REDIS.smembers('J'+str(self.num)+':villes')
    
    def getRoutes(self):
        ''' Renvoie tous les arretes où se trouvent les routes du joueur'''
        return REDIS.smembers('J'+str(self.num)+':routes')

    def getBatiments(self):
        ''' Renvoie toutes les intersection où se trouvent les batiments du joueur, tout type confondu'''
        return self.getColonies().union(self.getVilles())
                
    def add_chevallier(self,terre):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        REDIS.incr('J'+str(self.num)+':T'+str(terre.num)+':chevalliers')
 
    def get_chevalliers(self,terre):
        ''' Renvoie l'armée du joueur sur cette terre'''
        REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':chevalliers')
    
    def get_carte_armee_la_plus_grande(self,terre):
        ''' Renvoie vrai si le joueur a l'armée la plus grande sur cette terre'''
        u = Jeu.get_armee_la_plus_grande(terre)
        return u!=0 and u[0] == self
 
    def get_deplacement_voleur(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.deplacement_voleur[i]
        else:
            return 0

    def set_deplacement_voleur(self,terre,dep):
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.deplacement_voleur[i] = dep


    def get_route_la_plus_longue(self,terre):
        ''' Renvoie la taille de la route la plus longue du joueur sur cette terre'''
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.routes_les_plus_longues[i]
        
    def set_route_la_plus_longue(self,terre, l):
        ''' Définie la route la plus longue sur cette terre comme étant de taille l'''
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.routes_les_plus_longues[i] = l

    def route_la_plus_longue(self,terre, recalculer=False):
        ''' Calcule si elle est non calculée ou si recalculer est vrai, la route la plus longue de ce joueur sur cette terre. Si elle est déjà calculée alors renvoie juste la valeur déjà calculée '''
        if self.enRuine:
            return 0
        if terre in self.terres:
            if recalculer:
                i = 0
                for r in self.routes:
                    if r.position.getTerre() == terre and r.est_extremite():
                        i = max(i, r.rlplfr())
                self.set_route_la_plus_longue(terre,i)
                return i
            else:
                return self.get_route_la_plus_longue(terre)
        else:
            return 0
                       
    def get_carte_route_la_plus_longue(self,terre):
        ''' Vérifie si ce joueur a la carte de la route al plus longue sur cette terre'''
        u = Jeu.get_route_la_plus_longue(terre)
        return u!=0 and u[0]== self

    def addStaticPoint(self,terre,nb):
        ''' Ajoute nb points aux points statiques (ie batiments) de cette terre'''
        REDIS.incr('J'+str(self.num)+':T'+str(terre.num)+':points',nb)

    def getStaticPoints(self,terre):
        REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':points')

    def getPoints(self,terre):
        ''' Calcule le nombre de points de ce joueur sur cette terre'''
        if self.enRuine:
            return 0
        i = self.getTerreIndex(terre)
        p = 0
        if (self.get_carte_route_la_plus_longue(terre)):
            p += 2
        if (self.get_carte_armee_la_plus_grande(terre)):
            p += 2
        if i!=-1:
            return self.points[i] + self.getCartes(terre).get_cartes_de_type(Cartes.POINT_VICTOIRE) + p

    def addRoot(self):
        return ForetAction.setNewRoot(self) 
    
    def addFirstRoot(self):
        return ForetAction.setNewFirstRoot(self) 

    def addNextRoot(self,root):
        return ForetAction.setNewNextRoot(root,self) 

class Jeu:

# -----------------------------------------------------
#    Actions dans la journee
# -----------------------------------------------------

    @staticmethod
    def peut_construire_colonie(j,intersection):
        ''' Un joueur peut construire une colonie si il n'est aps en ruine, si il ne la construit pas a un emplacement voisin d'une autre colonie, si il la construit sur un emplacement voisin d'une de ses routes, si cet emplacement est sur terre et si il peut payer la construiction.'''
        col = intersection.hasColonie()
        if not j.enRuine and not col and not intersection.isMaritime() and j.peut_payer(intersection.getTerre(), Tarifs.COLONIE):
    
            for i in intersection.neigh:
                if i.hasColonie():
                    return False
            for i in intersection.neigh:
                a = i.lien(intersection)
                jrout = a.getRouteJoueur()
                if jrout == j.num:
                    return True
        return False

    @staticmethod
    @protection
    def construire_colonie(j, intersection):
        ''' Pose une nouvelle colonie du joueur j sur l'intersection si il en a la possibilité, et effectue le paiement.'''
        c = Colonie(j.num, intersection)
        terre = intersection.getTerre()
        j.payer(terre, Tarifs.COLONIE)
        j.addStaticPoint(terre,1)

        c.save()

    @staticmethod
    def peut_construire_route(j, arrete, construction_route = False):
        ''' Un joueur j peut construire une route sur l'arrete si il n'est pas en ruine, si il n'existe pas déjà de route non en ruine sur cet emplacement, si cette arrete est terrestre, si il peut payer ou s'il a jouer une carte développement de construction de route, et s'il existe une colonie ou une route voiine à cette arrete.'''
        rout = arrete.hasRoute()
        print arrete,'<----'
        if not j.enRuine and not rout and not arrete.isMaritime() and (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.ROUTE)):
            jcol1 = arrete.int1.getColonieJoueur()
            jcol2 = arrete.int2.getColonieJoueur()
            if (jcol1 == j.num) or (jcol2 == j.num):
                return True
            for a in arrete.neighb():
                jrout = a.getRouteJoueur()
                if (jrout == j.num):
                    return True
        return False

    @staticmethod
    def construire_route(j,arrete, construction_route = False):
        ''' Pose, si c'est possible, une route du joueur j sur l'arrete et effectue le paiement.'''
        if construction_route or Jeu.peut_construire_route(j,arrete):
            r = Route(j.num,arrete)
            terre = arrete.getTerre()
            if not construction_route:
                j.payer(terre,Tarifs.ROUTE)
            r.save()
            return True
        else:
            return False

if __name__ == '__main__':
    j = Joueur("1")
