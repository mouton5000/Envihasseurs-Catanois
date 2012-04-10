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


        self.a1 = p.it(72).lien(p.it(73))

        self.act1 = Action(1, 'construire_route', self.a1.num)
        self.act1.save()
        

        j1.set_route_la_plus_longue(self.tg,0)


 
    def test_parcour_vide(self):
        j1 = self.j1
        bdd = j1.executer()
        self.assertEquals(len(bdd.keys()),len(REDIS.keys()))

    def test_parcour_feuille_1(self):
        j1 = self.j1
        p = Plateau.getPlateau()
        self.n2.addAction(self.act1)
        bdd = j1.executer()

        self.assertTrue(Route.hasRoute(self.a1, bdd))
        self.assertFalse(Route.hasRoute(self.a1))
        self.assertEqual(Route.getRouteJoueur(self.a1, bdd), 1)


    def test_parcour_feuille_2(self):
        pass
    def test_parcour_feuille_3(self):
        pass
    def test_parcour_feuille_4(self):
        pass
    def test_parcour_feuille_5(self):
        pass
    

if __name__ == '__main__':
    unittest.main()
