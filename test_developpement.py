# -*- coding: utf8 -*-
from plateau import *
from test_joueurs import *
from redis import *

REDIS = redis.StrictRedis()


class TestDeveloppement(TestJoueur):
   
    def setUp(self):
        super(TestDeveloppement,self).setUp()
        self.j1 = Joueur(1)
        self.j2 = Joueur(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

    def test_acheter_developpement(self):
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.addTerre(tg)

        j1.setCartes(tg,Tarifs.DEVELOPPEMENT)
        self.assertTrue(Jeu.peut_acheter_carte_developpement(j1,tg))
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,tg))
        # En ruine
        j1.setEnRuine(False)
        
        j1.setCartes(tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,tg))
        j1.setCartes(td,Tarifs.DEVELOPPEMENT)
        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,td))
        
        j1.setCartes(tg,Tarifs.DEVELOPPEMENT)
        Jeu.acheter_carte_developpement(j1,tg)
        self.assertEqual(j1.getCartesEnSommeil(tg).size(),1) 

        
    def test_jouer_chevalliers(self):

        # Le joueur 1 joue une carte de chevallier si il en a en main et s'il ne l'a pas achete recemment. Il l'ajoute a son armee locale et deplace le voleur.
        
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j2.addTerre(td)
       
        j1.set_deplacement_voleur(tg,False) 
        j2.set_deplacement_voleur(tg,False)
        j2.set_deplacement_voleur(td,False)

        p = Plateau.getPlateau()

        Colonie(2,p.it(103)).save()
        Colonie(2,p.it(90)).save()
        
        h1 = p.hexa(42)
        h2 = p.hexa(35)

        desg = p.hexa(22)
        desd = p.hexa(25)
        
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        br = Voleur.VoleurType.BRIGAND
        # Aucun test pour voleur ici, ils sont deja fait dans deplacer voleur, les regles sont les memes

        c1 = CartesDeveloppement(3,0,0,0,0)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(0,1,1,1,1)
        
        j2.setCartes(tg,Cartes.RIEN)
        j2.setCartes(td,Cartes.RIEN)



        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_chevallier(j1,tg,br,h1,2))
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,h1,2))
        # En ruine
        j1.setEnRuine(False)
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
#        # Joueur en ruine
#        j1.enRuine = False
        
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,td,br,h2,2))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,h1,2))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,h1,2))

        j1.setCartes(tg,c1)
        j1.set_chevalliers(tg,0)
        self.assertTrue(Jeu.peut_jouer_chevallier(j1,tg,br,h1,2))
        Jeu.jouer_chevallier(j1,tg,br,h1,2)
        brg = Voleur.getBrigand(tg)
        self.assertEqual(brg.position,h1)
        self.assertEqual(j1.get_chevalliers(tg),1)
        self.assertEqual(j1.getCartes(tg),CartesDeveloppement(2,0,0,0,0))



    def test_peut_jouer_decouverte(self):
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.addTerre(tg)

        c1 = CartesDeveloppement(0,0,0,3,0)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,1,1,0,1)
        
        d1 = CartesRessources(1,1,0,0,0) #ok
        dneg = CartesRessources(-1,1,1,1,0) # négatif
        ddouble = CartesRessources(0.5,1.5,0,0,0) # non entier
        d2 = CartesRessources(1,1,0,0,1) # Trop de ressources
        d3 = CartesRessources(1,0,0,0,0) # Pas assez de ressources
        d4 = CartesGeneral(1,0,0,0,0,1,0,0,0,0) # Demande de carte de développement
        d5 = CartesGeneral(1,0,1,0,0,1,0,0,0,0) # Bon nombre de ressources mais demande de carte de déevloppement en plus

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_decouverte(j1,tg,d1))
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))
        # En ruine
        j1.setEnRuine(False)
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))
#        # Joueur en ruine
#        j1.enRuine = False
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,td,d1))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,dneg))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,ddouble))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d2))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d3))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d4))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d5))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))

        j1.setCartes(tg,c1)
        j1.setOr(tg,0)
        Jeu.jouer_decouverte(j1,tg,d1)
        self.assertEqual(j1.getCartes(tg),d1 + Cartes.DECOUVERTE * 2)
        self.assertEqual(j1.getOr(tg),0)
        
    def test_peut_jouer_construction_routes(self):

        p = Plateau.getPlateau()

        # le test sur la construction de route ou des bateaux n est pas fait ici
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.addTerre(tg)

        i1 = p.it(54)
        i2 = p.it(92)
        i3 = p.it(44)
        i4 = p.it(43)
        i5 = p.it(64)
        i6 = p.it(93)
        i7 = p.it(102)

        Colonie(1,i1).save()
        Colonie(1,i2).save()
        Route(1,i1.lien(i3)).save()

        c1 = CartesDeveloppement(0,0,0,0,3)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,1,1,1,0)
        
        a1 = i1.lien(i5)
        a2 = i3.lien(i4)
        a3 = i2.lien(i6)
        a4 = i2.lien(i7)

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))
        # En ruine
        j1.setEnRuine(False)
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))
#        # Joueur en ruine
#        j1.enRuine = False
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a3))
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,False,a3))
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,True,a3,False,a4))
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,False,a3,False,a4))
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,td,True,a1,True,a2))
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a1))
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,False,a4,False,a4))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))

        j1.addTerre(td)
        Colonie(1,p.it(59)).save()
        a5 = p.it(49).lien(p.it(59))
        j1.setCartes(tg,c1)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a5))

        j1.setCartes(tg,c1)
        Jeu.jouer_construction_routes(j1,tg,True,a1,True,a2)
        self.assertEqual(j1.getCartes(tg),Cartes.CONSTRUCTION_ROUTES * 2)
        r1 = Route.getRoute(a1)
        r2 = Route.getRoute(a2)
        self.assertTrue(r1 != 0)
        self.assertTrue(r2 != 0)
        self.assertEqual(r1.joueur,j1.num)
        self.assertEqual(r2.joueur,j1.num)

        j1.setCartes(tg,c1)
        Jeu.jouer_construction_routes(j1,tg,False,a3,False,a4)
        self.assertEqual(j1.getCartes(tg),Cartes.CONSTRUCTION_ROUTES * 2)
        b3s = Bateau.getBateaux(a3)
        b4s = Bateau.getBateaux(a4)
        self.assertTrue(len(b3s) != 0)
        self.assertTrue(len(b4s) != 0)
        self.assertTrue(b3s[0].joueur == j1.num)
        self.assertTrue(b4s[0].joueur == j1.num)
        self.assertEqual(len(j1.getBateauxTransport()),2)
        self.assertEqual(len(j1.getCargos()),0)
        self.assertEqual(len(j1.getVoiliers()),0)



    def test_peut_jouer_monopole(self):

        j1 = self.j1
        j2 = self.j2
        j3 = Joueur(3)
        j4 = Joueur(4)
        j5 = Joueur(5)
        j6 = Joueur(6)

        tg = self.tg
        td = self.td

        j1.addTerre(tg)
        j2.addTerre(tg)
        j2.addTerre(td)
        j3.addTerre(tg)
        j4.addTerre(tg)
        j5.addTerre(tg)
        j6.addTerre(td)

        r = Cartes.ARGILE
        rch = Cartes.CHEVALLIER
        
        c1 = Cartes.MONOPOLE
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,0,1,1,1)
        c4 = CartesGeneral(2,0,0,0,1,0,1,0,0,0)
        c5 = CartesRessources(2,0,0,0,0)

        j1.setCartes(tg,c1)
        j2.setCartes(tg,c4)
        j2.setCartes(td,c5)
        j3.setCartes(tg,c4)
        j4.setCartes(tg,c4)
        j5.setCartes(tg,c4)
        j6.setCartes(td,c4)
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,4]))
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,4]))
        # En ruine
        j1.setEnRuine(False)
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
#        # Joueur en ruine
#        j1.enRuine = False
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[2,3]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[2]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[1,3,4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,4,5]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,6]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,rch,[2,3,4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,td,rch,[2,6]))

        j2.setCartes(tg,c2)
        j3.setCartes(tg,c2)
        j4.setCartes(tg,c2)
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,4]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[2,3]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[2]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3,4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2,3]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[2]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[]))

        j1.setCartes(tg,c1)
        j2.setCartes(tg,c5)
        j3.setCartes(tg,c5)
        j4.setCartes(tg,c5)
        Jeu.jouer_monopole(j1,tg,r,[2,3,4])
        self.assertEqual(j1.getCartes(tg),c1 + Cartes.ARGILE*6)

        self.assertEqual(j2.getCartes(tg).get_cartes_de_type(r), 0)
        self.assertEqual(j3.getCartes(tg).get_cartes_de_type(r), 0)
        self.assertEqual(j4.getCartes(tg).get_cartes_de_type(r), 0)

    def test_armee_la_plus_grande(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j1.addTerre(td)
        j2.addTerre(tg)
        j2.addTerre(td)
       
        j1.set_deplacement_voleur(tg,False) 
        j1.set_deplacement_voleur(td,False) 
        j2.set_deplacement_voleur(tg,False)
        j2.set_deplacement_voleur(td,False)

        p = Plateau.getPlateau()

        Colonie(1,p.it(42)).save()
        Colonie(1,p.it(88)).save()
        Colonie(2,p.it(35)).save()
        Colonie(2,p.it(90)).save()
        
        h1 = p.hexa(16)
        h2 = p.hexa(17)
        h1d = p.hexa(39)

        desg = p.hexa(22)
        desd = p.hexa(25)
        
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        br = Voleur.VoleurType.BRIGAND
        # Aucun test pour voleur ici, ils sont deja fait dans deplacer voleur, les regles sont les memes

        c1 = CartesDeveloppement(100,0,0,0,0)
        
        j1.setCartes(tg,c1)
        j2.setCartes(tg,c1)
        j2.setCartes(td,c1)

        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),0)
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)

        Jeu.jouer_chevallier(j1,tg,br,h2,2)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),0)
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)
        
        Jeu.jouer_chevallier(j1,tg,br,h2,2)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),0)
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)
        
        Jeu.jouer_chevallier(j1,tg,br,h2,2)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(1,3))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)

        Jeu.jouer_chevallier(j2,tg,br,h1,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(1,3))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)

        Jeu.jouer_chevallier(j2,tg,br,h1,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(1,3))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)

        Jeu.jouer_chevallier(j2,tg,br,h1,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
        
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(1,3))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)
        
        Jeu.jouer_chevallier(j2,tg,br,h1,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
       
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(2,4))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)

        Jeu.jouer_chevallier(j2,td,br,h1d,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
       
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(2,4))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)
        
        Jeu.jouer_chevallier(j2,td,br,h1d,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
       
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(2,4))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)
       
        Jeu.jouer_chevallier(j2,td,br,h1d,1)
        brg = Voleur.getBrigand(tg)
        brg.deplacer(desg)
        brd = Voleur.getBrigand(td)
        brd.deplacer(desd)
        brg.save()
        brd.save()
       
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(2,4))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),(2,3))
        
        j2.ruiner()
        self.assertEqual(Jeu.get_armee_la_plus_grande(tg),(1,3))
        self.assertEqual(Jeu.get_armee_la_plus_grande(td),0)
        # En ruine
        j2.setEnRuine(False)


# Que se passe til si le meilleur passe en ruine?        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
#        # Joueur en ruine
#        j1.enRuine = False
        
