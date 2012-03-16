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
        self.j1.set_route_la_plus_longue(self.tg,0)
        self.j2.set_route_la_plus_longue(self.tg,0)
        Joueur.setNbJoueurs(2)

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
        j = len(j1.getColonies())
        Jeu.construire_colonie(j1,i83)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
        self.assertEqual(len(j1.getBatiments()),i+1)
        self.assertEqual(len(j1.getColonies()),j+1)
       
    def test_construire_route(self): 

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

# test d'evolution d'une colonie en ville

    def test_evoluer_colonie(self):
        p = Plateau.getPlateau()
        j1 = self.j1
        i1 = p.it(53)
        Colonie(1,i1).save()
        j2 = self.j2
        i2 = p.it(54)
        Colonie(2,i2).save()
        
        i3 = p.it(103)

        j1.setCartes(self.tg,Tarifs.VILLE)
        self.assertTrue(Jeu.peut_evoluer_colonie(j1,i1))
        self.assertFalse(Jeu.peut_evoluer_colonie(j1,i2)) # Colonie adverse
        self.assertFalse(Jeu.peut_evoluer_colonie(j1,i3)) # Pas de colonie
        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_evoluer_colonie(j1,i1)) # Pas assez ressource
        j1.setCartes(self.tg,Tarifs.VILLE)
        self.assertTrue(Jeu.peut_evoluer_colonie(j1,i1))


        i = len(j1.getVilles())
        j = len(j1.getColonies())
        k = len(j1.getBatiments())
        Jeu.evoluer_colonie(j1,i1)
        self.assertEqual(len(j1.getVilles()),i+1)
        self.assertEqual(len(j1.getColonies()),j-1)
        self.assertEqual(len(j1.getBatiments()),k)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
        j1.setCartes(self.tg,Tarifs.VILLE)
        self.assertFalse(Jeu.peut_evoluer_colonie(j1,i1)) # La colonie a déja evoluee

