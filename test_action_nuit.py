# *-* coding: utf8 *-*
import unittest
from arbre_action import *
from ActionNight import *
import ActionNight
from test_joueurs import *
import redis

REDIS = redis.StrictRedis()

class TestActionNuit(TestJoueur):

    def setUp(self):
        super(TestActionNuit,self).setUp()
        self.j1 = Joueur(1)
        self.j2 = Joueur(2)
        self.j3 = Joueur(3)
        self.j4 = Joueur(4)
        self.j5 = Joueur(5)
        self.j6 = Joueur(6)
        self.j7 = Joueur(7)
        self.j8 = Joueur(8)
        self.j9 = Joueur(9)

        joueurs = [self.j1, self.j2, self.j3, self.j4, self.j5, self.j6, self.j7, self.j8, self.j9]

        JoueurPossible.setNbJoueurs(9)
        p = Plateau.getPlateau()
        self.tg = p.ter(1)
        self.td = p.ter(2)
        jnums = []

        for j in joueurs:
            jp = JoueurPossible(j.num)
            jp.addTerre(self.tg)
            jp.set_route_la_plus_longue(self.tg,0)
            j.setNewRoot()
            jnums.append(j.num)

        ActionNight.setJoueursParPriorite(jnums)
        

    def test_defausse_nuit(self):
        Des.save([7,6,5,1])
        j1p = JoueurPossible(self.j1)
        j2p = JoueurPossible(self.j2)
        j3p = JoueurPossible(self.j3)

        tg = self.tg
        td = self.td


        j1p.setCartes(tg, CartesRessources(3,2,1,2,0))
        j2p.setCartes(tg, CartesRessources(3,2,1,2,0))
        j3p.setCartes(tg, CartesRessources(0,2,1,2,0))
        DeplacementVoleur.designer_deplaceur_de_voleur()

        self.j1.defausser(tg, [CartesRessources(1,1,1,1,0),[]]) 

        ActionNight.action_nuit()


