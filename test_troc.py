# -*- coding: utf8 -*-
from plateau import *
from test_joueurs import *
from redis import *

REDIS = redis.StrictRedis()


class TestTroc(TestJoueur):
   
    def setUp(self):
        super(TestTroc,self).setUp()
        self.j1 = Joueur(1)
        self.j2 = Joueur(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

    def test_acheter_ressource(self):
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j1.setCartes(tg,Cartes.RIEN)
        j1.setOr(tg,0)
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE)) # On ne peut acheter sans or
        j1.setOr(tg,1)
        self.assertTrue(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))
        j1.setOr(tg,2)
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(1,1,0,0,0))) # On ne peut acheter plus d'une carte à la fois
        j1.setOr(tg,1)
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(-1,2,0,0,0))) # On ne peut acheter négativement
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(0.5,0.5,0,0,0))) # On ne peut acheter qu'entièrement

        Jeu.acheter_ressource(j1,tg, Cartes.BLE)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))
        
        j1.setOr(td,1) #(en cas de bug)
        self.assertFalse(Jeu.peut_acheter_ressource(j1,td,Cartes.BLE)) # On ne peut acheter sur une terre non colonisée
