# -*- coding: utf8 -*-


__all__ = ['JoueurPossible', 'Tarifs', 'Des']

from pions import *
from plateau import *
from cartes import *
import random
import redis
import Jeu
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

class JoueurPossible:
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



if __name__ == '__main__':
    j = Joueur("1")
