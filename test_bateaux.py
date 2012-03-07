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
       
    def route(self): 
        j1.setCartes(self.tg,Tarifs.ROUTE)
        i66 = self.it[66] 
        i23 = self.it[23] 
        i75 = self.it[75] 
        i77 = self.it[77] 
        i67 = self.it[67] 
        i78 = self.it[78] 
        i34 = self.it[34] 
        i85 = self.it[85] 
        i56 = self.it[56] 
        a66 = i66.lien(i77)
        a23 = i23.lien(i34)
        a85 = i75.lien(i85)
        a77 = i77.lien(i67)
        a67 = i67.lien(i78)
        a56 = i67.lien(i56)
        a34 = i44.lien(i34)
        self.assertTrue(Jeu.peut_construire_route(j1,a66))  # ok relie a une route
        self.assertTrue(Jeu.peut_construire_route(j1,a34))  # ok relie a une colonie
        self.assertFalse(Jeu.peut_construire_route(j1,a55)) # existe deja
        self.assertFalse(Jeu.peut_construire_route(j1,a23)) # relie a rien
        self.assertFalse(Jeu.peut_construire_route(j1,a85)) # relie seulement a l'ennemi
        r7 = Route(j1,a66)
        r8 = Route(j1,a77)
        self.assertFalse(Jeu.peut_construire_route(j1,a67)) # c'est la mer
        self.assertFalse(Jeu.peut_construire_route(j1,a66)) # existe deja
        self.assertTrue(Jeu.peut_construire_route(j1,a56)) # cotier

        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_route(j1,a56)) # manque de ressource
        j1.setCartes(self.tg,Tarifs.ROUTE)
        self.assertTrue(Jeu.peut_construire_route(j1,a56))



        j1.enRuine = True
        self.assertFalse(Jeu.peut_construire_route(j1,a56)) # Joueur en ruine 
        j1.enRuine = False


        i = len(j1.routes)
        Jeu.construire_route(j1,a56)
        self.assertEqual(len(j1.routes),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)

        j1.setCartes(self.tg,Tarifs.BATEAU_TRANSPORT)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a67)) # Aucun lien


        c3 = Colonie(j1,i67)
        self.assertTrue(Jeu.peut_construire_bateau(j1,a67)) # ok
        self.assertTrue(Jeu.peut_construire_bateau(j1,self.it[67].lien(self.it[56]))) # ok

        i52 = self.it[52]
        a53 = i53.lien(i52)
        c4 = Colonie(j2,i53)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a53)) # relie mais a un adversaire

        a2 = self.it[2].lien(self.it[116])
        self.assertFalse(Jeu.peut_construire_bateau(j1,a2)) # relie a rien
        self.assertFalse(Jeu.peut_construire_bateau(j1,a34)) # relie mais terrestre
        
        Colonie(j1,self.it[2])
        Bateau(j2,a2)
       # self.assertFalse(Jeu.peut_construire_bateau(j1,a2)) # emplacement occupe
        
        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a67))
        j1.setCartes(self.tg,Tarifs.BATEAU_TRANSPORT)


        j1.enRuine = True
        self.assertFalse(Jeu.peut_construire_bateau(j1,a67)) # Joueur en ruine 
        j1.enRuine = False

        i = len(j1.bateaux_transport)
        Jeu.construire_bateau(j1,a67)
        self.assertEqual(len(j1.bateaux_transport),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
