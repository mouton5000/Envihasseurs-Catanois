import unittest
from cartes import *
from constructions import *
from plateau import *
from joueurs import *
import redis

REDIS = redis.StrictRedis()

class TestColonie(unittest.TestCase):
    def setUp(self):
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
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
        plateau.intersections = [self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8, self.i9, self.i10, self.i11, self.i12, self.i13, self.i14, self.i15, self.i16]
        self.h1 = Hexagone(1,self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0)
        self.h2 = Hexagone(2,self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)
        self.h3 = Hexagone(3,self.i2,self.i3,self.i11,self.i12,self.i13,self.i7,HexaType.ARGILE,6)
        self.h4 = Hexagone(4,self.i7,self.i13,self.i14,self.i15,self.i16,self.i8,HexaType.BOIS,12)

        plateau.hexagones = [self.h1,self.h2,self.h3,self.h4]
        self.t1 = Terre(1,'Antaria',[self.h2,self.h3,self.h4],[self.h1])
        plateau.terres = [self.t1]


        self.a1 = self.h2.liens[0]
        self.a2 = self.h2.liens[1]
        self.a3 = self.h2.liens[2]
        self.j1 = 1

        self.c1 = Colonie(self.j1,self.i1)
        self.c2 = Colonie(self.j1,self.i7)

        self.c1.save()
        self.c2.save()

    def test_bdd(self):
        self.assertTrue(REDIS.exists('I1:colonie'))
        self.assertTrue(REDIS.exists('I7:colonie'))
        self.assertFalse(REDIS.exists('I2:colonie'))
        self.assertEqual(REDIS.get('I1:colonie'),'1')
        self.assertEqual(REDIS.get('I1:isVille'),'False')
        self.assertEqual(REDIS.smembers('J1:colonies'),set(['1','7']))
        self.assertEqual(REDIS.smembers('J1:villes'),set([]))

        c = Colonie.getColonie(self.i2)
        self.assertEqual(c,0)
        c = Colonie.getColonie(self.i1)
        self.assertEqual(c.joueur,self.j1)
        self.assertEqual(c.isVille,False)
        self.assertEqual(c.position,self.i1)


    def test_evolution(self):
        self.assertFalse(self.c1.isVille)
        self.c1.evolue()
        self.assertTrue(self.c1.isVille)
        self.c1.save()
        self.assertTrue(REDIS.exists('I1:colonie'))
        self.assertEqual(REDIS.get('I1:colonie'),'1')
        self.assertEqual(REDIS.get('I1:isVille'),'True')
        self.assertEqual(REDIS.smembers('J1:colonies'),set(['7']))
        self.assertEqual(REDIS.smembers('J1:villes'),set(['1']))

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
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
        self.i1 = Intersection(1)
        self.i2 = Intersection(2)
        self.i3 = Intersection(3)
        self.i4 = Intersection(4)
        self.i5 = Intersection(5)
        self.i6 = Intersection(6)
        plateau.intersections = [self.i1, self.i2, self.i3, self.i4, self.i5, self.i6]

        self.a1 = Arrete(1,self.i1,self.i2)
        self.a2 = Arrete(2,self.i2,self.i3)
        self.a3 = Arrete(3,self.i3,self.i1)
        plateau.arretes = [self.a1,self.a2,self.a3]

        self.j1 = 1

        self.c1 = Colonie(self.j1,self.i1)
        self.c1.save()

        self.r1 = Route(self.j1,self.a1)
        self.r1.save()
        
    def test_bdd(self):
        self.assertTrue(REDIS.exists('A1:route'))
        self.assertTrue(REDIS.exists('J1:routes'))
        self.assertFalse(REDIS.exists('A2:route'))
        self.assertFalse(REDIS.exists('A3:route'))
        self.assertEqual(REDIS.get('A1:route'),'1')
        self.assertEqual(REDIS.smembers('J1:routes'),set(['1']))

        r = Route.getRoute(self.a2)
        self.assertEqual(r,0)
        r = Route.getRoute(self.a1)
        self.assertEqual(r.joueur,1)
        self.assertEqual(r.position, Plateau.getPlateau().ar(1))

    def test_est_extremite(self):
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
        i1 = Intersection(1)
        i2 = Intersection(2)
        i3 = Intersection(3)
        i4 = Intersection(4)
        i5 = Intersection(5)
        i6 = Intersection(6)
        a1 = Arrete(1,i1,i2)
        a2 = Arrete(2,i3,i2)
        a3 = Arrete(3,i2,i4)
        a4 = Arrete(4,i4,i5)
        a5 = Arrete(5,i4,i6)

        i10 = Intersection(10)
        i11 = Intersection(11)
        a = Arrete(6,i10,i11)
        plateau.intersections = [i1, i2, i3, i4, i5, i6,i10,i11]
        plateau.arretes = [a1,a2,a3,a4,a5,a]

        j1 = 1
        j2 = 2

        r1 = Route(j1,a1)
        r2 = Route(j1,a2)
        r3 = Route(j1,a3)
        r4 = Route(j1,a4)
        r5 = Route(j1,a5)

        r1.save()
        r2.save()
        r3.save()
        r4.save()
        r5.save()

        self.assertFalse(r3.est_extremite())
        c1 = Colonie(j1,i2)
        c1.save()     
        self.assertFalse(r3.est_extremite())
        c2 = Colonie(j1,i4)
        c2.save()        
        self.assertFalse(r3.est_extremite())

        REDIS.flushdb()
        r1.save()
        r2.save()
        r3.save()
        r4.save()
        r5.save()

        c3 = Colonie(j2,i2)
        c3.save()
        self.assertTrue(r3.est_extremite())

        c4 = Colonie(j2,i4)
        c4.save()
        self.assertTrue(r3.est_extremite())

        REDIS.flushdb()
        r2.save()
        r3.save()
        r4.save()
        r5.save()

        self.assertFalse(r3.est_extremite())

        REDIS.flushdb()
        r2.save()
        r3.save()
        r5.save()
        
        self.assertFalse(r3.est_extremite())

        REDIS.flushdb()
        r3.save()
        r5.save()
        self.assertTrue(r3.est_extremite())

        REDIS.flushdb()
        r3.save()
        self.assertTrue(r3.est_extremite())

        REDIS.flushdb()
        r1.save()
        r2.save()
        r3.save()
        r6 = Route(j2,a4)
        r6.save()
        self.assertTrue(r3.est_extremite())

        r7 = Route(j2,a5)
        r7.save()
        self.assertTrue(r3.est_extremite())

        REDIS.flushdb()
        r6.save()
        r7.save()
        r3.save()
        r8 = Route(j2,a1)
        r9 = Route(j2,a2)
        r8.save()
        r9.save()
        self.assertTrue(r3.est_extremite())

    def test_route_la_plus_longue(self):
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
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
        
        plateau.intersections = [i1, i2, i3, i4, i5, i6,i7,i8,i9,i10,i11,i12,i13,i14]

        h1 = Hexagone(1,i1,i2,i3,i4,i5,i6,HexaType.CAILLOU,6)
        h2 = Hexagone(2,i4,i7,i8,i9,i10,i5,HexaType.BOIS,9)
        h3 = Hexagone(3,i7,i11,i12,i13,i14,i8,HexaType.DESERT,0)
        plateau.hexagones = [h1, h2, h3]

        j1 = 1

        a1 = i3.lien(i4)
        a2 = i6.lien(i5)
        a3 = i5.lien(i4)
        a4 = i4.lien(i7)
        a5 = i7.lien(i11)
        a6 = i11.lien(i12)
        a7 = i7.lien(i8)
        a8 = i8.lien(i14)
        a9 = i14.lien(i13)
        a10 = i6.lien(i1)
        a11 = i2.lien(i1)
        a12 = i2.lien(i3)
        a13 = i10.lien(i5)
        a14 = i10.lien(i9)
        a15 = i9.lien(i8)
        a16 = i13.lien(i12)

        a1.num = 1
        a2.num = 2
        a3.num = 3
        a4.num = 4
        a5.num = 5
        a6.num = 6
        a7.num = 7
        a8.num = 8
        a9.num = 9
        a10.num = 10
        a11.num = 11
        a12.num = 12
        a13.num = 13
        a14.num = 14
        a15.num = 15
        a16.num = 16
        plateau.arretes = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16]

        r1 = Route(j1,a1)
        r2 = Route(j1,a2)
        r3 = Route(j1,a3)
        r4 = Route(j1,a4)
        r5 = Route(j1,a5)
        r6 = Route(j1,a6)
        r7 = Route(j1,a7)
        r8 = Route(j1,a8)
        r9 = Route(j1,a9)

        r1.save()
        r2.save()
        r3.save()
        r4.save()
        r5.save()
        r6.save()
        r7.save()
        r8.save()
        r9.save()

        self.assertEqual(r1.rlplfr(),5) 
        self.assertEqual(r2.rlplfr(),6) 
        self.assertEqual(r4.rlplfr(),4) 


