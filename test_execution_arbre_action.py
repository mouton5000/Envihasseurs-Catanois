# *-* coding: iso-8859-1 *-*
import unittest
from arbre_action import *
from test_joueurs import *
import redis

REDIS = redis.StrictRedis()

class TestExecutionArbreAction(TestJoueur):

    def setUp(self):
        super(TestExecutionArbreAction,self).setUp()
        self.j1 = Joueur(1)
        self.n1 = self.j1.setNewRoot()
        self.n2 = self.n1.addChild()
        self.n3 = self.n2.addChild()
        self.n4 = self.n3.addChild()
        self.n5 = self.n1.addChild()
        self.n6 = self.n5.addChild()
        self.n7 = self.n6.addChild()
        self.n8 = self.n6.addChild()
        self.n9 = self.n5.addChild()
        self.n10 = self.n9.addChild()
        self.n11 = self.n9.addChild()
        self.n12 = self.n1.addChild()


        p = Plateau.getPlateau()
        Colonie(1,p.it(62)).save()
        Route(1,p.it(62).lien(p.it(72))).save()

        self.tg = Plateau.getPlateau().ter(1)

        j1 = JoueurPossible(1)
        j1.recevoir(self.tg,Tarifs.ROUTE * 100)


        self.a1 = p.it(62).lien(p.it(52))
        self.a2 = p.it(52).lien(p.it(53))
        self.a3 = p.it(53).lien(p.it(43))
        self.a4 = p.it(43).lien(p.it(33))
        self.a5 = p.it(43).lien(p.it(44))
        self.a6 = p.it(44).lien(p.it(34))
        self.a7 = p.it(72).lien(p.it(73))
        self.a8 = p.it(73).lien(p.it(63))
        self.a9 = p.it(63).lien(p.it(53))
        self.a10 = p.it(63).lien(p.it(64))
        self.a11 = p.it(64).lien(p.it(54))
        self.a12 = p.it(54).lien(p.it(55))
        self.a13 = p.it(64).lien(p.it(74))
        self.a14 = p.it(84).lien(p.it(83))
        self.a15 = p.it(84).lien(p.it(74))
        self.a16 = p.it(74).lien(p.it(75))
        self.a17 = p.it(75).lien(p.it(85))

        self.act1 = Action(1, 'construire_route', self.a1.num)
        self.act2 = Action(2, 'construire_route', self.a2.num)
        self.act3 = Action(3, 'construire_route', self.a3.num)
        self.act4 = Action(4, 'construire_route', self.a4.num)
        self.act5 = Action(5, 'construire_route', self.a5.num)
        self.act6 = Action(6, 'construire_route', self.a6.num)
        self.act7 = Action(7, 'construire_route', self.a7.num)
        self.act8 = Action(8, 'construire_route', self.a8.num)
        self.act9 = Action(9, 'construire_route', self.a9.num)
        self.act10 = Action(10, 'construire_route', self.a10.num)
        self.act11 = Action(11, 'construire_route', self.a11.num)
        self.act12 = Action(12, 'construire_route', self.a12.num)
        self.act13 = Action(13, 'construire_route', self.a13.num)
        self.act14 = Action(14, 'construire_route', self.a14.num)
        self.act15 = Action(15, 'construire_route', self.a15.num)
        self.act16 = Action(16, 'construire_route', self.a16.num)
        self.act17 = Action(17, 'construire_route', self.a17.num)

        self.ars = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9, self.a10, self.a11, self.a12, self.a13, self.a14, self.a15, self.a16, self.a17]

        self.act1.save()
        self.act2.save()
        self.act3.save()
        self.act4.save()
        self.act5.save()
        self.act6.save()
        self.act7.save()
        self.act8.save()
        self.act9.save()
        self.act10.save()
        self.act11.save()
        self.act12.save()
        self.act13.save()
        self.act14.save()
        self.act15.save()
        self.act16.save()
        self.act17.save()
        

        j1.set_route_la_plus_longue(self.tg,0)
        



 
    def test_parcour_vide(self):
        j1 = self.j1
        bdd = j1.executer()
        self.assertEquals(len(bdd.keys()),len(REDIS.keys()))


    def base_arbre(self):
        self.n2.addAction(self.act1)
        self.n2.addAction(self.act2)
        
        self.n4.addAction(self.act3)
        self.n4.addAction(self.act4)
        self.n4.addAction(self.act5)
        
        self.n5.addAction(self.act1)
        self.n5.addAction(self.act7)
        self.n5.addAction(self.act8)
        
        self.n6.addAction(self.act9)
        self.n6.addAction(self.act10)

        self.n7.addAction(self.act11)

        self.n8.addAction(self.act13)
        
        self.n9.addAction(self.act10)
        self.n9.addAction(self.act11)
        self.n9.addAction(self.act13)
        
        self.n10.addAction(self.act16)
        self.n10.addAction(self.act17)
        
        self.n11.addAction(self.act15)
        self.n11.addAction(self.act14)
        
        self.n12.addAction(self.act7)

    def check_ars(self, bools, bdd):
        for i in xrange(len(bools)):
                self.assertEqual(Route.hasRoute(self.ars[i], bdd), bools[i])

    def test_parcour_feuille_1(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()
        bdd = j1.executer()

        self.assertFalse(Route.hasRoute(self.a1))
        self.assertEqual(Route.getRouteJoueur(self.a1, bdd), 1)

        self.check_ars([True,True,True,True,True,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 
    

    def test_parcour_feuille_2(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act1)
        bdd = j1.executer()
    
        self.check_ars([True,False,False,False,False,False,True,True,True,True,True,False,False,False,False,False,False], bdd) 
        self.assertFalse(Route.hasRoute(self.a1)) 
    

    def test_parcour_feuille_3(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act1)
        self.n7.addAction(self.act7)
        bdd = j1.executer()
    
        self.check_ars([True,False,False,False,False,False,True,True,True,True,False,False,True,False,False,False,False], bdd) 
        self.assertTrue(Route.hasRoute(self.a1, bdd))
        self.assertFalse(Route.hasRoute(self.a1)) 
        self.assertFalse(Route.hasRoute(self.a2, bdd))
        self.assertFalse(Route.hasRoute(self.a3, bdd))
        self.assertFalse(Route.hasRoute(self.a4, bdd))
        self.assertFalse(Route.hasRoute(self.a5, bdd))
        self.assertFalse(Route.hasRoute(self.a6, bdd))
        self.assertTrue(Route.hasRoute(self.a7, bdd))
        self.assertTrue(Route.hasRoute(self.a8, bdd))
        self.assertTrue(Route.hasRoute(self.a9, bdd))
        self.assertTrue(Route.hasRoute(self.a10, bdd))
        self.assertFalse(Route.hasRoute(self.a11, bdd))
        self.assertFalse(Route.hasRoute(self.a12, bdd))
        self.assertTrue(Route.hasRoute(self.a13, bdd))
        self.assertFalse(Route.hasRoute(self.a14, bdd))
        self.assertFalse(Route.hasRoute(self.a15, bdd))
        self.assertFalse(Route.hasRoute(self.a16, bdd))
        self.assertFalse(Route.hasRoute(self.a17, bdd))


    def test_parcour_feuille_4(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act1)
        self.n6.insertActionByIndex(1,self.act8)
        bdd = j1.executer()
    
        self.check_ars([True,False,False,False,False,False,True,True,False,True,True,False,True,False,False,True,True], bdd) 
        self.assertFalse(Route.hasRoute(self.a1)) 

    def test_parcour_feuille_5(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act1)
        self.n6.insertActionByIndex(1,self.act8)
        self.n10.insertActionByIndex(0,self.act17)
        bdd = j1.executer()
    
        self.check_ars([True,False,False,False,False,False,True,True,False,True,True,False,True,True,True,False,False], bdd) 
        self.assertFalse(Route.hasRoute(self.a1)) 
 
    def test_parcour_feuille_6(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act1)
        self.n5.addAction(self.act1)
        bdd = j1.executer()
    
        self.check_ars([False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False], bdd) 
        self.assertFalse(Route.hasRoute(self.a1)) 


    def test_sortie_1(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n4.addAction(self.act2)
        bdd = j1.executer()
        self.check_ars([True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 

    def test_sortie_2(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act2)
        self.n7.addAction(self.act10)
        self.n8.addAction(self.act7)
        bdd = j1.executer()
        self.check_ars([True,False,False,False,False,False,True,True,True,True,False,False,False,False,False,False,False], bdd) 
    

    
    def test_sortie_3(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act2)
        self.n6.addAction(self.act10)
        self.n9.addAction(self.act1)
        bdd = j1.executer()
        self.check_ars([True,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False], bdd) 
    

    def test_sortie_4(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act2)
        self.n6.addAction(self.act10)
        self.n10.addAction(self.act16)
        self.n11.addAction(self.act13)
        bdd = j1.executer()
        self.check_ars([True,False,False,False,False,False,True,True,False,True,True,False,True,False,False,False,False], bdd) 
    



    def test_sortie_5(self):
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        self.n2.addAction(self.act2)
        self.n5.addAction(self.act1)
        self.n12.addAction(self.act7)
        bdd = j1.executer()
        self.check_ars([False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 
    

    def test_insertion_action(self):
        # 3 possibilite : l'insertion se passe bien et renvoie True, elle ne se passe pas bien car elle est inconsistante avec une autre action, soit dans le même noeud, soit un noued ancetre, soit un noeud descendant, enfin elle ne se passe pas bien car l'action elle même n'est pas valide.

        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        b1 = j1.insererAction(self.act2, self.n6,2) # ok
        b2 = j1.insererAction(self.act9, self.n6,2) # Non valide, autre action du meme noeud située avant
        b3 = j1.insererAction(self.act10, self.n6,1) # Non valide, autre action du meme noeud située après
        b4 = j1.insererAction(self.act7, self.n6,2) # Non valide, autre action d'un ancetre n5
        b5 = j1.insererAction(self.act11, self.n6,2) # Non valide, autre action d'un descendant (1) n7
        b6 = j1.insererAction(self.act13, self.n6,2) # Non valide, autre action d'un descendant (2) n8
        b7 = j1.insererAction(self.act17, self.n5,2) # Non valide, autre action d'un descendant (3) n10
        b9 = j1.insererAction(self.act14, self.n5,2) # Non valide, autre action d'un descendant (4) n11


        self.assertTrue(b1)

if __name__ == '__main__':
    unittest.main()
