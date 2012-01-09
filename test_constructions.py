import unittest
from cartes import *
from constructions import *
from plateau import *
from joueurs import *

class TestColonie(unittest.TestCase):
    def setUp(self):
        self.i1 = Intersection(1)
        self.i2 = Intersection(2)
        self.i3 = Intersection(3)
        self.i4 = Intersection(4)
        self.i5 = Intersection(5)
        self.i6 = Intersection(6)
        self.i7 = Intersection(7)
        self.i8 = Intersection(8)
        self.i9 = Intersection(9)
        self.i10 = Intersection(10)
        self.i11 = Intersection(11)
        self.i12 = Intersection(12)
        self.i13 = Intersection(13)
        self.i14 = Intersection(14)
        self.i15 = Intersection(15)
        self.i16 = Intersection(16)
        self.h1 = Hexagone(self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0)
        self.h2 = Hexagone(self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)
        self.h3 = Hexagone(self.i2,self.i3,self.i11,self.i12,self.i13,self.i7,HexaType.ARGILE,6)
        self.h4 = Hexagone(self.i7,self.i13,self.i14,self.i15,self.i16,self.i8,HexaType.BOIS,12)
        self.a1 = self.h2.liens[0]
        self.a2 = self.h2.liens[1]
        self.a3 = self.h2.liens[2]
        j1 = Joueur(1)
        self.c1 = Colonie(j1,self.i1)
        self.c2 = Colonie(j1,self.i7)

    def test_absence(self):
        self.assertEqual(self.i1.colonie,self.c1)
        self.assertEqual(self.i2.colonie,0)
        self.assertEqual(self.c1.position,self.i1)

    def test_evolution(self):
        self.assertFalse(self.c1.isVille)
        self.c1.evolue()
        self.assertTrue(self.c1.isVille)

    def test_cotier(self):
        self.assertTrue(self.c1.isCotier())
        self.assertFalse(self.c2.isCotier())

    def test_ressources(self):
        ca1 = CartesRessources(0,0,1,0,0)
        self.assertEqual(self.c1.ressources(), [(12,ca1,0)])
        self.assertEqual(self.c1.ressources_from_past(12), (ca1,0))
        self.c2.evolue()
        ca2 = CartesRessources(2,0,0,0,0)
        ca3 = CartesRessources(0,0,4,0,0)
        self.assertEqual(self.c2.ressources(), [(6,ca2,0),(12,ca3,0)])
        self.assertEqual(self.c2.ressources_from_past(12), (ca3,0))
        self.assertEqual(self.c2.ressources_from_past(6), (ca2,0))
     
