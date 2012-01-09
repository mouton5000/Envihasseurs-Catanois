import unittest
from plateau import *

class TestCarte(unittest.TestCase):
    def setUp(self):
        pass

class TestIntersection(unittest.TestCase):
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
        self.h1 = Hexagone(self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0,CommerceType.BOIS,[self.i1,self.i2])
        self.h2 = Hexagone(self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)
        self.h3 = Hexagone(self.i2,self.i3,self.i11,self.i12,self.i13,self.i7,HexaType.ARGILE,6,CommerceType.TOUS,[self.i2,self.i3,self.i11,self.i12,self.i13,self.i7])
        self.h4 = Hexagone(self.i7,self.i13,self.i14,self.i15,self.i16,self.i8,HexaType.BOIS,12)
        self.a1 = self.h2.liens[0]
        self.a2 = self.h2.liens[1]
        self.a3 = self.h2.liens[2]

#
#   5  4
# 6      3  11
#   1  2       12
# 10     7  13
#    9 8       14
#        16 15
# 

    def test_dist(self):
        self.assertEqual(self.i1.dist(self.i1),0)
        self.assertEqual(self.i1.dist(self.i2),1)
        self.assertEqual(self.i1.dist(self.i3),2)
        self.assertEqual(self.i1.dist(self.i4),3)
        self.assertEqual(self.i1.dist(self.i14),4)
        self.assertEqual(self.i1.dist(self.i16),4)
        self.assertEqual(self.i3.dist(self.i10),3)
        self.assertEqual(self.i6.dist(self.i11),4)
        self.assertEqual(self.i13.dist(self.i14),1)
        self.assertEqual(self.i16.dist(self.i5),6)

    def test_num(self):
        self.assertEqual(self.i1.num,1)
        self.assertEqual(self.i2.num,2)

    def test_str(self):
        self.assertEqual(str(self.i1),"1")
        self.assertEqual(str(self.i2),"2")

    def test_genType(self):
        self.assertTrue(self.i1.isCotier())
        self.assertTrue(self.i2.isCotier())
        self.assertTrue(self.i4.isMaritime())
        self.assertTrue(self.i6.isMaritime())
        self.assertTrue(self.i9.isTerrestre())
        self.assertFalse(self.i1.isTerrestre())
        self.assertFalse(self.i2.isTerrestre())
        self.assertFalse(self.i4.isTerrestre())
        self.assertFalse(self.i6.isTerrestre())
        self.assertFalse(self.i9.isCotier())
        self.assertFalse(self.i1.isMaritime())
        self.assertFalse(self.i2.isMaritime())
        self.assertFalse(self.i4.isCotier())
        self.assertFalse(self.i6.isCotier())
        self.assertFalse(self.i9.isMaritime())

#        self.h1 = Hexagone(self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0,CommerceType.BOIS,[self.i1,self.i2])
#        self.h2 = Hexagone(self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)
#        self.h3 = Hexagone(self.i2,self.i3,self.i11,self.i12,self.i13,self.i7,HexaType.ARGILE,6,CommerceType.TOUS,[self.i2,self.i3,self.i11,self.i12,self.i13,self.i7])

    def test_ports(self):
        self.assertTrue(self.i1.isPort())
        self.assertTrue(self.i2.isPort())
        self.assertTrue(self.i2.isMarche())
        self.assertTrue(self.i2.isMarche())
        self.assertTrue(self.i11.isMarche())
        self.assertTrue(self.i12.isMarche())
        self.assertTrue(self.i13.isMarche())
        self.assertTrue(self.i7.isMarche())



class TestArrete(unittest.TestCase):
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
        self.a1 = self.i1.lien(self.i2)
        self.a2 = self.i4.lien(self.i5)
        self.a3 = self.i8.lien(self.i9)


    def test_str(self):
        self.assertEqual(str(self.a1),"1--2")

    def test_genType(self):
        self.assertTrue(self.a1.isCotier())
        self.assertTrue(self.a2.isMaritime())
        self.assertTrue(self.a3.isTerrestre())
        self.assertFalse(self.a1.isTerrestre())
        self.assertFalse(self.a2.isCotier())
        self.assertFalse(self.a3.isMaritime())
        self.assertFalse(self.a1.isMaritime())
        self.assertFalse(self.a2.isTerrestre())
        self.assertFalse(self.a3.isCotier())

#
#   5  4
# 6      3  11
#   1  2       12
# 10     7  13
#    9 8       14
#        16 15
# 


    def test_dist(self):
        a1 = self.i1.lien(self.i2)
        a2 = self.i3.lien(self.i2)
        a3 = self.i5.lien(self.i6)
        a4 = self.i14.lien(self.i15)

        a = self.i7.lien(self.i13)
        l = [self.i13.lien(self.i14), self.i14.lien(self.i15), self.i7.lien(self.i8),self.i8.lien(self.i16),self.i8.lien(self.i9),self.i7.lien(self.i2),self.i2.lien(self.i1),self.i2.lien(self.i3),self.i13.lien(self.i12),self.i12.lien(self.i11)]
        self.assertTrue(a1.dist(a2),1)
        self.assertTrue(a1.dist(a3),2)
        self.assertTrue(a1.dist(a4),4)
        self.assertTrue(a2.dist(a1),1)
        self.assertTrue(a2.dist(a3),3)
        self.assertTrue(a2.dist(a4),4)
        self.assertTrue(a3.dist(a1),2)
        self.assertTrue(a3.dist(a2),3)
        self.assertTrue(a3.dist(a4),6)
        self.assertTrue(a4.dist(a1),4)
        self.assertTrue(a4.dist(a2),4)
        self.assertTrue(a4.dist(a3),6)
        self.assertTrue(a.doubleNeighb(),l)



class TestHexagone(unittest.TestCase):
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
        self.h1 = Hexagone(self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,HexaType.MER,0)
        self.h2 = Hexagone(self.i1,self.i2,self.i7,self.i8,self.i9,self.i10,HexaType.BOIS,12)

    def test_str(self):
         self.assertEqual(str(self.h1),"mer,0,1--2--3--4--5--6")
         self.assertEqual(str(self.h2),"bois,12,1--2--7--8--9--10")

    def test_hexa(self):
         self.assertEqual(self.i1.hexagones,[self.h1, self.h2])
         self.assertEqual(self.h1.liens[0].hexagones,[self.h1, self.h2])

    def test_genType(self):
         self.assertTrue(self.h1.isMaritimeCotier())
         self.assertTrue(self.h2.isTerrestreCotier())
         self.assertFalse(self.h1.isTerrestre())
         self.assertFalse(self.h1.isMaritime())
         self.assertFalse(self.h2.isTerrestre())
         self.assertFalse(self.h2.isMaritime())

unittest.main()
