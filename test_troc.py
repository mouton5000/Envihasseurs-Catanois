# -*- coding: utf8 -*-
from plateau import *
from test_joueurs import *
import redis
from joueurs import *
from pions import *
from errors import *

REDIS = redis.StrictRedis()


class TestTroc(TestJoueur):
   
    def setUp(self):
        super(TestTroc,self).setUp()
        self.j1 = Joueur(1)
        self.j2 = Joueur(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

    def test_acheter_ressource(self):
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j1.setCartes(tg,Cartes.RIEN)
        j1.setOr(tg,0)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE)) # On ne peut acheter sans or
        self.assertEqual(err.exception.error_code, OrError.RESSOURCES_INSUFFISANTES)
        j1.setOr(tg,1)
        self.assertTrue(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))

        j1.setEnRuine(True)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))
        self.assertEqual(err.exception.error_code, OrError.JOUEUR_EN_RUINE)
        # Joueur en ruine
        j1.setEnRuine(False)

        j1.setOr(tg,2)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(1,1,0,0,0))) # On ne peut acheter plus d'une carte à la fois
        self.assertEqual(err.exception.error_code, OrError.FLUX_IMPOSSIBLE)
        j1.setOr(tg,1)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(-1,2,0,0,0))) # On ne peut acheter négativement
        self.assertEqual(err.exception.error_code, OrError.FLUX_IMPOSSIBLE)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(0.5,0.5,0,0,0))) # On ne peut acheter qu'entièrement
        self.assertEqual(err.exception.error_code, OrError.FLUX_IMPOSSIBLE)

        Jeu.acheter_ressource(j1,tg, Cartes.BLE)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))
        self.assertEqual(err.exception.error_code, OrError.RESSOURCES_INSUFFISANTES)
        
        j1.setOr(td,1) #(en cas de bug)
        with self.assertRaises(OrError) as err:
            self.assertFalse(Jeu.peut_acheter_ressource(j1,td,Cartes.BLE)) # On ne peut acheter sur une terre non colonisée
        self.assertEqual(err.exception.error_code, OrError.TERRE_NON_COLONISEE)


# Les joueurs echangent entre eux.
    def test_echanger_joueur(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j2.addTerre(tg)
        j2.addTerre(td)
        c1 = CartesGeneral(3,0,3,3,3,1,0,0,0,0)
        c2g = CartesRessources(3,3,3,1,0)
        c2d = CartesRessources(1,0,0,1,0)
        j1.setCartes(tg,c1)
        j2.setCartes(tg,c2g)
        j2.setCartes(td,c2d)
        
        c1ech1 = CartesRessources(1,0,0,0,0)
        c1ech2 = CartesRessources(0,1,0,0,0)
        c1ech3 = CartesGeneral(1,0,0,0,0,1,0,0,0,0)
        c1ech1neg = CartesRessources(1,-1,0,0,0)
        c1ech1double = CartesRessources(0.5,0,0,0,0)
        c2ech = CartesRessources(0,0,0,1,0)
        c2echneg = CartesRessources(0,0,0,1,-1)
        c2echdouble = CartesRessources(0,0,0,0.5,0)


        self.assertTrue(Jeu.peut_echanger(j1,2,tg,c1ech1,c2ech)) # Ok
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech1,c2ech))
        # Joueur en ruine
        j1.setEnRuine(False)
        
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech2,c2ech)) # J1 n'a pas la somme requise
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech3,c2ech)) # J1 offre des cartes de developpement  
        self.assertFalse(Jeu.peut_echanger(j1,2,td,c1ech3,c2ech)) # J1 n'est pas sur td
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech1neg,c2ech)) # Echange Negatif
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech1double,c2ech)) # Echange non entier
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech1,c2echneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger(j1,2,tg,c1ech1,c2echdouble)) # Echante non entier

        
       
        Jeu.echanger(j1,2,tg,c1ech1,c2ech)
        self.assertEqual(j1.getCartes(tg),c1 - c1ech1 + c2ech)        
        self.assertEqual(j2.getCartes(tg),c2g + c1ech1 - c2ech)        


