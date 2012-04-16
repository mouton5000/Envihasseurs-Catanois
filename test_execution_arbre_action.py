# *-* coding: utf8 *-*
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
        

        self.act101 = Action(101, 'construire_route', self.a1.num)
        self.act102 = Action(102, 'construire_route', self.a2.num)
        self.act103 = Action(103, 'construire_route', self.a3.num)
        self.act104 = Action(104, 'construire_route', self.a4.num)
        self.act105 = Action(105, 'construire_route', self.a5.num)
        self.act106 = Action(106, 'construire_route', self.a6.num)
        self.act107 = Action(107, 'construire_route', self.a7.num)
        self.act108 = Action(108, 'construire_route', self.a8.num)
        self.act109 = Action(109, 'construire_route', self.a9.num)
        self.act110 = Action(110, 'construire_route', self.a10.num)
        self.act111 = Action(111, 'construire_route', self.a11.num)
        self.act112 = Action(112, 'construire_route', self.a12.num)
        self.act113 = Action(113, 'construire_route', self.a13.num)
        self.act114 = Action(114, 'construire_route', self.a14.num)
        self.act115 = Action(115, 'construire_route', self.a15.num)
        self.act116 = Action(116, 'construire_route', self.a16.num)
        self.act117 = Action(117, 'construire_route', self.a17.num)

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
        self.act101.save()
        self.act102.save()
        self.act103.save()
        self.act104.save()
        self.act105.save()
        self.act106.save()
        self.act107.save()
        self.act108.save()
        self.act109.save()
        self.act110.save()
        self.act111.save()
        self.act112.save()
        self.act113.save()
        self.act114.save()
        self.act115.save()
        self.act116.save()
        self.act117.save()
        

        j1.set_route_la_plus_longue(self.tg,0)
        
        self.n13 = Node(13)
        self.n13.addAction(self.act1)



 
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
    
    def test_sortie_5_2(self):
        ''' Sortie de l'arbre à causes d'action non valides'''
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        act1 = Action(2001, 'construire_route', 2045)
        act1.save()
        act2 = Action(2002, 'construire_rouuuuute', self.a1.num)
        act2.save()
        act3 = Action(2003, 'construire_route', self.a1.num, self.a2.num)
        act3.save()
        self.n2.addAction(act1)
        self.n5.addAction(act2)
        self.n12.addAction(act3)
        bdd = j1.executer()
        self.check_ars([False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 
    
    def test_sortie_5_3(self):
        ''' Sortie de l'arbre à causes d'action non valides'''
        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()

        act1 = Action(2001, 'construire_route', 'yahoo')
        act1.save()
        act2 = Action(2002, 'construire_rouuuuute')
        act2.save()
        act3 = Action(2003, 'construire_route', self.a1.num, self.a2.num)
        act3.save()
        self.n2.addAction(act1)
        self.n5.addAction(act2)
        self.n12.addAction(act3)
        bdd = j1.executer()
        self.check_ars([False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 
    

    def test_insertion_action(self):
        # 3 possibilite : l'insertion se passe bien et renvoie True, elle ne se passe pas bien car elle est inconsistante avec une autre action, soit dans le même noeud, soit un noued ancetre, soit un noeud descendant, enfin elle ne se passe pas bien car l'action elle même n'est pas valide.

        j1 = self.j1
        p = Plateau.getPlateau()

        self.base_arbre()
        self.assertTrue(j1.insererAction(self.act102, self.n6,2)) # ok
        self.assertIn(str(self.act102.num), self.n6.getActionsNum())
        
        self.assertFalse(j1.insererAction(self.act2, self.n13,1)) # Ce noeud qui n'appartient pas à j1
        
        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(self.act109, self.n6,2) # Non valide, autre action du meme noeud située avant
        exc = err.exception
        self.assertEqual(exc.node, self.n6)
        self.assertEqual(exc.action, self.act109)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_OCCUPEE)
        self.assertNotIn(str(self.act109.num), self.n6.getActionsNum())

        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(self.act110, self.n6,1) # Non valide, autre action du meme noeud située après
        exc = err.exception
        self.assertEqual(exc.node, self.n6)
        self.assertEqual(exc.action, self.act10)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_OCCUPEE)
        self.assertNotIn(str(self.act110.num), self.n6.getActionsNum())
        
        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(self.act107, self.n6,2) # Non valide, autre action d'un ancetre n5
        exc = err.exception
        self.assertEqual(exc.node, self.n6)
        self.assertEqual(exc.action, self.act107)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_OCCUPEE)
        self.assertNotIn(str(self.act107.num), self.n6.getActionsNum())
        
        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(self.act111, self.n6,2) # Non valide, autre action d'un descendant (1) n7
        exc = err.exception
        self.assertEqual(exc.node, self.n7)
        self.assertEqual(exc.action, self.act11)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_OCCUPEE)
        self.assertNotIn(str(self.act111.num), self.n6.getActionsNum())
        
        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(self.act113, self.n6,2) # Non valide, autre action d'un descendant (2) n8
        exc = err.exception
        self.assertEqual(exc.node, self.n8)
        self.assertEqual(exc.action, self.act13)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_OCCUPEE)
        self.assertNotIn(str(self.act113.num), self.n6.getActionsNum())
 
        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(self.act117, self.n5,2) # Non valide, car l'action elle meme n'est pas valide
        exc = err.exception
        self.assertEqual(exc.node, self.n5)
        self.assertEqual(exc.action, self.act117)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_NON_RELIEE)
        self.assertNotIn(str(self.act117.num), self.n5.getActionsNum())
        
        act18 = Action(18, 'construire_route', p.it(73).lien(p.it(83)).num)
        act18.save()
        act118 = Action(118, 'construire_route', p.it(73).lien(p.it(83)).num)
        act118.save()
        self.n11.addAction(act18)
        with(self.assertRaises(NodeError)) as err:
            j1.insererAction(act118, self.n5,2) # Non valide, autre action d'un descendant (4) n11
        exc = err.exception
        self.assertEqual(exc.node, self.n11)
        self.assertEqual(exc.action, act18)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_OCCUPEE)
        self.assertNotIn(str(act118.num), self.n5.getActionsNum())
       
        for i in xrange(2000):
            Action.incrActionId() 
        with(self.assertRaises(NodeError)) as err:
            j1.insererNouvelleAction(self.n5,2,'construire_route', 'yahoo') # Non valide, action invalide
        exc = err.exception
        self.assertEqual(exc.node, self.n5)
        self.assertEqual(exc.action, Action.getAction(2000))
        self.assertEqual(exc.actionError.error_code, ActionError.MAUVAIS_PARAMETRES)
        self.assertNotIn(str(2000), self.n5.getActionsNum())

        with(self.assertRaises(NodeError)) as err:
            j1.insererNouvelleAction(self.n5, 2, 'construire_rouuuuute', self.a1.num) # Non valide, action invalide
        exc = err.exception
        self.assertEqual(exc.node, self.n5)
        self.assertEqual(exc.action, Action.getAction(2001))
        self.assertEqual(exc.actionError.error_code, ActionError.MAUVAIS_PARAMETRES)
        self.assertNotIn(str(2001), self.n5.getActionsNum())
        

        self.assertTrue(j1.insererNouvelleAction(self.n2,2, 'construire_route', p.it(52).lien(p.it(42)).num)) # ok
        self.assertIn(str(2002), self.n2.getActionsNum())

    def test_retirer_action(self):
        # 3 possibilite : retirer l'action se passe bien et renvoie True, elle ne se passe pas bien car elle est inconsistante avec une autre action, soit dans le même noeud, soit un noeud descendant, enfin elle ne se passe pas bien car l'action elle même n'est pas dans le noeud.

        j1 = self.j1
        p = Plateau.getPlateau()
        self.base_arbre()


        self.assertFalse(j1.retirerAction(self.act1, self.n3)) # Cette action n'est pas dans ce noeud
        self.assertFalse(j1.retirerAction(self.act3, self.n2)) # Cette action n'est pas dans ce noeud
        self.assertFalse(j1.retirerAction(self.act14,self.n5)) # Cette action n'est pas dans ce noeud
        self.assertFalse(j1.retirerAction(self.act1, self.n13)) # Ce noeud qui n'appartient pas à j1
        

        
        with(self.assertRaises(NodeError)) as err:
            j1.retirerAction(self.act1, self.n2) # La suppression de l'action a une répercussion sur une autre action de l'arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n2)
        self.assertEqual(exc.action, self.act2)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_NON_RELIEE)
        self.assertIn(str(self.act1.num), self.n2.getActionsNum())
      
  
        with(self.assertRaises(NodeError)) as err:
            j1.retirerAction(self.act2, self.n2) # La suppression de l'action a une répercussion sur une autre action d'un des descendant
        exc = err.exception
        self.assertEqual(exc.node, self.n4)
        self.assertEqual(exc.action, self.act3)
        self.assertEqual(exc.actionError.error_code, RouteError.ARRETE_NON_RELIEE)
        self.assertIn(str(self.act2.num), self.n2.getActionsNum())

        self.assertTrue(j1.retirerAction(self.act11,self.n9))
        self.assertNotIn(str(self.act11.num), self.n9.getActionsNum())

        


    def test_execution_partielle(self):
        j1 = self.j1
        p = Plateau.getPlateau()
        self.base_arbre()

        bdd = j1.executerPartiel(self.n2, 0)
        self.assertEqual(len(bdd.keys()), len(REDIS.keys()))
        

        bdd = j1.executerPartiel(self.n2, self.act1)
        self.assertTrue(Route.hasRoute(self.a1,bdd))
        self.assertFalse(Route.hasRoute(self.a1))
        

        bdd = j1.executerPartiel(self.n2, self.act1)
        self.check_ars([True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 
        

        bdd = j1.executerPartiel(self.n4, self.act4)
        self.check_ars([True,True,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False], bdd) 
        

        bdd = j1.executerPartiel(self.n9, self.act17) # Cette action n'est pas dans le noeud, on ne renvoie alors rien.
        self.assertEqual(bdd, None)
        

        bdd = j1.executerPartiel(self.n9, self.act17) # Cette action n'est pas dans le noeud, on ne renvoie alors rien.
        self.assertEqual(bdd, None)
        
        bdd = j1.executerPartiel(self.n13, self.act1) # Ce noeud n'appartient pas à j1 donc on ne renvoie rien.
        self.assertEqual(bdd, None)


if __name__ == '__main__':
    
    unittest.main()
