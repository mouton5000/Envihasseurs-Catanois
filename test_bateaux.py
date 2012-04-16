# -*- coding: utf8 -*-
from test_joueurs import *

REDIS = redis.StrictRedis()


class TestBateaux(TestJoueur):
   
    def setUp(self):
        super(TestBateaux,self).setUp()
        self.j1 = JoueurPossible(1)
        self.j2 = JoueurPossible(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

    def test_construire_bateaux(self):

        p = Plateau.getPlateau()
        j1 = self.j1
        j2 = self.j2

        j1.addTerre(self.tg)

        i1 = p.it(32)#
        i2 = p.it(65)#
        i3 = p.it(72)#

        a1 = p.it(12).lien(p.it(2))# Arrete maritime non reliée à la cote
        a2 = p.it(22).lien(p.it(32))# Arrete maritime reliée à une colonie
        a3 = p.it(33).lien(p.it(32))# Arrete cotière reliée à une colonie
        a4 = p.it(65).lien(p.it(66))# Arrete reliée à une colonie adverse
        a5 = p.it(84).lien(p.it(94))# Arrete terrestre
        a6 = p.it(72).lien(p.it(73))# Arrete terrestre reliée à une colonie
        a7 = p.it(35).lien(p.it(45))# Arrete maritime reliée à la terre mais pas a une colonie


        j1.setCartes(self.tg,Tarifs.BATEAU_TRANSPORT)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a1)) # Aucun lien
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_NON_RELIEE)


        Colonie(1,i1).save()
        self.assertTrue(Jeu.peut_construire_bateau(j1,a2)) # ok
        self.assertTrue(Jeu.peut_construire_bateau(j1,a3)) # ok
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a2))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a3))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        j1.set_defausser(self.tg, 1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a2))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a3))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg, 0)

        Colonie(2,i2).save()
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a4)) # relie mais a un adversaire
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_NON_RELIEE)

        Colonie(1,i3).save()
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a5)) # terrestre
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_NON_CONSTRUCTIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a6)) # relie mais terrestre
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_NON_CONSTRUCTIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a7)) # a cote de la côte mais pas d'une colonie
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_NON_RELIEE)
        
        j1.setCartes(self.tg,Cartes.RIEN)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_construire_bateau(j1,a2)) # Pas assez de ressources
        self.assertEqual(err.exception.error_code, BateauError.RESSOURCES_INSUFFISANTES)
        j1.setCartes(self.tg,Tarifs.BATEAU_TRANSPORT)



        i = len(j1.getBateauxTransport())
        Jeu.construire_bateau(j1,a2)
        self.assertEqual(len(j1.getBateauxTransport()),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)

    
    def test_deplacer_bateaux(self):
        
        j1 = self.j1
        j2 = self.j2
       
        j1.addTerre(self.tg)
 
        p = Plateau.getPlateau()

        a0 = p.it(52).lien(p.it(62))
        a1 = p.it(1).lien(p.it(2))
        a2 = p.it(102).lien(p.it(112))
        a3 = p.it(41).lien(p.it(42))
        a4 = p.it(101).lien(p.it(102))
        a5 = p.it(52).lien(p.it(53))
        a6 = p.it(52).lien(p.it(42))
        a7 = p.it(61).lien(p.it(62))
        a8 = p.it(112).lien(p.it(2))

        b1 = Bateau(1,1,a0, Cartes.RIEN,Bateau.BateauType.TRANSPORT, False)
        b12 = Bateau(2,1,a1, Cartes.RIEN,Bateau.BateauType.TRANSPORT, False)
        b2 = Bateau(3,2,a2, Cartes.RIEN,Bateau.BateauType.TRANSPORT, False)

        b1.save()
        b12.save()
        b2.save()

        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b1,a6)) # ok cotier
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b1,a7)) # ok
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a6))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a7))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)

        j1.set_defausser(self.tg, 1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a6))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a7))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg, 0)
        

        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a3)) # Trop loin
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_INATTEIGNABLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b2,a4)) # Bateau adverse
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a5)) # En pleine terre
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_TERRESTRE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b12,a8)) # Pirate
        self.assertEqual(err.exception.error_code, BateauError.BATEAU_PIRATE)
        
        a9 = p.it(56).lien(p.it(57))
        a10 = p.it(27).lien(p.it(37))
        a11 = p.it(57).lien(p.it(67))
        a12 = p.it(67).lien(p.it(77))
        a13 = p.it(37).lien(p.it(47))
        a14 = p.it(47).lien(p.it(57))
        a15 = p.it(57).lien(p.it(67))

        b13 = Bateau(4,1,a9, Cartes.RIEN,Bateau.BateauType.CARGO, False)
        b14 = Bateau(5,1,a10, Cartes.RIEN,Bateau.BateauType.VOILIER, False)
        b13.save()
        b14.save()

        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b13,a11)) # ok
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b13,a12)) # Trop loin
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_INATTEIGNABLE)
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b14,a13)) # ok, déplacement de 1 arrete
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b14,a14)) # ok, déplacement de  2 arretes
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b14,a15)) # Trop loin
        self.assertEqual(err.exception.error_code, BateauError.ARRETE_INATTEIGNABLE)
        
        b15 = Bateau(6,1,a7, Cartes.RIEN,Bateau.BateauType.VOILIER, False)
        b16 = Bateau(6,2,a6, Cartes.RIEN,Bateau.BateauType.CARGO, False)
        b15.save()
        b16.save()
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b1,a7)) # ok, déplacement sur un emplacement occupé par un autre bateau.
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b1,a6)) # ok, déplacement sur un emplacement occupé par un autre bateau.

        

        Jeu.deplacer_bateau(j1,b1,a7)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a0)) # a deja bouge
        self.assertEqual(err.exception.error_code, BateauError.BATEAU_DEJA_DEPLACE)

        b13 = Bateau.getBateau(1)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_deplacer_bateau(j1,b13,a0)) # a deja bouge
        self.assertEqual(err.exception.error_code, BateauError.BATEAU_DEJA_DEPLACE)