class TestRoute(unittest.TestCase):
    def setUp(self):
        self.i1 = Intersection(1)
        self.i2 = Intersection(2)
        self.i3 = Intersection(3)
        self.i4 = Intersection(4)
        self.i5 = Intersection(5)
        self.i6 = Intersection(6)
        self.a1 = Arrete(self.i1,self.i2)
        self.a2 = Arrete(self.i2,self.i3)
        self.a3 = Arrete(self.i3,self.i1)
        j1 = Joueur(1)
        self.c1 = Colonie(j1,self.i1)
        self.r1 = Route(j1,self.a1)
        
    def test_absence(self):
        self.assertEqual(self.a1.route,self.r1)
        self.assertEqual(self.a2.route,0)
        self.assertEqual(self.r1.position,self.a1)

    def test_est_extremite(self):
        i1 = Intersection(1)
        i2 = Intersection(2)
        i3 = Intersection(3)
        i4 = Intersection(4)
        i5 = Intersection(5)
        i6 = Intersection(6)
        a1 = Arrete(i1,i2)
        a2 = Arrete(i3,i2)
        a3 = Arrete(i2,i4)
        a4 = Arrete(i4,i5)
        a5 = Arrete(i4,i6)

        i10 = Intersection(10)
        i11 = Intersection(11)
        a = Arrete(i10,i11)

        j1 = Joueur(1)
        j2 = Joueur(2)

        r1 = Route(j1,a1)
        r2 = Route(j1,a2)
        r3 = Route(j1,a3)
        r4 = Route(j1,a4)
        r5 = Route(j1,a5)

        self.assertFalse(r3.est_extremite())
        c1 = Colonie(j1,i2)        
        self.assertFalse(r3.est_extremite())
        c2 = Colonie(j1,i4)        
        self.assertFalse(r3.est_extremite())

        c1.position = i10
        i2.colonie = 0
        c2.position = i10
        i4.colonie = 0


        c3 = Colonie(j2,i2)
        self.assertTrue(r3.est_extremite())

        c4 = Colonie(j2,i4)        
        self.assertTrue(r3.est_extremite())

        c3.position = i10
        i2.colonie = 0
        c4.position = i10
        i4.colonie = 0

        r1.position = a
        a1.route = 0
        self.assertFalse(r3.est_extremite())

        r4.position = a
        a4.route = 0
        self.assertFalse(r3.est_extremite())

        r2.position = a
        a2.route = 0
        self.assertTrue(r3.est_extremite())

        r5.position = a
        a5.route = 0
        self.assertTrue(r3.est_extremite())

        r2.position = a2
        a2.route = r2
        r1.position = a1
        a1.route = r1
        r6 = Route(j2,a4)
        self.assertTrue(r3.est_extremite())

        r7 = Route(j2,a5)
        self.assertTrue(r3.est_extremite())

        r1.position = a
        a1.route = 0
        r2.position = a
        a2.route = 0
        r8 = Route(j2,a1)
        r9 = Route(j2,a2)
        self.assertTrue(r3.est_extremite())

    def test_route_la_plus_longue(self):
        i1 = Intersection(1)
        i2 = Intersection(2)
        i3 = Intersection(3)
        i4 = Intersection(4)
        i5 = Intersection(5)
        i6 = Intersection(6)
        i7 = Intersection(7)
        i8 = Intersection(8)
        i9 = Intersection(9)
        i10 = Intersection(10)
        i11 = Intersection(11)
        i12 = Intersection(12)
        i13 = Intersection(13)
        i14 = Intersection(14)

        h1 = Hexagone(i1,i2,i3,i4,i5,i6,HexaType.CAILLOU,6)
        h2 = Hexagone(i4,i7,i8,i9,i10,i5,HexaType.BOIS,9)
        h3 = Hexagone(i7,i11,i12,i13,i14,i8,HexaType.DESERT,0)

        j1 = Joueur(1)

        r1 = Route(j1,i3.lien(i4))
        r2 = Route(j1,i6.lien(i5))
        r3 = Route(j1,i5.lien(i4))
        r4 = Route(j1,i4.lien(i7))
        r5 = Route(j1,i7.lien(i11))
        r6 = Route(j1,i11.lien(i12))
        r7 = Route(j1,i7.lien(i8))
        r8 = Route(j1,i8.lien(i14))
        r9 = Route(j1,i14.lien(i13))

        print '-------------------------'
        self.assertEqual(r1.rlplfr(),5) 
        print '-------------------------'
        self.assertEqual(r2.rlplfr(),6) 
        print '-------------------------'
        self.assertEqual(r4.rlplfr(),4) 


class TestBateau(unittest.TestCase):
    def setUp(self):
        j1 = Joueur(1)
        
        self.i1 = Intersection(1)
        self.i2 = Intersection(2)
        self.i3 = Intersection(3)
        
        self.a1 = Arrete(self.i1,self.i2)
        self.a2 = Arrete(self.i2,self.i3)
        self.a3 = Arrete(self.i3,self.i1)
        
        self.b1 = Bateau(j1,self.a1)
        
        self.in1 = Intersection(1)
        self.in2 = Intersection(2)
        self.in3 = Intersection(3)
        self.in4 = Intersection(4)
        self.in5 = Intersection(5)
        self.in6 = Intersection(6)
        self.in7 = Intersection(7)
        self.in8 = Intersection(8)
        self.in9 = Intersection(9)
        self.in10 = Intersection(10)
        self.in11 = Intersection(11)
        self.in12 = Intersection(11)
        self.in13 = Intersection(11)
        self.in14 = Intersection(11)
        self.h1 = Hexagone(self.in1,self.in2,self.in3,self.in4,self.in5,self.in6,HexaType.CAILLOU,2)
        self.h2 = Hexagone(self.in3,self.in7,self.in8,self.in9,self.in10,self.in4,HexaType.MER,0)
        self.h2 = Hexagone(self.in8,self.in11,self.in12,self.in13,self.in14,self.in9,HexaType.MER,0)

        self.an1 = self.in7.lien(self.in3)
        self.an2 = self.in3.lien(self.in4)
        self.an3 = self.in4.lien(self.in10)
        self.an4 = self.in10.lien(self.in9)
        self.an5 = self.in9.lien(self.in8)
        self.an6 = self.in8.lien(self.in7)
        self.an7 = self.in9.lien(self.in14)
        self.an8 = self.in14.lien(self.in13)
        self.an9 = self.in13.lien(self.in12)
        self.an10 = self.in12.lien(self.in11)
        self.an11 = self.in11.lien(self.in8)

        self.b2 = Bateau(j1,self.an1)


    def test_absence(self):
        self.assertEqual(self.a1.bateau,self.b1)
        self.assertEqual(self.a2.bateau,0)
        self.assertEqual(self.b1.position,self.a1)

    def test_cargaison(self):
        self.assertEqual(self.b1.cargaison,Cartes.RIEN)
        self.b1.append(Cartes.BLE)
        self.b1.append(Cartes.BOIS)
        self.b1.append(Cartes.CHEVALLIER)
        self.b1.append(Cartes.ARGILE)
        self.b1.append(Cartes.ARGILE)
        self.b1.append(Cartes.DECOUVERTE)
        self.b1.append(Cartes.MOUTON)
        
        self.assertEqual(self.b1.cargaison, CartesGeneral(2,1,1,0,0,1,0,0,1,0))
        self.assertEqual(self.b1.cargaison.size(), 6)
        
        self.b1.remove(Cartes.BOIS) 
        self.assertEqual(self.b1.cargaison, CartesGeneral(2,1,0,0,0,1,0,0,1,0))
        self.assertEqual(self.b1.cargaison.size(), 5)
        self.b1.append(Cartes.MOUTON)
        self.assertEqual(self.b1.cargaison, CartesGeneral(2,1,0,0,1,1,0,0,1,0))
        self.assertEqual(self.b1.cargaison.size(), 6)
        self.b1.remove(Cartes.MOUTON)
        self.assertEqual(self.b1.cargaison, CartesGeneral(2,1,0,0,0,1,0,0,1,0))
        self.assertEqual(self.b1.cargaison.size(), 5)

    def test_evolue(self):
        self.assertTrue(self.b1.etat,Bateau.BateauType.TRANSPORT)
        self.cargaisonMax = 6
        self.vitesse = 1
        self.b1.evolue()
        self.assertTrue(self.b1.etat,Bateau.BateauType.CARGO)
        self.cargaisonMax = 10
        self.vitesse = 1
        self.b1.evolue()
        self.cargaisonMax = 10
        self.vitesse = 2
        self.assertTrue(self.b1.etat,Bateau.BateauType.VOILIER)

    def test_deplacer(self):
        self.b1.deplacer(self.a2)
        self.assertEqual(self.a1.bateau,0)
        self.assertEqual(self.a2.bateau,self.b1)
        self.assertEqual(self.b1.position,self.a2)

    def test_est_proche(self):
        t = Terre("",[self.h1],[self.h2])
        
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an2)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an3)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an4)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an5)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an6)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an7)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an8)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an9)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an10)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an11)
        self.assertFalse(self.b2.est_proche(t))

        self.b2.evolue()
        self.b2.evolue()
        
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an2)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an3)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an4)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an5)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an6)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an7)
        self.assertTrue(self.b2.est_proche(t))
        self.b2.deplacer(self.an8)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an9)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an10)
        self.assertFalse(self.b2.est_proche(t))
        self.b2.deplacer(self.an11)
        self.assertTrue(self.b2.est_proche(t))
        
        
