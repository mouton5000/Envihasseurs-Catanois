# -*- coding: utf8 -*-

import random
import redis

REDIS = redis.StrictRedis()

class User:
  
    def __init__(self, jnum, username, hpw):
        self.jnum = jnum
        self.username = username
        self.hpw = hpw

    def save(self):
        key = 'Us:'+self.username
        REDIS.set(key, self.jnum)
        REDIS.set(key+':hpw', self.hpw)
        REDIS.set('J'+str(self.jnum)+':username',self.username)

    @staticmethod
    def getUser(username):
        key = 'Us:'+username
        if REDIS.exists(key):
            jnum = int(REDIS.get(key))
            hpw = REDIS.get(key+':hpw')
            return User(jnum, username, hpw)
        return 0
    
    @staticmethod
    def getUsersAndColors():
        ''' Renvoie les utilisateurs associés à leur couleur de tous les joueurs sous forme d'un tableau [username,jnum,color] où chaque couleur est un triplet (r,b,g). Attention les éélments des triplets sont des chaines de caractères, pas des chiffres'''
        import joueurs
        nb = joueurs.JoueurPossible.getNbJoueurs()
        pipe = REDIS.pipeline()
        for i in xrange(nb):
            key = 'J'+str(i+1)
            pipe.get(key+':username')
            pipe.get(key+':red')
            pipe.get(key+':blue')
            pipe.get(key+':green')
        res = pipe.execute()

        users = []
        for i in xrange(nb):
            username = res[i*4]
            color = []
            color.append(res[i*4+1])
            color.append(res[i*4+2])
            color.append(res[i*4+3])
            users.append([username,i+1,color])
        return users


    def setColor(self,red,blue,green):
        from arbre_action import Joueur
        Joueur(self.jnum).setColor(red,blue,green)

    def getColor(self):
        from arbre_action import Joueur
        j = Joueur(self.jnum)
        return [j.getRed(),j.getBlue(),j.getGreen()]
