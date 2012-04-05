

from cartes import *


class Echange:

    def __init__(self,j1,j2,terre,don,recu, accepted = False):
        self.num = REDIS.incr("LastEchange")
        self.j1 = j1
        self.j2 = j2
        self.terre = terre
        self.don = don
        self.recu = recu
        self.accepted = accepted

    def isAccepted():
        self.accepted = accepted

    def save(self):
        key = "E"+str(self.num)
        REDIS.set(key + ':joueurProposant', self.j1.num)
        REDIS.set(key + ':joueurAcceptant', self.j2.num)
        REDIS.set(key + ':terre', self.terre.num)
        self.don.setTo(key + ':don')
        self.recu.setTo(key + ':recu')
        REDIS.set(key + ':accepte', self.accepted)

    @staticmethod
    def getEchange(num):
        key = "E"+str(num)
        j1N = int(REDIS.get(key + ':joueurProposant'))
        j2N = int(REDIS.get(key + ':joueurAcceptant'))
        terreN = int(REDIS.get(key + ':terre'))
        accepted = REDIS.get(key + ':accepte') == 'True'

        don = CartesGeneral.get(key+':don')
        recu = CartesGeneral.get(key+':recu')

        j1 = Joueur(j1N)
        j2 = Joueur(j2N)
        terre = Plateau.getPlateau().ter(terreN)

        return Echange(num,j1,j2,terre,don,recui, accepted)

class DeplacementVoleur:
    pass

