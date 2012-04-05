# -*- coding: utf8 -*-

__all__ = ['Des', 'Monopole']

import redis
from cartes import *
from joueurs import *
from plateau import *
REDIS = redis.StrictRedis()


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

class Monopole:
    def __init__(self,num,j,jvols,terre,carte):
        if num == 0:
            self.num = REDIS.incr("LastMonopole")
        else:
            self.num = num
        self.j = j
        self.jvols = jvols
        self.terre = terre
        self.carte = carte

    def save(self, bdd):
        key = "M"+str(self.num)
        bdd.set(key + ':joueur', self.j.num)
        for j in self.jvols:
            bdd.sadd(key + ':joueurVoles', j)
        bdd.set(key + ':terre', self.terre.num)
        self.carte.setTo(key + ':carte')

    @staticmethod
    def getMonopole(num):
        key = "M"+str(num)
        j1N = int(REDIS.get(key + ':joueur'))
        jvols = []
        for j in REDIS.smembers(key + ':joueurVoles'):
            jvols.append(int(j))
        terreN = int(REDIS.get(key + ':terre'))
        accepted = REDIS.get(key + ':accepte') == 'True'

        carte = CartesGeneral.get(key+':carte')

        j1 = JoueurPossible(j1N)
        terre = Plateau.getPlateau().ter(terreN)

        return Monopole(num,j1,jvols,terre,carte)

# Execution Monopole

    def executer(self):
        i = 0
        for j in self.jvols:
            j = JoueurPossible(j)
            r =  j.getCartes(self.terre).get_cartes_de_type(self.carte)
            i += r
            j.payer(self.terre,self.carte*r)
        self.j.recevoir(self.terre,self.carte*i)

