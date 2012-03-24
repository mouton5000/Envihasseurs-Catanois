# *-* coding: iso-8859-1 *-*

import operator
import random
import redis

REDIS = redis.StrictRedis()

class CartesGeneral:
    ''' Cette classe représente les cartes que les joueurs ont en main. Aussi bien les cartes de ressources que les cartes de développement. Elles sont représentées ensembles de la même façon pour la simple raison qu'elles sont manipulées de la même façon. Il s'agit d'un upplet d'entiers, chaque coordonnée correspond à un type de carte.'''
    attributs = ['argile', 'ble', 'bois', 'caillou', 'mouton', 'chevalliers',
                 'monopoles', 'pointsVictoire', 'decouverte',
                 'constructionDeRoute']

    def __init__(self, argile, ble, bois, caillou, mouton, chevalliers,
        monopoles, pointsVictoire, decouverte, constructionDeRoute):
        ''' Construit l'upplet de carte manuellement.'''
        self.argile = argile
        self.ble = ble
        self.bois = bois
        self.caillou = caillou
        self.mouton = mouton
        self.chevalliers = chevalliers
        self.monopoles = monopoles
        self.pointsVictoire = pointsVictoire
        self.decouverte = decouverte
        self.constructionDeRoute = constructionDeRoute

    def _comparison(self, other, operation):
        ''' Renvoie vrai si l'opération appliquée à tout attribut de self et other renvoie vrai.'''
        return all(operation(getattr(self, att), getattr(other, att))
            for att in CartesGeneral.attributs)

    def __eq__(self,other):
        ''' Renvoie vrai si les deux mains sont identiques'''
        return self._comparison(other, operator.eq)

    def __add__(self,other):
        ''' Renvoie la fusion des deux mains'''
        args = [getattr(self, att) + getattr(other, att)
                for att in CartesGeneral.attributs]
        return CartesGeneral(*args)

    def __mul__(self,other):
        ''' Multiplie chaque carte de la main par un nombre other'''
        args = [getattr(self, att) * other
                for att in CartesGeneral.attributs]
        return CartesGeneral(*args)

    def __sub__(self,other):
        ''' Renvoie la différence de la première main par la deuxième main'''
        return self + other*(-1)

    def size(self):
        ''' Renvoie le nombre de cartes en main'''
        return sum(getattr(self, att) for att in CartesGeneral.attributs)

    def ressources_size(self):
        ''' Renvoie le nombre de ressources en main'''
        return self.argile + self.ble + self.bois + self.caillou + self.mouton

    def __lt__(self,other):
        ''' Renvoie vrai si la main de other a strictement plus de carte de chaque type que self'''
        return self._comparison(other, operator.lt)

    def __gt__(self,other):
        ''' Renvoie vrai si la main de other a strictement moins de carte de chaque type que self. Ce n'est donc pas l'opération inverse de le'''
        return self._comparison(other, operator.gt)

    def __le__(self,other):
        ''' Renvoie vrai si la main de other a plus de carte de chaque type que self'''
        return self._comparison(other, operator.le)

    def __ge__(self,other):
        ''' Renvoie vrai si la main de other a moins de carte de chaque type que self. Ce n'est donc pas l'opération inverse de lt'''
        return self._comparison(other, operator.ge)

    def __str__(self):
        return '(' +  ', '.join(str(getattr(self, att)) for att in CartesGeneral.attributs) + ')'

    def est_ressource(self):
        ''' Renvoie vrai si la main ne contient que des ressources'''
        return (self.chevalliers == 0 and self.pointsVictoire == 0
                and self.decouverte == 0 and self.constructionDeRoute == 0
                and self.monopoles == 0)

    def est_entier(self):
        ''' Renvoie vrai si la main ne contient que des nombres entiers'''
        return all(isinstance(getattr(self, att), int)
            for att in CartesGeneral.attributs)

    def est_physiquement_possible(self):
        ''' Renvoie vrai si la main ne contient que des entiers positifs'''
        return self >= Cartes.RIEN and self.est_entier()

    def carte(self,nb):
        ''' Renvoie la cartes numéro nb de la main, si elles sont classées dans l'ordre des attributs.'''
        if 0 >= nb > self.ressources_size():
            return 0

        if nb <= self.argile:
            return Cartes.ARGILE
        else:
            nb -= self.argile

        if nb <= self.ble:
            return Cartes.BLE
        else:
            nb -= self.ble

        if nb <= self.bois:
            return Cartes.BOIS
        else:
            nb -= self.bois

        if nb <= self.caillou:
            return Cartes.CAILLOU
        else:
            nb -= self.caillou

        if nb <= self.mouton:
            return Cartes.MOUTON
        else:
            nb -= self.mouton
        return 0

        
    def get_cartes_de_type(self,carte):
        ''' Renvoie le nombre de carte en main du type désigné.'''
        if carte == Cartes.ARGILE:
            i = self.argile
        elif carte == Cartes.BLE:
            i = self.ble
        elif carte == Cartes.BOIS:
            i = self.bois
        elif carte == Cartes.CAILLOU:
            i = self.caillou
        elif carte == Cartes.MOUTON:
            i = self.mouton
        elif carte == Cartes.CHEVALLIER:
            i = self.chevalliers
        elif carte == Cartes.MONOPOLE:
            i = self.monopoles
        elif carte == Cartes.DECOUVERTE:
            i = self.decouverte
        elif carte == Cartes.CONSTRUCTION_ROUTES:
            i = self.constructionDeRoute
        elif carte == Cartes.POINT_VICTOIRE:
            i = self.pointsVictoire
        else:
            return 0
        return i


    def setTo(self,key, bdd = REDIS):
        for att in CartesGeneral.attributs:
            bdd.set(key+':'+att,getattr(self,att))
        bdd.set(key+':exists',0)

    @staticmethod
    def get(key, bdd = REDIS):
        if bdd.exists(key+':exists'):
            values = [bdd.get(key+':'+att) for att in CartesGeneral.attributs]
            valuesInt = []
            for value in values:
                valuesInt.append(int(value))
            return CartesGeneral(*valuesInt)
        return Cartes.RIEN


