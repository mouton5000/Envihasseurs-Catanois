# *-* coding: iso-8859-1 *-*
import unittest
from arbre_action import *
import redis

REDIS = redis.StrictRedis()

class TestArbreAction(unittest.TestCase):

    def setUp(self):
        REDIS.flushdb()
        self.j1 = Joueur(1)

    def test_first_root(self):
        n =self.j1.setNewRoot()
        nu = NodeCst.NULL
        self.assert_node(n,nu,nu,nu,nu,nu,n,self.j1)

    def test_add_child(self):
        n =self.j1.setNewRoot()
        nu = NodeCst.NULL

        n1 = n.addChild()
        n2 = n.addChild()
        n4 = n1.addChild()
        n5 = n2.addChild()
        n6 = n2.addChild()
        n3 = n.addChild()
        n7 = n3.addChild()
        n8 = n3.addChild()
        n10 = n8.addChild()
        n9 = n3.addChild()
        n11 = n8.addChild()

        # On obtient l'arbre ci contre :
        # 
        #           0 
        #    1      2          3
        #    4     5 6     7   8   9
        #                    10 11

        
        self.assert_node(n,n1,nu,nu,nu,n3,n,self.j1)
        self.assert_node(n1,n4,n,n2,nu,n4,n,self.j1)
        self.assert_node(n2,n5,n,n3,n1,n6,n,self.j1)
        self.assert_node(n3,n7,n,nu,n2,n9,n,self.j1)
        self.assert_node(n4,nu,n1,nu,nu,nu,n,self.j1)
        self.assert_node(n5,nu,n2,n6,nu,nu,n,self.j1)
        self.assert_node(n6,nu,n2,nu,n5,nu,n,self.j1)
        self.assert_node(n7,nu,n3,n8,nu,nu,n,self.j1)
        self.assert_node(n8,n10,n3,n9,n7,n11,n,self.j1)
        self.assert_node(n9,nu,n3,nu,n8,nu,n,self.j1)
        self.assert_node(n10,nu,n8,n11,nu,nu,n,self.j1)
        self.assert_node(n11,nu,n8,nu,n10,nu,n,self.j1)

    def test_add_first_child(self):
        n =self.j1.setNewRoot()
        nu = NodeCst.NULL

        n3 = n.addFirstChild()
        n8 = n3.addChild()


        n2 = n.addFirstChild()
        n7 = n3.addFirstChild()
        n1 = n.addFirstChild()
        n4 = n1.addFirstChild()
        n9 = n3.addChild()
        n6 = n2.addFirstChild()
        n5 = n2.addFirstChild()
        n11 = n8.addChild()
        n10 = n8.addFirstChild()


        # On obtient l'arbre ci contre :
        # 
        #           0 
        #    1      2          3
        #    4     5 6     7   8   9
        #                    10 11

        
        self.assert_node(n,n1,nu,nu,nu,n3,n,self.j1)
        self.assert_node(n1,n4,n,n2,nu,n4,n,self.j1)
        self.assert_node(n2,n5,n,n3,n1,n6,n,self.j1)
        self.assert_node(n3,n7,n,nu,n2,n9,n,self.j1)
        self.assert_node(n4,nu,n1,nu,nu,nu,n,self.j1)
        self.assert_node(n5,nu,n2,n6,nu,nu,n,self.j1)
        self.assert_node(n6,nu,n2,nu,n5,nu,n,self.j1)
        self.assert_node(n7,nu,n3,n8,nu,nu,n,self.j1)
        self.assert_node(n8,n10,n3,n9,n7,n11,n,self.j1)
        self.assert_node(n9,nu,n3,nu,n8,nu,n,self.j1)
        self.assert_node(n10,nu,n8,n11,nu,nu,n,self.j1)
        self.assert_node(n11,nu,n8,nu,n10,nu,n,self.j1)

    def test_add_sibling(self):
        n =self.j1.setNewRoot()
        nu = NodeCst.NULL

        n1 = n.addChild()
        n2 = n1.addSibling()
        n3 = n2.addSibling()
        n4 = n1.addChild()
        n5 = n2.addChild()
        n6 = n5.addSibling()
        n9 = n3.addChild()
        n7 = n3.addFirstChild()
        n8 = n7.addSibling()
        n10 = n8.addChild()
        n12 = n8.addChild()
        n11 = n10.addSibling()

        # On obtient l'arbre ci contre :
        # 
        #           0 
        #    1      2            3
        #    4     5 6     7     8     9
        #                     10 11 12

        
        self.assert_node(n,n1,nu,nu,nu,n3,n,self.j1)
        self.assert_node(n1,n4,n,n2,nu,n4,n,self.j1)
        self.assert_node(n2,n5,n,n3,n1,n6,n,self.j1)
        self.assert_node(n3,n7,n,nu,n2,n9,n,self.j1)
        self.assert_node(n4,nu,n1,nu,nu,nu,n,self.j1)
        self.assert_node(n5,nu,n2,n6,nu,nu,n,self.j1)
        self.assert_node(n6,nu,n2,nu,n5,nu,n,self.j1)
        self.assert_node(n7,nu,n3,n8,nu,nu,n,self.j1)
        self.assert_node(n8,n10,n3,n9,n7,n12,n,self.j1)
        self.assert_node(n9,nu,n3,nu,n8,nu,n,self.j1)
        self.assert_node(n10,nu,n8,n11,nu,nu,n,self.j1)
        self.assert_node(n11,nu,n8,n12,n10,nu,n,self.j1)
        self.assert_node(n12,nu,n8,nu,n11,nu,n,self.j1)
    
    def test_remove(self):
        n =n1 = self.j1.setNewRoot()
        nu = NodeCst.NULL

        n2 = n1.addChild()
        n3 = n1.addChild()
        n4 = n1.addChild()
        

        n5 = n3.addChild()
        n6 = n3.addChild()
        
        n7 = n6.addChild()
        n8 = n6.addChild()
        n9 = n6.addChild()
 
        n10 = n8.addChild()
        n11 = n8.addChild()
        n12 = n8.addChild()
        
        n13 = n2.addChild()
        n14 = n2.addChild()

        # On obtient l'arbre ci contre :
        # 
        #           0 
        #    1      2            3
        #    4     5 6     7     8     9
        #                     10 11 12

        
        n11.removeNode()

        self.assert_node(n1,n2,nu,nu,nu,n4,n1,self.j1)
        self.assert_node(n2,n13,n1,n3,nu,n14,n1,self.j1)
        self.assert_node(n3,n5,n1,n4,n2,n6,n1,self.j1)
        self.assert_node(n4,nu,n1,nu,n3,nu,n1,self.j1)
        self.assert_node(n5,nu,n3,n6,nu,nu,n1,self.j1)
        self.assert_node(n6,n7,n3,nu,n5,n9,n1,self.j1)
        self.assert_node(n7,nu,n6,n8,nu,nu,n1,self.j1)
        self.assert_node(n8,n10,n6,n9,n7,n12,n1,self.j1)
        self.assert_node(n9,nu,n6,nu,n8,nu,n1,self.j1)
        self.assert_node(n10,nu,n8,n12,nu,nu,n1,self.j1)
        self.assert_node(n12,nu,n8,nu,n10,nu,n1,self.j1)
        self.assert_node(n13,nu,n2,n14,nu,nu,n1,self.j1)
        self.assert_node(n14,nu,n2,nu,n13,nu,n1,self.j1)
        
        n8.removeNode()

        self.assert_node(n1,n2,nu,nu,nu,n4,n1,self.j1)
        self.assert_node(n2,n13,n1,n3,nu,n14,n1,self.j1)
        self.assert_node(n3,n5,n1,n4,n2,n6,n1,self.j1)
        self.assert_node(n4,nu,n1,nu,n3,nu,n1,self.j1)
        self.assert_node(n5,nu,n3,n6,nu,nu,n1,self.j1)
        self.assert_node(n6,n7,n3,nu,n5,n9,n1,self.j1)
        self.assert_node(n7,nu,n6,n10,nu,nu,n1,self.j1)
        self.assert_node(n9,nu,n6,nu,n12,nu,n1,self.j1)
        self.assert_node(n10,nu,n6,n12,n7,nu,n1,self.j1)
        self.assert_node(n12,nu,n6,n9,n10,nu,n1,self.j1)
        self.assert_node(n13,nu,n2,n14,nu,nu,n1,self.j1)
        self.assert_node(n14,nu,n2,nu,n13,nu,n1,self.j1)
        

        n9.removeNode()

        self.assert_node(n1,n2,nu,nu,nu,n4,n1,self.j1)
        self.assert_node(n2,n13,n1,n3,nu,n14,n1,self.j1)
        self.assert_node(n3,n5,n1,n4,n2,n6,n1,self.j1)
        self.assert_node(n4,nu,n1,nu,n3,nu,n1,self.j1)
        self.assert_node(n5,nu,n3,n6,nu,nu,n1,self.j1)
        self.assert_node(n6,n7,n3,nu,n5,n12,n1,self.j1)
        self.assert_node(n7,nu,n6,n10,nu,nu,n1,self.j1)
        self.assert_node(n10,nu,n6,n12,n7,nu,n1,self.j1)
        self.assert_node(n12,nu,n6,nu,n10,nu,n1,self.j1)
        self.assert_node(n13,nu,n2,n14,nu,nu,n1,self.j1)
        self.assert_node(n14,nu,n2,nu,n13,nu,n1,self.j1)
        

        n7.removeNode()

        self.assert_node(n1,n2,nu,nu,nu,n4,n1,self.j1)
        self.assert_node(n2,n13,n1,n3,nu,n14,n1,self.j1)
        self.assert_node(n3,n5,n1,n4,n2,n6,n1,self.j1)
        self.assert_node(n4,nu,n1,nu,n3,nu,n1,self.j1)
        self.assert_node(n5,nu,n3,n6,nu,nu,n1,self.j1)
        self.assert_node(n6,n10,n3,nu,n5,n12,n1,self.j1)
        self.assert_node(n10,nu,n6,n12,nu,nu,n1,self.j1)
        self.assert_node(n12,nu,n6,nu,n10,nu,n1,self.j1)
        self.assert_node(n13,nu,n2,n14,nu,nu,n1,self.j1)
        self.assert_node(n14,nu,n2,nu,n13,nu,n1,self.j1)
        

        n3.removeNode()

        self.assert_node(n1,n2,nu,nu,nu,n4,n1,self.j1)
        self.assert_node(n2,n13,n1,n5,nu,n14,n1,self.j1)
        self.assert_node(n4,nu,n1,nu,n6,nu,n1,self.j1)
        self.assert_node(n5,nu,n1,n6,n2,nu,n1,self.j1)
        self.assert_node(n6,n10,n1,n4,n5,n12,n1,self.j1)
        self.assert_node(n10,nu,n6,n12,nu,nu,n1,self.j1)
        self.assert_node(n12,nu,n6,nu,n10,nu,n1,self.j1)
        self.assert_node(n13,nu,n2,n14,nu,nu,n1,self.j1)
        self.assert_node(n14,nu,n2,nu,n13,nu,n1,self.j1)
        

        n2.removeNode()

        self.assert_node(n1,n13,nu,nu,nu,n4,n1,self.j1)
        self.assert_node(n4,nu,n1,nu,n6,nu,n1,self.j1)
        self.assert_node(n5,nu,n1,n6,n14,nu,n1,self.j1)
        self.assert_node(n6,n10,n1,n4,n5,n12,n1,self.j1)
        self.assert_node(n10,nu,n6,n12,nu,nu,n1,self.j1)
        self.assert_node(n12,nu,n6,nu,n10,nu,n1,self.j1)
        self.assert_node(n13,nu,n1,n14,nu,nu,n1,self.j1)
        self.assert_node(n14,nu,n1,n5,n13,nu,n1,self.j1)


    def assert_node(self, n, nN, fN, sN, pSN, lCN, r, p):
        ''' Vérifie si pour le noeud n, son premier fils est nN, son pere est fN, son frere droit est sN, son frere gauche est pSN, sont dernier fils est lCN, sa racine est r et son joueuer est p'''

        self.assertEqual(n.getFirstChild(),nN)
        self.assertEqual(n.getFatherNode(),fN)
        self.assertEqual(n.getSiblingNode(),sN)
        self.assertEqual(n.getPSiblingNode(),pSN)
        self.assertEqual(n.getLastChildNode(),lCN)
        self.assertEqual(n.getRoot(),r)
        self.assertEqual(n.getPlayer(),p)
        


if __name__ == '__main__':
    unittest.main()
