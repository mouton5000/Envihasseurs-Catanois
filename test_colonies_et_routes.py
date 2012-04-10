# -*- coding: utf8 -*-
from test_joueurs import *

REDIS = redis.StrictRedis()


class TestColonieEtRoute(TestJoueur):
   
    def setUp(self):
        super(TestColonieEtRoute,self).setUp()
        self.j1 = JoueurPossible(1)
        self.j2 = JoueurPossible(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)
        self.j1.set_route_la_plus_longue(self.tg,0)
        self.j2.set_route_la_plus_longue(self.tg,0)
        JoueurPossible.setNbJoueurs(2)

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

        j1.setEnRuine(True)
        with self.assertRaises(ColonieError) as err:
            Jeu.peut_construire_colonie(j1,i83) # En ruine
        self.assertEqual(err.exception.error_code, ColonieError.JOUEUR_EN_RUINE)

        j1.setEnRuine(False)

        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i72))# Il y a deja une colonie
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_OCCUPE)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i73))# Il y a une colonie a 1 case
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENTS_VOISINS_OCCUPES)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i54))# Il n'y a aucun lien
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_NON_RELIE)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i51))# C'est la mer
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_MARITIME)
        
        j1.setCartes(self.tg,Cartes.RIEN)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i83)) # Plus assez de ressources
        self.assertEqual(err.exception.error_code, ColonieError.RESSOURCES_INSUFFISANTES)
        
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
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i53)) # Colonie adverse
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_OCCUPE)
        with self.assertRaises(ColonieError) as err:
           self.assertFalse(Jeu.peut_construire_colonie(j1,i43)) # Colonie adverse a une case
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENTS_VOISINS_OCCUPES)
        with self.assertRaises(ColonieError) as err:
           self.assertFalse(Jeu.peut_construire_colonie(j1,i44)) # Relie a une route mais adverse
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_NON_RELIE)

        i63 = p.it(63)
        a63 = i63.lien(i53)
        a73 = i63.lien(i73)
        r5 = Route(2,a63)
        r6 = Route(1,a73)
        r5.save()
        r6.save()
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_construire_colonie(j1,i63)) # Relie a une route mais colonie adverse a une case
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENTS_VOISINS_OCCUPES)
       
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
        
        j1.setEnRuine(True)
        
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a4333))
        self.assertEqual(err.exception.error_code, RouteError.JOUEUR_EN_RUINE)
        
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a5363))
        self.assertEqual(err.exception.error_code, RouteError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a5343)) # existe deja
        self.assertEqual(err.exception.error_code, RouteError.ARRETE_OCCUPEE)
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a103104)) # relie a rien
        self.assertEqual(err.exception.error_code, RouteError.ARRETE_NON_RELIEE)
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a4434)) # relie seulement a l'ennemi
        self.assertEqual(err.exception.error_code, RouteError.ARRETE_NON_RELIEE)
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a5464)) # relie seulement a l'ennemi
        self.assertEqual(err.exception.error_code, RouteError.ARRETE_NON_RELIEE)
        

        self.assertTrue(Jeu.peut_construire_route(j1,a4344))  # ok relie a une route


        a6261 = i62.lien(i61)
        a6252 = i62.lien(i52)
        Colonie(1,i62).save()
        
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a6261)) # c'est la mer
        self.assertEqual(err.exception.error_code, RouteError.ARRETE_MARITIME)
        self.assertTrue(Jeu.peut_construire_route(j1,a6252)) # cotier

        j1.setCartes(self.tg,Cartes.RIEN)
        with self.assertRaises(RouteError) as err:
            self.assertFalse(Jeu.peut_construire_route(j1,a4333)) # manque de ressource
        self.assertEqual(err.exception.error_code, RouteError.RESSOURCES_INSUFFISANTES)
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
        
        j1.setEnRuine(True)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_evoluer_colonie(j1,i1))
        self.assertEqual(err.exception.error_code, ColonieError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_evoluer_colonie(j1,i2)) # Colonie adverse
        self.assertEqual(err.exception.error_code, ColonieError.NON_PROPRIETAIRE)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_evoluer_colonie(j1,i3)) # Pas de colonie
        self.assertEqual(err.exception.error_code, ColonieError.COLONIE_INEXISTANTE)
        j1.setCartes(self.tg,Cartes.RIEN)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_evoluer_colonie(j1,i1)) # Pas assez ressource
        self.assertEqual(err.exception.error_code, ColonieError.RESSOURCES_INSUFFISANTES)
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
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_evoluer_colonie(j1,i1)) # La colonie a déja evoluee
        self.assertEqual(err.exception.error_code, ColonieError.COLONIE_DEJA_EVOLUEE)

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
        with self.assertRaises(RecolteError) as err:
            self.assertFalse(peut_recolter_ressources(-1))
        self.assertEquals(err.exception.error_code, RecolteError.HORS_LIMITE)
        with self.assertRaises(RecolteError) as err:
            self.assertFalse(peut_recolter_ressources(0))
        self.assertEquals(err.exception.error_code, RecolteError.HORS_LIMITE)
        with self.assertRaises(RecolteError) as err:
            self.assertFalse(peut_recolter_ressources(1))
        self.assertEquals(err.exception.error_code, RecolteError.HORS_LIMITE)
        with self.assertRaises(RecolteError) as err:
            self.assertFalse(peut_recolter_ressources(7))
        self.assertEquals(err.exception.error_code, RecolteError.SEPT)
        with self.assertRaises(RecolteError) as err:
            self.assertFalse(peut_recolter_ressources(13))
        self.assertEquals(err.exception.error_code, RecolteError.HORS_LIMITE)
        self.assertTrue(peut_recolter_ressources(2))
        self.assertTrue(peut_recolter_ressources(3))
        self.assertTrue(peut_recolter_ressources(4))
        self.assertTrue(peut_recolter_ressources(5))
        self.assertTrue(peut_recolter_ressources(6))
        self.assertTrue(peut_recolter_ressources(8))
        self.assertTrue(peut_recolter_ressources(9))
        self.assertTrue(peut_recolter_ressources(10))
        self.assertTrue(peut_recolter_ressources(11))
        self.assertTrue(peut_recolter_ressources(12))

        c = Cartes.RIEN

        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        recolter_ressources(5)
        self.assertEqual(j1.getCartes(tg),CartesRessources(1,0,0,0,1))
        self.assertEqual(j1.getOr(tg),0)
        j1.setCartes(tg,c)
        recolter_ressources(9)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,4,0,0))
        self.assertEqual(j1.getOr(tg),0)
        j1.setCartes(tg,c)
        recolter_ressources(6)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),1)
        
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        j1.setEnRuine(True)
        recolter_ressources(6)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),0)
        recolter_ressources(5)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),0)
        # En ruine
        j1.setEnRuine(False)

        v = Voleur.getBrigand(tg)

        # Voleur sur une colonie
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        v.deplacer(p.hexa(42))
        v.save()
        recolter_ressources(5)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,0,0,1))
        self.assertEqual(j1.getOr(tg),0)
        
        # Voleur sur un village
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        v.deplacer(p.hexa(12))
        v.save()
        recolter_ressources(3)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),0)

        # Voleur sur de l'or
        j1.setCartes(tg,c)
        j1.setOr(tg,0)
        v.deplacer(p.hexa(26))
        v.save()
        recolter_ressources(6)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),0)


        # Colonie sur deux terres en même temps
        Colonie(2,p.it(54)).save()# Terre Gauche, 8 : Caillou, 10 : Ble
        Colonie(2,p.it(69)).save() # Terre Droite # 8 : Mouton, 4 Brigand Or, Commerce 

 
        j2.setCartes(tg,c) 
        j2.setCartes(td,c) 
        j2.setOr(tg,0)
        j2.setOr(td,0)
        recolter_ressources(8)
        self.assertEqual(j2.getCartes(tg),CartesRessources(0,0,0,1,0))
        self.assertEqual(j2.getCartes(td),CartesRessources(0,0,0,0,1))
        self.assertEqual(j2.getOr(tg),0)
        self.assertEqual(j2.getOr(td),0)
        
        j2.setCartes(tg,c) 
        j2.setCartes(td,c) 
        recolter_ressources(4)
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

        
        j1.ruiner()
        self.assertEqual(j1.get_route_la_plus_longue(tg),0)
        self.assertEqual(j1.get_route_la_plus_longue(td),0)
        # En ruine
        j1.setEnRuine(False)


    def test_route_la_plus_longue_global(self):
        j1 = self.j1
        j2 = self.j2
        j3 = JoueurPossible(3)
        JoueurPossible.setNbJoueurs(3)
        p = Plateau.getPlateau()

        tg = self.tg

        j1.addTerre(tg)
        j2.addTerre(tg)
        j3.addTerre(tg)

        Colonie(1,p.it(83)).save()
        Colonie(2,p.it(23)).save()
        Colonie(3,p.it(52)).save()

        Route(1,p.it(34).lien(p.it(44))).save()
        Route(1,p.it(72).lien(p.it(73))).save()
        Route(1,p.it(94).lien(p.it(104))).save()
        Route(1,p.it(94).lien(p.it(95))).save()
        Route(2,p.it(43).lien(p.it(44))).save()
        Route(2,p.it(63).lien(p.it(64))).save()

        a1 = p.it(83).lien(p.it(73)) 
        a2 = p.it(73).lien(p.it(63)) 
        a3 = p.it(63).lien(p.it(53)) 
        a4 = p.it(53).lien(p.it(43)) 
        a5 = p.it(83).lien(p.it(84)) 
        i6 = p.it(43)
        i7 = p.it(63)
        a8 = p.it(84).lien(p.it(74)) 
        a9 = p.it(74).lien(p.it(75)) 
        a10 = p.it(23).lien(p.it(24)) 
        a11 = p.it(24).lien(p.it(34)) 
        a12 = p.it(34).lien(p.it(35)) 
        a13 = p.it(35).lien(p.it(45)) 
        a14 = p.it(23).lien(p.it(33)) 
        a15 = p.it(33).lien(p.it(32)) 
        i16 = p.it(34)
        a17 = p.it(32).lien(p.it(42)) 
        a18 = p.it(52).lien(p.it(62)) 
        a19 = p.it(62).lien(p.it(72)) 
        a20 = p.it(72).lien(p.it(82)) 
        a21 = p.it(82).lien(p.it(92)) 
        a22 = p.it(92).lien(p.it(93)) 
        i23 = p.it(72)
        a24 = p.it(93).lien(p.it(103)) 
        a25 = p.it(103).lien(p.it(104)) 
        a26 = p.it(104).lien(p.it(114)) 
        a27 = p.it(114).lien(p.it(115)) 
        i28 = p.it(104)
        a29 = p.it(75).lien(p.it(85)) 
        a30 = p.it(115).lien(p.it(105)) 
        a31 = p.it(105).lien(p.it(95)) 
        a32 = p.it(95).lien(p.it(85)) 
        a33 = p.it(42).lien(p.it(52)) 
        i34 = p.it(95)


        t1 = 0
        t2 = 0
        t3 = 0
        t4 = 0
        t5 = (1,5)
        t6 = (1,5)
        t7 = 0
        t8 = 0
        t9 = (1,5)
        t10 = (1,5)
        t11 = (1,5)
        t12 = (1,5)
        t13 = (1,5)
        t14 = (1,5)
        t15 = (2,6)
        t16 = (1,5)
        t17 = (1,5)
        t18 = (1,5)
        t19 = (1,5)
        t20 = (1,5)
        t21 = (1,5)
        t22 = (1,5)
        t23 = (1,5)
        t24 = (1,5)
        t25 = (1,5)
        t26 = (3,6)
        t27 = (3,7)
        t28 = 0
        t29 = (1,6)
        t30 = (1,6)
        t31 = (1,6)
        t32 = (1,6)
        t33 = (1,6)
        t34 = (1,6)
        t35 = (2,6)

        j1.setCartes(tg,Tarifs.COLONIE*100 + Tarifs.ROUTE*100)
        j2.setCartes(tg,Tarifs.COLONIE*100 + Tarifs.ROUTE*100)
        j3.setCartes(tg,Tarifs.COLONIE*100 + Tarifs.ROUTE*100)

        Jeu.construire_route(j1,a1)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t1)
        Jeu.construire_route(j1,a2)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t2)
        Jeu.construire_route(j1,a3)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t3)
        Jeu.construire_route(j1,a4)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t4)
        Jeu.construire_route(j1,a5)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t5)
        Jeu.construire_colonie(j2,i6)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t6)
        Jeu.construire_colonie(j2,i7)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t7)
        Jeu.construire_route(j1,a8)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t8)
        Jeu.construire_route(j1,a9)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t9)
        Jeu.construire_route(j2,a10)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t10)
        Jeu.construire_route(j2,a11)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t11)
        Jeu.construire_route(j2,a12)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t12)
        Jeu.construire_route(j2,a13)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t13)
        Jeu.construire_route(j2,a14)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t14)
        Jeu.construire_route(j2,a15)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t15)
        Jeu.construire_colonie(j1,i16)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t16)
        Jeu.construire_route(j2,a17)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t17)
        Jeu.construire_route(j3,a18)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t18)
        Jeu.construire_route(j3,a19)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t19)
        Jeu.construire_route(j3,a20)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t20)
        Jeu.construire_route(j3,a21)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t21)
        Jeu.construire_route(j3,a22)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t22)
        Jeu.construire_colonie(j1,i23)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t23)
        Jeu.construire_route(j3,a24)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t24)
        Jeu.construire_route(j3,a25)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t25)
        Jeu.construire_route(j3,a26)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t26)
        Jeu.construire_route(j3,a27)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t27)
        Jeu.construire_colonie(j1,i28)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t28)
        Jeu.construire_route(j1,a29)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t29)
        Jeu.construire_route(j3,a30)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t30)
        Jeu.construire_route(j3,a31)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t31)
        Jeu.construire_route(j3,a32)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t32)
        Jeu.construire_route(j2,a33)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t33)
        Jeu.construire_colonie(j1,i34)
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t34)
        
        j1.ruiner()
        self.assertEqual(Jeu.get_route_la_plus_longue(tg),t35)
        # En ruine
        j1.setEnRuine(False)
