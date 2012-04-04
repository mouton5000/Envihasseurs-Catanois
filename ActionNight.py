# -*- coding: utf8 -*-

__all__ = ['Des']

import redis
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

