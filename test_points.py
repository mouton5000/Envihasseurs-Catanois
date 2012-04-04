# -*- coding: utf8 -*-
from test_joueurs import *

REDIS = redis.StrictRedis()


class TestPoints(TestJoueur):
   
    def setUp(self):
        super(TestPoints,self).setUp()
        self.j1 = Joueur(1)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

    def test_points(self):
        j1 = self.j1
        p = Plateau.getPlateau()
        tg = self.tg
        td = self.td
        j1.addTerre(tg)

        j1.setCartes(tg, Tarifs.COLONIE*10 + Tarifs.ROUTE*10 + Tarifs.VILLE*10 + Tarifs.BATEAU_TRANSPORT + Tarifs.CARGO + Tarifs.VOILIER)

        Colonie(1,p.it(53)).save()
        Route(1,p.it(53).lien(p.it(63))).save()
        
        Colonie(1,p.it(92)).save()
        Route(1,p.it(92).lien(p.it(93))).save()

        j1.setStaticPoints(tg,2)
        self.assertEqual(j1.getStaticPoints(tg),2)
        self.assertEqual(j1.getPoints(tg),2)
        
        Jeu.construire_route(j1,p.it(93).lien(p.it(103)))
        self.assertEqual(j1.getStaticPoints(tg),2)
        self.assertEqual(j1.getPoints(tg),2) # Route = 0 point

        Jeu.construire_route(j1,p.it(103).lien(p.it(104)))
        self.assertEqual(j1.getStaticPoints(tg),2)
        self.assertEqual(j1.getPoints(tg),2)
        
        Jeu.construire_colonie(j1,p.it(104))
        self.assertEqual(j1.getStaticPoints(tg),3)
        self.assertEqual(j1.getPoints(tg),3) # Colonie = 1 point

        Jeu.evoluer_colonie(j1, p.it(104))
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),4) # Ville = 2 points

        j1.recevoir(tg,Cartes.POINT_VICTOIRE)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),5) # Carte pv = 1 point
        self.assertEqual(j1.getVisiblePoints(tg),4) # Les cartes PV ne sont pas visibles
        j1.payer(tg,Cartes.POINT_VICTOIRE)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),4)

        # Le bateau vaut 0 point
        ab = p.it(104).lien(p.it(103))
        Jeu.construire_bateau(j1,ab)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),4) 
        b = Bateau.getBateaux(ab)[0]
        Jeu.evoluer_bateau(j1,b)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),4)
        Jeu.evoluer_bateau(j1,b)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),4)
        self.assertEqual(j1.getPoints(td),0) 

        # La route la plus longue vaut 2 points
        Jeu.set_route_la_plus_longue(tg,1,2390)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),6)
        self.assertEqual(j1.getVisiblePoints(tg),6)
        

        # La plus grande armee vaut 2 points
        # Le challenge est fait manuellement pour éviter d'avoir à déplacer le voleur.
        Jeu.set_armee_la_plus_grande(tg,1,90)
        self.assertEqual(j1.getStaticPoints(tg),4)
        self.assertEqual(j1.getPoints(tg),8)
        self.assertEqual(j1.getVisiblePoints(tg),8)
        self.assertEqual(j1.getPoints(td),0) 

        
        j1.setEnRuine(True)
        self.assertEqual(j1.getStaticPoints(tg),0)
        self.assertEqual(j1.getPoints(tg),0)
        # Joueur en ruine
        j1.setEnRuine(False)