# Les joueurs echangent avec les ports et marche.
    def test_echanger_commerce(self):
        
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.addTerre(tg)

        p =Plateau.getPlateau()

        c1 = CartesRessources(3,8,4,4,4)
        cneg = CartesRessources(-1,2,0,0,0)
        cdouble = CartesRessources(0.5,0.5,0,0,0)
        ctoomuch = CartesRessources(2,0,0,0,0)

        j1.setCartes(tg,c1)
        
        port = p.hexa(2)
        marche = p.hexa(32)

        br = Voleur.getBrigand(tg)
        pr = Voleur.getPirate(tg)
        br.deplacer(p.hexa(22))
        pr.deplacer(p.hexa(1))
        br.save()
        pr.save()
        
        self.assertTrue(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        
        j1.setEnRuine(True)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertEqual(err.exception.error_code, CommerceError.JOUEUR_EN_RUINE)
        # Joueur en ruine
        j1.setEnRuine(False)
        
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,td,Cartes.BOIS,Cartes.ARGILE)) # Pas la bonne Terre
        self.assertEqual(err.exception.error_code, CommerceError.TERRE_NON_COLONISEE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Aucun Commerce
        self.assertEqual(err.exception.error_code, CommerceError.COMMERCE_NON_UTILISABLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Aucun Commerce.
        self.assertEqual(err.exception.error_code, CommerceError.COMMERCE_NON_UTILISABLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.ARGILE,Cartes.BOIS)) # Pas assez de argile
        self.assertEqual(err.exception.error_code, CommerceError.RESSOURCES_INSUFFISANTES)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,cneg,Cartes.BOIS)) # Echange negatif
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,cdouble,Cartes.BOIS)) # Echante non entier
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,ctoomuch,Cartes.BOIS)) # Trop de demande
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,cneg)) # Echange negatif
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,cdouble)) # Echange non entier
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,ctoomuch)) # Trop de demande
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        
        
       
        Jeu.echanger_classique(j1,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j1.getCartes(tg), CartesRessources(4,8,0,4,4))

        c1 = CartesRessources(2,6,3,3,3)
        j1.setCartes(tg,c1)
        br.deplacer(p.hexa(22))
        pr.deplacer(p.hexa(1))
        br.save()
        pr.save()
        
        Colonie(1,p.it(23)).save()
        port.commerceType = CommerceType.TOUS
        self.assertTrue(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        
        j1.setEnRuine(True)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertEqual(err.exception.error_code, CommerceError.JOUEUR_EN_RUINE)
        # Joueur en ruine
        j1.setEnRuine(False)
        
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,td,Cartes.BOIS,Cartes.ARGILE)) # Pas la bonne terre
        self.assertEqual(err.exception.error_code, CommerceError.TERRE_NON_COLONISEE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.ARGILE,Cartes.BLE)) # Pas assez de ressource
        self.assertEqual(err.exception.error_code, CommerceError.RESSOURCES_INSUFFISANTES)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,cneg,Cartes.BOIS)) # Echange negatif
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,cdouble,Cartes.BOIS)) # Echante non entier
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,ctoomuch,Cartes.BOIS)) # Trop de demande
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,cneg)) # Echange negatif
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,cdouble)) # Echange non entier
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,ctoomuch)) # Trop de demande
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        pr.deplacer(port)
        pr.save()
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Pirate
        self.assertEqual(err.exception.error_code, CommerceError.COMMERCE_NON_UTILISABLE)

        br.deplacer(p.hexa(22))
        pr.deplacer(p.hexa(1))
        br.save()
        pr.save()
       
        Jeu.echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j1.getCartes(tg), CartesRessources(3,6,0,3,3))

        c1 = CartesRessources(1,4,2,2,2)
        j1.setCartes(tg,c1)
        port.commerceType = CommerceType.BOIS
        self.assertTrue(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        
        j1.setEnRuine(True)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertEqual(err.exception.error_code, CommerceError.JOUEUR_EN_RUINE)
        # Joueur en ruine
        j1.setEnRuine(False)
        
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,td,Cartes.BOIS,Cartes.ARGILE)) # Pas la bonne terre
        self.assertEqual(err.exception.error_code, CommerceError.TERRE_NON_COLONISEE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.ARGILE,Cartes.BLE)) # Pas assez de ressource
        self.assertEqual(err.exception.error_code, CommerceError.RESSOURCES_INSUFFISANTES)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,cneg,Cartes.BOIS)) # Echange negatif
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,cdouble,Cartes.BOIS)) # Echante non entier
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,ctoomuch,Cartes.BOIS)) # Trop de demande
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,cneg)) # Echange negatif
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,cdouble)) # Echange non entier
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,ctoomuch)) # Trop de demande
        self.assertEqual(err.exception.error_code, CommerceError.FLUX_IMPOSSIBLE)
        pr.deplacer(port)
        pr.save()
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Pirate
        self.assertEqual(err.exception.error_code, CommerceError.COMMERCE_NON_UTILISABLE)

        br.deplacer(p.hexa(22))
        pr.deplacer(p.hexa(1))
        br.save()
        pr.save()
        
        Jeu.echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j1.getCartes(tg), CartesRessources(2,4,0,2,2))
        
        j2 = self.j2
        j2.addTerre(tg)
        c2 = CartesRessources(2,3,3,3,3)
        j2.setCartes(tg,c2)
        
        Colonie(2,p.it(83)).save()
        marche.commerceType = CommerceType.TOUS
        self.assertTrue(Jeu.peut_echanger_commerce_tous(j2,tg,Cartes.BOIS,Cartes.ARGILE))
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j2,tg,Cartes.ARGILE,Cartes.BLE)) ## Pas assez de ressource
        self.assertEqual(err.exception.error_code, CommerceError.RESSOURCES_INSUFFISANTES)

        br.deplacer(marche)
        br.save()
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce_tous(j2,tg,Cartes.BOIS,Cartes.ARGILE)) # Brigand
        self.assertEqual(err.exception.error_code, CommerceError.COMMERCE_NON_UTILISABLE)
        
        br.deplacer(p.hexa(22))
        pr.deplacer(p.hexa(1))
        br.save()
        pr.save()
        Jeu.echanger_commerce_tous(j2,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j2.getCartes(tg), CartesRessources(3,3,0,3,3))

        c2 = CartesRessources(1,2,2,2,2)
        j2.setCartes(tg,c2)
        marche.commerceType = CommerceType.BOIS
        self.assertTrue(Jeu.peut_echanger_commerce(j2,tg,Cartes.BOIS,Cartes.ARGILE))
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j2,tg,Cartes.ARGILE,Cartes.BLE)) # Pas assez de ressource
        self.assertEqual(err.exception.error_code, CommerceError.RESSOURCES_INSUFFISANTES)

        br.deplacer(marche)
        br.save()
        with self.assertRaises(CommerceError) as err:
            self.assertFalse(Jeu.peut_echanger_commerce(j2,tg,Cartes.BOIS,Cartes.ARGILE)) # Brigand
        self.assertEqual(err.exception.error_code, CommerceError.COMMERCE_NON_UTILISABLE)
        
        br.deplacer(p.hexa(22))
        pr.deplacer(p.hexa(1))
        br.save()
        pr.save()
        
       
        Jeu.echanger_commerce(j2,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j2.getCartes(tg), CartesRessources(2,2,0,2,2))

