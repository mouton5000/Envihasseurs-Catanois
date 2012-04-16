# *-* coding: utf8 *-*
import unittest
from arbre_action import *
from test_joueurs import *
import redis

REDIS = redis.StrictRedis()

class TestEchange(TestJoueur):
    def setUp(self):
        super(TestEchange,self).setUp()
        self.j1 = Joueur(1)
        self.n1 = self.j1.setNewRoot()
        self.n2 = self.n1.addChild()
        self.n3 = self.n2.addChild()
        self.n4 = self.n3.addChild()
        self.n5 = self.n3.addChild()
        self.n6 = self.n2.addChild()
        self.n7 = self.n6.addChild()
        self.n8 = self.n6.addChild()

        self.j2 = Joueur(2)
        self.n11 = self.j2.setNewRoot()
        self.n12 = self.n11.addChild()
        self.n13 = self.n12.addChild()
        self.n14 = self.n13.addChild()
        self.n15 = self.n13.addChild()
        self.n16 = self.n12.addChild()
        self.n17 = self.n16.addChild()
        self.n18 = self.n16.addChild()

        p = Plateau.getPlateau()

        self.tg = Plateau.getPlateau().ter(1)

        self.j1p = JoueurPossible(1)
        self.j2p = JoueurPossible(2)


        self.act1 = Action(1, 'acheter_carte_developpement', '1')
        self.act2 = Action(2, 'acheter_carte_developpement', '1')
        self.act3 = Action(3, 'acheter_carte_developpement', '1')
        self.act4 = Action(4, 'acheter_carte_developpement', '1')
        self.act5 = Action(5, 'acheter_carte_developpement', '1')
        self.act6 = Action(6, 'acheter_carte_developpement', '1')
        self.act7 = Action(7, 'acheter_carte_developpement', '1')
        self.act8 = Action(8, 'acheter_carte_developpement', '1')
        self.act9 = Action(9, 'acheter_carte_developpement', '1')
        self.act10 = Action(10, 'acheter_carte_developpement', '1')
        

        self.act11 = Action(11, 'acheter_carte_developpement', '1')
        self.act12 = Action(12, 'acheter_carte_developpement', '1')
        self.act13 = Action(13, 'acheter_carte_developpement', '1')
        self.act14 = Action(14, 'acheter_carte_developpement', '1')
        self.act15 = Action(15, 'acheter_carte_developpement', '1')
        self.act16 = Action(16, 'acheter_carte_developpement', '1')
        self.act17 = Action(17, 'acheter_carte_developpement', '1')
        self.act18 = Action(18, 'acheter_carte_developpement', '1')
        self.act19 = Action(19, 'acheter_carte_developpement', '1')
        self.act20 = Action(20, 'acheter_carte_developpement', '1')
        
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
        self.act18.save()
        self.act19.save()
        self.act20.save()
        
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

        JoueurPossible.setNbJoueurs(5)        

    def base_arbres(self):
        self.n2.addAction(self.act1)
        self.n2.addAction(self.act2)
        self.n3.addAction(self.act3)
        self.n4.addAction(self.act4)
        self.n4.addAction(self.act5)
        self.n5.addAction(self.act6)
        self.n6.addAction(self.act7)
        self.n6.addAction(self.act8)
        self.n7.addAction(self.act9)
        self.n8.addAction(self.act10)

        self.n12.addAction(self.act11)
        self.n12.addAction(self.act12)
        self.n13.addAction(self.act13)
        self.n14.addAction(self.act14)
        self.n14.addAction(self.act15)
        self.n15.addAction(self.act16)
        self.n16.addAction(self.act17)
        self.n16.addAction(self.act18)
        self.n17.addAction(self.act19)
        self.n18.addAction(self.act20)

    def test_proposer_echange_terre_partenaire(self):
        
        c1 = Cartes.ARGILE
        c2 = Cartes.BOIS
        self.j1p.recevoir(self.tg, c1)
        self.j2p.recevoir(self.tg, c2)
        self.j2p.recevoir(self.td, c2)
        
        self.j1p.addTerre(self.tg)
        self.j2p.addTerre(self.td)
        
        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1,c2)
        self.assertEqual(err.exception.error_code, EchangeError.TERRE_PARTENAIRE_NON_COLONISEE)
        # Proposition d'echange sur une terre que le partenaire n'a pas colonisee

    def test_proposer_echange(self):
        # Un echange ne peut etre proposé par un joueur que si, il a les moyens de payer son echange quelque soit l'endroit où il se trouve dans l'arbre d'action, y compris avant la toute première action.

        c1 = Cartes.ARGILE
        c2 = Cartes.BOIS
        self.j1p.addTerre(self.tg)
        self.j2p.addTerre(self.tg)
        self.j2p.addTerre(self.td)
        
        self.j1p.recevoir(self.tg, c1)
        self.j2p.recevoir(self.tg, c2)
        self.j2p.recevoir(self.td, c2)


        self.j1p.setEnRuine(True)
        with self.assertRaises(ActionNightError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1,c2)
        self.assertEqual(err.exception.error_code, ActionNightError.JOUEUR_EN_RUINE)
        # Joueur en ruine
        self.j1p.setEnRuine(False)
        
        self.j1p.set_defausser(self.tg,1)
        with self.assertRaises(ActionNightError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1,c2)
        self.assertEqual(err.exception.error_code, ActionNightError.DOIT_DEFAUSSER)
        self.j1p.set_defausser(self.tg,0)

        self.j2p.setEnRuine(True)
        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1,c2)
        self.assertEqual(err.exception.error_code, EchangeError.PARTENAIRE_EN_RUINE)
        # Joueur en ruine
        self.j2p.setEnRuine(False)

        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(6, self.tg, c1,c2)
        self.assertEqual(err.exception.error_code, EchangeError.PARTENAIRE_INEXISTANT)
        
        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(-1, self.tg, c1,c2)
        self.assertEqual(err.exception.error_code, EchangeError.PARTENAIRE_INEXISTANT)

        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.td, c1,c2)
        self.assertEqual(err.exception.error_code, EchangeError.TERRE_NON_COLONISEE)
        # Proposition d'echange sur une terre que l'on a pas colonisee

        c1double = c1 * 0.5
        c1neg = c1 * -1
        c2double = c2 * 0.5
        c2neg = c2 * -1


        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1neg,c2)
        self.assertEqual(err.exception.error_code, EchangeError.FLUX_IMPOSSIBLE) # Echange negatif
        
        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1double,c2)
        self.assertEqual(err.exception.error_code, EchangeError.FLUX_IMPOSSIBLE) # Echange non entier
        
        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1,c2neg)
        self.assertEqual(err.exception.error_code, EchangeError.FLUX_IMPOSSIBLE) # Echange negatif
        
        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1,c2double)
        self.assertEqual(err.exception.error_code, EchangeError.FLUX_IMPOSSIBLE) # Echange non entier

        with self.assertRaises(EchangeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c1*2,c2)
        self.assertEqual(err.exception.error_code, EchangeError.DON_INCOMPATIBLE) # Echange trop grand par rapport aux cartes disponnibles, alors que l'arbre d'action est vide

        self.j1p.recevoir(self.tg, Tarifs.DEVELOPPEMENT* 5 - c1)
        self.j2p.recevoir(self.tg, Tarifs.DEVELOPPEMENT* 5)
        self.j2p.recevoir(self.td, Tarifs.DEVELOPPEMENT* 5)
        self.base_arbres()

        c = Tarifs.DEVELOPPEMENT

        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n4)
        self.assertEqual(exc.action, self.act5)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
       
        self.j1p.recevoir(self.tg,c)
        self.n5.addAction(self.act1) 
        self.n5.addAction(self.act2) 
        
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n5)
        self.assertEqual(exc.action, self.act2)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j1p.recevoir(self.tg,c)
        self.n3.addAction(self.act1) 
        
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n5)
        self.assertEqual(exc.action, self.act2)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)

        self.j1p.recevoir(self.tg,c)
        self.n7.addAction(self.act1) 
        self.n7.addAction(self.act2) 
        self.n7.addAction(self.act3) 
        
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n7)
        self.assertEqual(exc.action, self.act3)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j1p.recevoir(self.tg,c)
        self.n8.addAction(self.act1) 
        self.n8.addAction(self.act2) 
        self.n8.addAction(self.act3) 
        self.n8.addAction(self.act4) 
        
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n8)
        self.assertEqual(exc.action, self.act4)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j1p.recevoir(self.tg,c)
        self.n6.addAction(self.act1) 
        
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n8)
        self.assertEqual(exc.action, self.act4)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j1p.recevoir(self.tg,c)
        self.n2.addAction(self.act3) 
        
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n8)
        self.assertEqual(exc.action, self.act4)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        
        self.j1p.recevoir(self.tg,c)

        
        self.assertTrue(self.j1.peut_proposer_echange(2, self.tg, c,c2))
        self.assertFalse(self.j2p.peut_payer(self.tg,c*6+c2))
        self.assertTrue(self.j1.peut_proposer_echange(2, self.tg, c,c*6+c2)) # La demande d'échange est indépendante du fait que j2 puisse l'accepter ou non

        cartes_avant = self.j1p.getCartes(self.tg)
        self.j1.proposer_echange(2,self.tg,c,c2)
        cartes_apres = self.j1p.getCartes(self.tg)
        self.assertEqual(cartes_avant-cartes_apres, c) # Les cartes proposées à l'échanges sont reservées et ne peuvent plus être utilisées.

        ech = Echange.getEchange(1)
        self.assertEqual(self.j1,ech.j1) 
        self.assertEqual(self.j2,ech.j2) 
        self.assertEqual(self.tg,ech.terre) 
        self.assertEqual(c,ech.don) 
        self.assertEqual(c2,ech.recu) 
        self.assertFalse(ech.accepted) 

        # Donc j1 ne peut plus échanger
        with self.assertRaises(NodeError) as err:
            self.j1.peut_proposer_echange(2, self.tg, c,c2)
        # Si le joueur 1 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n8)
        self.assertEqual(exc.action, self.act4)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)

         

    def test_accepter_echange(self):
        # Un echange ne peut etre accepté par un joueur que si, il a les moyens de payer son echange quelque soit l'endroit où il se trouve dans l'arbre d'action, y compris avant la toute première action.
        
        c1 = Cartes.ARGILE
        c2 = Cartes.BOIS
        self.j1p.addTerre(self.tg)
        self.j2p.addTerre(self.tg)
        self.j2p.addTerre(self.td)
        
        self.j1p.recevoir(self.tg, c1)
        self.j2p.recevoir(self.tg, c2)
        
        self.j1.proposer_echange(2, self.tg, c1,c2)

        j3 = Joueur(3)
        ech = Echange.getEchange(1)
        with self.assertRaises(EchangeError) as err:
            j3.peut_accepter_echange(ech)
        self.assertEqual(err.exception.error_code, EchangeError.NON_PARTENAIRE)
        
        self.j2p.payer(self.tg, c2)

        with self.assertRaises(EchangeError) as err:
            self.j2.peut_accepter_echange(ech)
        self.assertEqual(err.exception.error_code, EchangeError.DON_INCOMPATIBLE)


        c = Tarifs.DEVELOPPEMENT
        self.j2p.recevoir(self.tg, c* 5)
        ech.recu = c
        self.base_arbres()
        
        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n14)
        self.assertEqual(exc.action, self.act15)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        
        self.j2p.recevoir(self.tg, c) 
        self.n15.addAction(self.act11)
        self.n15.addAction(self.act12)

        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n15)
        self.assertEqual(exc.action, self.act12)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j2p.recevoir(self.tg, c) 
        self.n13.addAction(self.act11)

        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n15)
        self.assertEqual(exc.action, self.act12)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j2p.recevoir(self.tg, c) 
        self.n17.addAction(self.act11)
        self.n17.addAction(self.act12)
        self.n17.addAction(self.act13)
        self.n17.addAction(self.act14)
        self.n17.addAction(self.act15)

        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n17)
        self.assertEqual(exc.action, self.act13)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j2p.recevoir(self.tg, c)        
        self.j2p.recevoir(self.tg, c) 
        self.j2p.recevoir(self.tg, c) 
        
        self.n18.addAction(self.act11)
        self.n18.addAction(self.act12)
        self.n18.addAction(self.act13)
        self.n18.addAction(self.act14)
        self.n18.addAction(self.act15)
        self.n18.addAction(self.act16)

        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n18)
        self.assertEqual(exc.action, self.act16)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)
        

        self.j2p.recevoir(self.tg, c) 
        
        self.n16.addAction(self.act11)
        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n18)
        self.assertEqual(exc.action, self.act16)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)

        
        self.j2p.recevoir(self.tg, c) 
        self.n12.addAction(self.act13)

        with self.assertRaises(NodeError) as err:
            self.j2.peut_accepter_echange(ech)
        # Si le joueur 2 ne donne ne serait-ce qu'une carte à un autre joueur, il est dans l'incapacité d'effectuer toutes les actions de son arbre.
        exc = err.exception
        self.assertEqual(exc.node, self.n18)
        self.assertEqual(exc.action, self.act16)
        self.assertEqual(exc.actionError.error_code, RouteError.RESSOURCES_INSUFFISANTES)

        self.j2p.recevoir(self.tg, c) 
        cartes_avant = self.j2p.getCartes(self.tg)
        self.j2.accepter_echange(ech)
        cartes_apres = self.j2p.getCartes(self.tg)
        self.assertEquals(cartes_avant - cartes_apres, c)
        
        with self.assertRaises(EchangeError) as err:
            self.j2.peut_accepter_echange(ech)
        self.assertEqual(err.exception.error_code, EchangeError.DEJA_ACCEPTE)

        ech = Echange.getEchange(1)
        self.assertEqual(self.j1,ech.j1) 
        self.assertEqual(self.j2,ech.j2) 
        self.assertEqual(self.tg,ech.terre) 
        self.assertEqual(c1,ech.don) 
        self.assertEqual(c,ech.recu) 
        self.assertTrue(ech.accepted)


    def test_execution_echange(self):
        c1 = Cartes.ARGILE
        c2 = Cartes.BOIS
        self.j1p.addTerre(self.tg)
        self.j2p.addTerre(self.tg)
        self.j2p.addTerre(self.td)
        
        self.j1p.recevoir(self.tg, c1)
        self.j2p.recevoir(self.tg, c2)

        self.j1.proposer_echange(2, self.tg, c1,c2)
        ech1 = Echange.getEchange(1)
        ech1.executer()
        self.assertEquals(self.j1p.getCartes(self.tg), c1)

        self.j1.proposer_echange(2, self.tg, c1,c2)
        ech2 = Echange.getEchange(2)
        self.j2.accepter_echange(ech2)
        ech2.executer()
        self.assertEquals(self.j1p.getCartes(self.tg), c2)
        self.assertEquals(self.j2p.getCartes(self.tg), c1)




    def test_annulation_echange(self):
        c1 = Cartes.ARGILE
        c2 = Cartes.BOIS
        self.j1p.addTerre(self.tg)
        self.j2p.addTerre(self.tg)
        self.j2p.addTerre(self.td)
       
        j3 = Joueur(3)
 
        self.j1p.recevoir(self.tg, c1)
        self.j2p.recevoir(self.tg, c2)

        self.j1.proposer_echange(2, self.tg, c1,c2)
        ech = Echange.getEchange(1)
        with self.assertRaises(EchangeError) as err:
            j3.peut_annuler_echange(ech)
        self.assertEqual(err.exception.error_code, EchangeError.NON_PARTENAIRE)

        self.assertTrue(self.j2.peut_annuler_echange(ech))
        self.j2.annuler_echange(ech)
        ech = Echange.getEchange(1)
        self.assertEquals(ech,0)
        self.assertEquals(self.j1p.getCartes(self.tg), c1)
        self.assertEquals(self.j2p.getCartes(self.tg), c2)

        
        self.j1.proposer_echange(2, self.tg, c1,c2)
        ech = Echange.getEchange(2)
        self.assertNotEquals(ech,0)

        self.assertTrue(self.j1.peut_annuler_echange(ech))
        self.j1.annuler_echange(ech)
        ech = Echange.getEchange(2)
        self.assertEquals(ech,0)
        self.assertEquals(self.j1p.getCartes(self.tg), c1)
        self.assertEquals(self.j2p.getCartes(self.tg), c2)
        

        self.j1.proposer_echange(2, self.tg, c1,c2)
        ech = Echange.getEchange(3)
        self.assertNotEquals(ech,0)
        self.j2.accepter_echange(ech)

        self.assertTrue(self.j2.peut_annuler_echange(ech))
        self.j2.annuler_echange(ech)
        ech = Echange.getEchange(3)
        self.assertEquals(ech,0)
        self.assertEquals(self.j1p.getCartes(self.tg), c1)
        self.assertEquals(self.j2p.getCartes(self.tg), c2)
        


        self.j1.proposer_echange(2, self.tg, c1,c2)
        ech = Echange.getEchange(4)
        self.assertNotEquals(ech,0)
        self.j2.accepter_echange(ech)

        self.assertTrue(self.j1.peut_annuler_echange(ech))
        self.j1.annuler_echange(ech)
        ech = Echange.getEchange(4)
        self.assertEquals(ech,0)
        print self.j1p.getCartes(self.tg), c1
        self.assertEquals(self.j1p.getCartes(self.tg), c1)
        self.assertEquals(self.j2p.getCartes(self.tg), c2)