# test les echanges entre terre et bateau, et les evolutions de bateau
# Ces tests sont faits au même endroit car ces deux évènements sont possibles dans les mêmes conditions

    def test_echanger_evoluer_bateau(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        j1.addTerre(tg)
        j2.addTerre(tg)
        cartes = CartesGeneral(3,3,3,3,3,1,0,0,1,2)
        j1.setCartes(tg,cartes)
        j2.setCartes(tg,CartesGeneral(5,5,5,5,5,5,5,5,5,5))

        p = Plateau.getPlateau()
        
        i1 = p.it(52)
        i2 = p.it(103)

        a1 = p.it(52).lien(p.it(42))
        a2 = p.it(51).lien(p.it(41))
        a3 = p.it(103).lien(p.it(113))
        a4 = p.it(32).lien(p.it(33))
        a5 = p.it(13).lien(p.it(23))
        a6 = p.it(100).lien(p.it(90))
        a7 = p.it(52).lien(p.it(42))


        c = CartesGeneral(1,2,0,0,1,1,1,0,0,0)
        b1 = Bateau(1,1,a1,c,Bateau.BateauType.TRANSPORT,False)
        b2 = Bateau(2,1,a2,c,Bateau.BateauType.TRANSPORT,False)
        b3 = Bateau(3,1,a3,c,Bateau.BateauType.TRANSPORT,False)
        b4 = Bateau(4,1,a4,c,Bateau.BateauType.TRANSPORT,False)
        b5 = Bateau(5,1,a5,c,Bateau.BateauType.TRANSPORT,False)
        b6 = Bateau(6,1,a6,c,Bateau.BateauType.TRANSPORT,False)
        b7 = Bateau(7,2,a7,c,Bateau.BateauType.TRANSPORT,False)

        b1.save()
        b2.save()
        b3.save()
        b4.save()
        b5.save()
        b6.save()
        b7.save()


        c1 = Colonie(1,i1)
        c2 = Colonie(2,i2)

        c1.save()
        c2.save()
        
        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b1)) # OK touche une colonie
        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b5)) # Ok touche un port
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        j1.set_defausser(self.tg, 1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg, 0)
        
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b2)) # En pleine mer
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b3)) # Colonie ennemie
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b4)) # Relie à la terre mais pas en position echange
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b6)) # Port mais sur une terre non colonisee
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b7)) # Relié à une colonie mais pas un bateau allie
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)
        j1.setCartes(tg,Cartes.RIEN)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1)) # Relié a une colonie mais Pas assez ressource
        self.assertEqual(err.exception.error_code, BateauError.RESSOURCES_INSUFFISANTES)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5)) # 
        self.assertEqual(err.exception.error_code, BateauError.RESSOURCES_INSUFFISANTES)
        j1.setCartes(tg,cartes) 

        cecht = CartesGeneral(0,0,0,0,0,0,0,0,0,1) 
        cechb = CartesGeneral(0,0,0,0,1,1,0,0,0,0) 
        cechttoomuch1 = CartesGeneral(2,0,0,0,0,0,0,0,0,1) 
        cechttoomuch2 = CartesGeneral(0,0,0,0,0,0,0,1,0,0) 
        cechbtoomuch = CartesGeneral(2,0,0,0,0,0,0,0,0,0) 
        cechtneg = CartesGeneral(0,0,0,0,0,0,0,0,-1,1) 
        cechbneg = CartesGeneral(0,0,0,0,1,1,0,-1,0,0) 
        cechtdouble = CartesGeneral(0,0,0,0,0,0,0,0,0,0.5) 
        cechbdouble = CartesGeneral(0,0,0,0,1,0.5,0,0,0,0) 
        
        
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        j1.set_defausser(self.tg, 1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg, 0)
        
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b2,cecht,cechb)) # En pleine mer
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b3,cecht,cechb)) # Colonie ennemie
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b4,cecht,cechb)) # Relie a rien
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb)) # Ok touche un port
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b6,cecht,cechb)) # Port mais sur une terre non colonisee
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b7,cecht,cechb)) # Pas un bateau allie
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch1,cechb)) # Trop de ressources demandees, le bateau est plein
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch2,cechb)) # Trop de ressources demandees la colonie n'a pas tout ca
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbtoomuch)) # Trop de ressources demandees, le bateau n'a pas tout ca
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtneg,cechb)) # Echange negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbneg)) # Echange negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtdouble,cechb)) # Echange non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbdouble)) # Echange non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)