class CartesRessources(CartesGeneral):
    ''' Permet une petite facilité quand on ne travaille qu'avec des ressources'''
    def __init__(self,argile,ble,bois,caillou,mouton):
        CartesGeneral.__init__(self,argile,ble,bois,caillou,mouton,0,0,0,0,0)

    def __str__(self):
        return '(' + str(self.argile) +','+ str(self.ble) + ',' + str(self.bois) + ',' + str(self.caillou) + ',' + str(self.mouton) + ')'

    @staticmethod
    def get_random_ressource():
        ''' Renvoie une ressource aléatoire parmi les 5 qui existe'''
        i = random.Random().randint(1,5)
        if (i == 1):
            carte = Cartes.ARGILE
        elif i == 2:
            carte = Cartes.BLE
        elif i == 3:
            carte = Cartes.BOIS
        elif i == 4:
            carte = Cartes.CAILLOU
        elif i == 5:
            carte = Cartes.MOUTON
        return carte
        

class CartesDeveloppement(CartesGeneral):
    ''' Permet une petite facilité quand on ne travaille qu'avec des certes de développement'''

    def __init__(self,chevalliers, monopoles, pointsVictoire, decouverte, constructionDeRoute):
        CartesGeneral.__init__(self,0,0,0,0,0,chevalliers, monopoles, pointsVictoire, decouverte, constructionDeRoute)

    def __str__(self):
        return '(' + str(self.chevalliers) +','+ str(self.monopoles) + ',' + str(self.pointsVictoire) + ',' + str(self.decouverte) + ',' + str(self.constructionDeRoute) + ')'

class Cartes:
    ''' Vecteurs unitaires'''
    RIEN = CartesGeneral(0,0,0,0,0,0,0,0,0,0)
    ARGILE = CartesRessources(1,0,0,0,0)
    BLE = CartesRessources(0,1,0,0,0)
    BOIS = CartesRessources(0,0,1,0,0)
    CAILLOU = CartesRessources(0,0,0,1,0)
    MOUTON = CartesRessources(0,0,0,0,1)
    CHEVALLIER = CartesDeveloppement(1,0,0,0,0)
    MONOPOLE = CartesDeveloppement(0,1,0,0,0)
    POINT_VICTOIRE = CartesDeveloppement(0,0,1,0,0)
    DECOUVERTE = CartesDeveloppement(0,0,0,1,0)
    CONSTRUCTION_ROUTES = CartesDeveloppement(0,0,0,0,1)