# Les joueurs recoltent leur ressources : lancement des des, autre que 7, recolte des ressources en fonction des villages et des villes, et des brigands. Recolte de l'or
    def test_recolter_ressources(self):
        
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j2.addTerre(tg)
        j2.addTerre(td)
   
        p = Plateau.getPlateau()
 
        c1 = Colonie(1,p.it(94)) # 5 Mouton, 5 Argile, 9 Bois
        c2 = Colonie(1,p.it(115)) # 9 Bois, Port
        c3 = Colonie(1,p.it(43)) # Ville 3 Ble, 9 Bois
        c4 = Colonie(1,p.it(63)) # 6 Or, Desert, Commerce
        c3.evolue()
        c1.save()
        c2.save()
        c3.save()
        c4.save()

        #self.tg.deplacer_brigand(self.h3)
        #self.td.brigand = Voleur(self.h27,Voleur.VoleurType.BRIGAND)
        
        # Tout lancement de dé inférieur à 2, supérieur à 12, ou égal à 7 ne revoie pas de ressouces.
        self.assertFalse(Jeu.peut_recolter_ressources(-1))
        self.assertFalse(Jeu.peut_recolter_ressources(0))
        self.assertFalse(Jeu.peut_recolter_ressources(1))
        self.assertFalse(Jeu.peut_recolter_ressources(7))
        self.assertFalse(Jeu.peut_recolter_ressources(13))
        self.assertTrue(Jeu.peut_recolter_ressources(2))
        self.assertTrue(Jeu.peut_recolter_ressources(3))
        self.assertTrue(Jeu.peut_recolter_ressources(4))
        self.assertTrue(Jeu.peut_recolter_ressources(5))
        self.assertTrue(Jeu.peut_recolter_ressources(6))
        self.assertTrue(Jeu.peut_recolter_ressources(8))
        self.assertTrue(Jeu.peut_recolter_ressources(9))
        self.assertTrue(Jeu.peut_recolter_ressources(10))
        self.assertTrue(Jeu.peut_recolter_ressources(11))
        self.assertTrue(Jeu.peut_recolter_ressources(12))

        c = Cartes.RIEN

        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        Jeu.recolter_ressources(5)
        self.assertEqual(j1.getCartes(tg),CartesRessources(1,0,0,0,1))
        self.assertEqual(j1.getOr(tg),0)
        j1.setCartes(tg,c)
        Jeu.recolter_ressources(9)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,4,0,0))
        self.assertEqual(j1.getOr(tg),0)
        j1.setCartes(tg,c)
        Jeu.recolter_ressources(6)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),1)

        #j1.setCartes(tg,c)
        #j1.setOr(0)
        #self.j1.enRuine = True
        #Jeu.recolter_ressources(4)
        #self.assertEqual(j1.getCartes(tg),c)
        #self.assertEqual(j1.getOr(tg),0)
        #Jeu.recolter_ressources(9)
        #self.assertEqual(j1.getCartes(tg),c)
        #self.assertEqual(j1.getOr(tg),0)
        #self.j1.enRuine = False
        

        v = tg.getBrigand()

        # Voleur sur une colonie
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        v.deplacer(p.hexa(42))
        v.save()
        Jeu.recolter_ressources(5)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,0,0,1))
        self.assertEqual(j1.getOr(tg),0)
        
        # Voleur sur un village
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        v.deplacer(p.hexa(12))
        v.save()
        Jeu.recolter_ressources(3)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),0)

        # Voleur sur de l'or
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        v.deplacer(p.hexa(26))
        v.save()
        Jeu.recolter_ressources(6)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),0)


        # Colonie sur deux terres en même temps
        Colonie(2,p.it(54)).save()# Terre Gauche, 8 : Caillou, 10 : Ble
        Colonie(2,p.it(69)).save() # Terre Droite # 8 : Mouton, 4 Brigand Or, Commerce 

 
        j2.setCartes(tg,c) 
        j2.setCartes(td,c) 
        j2.setOr(tg,0)
        j2.setOr(td,0)
        Jeu.recolter_ressources(8)
        self.assertEqual(j2.getCartes(tg),CartesRessources(0,0,0,1,0))
        self.assertEqual(j2.getCartes(td),CartesRessources(0,0,0,0,1))
        self.assertEqual(j2.getOr(tg),0)
        self.assertEqual(j2.getOr(td),0)
        
        j2.setCartes(tg,c) 
        j2.setCartes(td,c) 
        Jeu.recolter_ressources(4)
        self.assertEqual(j2.getCartes(tg),c)
        self.assertEqual(j2.getCartes(td),c)
        self.assertEqual(j2.getOr(tg),0)
        self.assertEqual(j2.getOr(td),0)
        

    def test_route_la_plus_longue(self):
        p = Plateau.getPlateau()
        j1 = self.j1
        j2 = self.j2

        tg = self.tg
        td = self.td

        j1.addTerre(tg)
        j1.addTerre(td)
        j2.addTerre(tg)
        j2.addTerre(td)

        Route(1,p.it(52).lien(p.it(53))).save()
        Route(1,p.it(53).lien(p.it(43))).save()
        Route(1,p.it(53).lien(p.it(63))).save()
        Route(1,p.it(63).lien(p.it(73))).save()
        Route(1,p.it(73).lien(p.it(83))).save()
        Route(1,p.it(83).lien(p.it(84))).save()
        Route(1,p.it(84).lien(p.it(74))).save()
        Route(1,p.it(74).lien(p.it(64))).save()
        Route(1,p.it(64).lien(p.it(63))).save()
        

        Route(1,p.it(59).lien(p.it(69))).save()
        Route(1,p.it(69).lien(p.it(70))).save()
        Route(1,p.it(70).lien(p.it(80))).save()
 
        
        j1.recalcul_route_la_plus_longue(tg)
        j1.recalcul_route_la_plus_longue(td)
        self.assertEqual(j1.get_route_la_plus_longue(tg),8)
        self.assertEqual(j1.get_route_la_plus_longue(td),3)

        j1.setCartes(tg,Tarifs.ROUTE)
        Jeu.construire_route(j1,p.it(43).lien(p.it(44)))
        self.assertEqual(j1.get_route_la_plus_longue(tg),9)
        self.assertEqual(j1.get_route_la_plus_longue(td),3)
        
        j1.setCartes(tg,Tarifs.ROUTE)
        Jeu.construire_route(j1,p.it(52).lien(p.it(42)))
        self.assertEqual(j1.get_route_la_plus_longue(tg),9)
        self.assertEqual(j1.get_route_la_plus_longue(td),3)


        j2.setCartes(tg,Tarifs.COLONIE)
        Route(2,p.it(84).lien(p.it(94))).save()
        Jeu.construire_colonie(j2,p.it(84))
        self.assertEqual(j1.get_route_la_plus_longue(tg),6)
        self.assertEqual(j1.get_route_la_plus_longue(td),3)

        
        #j1.enRuine = True
        #self.assertEqual(j1.route_la_plus_longue(tg,True),0)
        # Joueur en ruine
        #j1.enRuine = False