#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_evoluer_bateau(j1,ab1))
#        # Joueur en ruine
#        j1.enRuine = False
        
        j1.setCartes(tg,cartes)
        Jeu.echanger_bateau(j1,b1,cecht,cechb)
        self.assertEqual(j1.getCartes(tg),cartes - cecht + cechb)
        self.assertEqual(b1.cargaison,c + cecht - cechb)
        b8 = Bateau.getBateau(1)
        self.assertEqual(b8.cargaison,c + cecht - cechb)
        j1.recevoir(tg,cecht - cechb)
        b1.append(cechb - cecht)

        j1.setCartes(tg,Tarifs.CARGO)
        Jeu.evoluer_bateau(j1,b1)
        self.assertEqual(j1.getCartes(tg),Cartes.RIEN)
        self.assertEqual(b1.etat, Bateau.BateauType.CARGO)
        b8 = Bateau.getBateau(1)
        self.assertEqual(b8.etat, Bateau.BateauType.CARGO)

        j1.setCartes(tg,cartes)


        b2.evolue()
        b3.evolue()
        b4.evolue()
        b5.evolue()
        b6.evolue()
        b7.evolue()
        
        b1.save()
        b2.save()
        b3.save()
        b4.save()
        b5.save()
        b6.save()
        b7.save()

        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b1)) # OK touche une colonie
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        j1.set_defausser(self.tg, 1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg, 0)
        
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b2)) # En pleine mer
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b3)) # Colonie ennemie
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b4)) # Relie à la terre mais pas en position echange
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b6)) # Port mais sur une terre non colonisee
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b7)) # Relié à une colonie mais pas un bateau allie
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)
        j1.setCartes(tg,Cartes.RIEN)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1)) # Relié a une colonie mais Pas assez ressource
        self.assertEqual(err.exception.error_code, BateauError.RESSOURCES_INSUFFISANTES)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5)) # 
        self.assertEqual(err.exception.error_code, BateauError.RESSOURCES_INSUFFISANTES)
        j1.setCartes(tg,cartes) 

        cecht = CartesGeneral(2,2,0,0,0,0,0,0,0,1) 
        cechb = CartesGeneral(0,0,0,0,1,1,0,0,0,0) 
        cechttoomuch1 = CartesGeneral(2,2,2,2,0,0,0,0,0,1) 
        cechttoomuch2 = CartesGeneral(0,0,0,0,0,0,0,1,0,0) 
        cechbtoomuch = CartesGeneral(2,0,0,0,0,0,0,0,0,0) 
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_echanger_bateau(j1,ab1,cecht,cechb))
#        # Joueur en ruine
#        j1.enRuine = False
        
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb)) # OK touche une colonie
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb)) # Ok touche un port
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        j1.set_defausser(self.tg,1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg,0)
        
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b2,cecht,cechb)) # En pleine mer
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b3,cecht,cechb)) # Colonie ennemie
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b4,cecht,cechb)) # Relie a rien
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b6,cecht,cechb)) # Port mais sur une terre non colonisee
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b7,cecht,cechb)) # Pas un bateau allie
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch1,cechb)) # Trop de ressources demandees, le bateau est plein
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch2,cechb)) # Trop de ressources demandees la colonie n'a pas tout ca
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbtoomuch)) # Trop de ressources demandees, le bateau n'a pas tout ca
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtneg,cechb)) # Echange negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbneg)) # Echange negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtdouble,cechb)) # Echange non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbdouble)) # Echange non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)