class TestVoleur(unittest.TestCase):
    def setUp(self):
        self.i1 = Intersection(1)
        self.i2 = Intersection(2)
        self.i3 = Intersection(3)
        self.i4 = Intersection(4)
        self.i5 = Intersection(5)
        self.i6 = Intersection(6)
        self.i7 = Intersection(7)
        self.i8 = Intersection(8)
        self.i9 = Intersection(9)
        self.i10 = Intersection(10)
        self.i11 = Intersection(11)
        self.i12 = Intersection(12)
        self.i13 = Intersection(13)
        self.i14 = Intersection(14)
        self.i15 = Intersection(15)
        self.i16 = Intersection(16)
        self.i17 = Intersection(17)
        self.i18 = Intersection(18)
        self.i19 = Intersection(19)
        self.h1 = Hexagone(self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0)
        self.h2 = Hexagone(self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)
        self.h3 = Hexagone(self.i2,self.i3,self.i11,self.i12,self.i13,self.i7,HexaType.ARGILE,6)
        self.h4 = Hexagone(self.i7,self.i13,self.i14,self.i15,self.i16,self.i8,HexaType.BOIS,12)
        self.h5 = Hexagone(self.i8,self.i9,self.i17,self.i18,self.i19,self.i16,HexaType.MER,0)
        self.v1 = Voleur(self.h1, Voleur.VoleurType.PIRATE)
        self.v2 = Voleur(self.h2, Voleur.VoleurType.BRIGAND)
 

    def test_absence(self):
        self.assertEqual(self.h1.voleur,self.v1)
        self.assertEqual(self.v1.position,self.h1)
        self.assertEqual(self.h2.voleur,self.v2)
        self.assertEqual(self.v2.position,self.h2)
        self.assertEqual(self.h3.voleur,0)
        self.assertEqual(self.h4.voleur,0)
        self.assertEqual(self.h5.voleur,0)
    
    def test_deplacer(self):
        self.v1.deplacer(self.h5)
        self.v2.deplacer(self.h3)
        self.assertEqual(self.h5.voleur,self.v1)
        self.assertEqual(self.v1.position,self.h5)
        self.assertEqual(self.h3.voleur,self.v2)
        self.assertEqual(self.v2.position,self.h3)
        self.assertEqual(self.h1.voleur,0)
        self.assertEqual(self.h2.voleur,0)
        self.assertEqual(self.h4.voleur,0)


unittest.main()
