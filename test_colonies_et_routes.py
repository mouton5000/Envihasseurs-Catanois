# -*- coding: utf8 -*-
from plateau import *
from test_joueurs import *
from redis import *

REDIS = redis.StrictRedis()


class TestColonieEtRoute(TestJoueur):
   
    def setUp(self):
        super(TestColonieEtRoute,self).setUp()
        self.j1 = Joueur(1)
        self.j2 = Joueur(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)
        REDIS.flushdb()

    def test_construire_colonie(self):
        p = Plateau.getPlateau()

        j1 = self.j1
        j2 = self.j2

        i72 = p.it(72) 
        i73 = p.it(73)
        i83 = p.it(83)
        i51 = p.it(51)
        i54 = p.it(54)
        a72 = i72.lien(i73)
        a73 = i73.lien(i83)

        c1 = Colonie(1,i72)
        r1 = Route(1,a72)
        r2 = Route(1,a73)

        c1.save()
        r1.save()
        r2.save()

        j1.setCartes(self.tg,Tarifs.COLONIE)
        self.assertTrue(Jeu.peut_construire_colonie(j1,i83)) # Ok
        self.assertFalse(Jeu.peut_construire_colonie(j1,i72))# Il y a deja une colonie
        self.assertFalse(Jeu.peut_construire_colonie(j1,i73))# Il y a une colonie a 1 case
        self.assertFalse(Jeu.peut_construire_colonie(j1,i54))# Il n'y a aucun lien
        self.assertFalse(Jeu.peut_construire_colonie(j1,i51))# C'est la mer
        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_colonie(j1,i83)) # Plus assez de ressources
        
        i53 = p.it(53) 
        i43 = p.it(43) 
        i44 = p.it(44) 
        a53 = i53.lien(i43)
        a43 = i43.lien(i44)
        j1.setCartes(self.tg,Tarifs.COLONIE)
        c2 = Colonie(2,i53)
        r3 = Route(2,a53)
        r4 = Route(2,a43)

        c2.save()
        r3.save()
        r4.save()
        self.assertFalse(Jeu.peut_construire_colonie(j1,i53)) # Colonie adverse
        self.assertFalse(Jeu.peut_construire_colonie(j1,i43)) # Colonie adverse a une case
        self.assertFalse(Jeu.peut_construire_colonie(j1,i44)) # Relie a une route mais adverse

        i63 = p.it(63)
        a63 = i63.lien(i53)
        a73 = i63.lien(i73)
        r5 = Route(2,a63)
        r6 = Route(1,a73)
        r5.save()
        r6.save()
        self.assertFalse(Jeu.peut_construire_colonie(j1,i63)) # Relie a une route mais colonie adverse a une case
       
        i = len(j1.getBatiments())
        Jeu.construire_colonie(j1,i83)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
        self.assertEqual(len(j1.getBatiments()),i+1)
       
    def test_route(self): 

        j1 = self.j1
        j2 = self.j2

        p = Plateau.getPlateau()
        i43 = p.it(43)
        i33 = p.it(33)
        i53 = p.it(53)
        i63 = p.it(63)
        i62 = p.it(62)
        i52 = p.it(52)
        i61 = p.it(61)
        i103 = p.it(103)
        i104 = p.it(104)
        i44 = p.it(44)
        i34 = p.it(34)
        i54 = p.it(54)
        i64 = p.it(64)

        a4333 = i43.lien(i33)
        a5363 = i53.lien(i63)
        a5343 = i53.lien(i43)
        a103104 = i103.lien(i104)
        a4434 = i44.lien(i34)
        a5464 = i54.lien(i64)
        a4454 = i44.lien(i54)
        a4344 = i43.lien(i44)


        Colonie(1,i53).save()
        Route(1,a5343).save()
        Colonie(2,i44).save()
        Route(2,a4454).save()

        j1.setCartes(self.tg,Tarifs.ROUTE)

        self.assertTrue(Jeu.peut_construire_route(j1,a4333))  # ok relie a une route
        self.assertTrue(Jeu.peut_construire_route(j1,a5363))  # ok relie a une colonie
        self.assertFalse(Jeu.peut_construire_route(j1,a5343)) # existe deja
        self.assertFalse(Jeu.peut_construire_route(j1,a103104)) # relie a rien
        self.assertFalse(Jeu.peut_construire_route(j1,a4434)) # relie seulement a l'ennemi
        self.assertFalse(Jeu.peut_construire_route(j1,a5464)) # relie seulement a l'ennemi
        self.assertTrue(Jeu.peut_construire_route(j1,a4344))  # ok relie a une route


        a6261 = i62.lien(i61)
        a6252 = i62.lien(i52)
        Colonie(1,i62).save()
        
        self.assertFalse(Jeu.peut_construire_route(j1,a6261)) # c'est la mer
        self.assertTrue(Jeu.peut_construire_route(j1,a6252)) # cotier

        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_route(j1,a4333)) # manque de ressource
        j1.setCartes(self.tg,Tarifs.ROUTE)


        i = len(j1.getRoutes())
        Jeu.construire_route(j1,a4333)
        self.assertEqual(len(j1.getRoutes()),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