#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_evoluer_bateau(j1,ab1))
#        # Joueur en ruine
#        j1.enRuine = False
        
        j1.setCartes(tg,cartes)
        Jeu.echanger_bateau(j1,b1,cecht,cechb)
        self.assertEqual(j1.getCartes(tg),cartes - cecht + cechb)
        self.assertEqual(b1.cargaison,c + cecht - cechb)
        b8 = Bateau.getBateau(1)
        self.assertEqual(b8.cargaison,c + cecht - cechb)
        j1.recevoir(tg,cecht - cechb)
        b1.append(cechb - cecht)

        j1.setCartes(tg,Tarifs.VOILIER)
        Jeu.evoluer_bateau(j1,b1)
        self.assertEqual(j1.getCartes(tg),Cartes.RIEN)
        self.assertEqual(b1.etat, Bateau.BateauType.VOILIER)
        b8 = Bateau.getBateau(1)
        self.assertEqual(b8.etat, Bateau.BateauType.VOILIER)
        
        b2.evolue()
        b3.evolue()
        b4.evolue()
        b5.evolue()
        b6.evolue()
        b7.evolue()

        b1.save()
        b2.save()
        b3.save()
        b4.save()
        b5.save()
        b6.save()
        b7.save()
        j1.setCartes(tg,cartes)

        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1)) # Un voilier ne peut evoluer
        self.assertEqual(err.exception.error_code, BateauError.DEJA_EVOLUE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5)) # 
        self.assertEqual(err.exception.error_code, BateauError.DEJA_EVOLUE)

        cecht = CartesGeneral(2,2,0,0,0,0,0,0,0,1) 
        cechb = CartesGeneral(0,0,0,0,1,1,0,0,0,0) 
        cechttoomuch1 = CartesGeneral(2,2,2,2,0,0,0,0,0,1) 
        cechttoomuch2 = CartesGeneral(0,0,0,0,0,0,0,1,0,0) 
        cechbtoomuch = CartesGeneral(2,0,0,0,0,0,0,0,0,0) 
        
        
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb)) # OK touche une colonie
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb)) # Ok touche un port
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)

        j1.set_defausser(self.tg,1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg,0)
        
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b2,cecht,cechb)) # En pleine mer
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b3,cecht,cechb)) # Colonie ennemie
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b4,cecht,cechb)) # Relie a rien
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b6,cecht,cechb)) # Port mais sur une terre non colonisee
        self.assertEqual(err.exception.error_code, BateauError.PAS_EMPLACEMENT_ECHANGE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b7,cecht,cechb)) # Pas un bateau allie
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch1,cechb)) # Trop de ressources demandees, le bateau est plein
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch2,cechb)) # Trop de ressources demandees la colonie n'a pas tout ca
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbtoomuch)) # Trop de ressources demandees, le bateau n'a pas tout ca
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtneg,cechb)) # Echange negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbneg)) # Echange negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtdouble,cechb)) # Echange non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbdouble)) # Echange non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)