class TestBateau(unittest.TestCase):
    def setUp(self):
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
        j1 = 1

        self.i1 = Intersection(1)
        self.i2 = Intersection(2)
        self.i3 = Intersection(3)
        plateau.intersections = [self.i1,self.i2,self.i3]

        
        self.a1 = Arrete(1,self.i1,self.i2)
        self.a2 = Arrete(2,self.i2,self.i3)
        self.a3 = Arrete(3,self.i3,self.i1)
        plateau.arretes = [self.a1,self.a2,self.a3]        


        self.b1 = Bateau(1,j1,self.a1,Cartes.RIEN,Bateau.BateauType.TRANSPORT,False)
        self.b1.save()

    def test_bdd(self):
        self.assertTrue(REDIS.exists('B1:position'))
        self.assertTrue(REDIS.exists('A1:bateaux'))
        self.assertTrue(REDIS.exists('J1:transports'))
        self.assertTrue(REDIS.exists('J1:transports:positions'))
        self.assertFalse(REDIS.exists('A2:bateaux'))
        self.assertFalse(REDIS.exists('A3:bateaux'))
        self.assertFalse(REDIS.exists('J1:cargos'))
        self.assertFalse(REDIS.exists('J1:cargos:positions'))
        self.assertFalse(REDIS.exists('J1:voilliers'))
        self.assertFalse(REDIS.exists('J1:voilliers:positions'))
        self.assertTrue(REDIS.exists('B1:cargaison:argile'))

        self.assertEqual(REDIS.get('B1:position'),'1')
        self.assertEqual(REDIS.smembers('A1:bateaux'),set('1'))
        self.assertEqual(REDIS.smembers('J1:transports'),set('1'))
        self.assertEqual(REDIS.get('B1:cargaison:ble'),'0')
        self.assertEqual(REDIS.get('B1:aBouge'),'False')
        self.assertEqual(REDIS.get('B1:type'),Bateau.BateauType.TRANSPORT)
        self.assertEqual(REDIS.get('B1:joueur'),'1')

        b = Bateau.getBateau(2)
        self.assertEqual(b,0)
        b = Bateau.getBateau(1)
        self.assertEqual(b.num,1)
        self.assertEqual(b.position,Plateau.getPlateau().ar(1))
        self.assertEqual(b.joueur,1)
        self.assertEqual(b.etat,Bateau.BateauType.TRANSPORT)
        self.assertEqual(b.cargaison,Cartes.RIEN)
        self.assertEqual(b.aBouge,False)

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
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
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
        h1 = Hexagone(1,i1,i2,i3,i4,i5,i6,HexaType.CAILLOU,2)
        h2 = Hexagone(2,i3,i7,i8,i9,i10,i4,HexaType.MER,0)
        h3 = Hexagone(3,i8,i11,i12,i13,i14,i9,HexaType.MER,0)
        t = Terre(1,"Antaria",[h1],[h2,h3])
        
        a1 = i1.lien(i2)
        a2 = i2.lien(i3)
        a3 = i3.lien(i4)
        a4 = i4.lien(i5)
        a5 = i5.lien(i6)
        a6 = i6.lien(i1)
        a7 = i3.lien(i7)
        a8 = i7.lien(i8)
        a9 = i8.lien(i9)
        a10 = i9.lien(i10)
        a11 = i10.lien(i4)
        a12 = i8.lien(i11)
        a13 = i11.lien(i12)
        a14 = i12.lien(i13)
        a15 = i13.lien(i14)
        a16 = i14.lien(i9)

        a1.num = 1
        a2.num = 2
        a3.num = 3
        a4.num = 4
        a5.num = 5
        a6.num = 6
        a7.num = 7
        a8.num = 8
        a9.num = 9
        a10.num = 10
        a11.num = 11
        a12.num = 12
        a13.num = 13
        a14.num = 14
        a15.num = 15
        a16.num = 16
        plateau.arretes = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16]
        
        j1 = Joueur(1)
        b2 = Bateau(2,j1,a5,Cartes.RIEN,Bateau.BateauType.TRANSPORT,False)
       
 
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a3)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a11)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a8)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a9)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a10)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a12)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a13)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a14)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a15)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a16)
        self.assertFalse(b2.est_proche(t))

        b2.evolue()
        b2.evolue()
        
        b2.deplacer(a3)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a7)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a8)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a9)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a10)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a11)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a12)
        self.assertTrue(b2.est_proche(t))
        b2.deplacer(a13)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a14)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a15)
        self.assertFalse(b2.est_proche(t))
        b2.deplacer(a16)
        self.assertTrue(b2.est_proche(t))
        
        
