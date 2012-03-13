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
        j1.setCartes(tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,tg))
        j1.setCartes(td,Tarifs.DEVELOPPEMENT)
        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,td))
        
        j1.setCartes(tg,Tarifs.DEVELOPPEMENT)
        Jeu.acheter_carte_developpement(j1,tg)
        print j1.getCartes(tg)
        self.assertEqual(j1.getCartes(tg).size(),1) 

#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,tg))
#        # Joueur en ruine
#        j1.enRuine = False
        
    def teest_jouer_chevalliers(self):

        # Le joueur 1 joue une carte de chevallier si il en a en main et s'il ne l'a pas achete recemment. Il l'ajoute a son armee locale et deplace le voleur.
        
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.terres = [tg]
        j2.terres = [tg,td]

        Colonie(j2,self.it[86]) 
        Colonie(j2,self.it[81]) 
        
        self.tg.deplacer_brigand(self.h23)
        self.td.brigand = Voleur(self.h26,Voleur.VoleurType)
        
        br = Voleur.VoleurType.BRIGAND
        # Aucun test pour voleur ici, ils sont deja fait dans deplacer voleur, les regles sont les memes

        c1 = CartesDeveloppement(3,0,0,0,0)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(0,1,1,1,1)
        
        j2.setCartes(tg,Cartes.RIEN)
        j2.setCartes(td,Cartes.RIEN)

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
        
        j1.enRuine = True
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
        # Joueur en ruine
        j1.enRuine = False
        
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,td,br,self.h37,j2))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))

        j1.setCartes(tg,c1)
        j1.chevalliers = [0]
        Jeu.jouer_chevallier(j1,tg,br,self.h32,j2)
        self.assertEqual(tg.brigand.position,self.h32)
        self.assertEqual(j1.chevalliers,[1])

    def teest_peut_jouer_decouverte(self):
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.terres = [tg]

        c1 = CartesDeveloppement(0,0,0,3,0)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,1,1,0,1)
        
        d1 = CartesRessources(1,1,0,0,0)
        dneg = CartesRessources(-1,1,1,1,0)
        ddouble = CartesRessources(0.5,1.5,0,0,0)
        d2 = CartesRessources(1,1,0,0,1)
        d3 = CartesRessources(1,0,0,0,0)
        d4 = CartesGeneral(1,0,0,0,0,1,0,0,0,0)
        d5 = CartesGeneral(1,0,1,0,0,1,0,0,0,0)

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_decouverte(j1,tg,d1))
        
        j1.enRuine = True
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))
        # Joueur en ruine
        j1.enRuine = False
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
        j1.aur = [0]
        Jeu.jouer_decouverte(j1,tg,d1)
        self.assertEqual(j1.getCartes(tg),d1 + Cartes.DECOUVERTE * 2)
        self.assertEqual(j1.aur,[0])
        
    def teest_peut_jouer_construction_routes(self):


        # le test sur la construction de route ou des bateaux n est pas fait ici
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.terres = [tg]

        Colonie(j1,self.it[23])
        Colonie(j1,self.it[3])
        Route(j1,self.it[23].lien(self.it[34])) 

        c1 = CartesDeveloppement(0,0,0,0,3)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,1,1,1,0)
        
        a1 = self.it[23].lien(self.it[12])
        a2 = self.it[34].lien(self.it[44])
        a3 = self.it[3].lien(self.it[14])
        a4 = self.it[3].lien(self.it[117])

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))
        
        j1.enRuine = True
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a2))
        # Joueur en ruine
        j1.enRuine = False
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

        j1.terres = [tg,td]
        Colonie(j1,self.it[49])
        a5 = self.it[49].lien(self.it[59])
        j1.setCartes(tg,c1)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,True,a1,True,a5))

        j1.setCartes(tg,c1)
        Jeu.jouer_construction_routes(j1,tg,True,a1,True,a2)
        self.assertEqual(j1.getCartes(tg),Cartes.CONSTRUCTION_ROUTES * 2)
        self.assertTrue(a1.route != 0)
        self.assertTrue(a2.route != 0)
        self.assertTrue(a1.route.joueur == j1)
        self.assertTrue(a2.route.joueur == j1)

        j1.setCartes(tg,c1)
        Jeu.jouer_construction_routes(j1,tg,False,a3,False,a4)
        self.assertEqual(j1.getCartes(tg),Cartes.CONSTRUCTION_ROUTES * 2)
        self.assertTrue(a3.bateau != 0)
        self.assertTrue(a4.bateau != 0)
        self.assertTrue(a3.bateau.joueur == j1)
        self.assertTrue(a4.bateau.joueur == j1)
        self.assertEqual(len(j1.bateaux_transport),2)
        self.assertEqual(len(j1.cargo),0)
        self.assertEqual(len(j1.voilier),0)



    def teest_peut_jouer_monopole(self):

        j1 = self.j1
        j2 = self.j2
        j3 = self.j3
        j4 = self.j4
        j5 = Joueur(5)
        j6 = Joueur(6)

        tg = self.tg
        td = self.td

        j1.terres = [tg]
        j2.terres = [tg,td]
        j3.terres = [tg]
        j4.terres = [tg]
        j5.terres = [tg]
        j6.terres = [td]

        j1.mains = [0]
        j2.mains = [0,0]
        j3.mains = [0]
        j4.mains = [0]
        j5.mains = [0]
        j6.mains = [0]
        
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
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        
        j1.enRuine = True
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        # Joueur en ruine
        j1.enRuine = False
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j1,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4,j5]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j6]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,rch,[j2,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,td,rch,[j2,j6]))

        j2.setCartes(tg,c2)
        j3.setCartes(tg,c2)
        j4.setCartes(tg,c2)
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[]))

        j1.setCartes(tg,c1)
        j2.setCartes(tg,c5)
        j3.setCartes(tg,c5)
        j4.setCartes(tg,c5)
        Jeu.jouer_monopole(j1,tg,r,[j2,j3,j4])
        self.assertEqual(j1.getCartes(tg),c1 + Cartes.ARGILE*6)

        self.assertEqual(j2.getCartes(tg).get_cartes_de_type(r), 0)
        self.assertEqual(j3.getCartes(tg).get_cartes_de_type(r), 0)
        self.assertEqual(j4.getCartes(tg).get_cartes_de_type(r), 0)