#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_evoluer_bateau(j1,ab1))
#        # Joueur en ruine
#        j1.enRuine = False
        
        j1.setCartes(tg,cartes)
        Jeu.echanger_bateau(j1,b1,cecht,cechb)
        self.assertEqual(j1.getCartes(tg),cartes - cecht + cechb)
        self.assertEqual(b1.cargaison,c + cecht - cechb)
        b8 = Bateau.getBateau(1)
        self.assertEqual(b8.cargaison,c + cecht - cechb)
        j1.recevoir(tg,cecht - cechb)
        b1.append(cechb - cecht)

        

# Les joueurs colonisent d'autres terres

    def test_coloniser(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
    
        p = Plateau.getPlateau()

        j1.addTerre(tg)
        j2.addTerre(tg)
        j2.addTerre(td)
        c = Cartes.RIEN
        
          
        # Colonisation avec un bateau, l'emplacement de la colonie et la partie de la cargaison a transferer
        # Le bateau n'est pas sur une cote
        # Le bateau est pas au joueur
        # La colonie n'est pas sur l'hexagone cotier ou un de ses voisins
        # La terre est deja colonisee
        # La position de la colonie est occupee a 0 ou 1 case pret par une colonie ou ville d'un autre joueur
        # La cargaison n'est pas suffisante
        # La cargaison transferee est plus grande que le reste        
        # Le transfert n'est physiquement pas valide
        # Une fois la colonisation faite, tester les ressources et la cargaison, la nouvelle terre, la nouvelle main et la nouvelle qtt d'or du colon

        i1 = p.it(48) # Point de colonisation
        i2 = p.it(90) # Colonisation trop lointaine
        i3 = p.it(47) # Pour le bateau
        i4 = p.it(57) # Pour le bateau (2)
        a1 = i1.lien(i3) # Arrete initiale du bateau
        a2 = i3.lien(i4) # Arrete du bateau après déplacement
        i5 = p.it(50) # Sur un hexagone voisin
        i6 = p.it(69) # Sur un hexagone voisin, mais proche d'une colonie adverse
        i7 = p.it(79) # Pour mettre une colonie de j2
        i8 = p.it(108) # Bateau du joueur 2
        i9 = p.it(98) # Bateau du joueur 2
        a3 = i8.lien(i9) # Arrete du bateau du joueur 2
        
        b1 = Bateau(1,1,a1, Cartes.RIEN,Bateau.BateauType.TRANSPORT, False)
        b2 = Bateau(2,2,a3, Cartes.RIEN,Bateau.BateauType.TRANSPORT, False)

        b1.save()
        b2.save()

        carg1 = CartesRessources(1,1,1,0,1) # Juste assez pour coloniser
        carg2 = CartesGeneral(3,1,3,0,1,1,0,0,1,0) # Juste assez pour coloniser et transferer
        carg3 = CartesRessources(1,1,0,0,1) # Cargaison pas suffisante
        transf1toomuch = Cartes.BLE # Plus de ressource dans le bateau
        transf1neg = Cartes.BLE * -1 # Transfert nefatif
        transf2 = CartesGeneral(1,0,2,0,0,1,0,0,0,0) # Juste assez pour coloniser et transferer
        transf2double = Cartes.BOIS * 0.5 # Transfert non entier

        b1.cargaison = carg1
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i1,Cartes.RIEN))
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i5,Cartes.RIEN))
        
        j1.setEnRuine(True)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i1,Cartes.RIEN))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i5,Cartes.RIEN))
        self.assertEqual(err.exception.error_code, ActionError.JOUEUR_EN_RUINE)
        # En ruine
        j1.setEnRuine(False)
        
        j1.set_defausser(self.tg, 1)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i1,Cartes.RIEN))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        with self.assertRaises(ActionError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i5,Cartes.RIEN))
        self.assertEqual(err.exception.error_code, ActionError.DOIT_DEFAUSSER)
        j1.set_defausser(self.tg, 0)
        
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i2,Cartes.RIEN)) # Trop loin
        self.assertEqual(err.exception.error_code, BateauError.EMPLACEMENT_INATTEIGNABLE)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i3,Cartes.RIEN)) # Dans l'eau
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_MARITIME)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i1,transf1toomuch)) # Transfert trop eleve
        self.assertEqual(err.exception.error_code, BateauError.FLUX_TROP_ELEVE)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i1,transf1neg)) # Transfert negatif
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)

        

        b1.cargaison = carg3
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i1,Cartes.RIEN)) # Pas assez de cargaison
        self.assertEqual(err.exception.error_code, ColonieError.RESSOURCES_INSUFFISANTES)
        
        b2.cargaison = carg1
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b2,i8,Cartes.RIEN)) # Pas le bon bateau
        self.assertEqual(err.exception.error_code, BateauError.NON_PROPRIETAIRE)

        b1.cargaison = carg2
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i1,transf2))
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i1,transf2double)) # Transfert non entier
        self.assertEqual(err.exception.error_code, BateauError.FLUX_IMPOSSIBLE)

        b2.cargaison = carg1
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j2,b2,i9,Cartes.RIEN)) # La terre est deja colonisee
        self.assertEqual(err.exception.error_code, BateauError.TERRE_DEJA_COLONISEE)
        
        c = Colonie(2,i7)    
        c.save()
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i7,transf2)) # Il y a une colonie a cet emplacement
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENT_OCCUPE)
        with self.assertRaises(ColonieError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i6,transf2)) # Il y a une colonie voisine
        self.assertEqual(err.exception.error_code, ColonieError.EMPLACEMENTS_VOISINS_OCCUPES)
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i5,transf2))
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_coloniser(j1,b1,i48,transf2))
#        # Joueur en ruine
#        j1.enRuine = False

        b1.deplacer(a2)
        with self.assertRaises(BateauError) as err:
            self.assertFalse(Jeu.peut_coloniser(j1,b1,i5,transf2)) # Le bateau n'est pas cotier
        self.assertEqual(err.exception.error_code, BateauError.EMPLACEMENT_INATTEIGNABLE)
        b1.deplacer(a1)
        b1.aBouge = True
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i5,transf2)) # Le bateau n'est pas cotier
        Jeu.coloniser(j1,b1,i5,transf2)
        

        self.assertTrue(j1.aColoniseTerre(td))
        self.assertEqual(j1.getCartes(td),transf2)
        self.assertEqual(j1.getOr(td),0)
#        self.assertEqual(j1.get_deplacement_voleur(td),False)
        self.assertEqual(j1.get_chevalliers(td),0)
        self.assertEqual(j1.get_route_la_plus_longue(td),0)
        self.assertEqual(j1.getStaticPoints(td),1) 
#        self.assertEqual(j1.get_carte_armee_la_plus_grande(td),False) 
#        self.assertEqual(j1.get_carte_route_la_plus_longue(td),False) 
#        j2.cartes_routes_les_plus_longues = [False,False]
        b1 = Bateau.getBateau(b1.num)
        self.assertEqual(b1.cargaison,carg2 - transf2 - Tarifs.COLONIE)
        self.assertEqual(len(j1.getColonies()),1)
        self.assertEqual(len(j1.getRoutes()),0)