class TestVoleur(unittest.TestCase):
    def setUp(self):
        REDIS.flushdb()
        plateau = Plateau.getPlateau()
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
        plateau.intersections = [self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,self.i7,self.i8,self.i9,self.i10,self.i11,self.i12,self.i13,self.i14,self.i15,self.i16,self.i17,self.i18,self.i19]
        self.h1 = Hexagone(1,self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0)
        self.h2 = Hexagone(2,self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)
        self.h3 = Hexagone(3,self.i2,self.i3,self.i11,self.i12,self.i13,self.i7,HexaType.ARGILE,6)
        self.h4 = Hexagone(4,self.i7,self.i13,self.i14,self.i15,self.i16,self.i8,HexaType.BOIS,12)
        self.h5 = Hexagone(5,self.i8,self.i9,self.i17,self.i18,self.i19,self.i16,HexaType.MER,0)

        plateau.hexagones = [self.h1,self.h2,self.h3,self.h4,self.h5]
        
        self.t = Terre(1,'Antaria',[self.h2,self.h3,self.h4],[self.h1,self.h5])
        plateau.terres = [self.t]

        self.v1 = Voleur(self.h1, Voleur.VoleurType.PIRATE,self.t)
        self.v2 = Voleur(self.h2, Voleur.VoleurType.BRIGAND,self.t)
        self.v1.save()
        self.v2.save()
         

    def test_bdd(self):
        self.assertTrue(REDIS.exists('T1:brigand:position'))
        self.assertTrue(REDIS.exists('T1:pirate:position'))
        print REDIS.get('T1:pirate:position')
        self.assertEqual(REDIS.get('T1:pirate:position'),'1')       
        self.assertEqual(REDIS.get('T1:brigand:position'),'2')       

 
        v1 = self.t.getPirate()
        v2 = self.t.getBrigand()
        self.assertNotEqual(v1,0)
        self.assertNotEqual(v2,0)
        self.assertEqual(v1.position, self.h1)
        self.assertEqual(v2.position, self.h2)
    
    def test_deplacer(self):
        self.v1.deplacer(self.h5)
        self.v2.deplacer(self.h3)
        self.assertEqual(self.v1.position,self.h5)
        self.assertEqual(self.v2.position,self.h3)


if __name__ == '__main__':
    unittest.main()
