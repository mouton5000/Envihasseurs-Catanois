import unittest
from cartes import *

class TestCartesRessources(unittest.TestCase):
    def setUp(self):
        self.c0 = CartesRessources(0,0,0,0,0)
        self.c1 = Cartes.ARGILE
        self.c2 = Cartes.BLE
        self.c3 = Cartes.BOIS
        self.c4 = Cartes.CAILLOU
        self.c5 = Cartes.MOUTON
    
    def test_add(self):
        c = CartesRessources(1,3,2,1,2)
        self.assertEqual(self.c1 + self.c2 + self.c2 + self.c2 + self.c3 + self.c3 + self.c4 + self.c5 + self.c5,c)

    def test_sub(self):
        c = CartesRessources(0,-1,0,-2,0)
        self.assertEqual(self.c0 - self.c2 - self.c4 - self.c4,c)

    def test_mult(self):
        c = CartesRessources(3,2,-1,2,3)
        self.assertEqual(self.c1*3 + self.c2*2 + self.c3*(-1) + self.c4*2 + self.c5*3,c)


class TestCartesDeveloppement(unittest.TestCase):
    def setUp(self):
        self.c0 = CartesDeveloppement(0,0,0,0,0)
        self.c1 = Cartes.CHEVALLIER
        self.c2 = Cartes.MONOPOLE
        self.c3 = Cartes.POINT_VICTOIRE
        self.c4 = Cartes.DECOUVERTE
        self.c5 = Cartes.CONSTRUCTION_ROUTES
    
    def test_add(self):
        c = CartesDeveloppement(1,3,2,1,2)
        self.assertEqual(self.c1 + self.c2 + self.c2 + self.c2 + self.c3 + self.c3 + self.c4 + self.c5 + self.c5,c)

    def test_sub(self):
        c = CartesDeveloppement(0,-1,0,-2,0)
        self.assertEqual(self.c0 - self.c2 - self.c4 - self.c4,c)

    def test_mult(self):
        c = CartesDeveloppement(3,2,-1,2,3)
        self.assertEqual(self.c1*3 + self.c2*2 + self.c3*(-1) + self.c4*2 + self.c5*3,c)

class TestCartesGeneral(unittest.TestCase):
    def setUp(self):
        self.c0 = Cartes.RIEN
        self.c1 = Cartes.CHEVALLIER
        self.c2 = Cartes.MONOPOLE
        self.c3 = Cartes.POINT_VICTOIRE
        self.c4 = Cartes.DECOUVERTE
        self.c5 = Cartes.CONSTRUCTION_ROUTES

        self.c6 = Cartes.ARGILE
        self.c7 = Cartes.BLE
        self.c8 = Cartes.BOIS
        self.c9 = Cartes.CAILLOU
        self.c10 = Cartes.MOUTON
      
    def test_ineq(self):
        self.assertFalse(self.c0 < self.c1)
        self.assertFalse(self.c0 < self.c2)
        self.assertFalse(self.c0 < self.c3)
        self.assertFalse(self.c0 < self.c4)
        self.assertFalse(self.c0 < self.c5)
        self.assertFalse(self.c0 < self.c6)
        self.assertFalse(self.c0 < self.c7)
        self.assertFalse(self.c0 < self.c8)
        self.assertFalse(self.c0 < self.c9)
        self.assertFalse(self.c0 < self.c10)
        self.assertTrue(self.c0 <= self.c1)
        self.assertTrue(self.c0 <= self.c2)
        self.assertTrue(self.c0 <= self.c3)
        self.assertTrue(self.c0 <= self.c4)
        self.assertTrue(self.c0 <= self.c5)
        self.assertTrue(self.c0 <= self.c6)
        self.assertTrue(self.c0 <= self.c7)
        self.assertTrue(self.c0 <= self.c8)
        self.assertTrue(self.c0 <= self.c9)
        self.assertTrue(self.c0 <= self.c10)
        self.assertFalse(self.c0 > self.c1 * -1)
        self.assertFalse(self.c0 > self.c2 * -1)
        self.assertFalse(self.c0 > self.c3 * -1)
        self.assertFalse(self.c0 > self.c4 * -1)
        self.assertFalse(self.c0 > self.c5 * -1)
        self.assertFalse(self.c0 > self.c6 * -1)
        self.assertFalse(self.c0 > self.c7 * -1)
        self.assertFalse(self.c0 > self.c8 * -1)
        self.assertFalse(self.c0 > self.c9 * -1)
        self.assertFalse(self.c0 > self.c10 * -1)
        self.assertTrue(self.c0 >= self.c1 * -1)
        self.assertTrue(self.c0 >= self.c2 * -1)
        self.assertTrue(self.c0 >= self.c3 * -1)
        self.assertTrue(self.c0 >= self.c4 * -1)
        self.assertTrue(self.c0 >= self.c5 * -1)
        self.assertTrue(self.c0 >= self.c6 * -1)
        self.assertTrue(self.c0 >= self.c7 * -1)
        self.assertTrue(self.c0 >= self.c8 * -1)
        self.assertTrue(self.c0 >= self.c9 * -1)
        self.assertTrue(self.c0 >= self.c10 * -1)
        self.assertFalse(self.c1< self.c3)
        self.assertFalse(self.c2< self.c1)
        self.assertFalse(self.c3< self.c5)
        self.assertFalse(self.c4< self.c6)
        self.assertFalse(self.c5< self.c8)
        self.assertFalse(self.c6< self.c10)
        self.assertFalse(self.c1<= self.c3)
        self.assertFalse(self.c2<= self.c1)
        self.assertFalse(self.c3<= self.c5)
        self.assertFalse(self.c4<= self.c6)
        self.assertFalse(self.c5<= self.c8)
        self.assertFalse(self.c6<= self.c10)
       
unittest.main()
