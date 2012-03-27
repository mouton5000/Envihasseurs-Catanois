# -*- coding: utf8 -*-
from plateau import *
from test_joueurs import *
from redis import *

REDIS = redis.StrictRedis()


class TestVoleur(TestJoueur):
   
    def setUp(self):
        super(TestVoleur,self).setUp()
        self.j1 = Joueur(1)
        self.j2 = Joueur(2)
        self.tg = Plateau.getPlateau().ter(1)
        self.td = Plateau.getPlateau().ter(2)

    def test_designer_deplaceur_voleur(self):
        j1 = self.j1
        j2 = self.j2
        j3 = Joueur(3)
        j4 = Joueur(4)
        j5 = Joueur(5)
        j6 = Joueur(6)

        tg = self.tg
        td = self.td

        j1.addTerre(tg)
        j2.addTerre(tg)
        j3.addTerre(tg)
        j4.addTerre(tg)
        j5.addTerre(tg)
        j6.addTerre(tg)

        j2.addTerre(td)
        j4.addTerre(td)
        j1.addTerre(td)
        j3.addTerre(td)
        j5.addTerre(td)
        
        Des.save([10,6,4,3])
        Des.setOrigin(0)
        Jeu.designer_deplaceur_de_voleur()

        self.assertFalse(j1.get_deplacement_voleur(tg))
        self.assertFalse(j2.get_deplacement_voleur(tg))
        self.assertFalse(j3.get_deplacement_voleur(tg))
        self.assertFalse(j4.get_deplacement_voleur(tg))
        self.assertFalse(j5.get_deplacement_voleur(tg))
        self.assertFalse(j6.get_deplacement_voleur(tg))

        self.assertFalse(j2.get_deplacement_voleur(td))
        self.assertFalse(j4.get_deplacement_voleur(td))
        self.assertFalse(j1.get_deplacement_voleur(td))
        self.assertFalse(j3.get_deplacement_voleur(td))
        self.assertFalse(j5.get_deplacement_voleur(td))

        Des.save([7,6,4,3])
        Des.setOrigin(0)
        Jeu.designer_deplaceur_de_voleur()
        
        self.assertTrue(j1.get_deplacement_voleur(tg))
        self.assertFalse(j2.get_deplacement_voleur(tg))
        self.assertFalse(j3.get_deplacement_voleur(tg))
        self.assertFalse(j4.get_deplacement_voleur(tg))
        self.assertFalse(j5.get_deplacement_voleur(tg))
        self.assertFalse(j6.get_deplacement_voleur(tg))

        self.assertTrue(j2.get_deplacement_voleur(td))
        self.assertFalse(j4.get_deplacement_voleur(td))
        self.assertFalse(j1.get_deplacement_voleur(td))
        self.assertFalse(j3.get_deplacement_voleur(td))
        self.assertFalse(j5.get_deplacement_voleur(td))


        Des.save([7,6,4,3])
        Des.setOrigin(4)
        Jeu.designer_deplaceur_de_voleur()
        
        self.assertFalse(j1.get_deplacement_voleur(tg))
        self.assertFalse(j2.get_deplacement_voleur(tg))
        self.assertFalse(j3.get_deplacement_voleur(tg))
        self.assertFalse(j4.get_deplacement_voleur(tg))
        self.assertTrue(j5.get_deplacement_voleur(tg))
        self.assertFalse(j6.get_deplacement_voleur(tg))

        self.assertFalse(j2.get_deplacement_voleur(td))
        self.assertFalse(j4.get_deplacement_voleur(td))
        self.assertFalse(j1.get_deplacement_voleur(td))
        self.assertFalse(j3.get_deplacement_voleur(td))
        self.assertTrue(j5.get_deplacement_voleur(td))



        # L'origine se déplace toute seule, elle vaut maintenant 8
        Des.save([7,6,4,3])
        self.assertEqual(Des.getOrigin(),8)
        Jeu.designer_deplaceur_de_voleur()
        
        self.assertFalse(j1.get_deplacement_voleur(tg))
        self.assertFalse(j2.get_deplacement_voleur(tg))
        self.assertTrue(j3.get_deplacement_voleur(tg))
        self.assertFalse(j4.get_deplacement_voleur(tg))
        self.assertFalse(j5.get_deplacement_voleur(tg))
        self.assertFalse(j6.get_deplacement_voleur(tg))

        self.assertFalse(j2.get_deplacement_voleur(td))
        self.assertFalse(j4.get_deplacement_voleur(td))
        self.assertFalse(j1.get_deplacement_voleur(td))
        self.assertTrue(j3.get_deplacement_voleur(td))
        self.assertFalse(j5.get_deplacement_voleur(td))


        # Plusieurs 7
        Des.save([3,7,4,7])
        Des.setOrigin(18)
        Jeu.designer_deplaceur_de_voleur()
        
        self.assertFalse(j1.get_deplacement_voleur(tg))
        self.assertTrue(j2.get_deplacement_voleur(tg))
        self.assertFalse(j3.get_deplacement_voleur(tg))
        self.assertTrue(j4.get_deplacement_voleur(tg))
        self.assertFalse(j5.get_deplacement_voleur(tg))
        self.assertFalse(j6.get_deplacement_voleur(tg))

        self.assertFalse(j2.get_deplacement_voleur(td))
        self.assertTrue(j4.get_deplacement_voleur(td))
        self.assertFalse(j1.get_deplacement_voleur(td))
        self.assertFalse(j3.get_deplacement_voleur(td))
        self.assertTrue(j5.get_deplacement_voleur(td))
        

        Des.save([12,6,4,3])
        Jeu.designer_deplaceur_de_voleur()
        
        self.assertFalse(j1.get_deplacement_voleur(tg))
        self.assertFalse(j2.get_deplacement_voleur(tg))
        self.assertFalse(j3.get_deplacement_voleur(tg))
        self.assertFalse(j4.get_deplacement_voleur(tg))
        self.assertFalse(j5.get_deplacement_voleur(tg))
        self.assertFalse(j6.get_deplacement_voleur(tg))

        self.assertFalse(j2.get_deplacement_voleur(td))
        self.assertFalse(j4.get_deplacement_voleur(td))
        self.assertFalse(j1.get_deplacement_voleur(td))
        self.assertFalse(j3.get_deplacement_voleur(td))
        self.assertFalse(j5.get_deplacement_voleur(td))
        
        j1.ruiner()
        # Plusieurs 7
        Des.save([3,7,4,7])
        Des.setOrigin(18)
        Jeu.designer_deplaceur_de_voleur()
        
        self.assertFalse(j2.get_deplacement_voleur(tg))
        self.assertTrue(j3.get_deplacement_voleur(tg))
        self.assertFalse(j4.get_deplacement_voleur(tg))
        self.assertFalse(j5.get_deplacement_voleur(tg))
        self.assertTrue(j6.get_deplacement_voleur(tg))

        # Joueur en ruine
        j1.setEnRuine(False)
    
    def test_deplacer_voleur(self):
        p = Plateau.getPlateau()
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.addTerre(tg)
        j2.addTerre(tg)
        j2.addTerre(td)

        brg = Voleur.getBrigand(tg)
        prg = Voleur.getPirate(tg)
        brd = Voleur.getBrigand(td)
        prd = Voleur.getPirate(td) 

        desg = p.hexa(22)
        desd = p.hexa(25)
        marg = p.hexa(1)
        mard = p.hexa(4)

        brg.deplacer(desg)
        prg.deplacer(desd)
        brd.deplacer(marg)
        prd.deplacer(mard)
        brg.save()
        prg.save()

        br = Voleur.VoleurType.BRIGAND
        pr = Voleur.VoleurType.PIRATE
       
        j1.set_deplacement_voleur(tg,True) 

        # Deplacement du voleur s'il n'y a aucun autre joueur sur la terre privee de l'hexagone actuellement occupe : l'hexagone choisi doit alors etre un desert, si c'est le brigand, nul si c'est un pirate et le joueur vole nul.

        # Aucun joueur sur l'ile, ce cas ne devrait pas arriver
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,desg,0))

#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,0))
#        # Joueur en ruine
#        j1.enRuine = False

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(26),0)) # Non desert
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(32),0)) # Desert mais Marche
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desd,0)) # Autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(31),0)) # Mer
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,2)) # Il ne faut pas de joueur

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,0,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,marg,0)) # Il ne faut pas d hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,2)) # Il ne faut pas de joueur
        
        # Un seul joueur sur l'ile 
        
        Colonie(1,p.it(94)).save()
        Bateau(1,1,p.it(41).lien(p.it(51)), Cartes.RIEN,Bateau.BateauType.TRANSPORT,False).save()

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,desg,0))

#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,0))
#        # Joueur en ruine
#        j1.enRuine = False

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(26),0)) # non desert
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(32),0)) # desert mais marche
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desd,0)) # autre terre        
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(31),0)) # mer
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,2)) # il ne faut pas de joueur

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,0,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,marg,0)) # Il ne faut pas d hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,2)) # Il ne faut pas de joueur

        #Deux joueurs sur l ile mais le voleur est sur le seul hexagone occupe par le deuxieme joueur

        Colonie(2,p.it(92)).save() # Colonie cotiere pas sur un port
        b2 = Bateau(2,2,p.it(82).lien(p.it(92)), Cartes.RIEN,Bateau.BateauType.TRANSPORT,False) #Bateau Cotier
        b2.save()

        brg.deplacer(p.hexa(36))
        prg.deplacer(p.hexa(41))
        brg.save()
        prg.save()

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,desg,0))

        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,0))
        # Joueur en ruine
        j1.setEnRuine(False)

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(36),0)) # Aucun deplacement
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(26),0)) # non desert
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(32),0)) # desert mais marche
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desd,0)) # autre terre        
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(31),0)) # mer
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,2)) # il ne faut pas de joueur

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,0,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(4),0)) # Il ne faut pas d hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(41),0)) # Aucun deplacement
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,2)) # Il ne faut pas de joueur        
        # Brigand
        # Deplacement sur un hexagone sans joueur
        # Deplacement sur le meme hexagone
        # Deplacement dans la mer
        # Deplacements sur une autre terre

        brg.deplacer(desg)
        brg.save()
        prg.save()
        
        Colonie(2,p.it(35)).save() # Colonie cotiere pas sur un port

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,0,2)) # Pas d'hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(16),0)) # Pas de joueur
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(12),2)) # Le joueur 2 n'est pas la
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,desg,2)) # Le voleur ne bouge pas
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(13),2)) # Deplacement a cote de la deuxieme colonie du joueur mais en mer
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(17),2))
        
        j1.set_deplacement_voleur(tg, False)
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(17),2)) # Ce n'est pas a son our
        j1.set_deplacement_voleur(tg, True)

        Colonie(2,p.it(48)).save() # Colonie cotiere pas sur un port sur td
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(19),2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,br,p.hexa(19),2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,br,p.hexa(17),2)) # Deplacement depuis une terre non colonisee
        
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(37),1)) # Le joueur 1 ne peut s'attaquer a lui meme
        
        # Pirate
        # Deplacement sur un hexagone sans colonie ni bateau
        # Deplacement sur le meme hexagone
        # Deplacement sur la terre
        # Deplacements sur une autre terre
        # Deplacement du voleur s'il n'y a aucun autre bateau ou colonie cotier sur la terre privee de l'hexagone occupe
        # Deplacement du pirate s il avait disparu

        prg.deplacer(marg)
        brg.save()
        prg.save()

        Colonie(2,p.it(115)).save()

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,2)) # Pas d'hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(11),0)) # Pas de joueur
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(11),2)) # Le joueur 2 n'est pas la
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,marg,2)) # Le voleur ne bouge pas
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(36),2)) # Deplacement en terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(47),2)) # Deplacement en terre
        
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(57),2))
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(41),2))
        
        prg.deplacer(0)
        brg.save()
        prg.save()
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(57),2))
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(41),2))

#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(52),0))
#        # Joueur en ruine
#        j1.enRuine = False

        j1.set_deplacement_voleur(tg,False)
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(57),2)) # Ce n'est pas a son tour
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(41),2)) # Ce n'est pas a son tour

        j1.set_deplacement_voleur(tg,True)
        Colonie(2,p.it(90)).save()
        b2.deplacer(p.it(107).lien(p.it(108)))
        b2.save()
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(45),2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(44),2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,pr,p.hexa(45),2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,pr,p.hexa(44),2)) # Deplacement sur une autre terre
        
        b2.deplacer(p.it(92).lien(p.it(82)))
        b2.save()
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,pr,p.hexa(57),2)) # Deplacement depuis une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,pr,p.hexa(41),2)) # Deplacement depuis une autre terre
 
        prg.deplacer(marg)
        brg.save()
        prg.save()
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(57),2))
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(41),2))
  
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(21),1)) # Le joueur 1 ne peut s'attaquer a lui meme
 
        # Vol
        # Vol avec bateau a 1 case
        # Vol sans bateau a 1 case
        # Vol d'un joueur pas sur l'hexagone
        # Vol d'un joueur n'ayant plus de cartes
        # Vol d'un joueur n'ayant que des cartes de developpement
        # Vol d'un joueur sur une autre terre

        c0 = Cartes.RIEN
        c2 = Cartes.BLE
        cch = Cartes.CHEVALLIER
        
        j1.setCartes(tg,c0)
        j1.setOr(tg,0)
        j2.setCartes(tg,c0)
        j2.setCartes(td,c0)
        j2.setOr(tg,2)
        j2.setOr(td,1)

        
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(17),2))
        Jeu.deplacer_voleur(j1,tg,br,p.hexa(17),2)
        brg = Voleur.getBrigand(tg)
        self.assertEqual(brg.position,p.hexa(17))
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c0)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j2.getOr(tg),2)
        self.assertEqual(j2.getOr(td),1)

        j2.setCartes(tg,c2)
        brg.deplacer(desg)
        brg.save()
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(17),2))
        Jeu.deplacer_voleur(j1,tg,br,p.hexa(17),2)

        brg = Voleur.getBrigand(tg)
        self.assertEqual(brg.position,p.hexa(17))
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c2)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j2.getOr(tg),2)
        self.assertEqual(j2.getOr(td),1)

        j2.setCartes(tg,cch)
        j1.setCartes(tg,c0)
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(57),2))
        Jeu.deplacer_voleur(j1,tg,pr,p.hexa(57),2)

        prg = Voleur.getPirate(tg)
        self.assertEqual(prg.position,p.hexa(57))
        self.assertEqual(j2.getCartes(tg),cch)
        self.assertEqual(j1.getCartes(tg),c0)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j2.getOr(tg),2)
        self.assertEqual(j2.getOr(td),1)

        # Vol d un bateau par un pirate
        j1.setCartes(tg,c0)
        j2.setCartes(tg,c0)
        j2.setCartes(td,c0)
        b2.deplacer(p.it(25).lien(p.it(35)))
        b2.cargaison = Cartes.BLE
        b2.save()
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,p.hexa(7),2))
        Jeu.deplacer_voleur(j1,tg,pr,p.hexa(7),2)
        prg = Voleur.getPirate(tg)
        self.assertEqual(prg.position,p.hexa(7))
        self.assertEqual(j2.getCartes(tg),c0)
        b2 = Bateau.getBateau(2)
        self.assertEqual(b2.cargaison,c0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)

        # Vol d un bateau par un brigand
        j1.setCartes(tg,c0)
        j2.setCartes(tg,c0)
        j2.setCartes(td,c0)
        b2.deplacer(p.it(25).lien(p.it(35)))
        b2.cargaison = Cartes.BLE
        b2.save()
        brg.deplacer(desg)
        brg.save()
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(17),2))
        Jeu.deplacer_voleur(j1,tg,br,p.hexa(17),2)
        brg = Voleur.getBrigand(tg)
        self.assertEqual(brg.position,p.hexa(17))
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)
        b2 = Bateau.getBateau(2)
        self.assertEqual(b2.cargaison,c0)
        
        # Vol d un joueur qui n a rien par un brigand, le bateau est mal place
        j1.setCartes(tg,c0)
        j2.setCartes(tg,c0)
        j2.setCartes(td,c0)
        b2.deplacer(p.it(1).lien(p.it(2)))
        b2.cargaison = Cartes.BLE
        b2.save()
        brg.deplacer(desg)
        brg.save()
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(17),2))
        Jeu.deplacer_voleur(j1,tg,br,p.hexa(17),2)
        brg = Voleur.getBrigand(tg)
        self.assertEqual(brg.position,p.hexa(17))
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c0)
        b2 = Bateau.getBateau(2)
        self.assertEqual(b2.cargaison,Cartes.BLE)

        # Vol d un joueur qui n a rien par un pirate, le bateau est mal place
        j1.setCartes(tg,c0)
        j2.setCartes(tg,c0)
        j2.setCartes(td,c0)
        b2.deplacer(p.it(1).lien(p.it(2)))
        b2.cargaison = Cartes.BLE
        b2.save()
        j1.set_deplacement_voleur(tg, True)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,p.hexa(47),2))
        Jeu.deplacer_voleur(j1,tg,br,p.hexa(47),2)
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c0)
        b2 = Bateau.getBateau(2)
        self.assertEqual(b2.cargaison,Cartes.BLE)

    def test_defausser(self):
        p = Plateau.getPlateau()
        j1 = self.j1
        tg = self.tg
        j1.addTerre(tg)
         
        c1 = CartesGeneral(2,2,2,0,3,1,2,1,0,0) # Defausser
        c2 = CartesGeneral(1,0,1,1,0,1,2,1,0,0) # Rien a defausser, attention a ne pas defausser les cartes de devellopement
        c3 = CartesRessources(3,3,3,4,3) # Defausser deux fois
        
        d1 = CartesRessources(1,1,1,0,2) # Ok
        dneg = CartesRessources(-1,2,2,0,2) # Non positif
        ddouble = CartesRessources(0.5,1.5,1,0,2) # Non entier
        d2 = CartesRessources(1,1,1,0,1) # Pas assez de cartes deffaussees
        d3 = CartesRessources(1,2,1,0,2) # Trop de cartes deffaussees
        d4 = CartesRessources(1,1,1,1,1) # Pas assez de ressourcesen main
        d5 = CartesGeneral(0,0,0,0,0,1,2,1,0,0) # Cartes developpement pour c2
        d6 = CartesGeneral(1,1,1,0,0,1,0,1,0,0) # Cartes developpement pour c1
        d7 = CartesRessources(3,2,2,3,2) # Ok avec d3
        d8 = CartesRessources(1,0,0,0,0) # Ok avec c2 si on defaussait pour 7 cartes ou moins. Donc pas ok

        Des.save([3,6,5,1])
        j1.setCartes(tg,c1)
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[])))
        Des.save([3,7,5,1])
        self.assertTrue(Jeu.peut_defausser(j1,tg,(d1,[])))
        
        j1.setEnRuine(True)
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[])))
        # Joueur en ruine
        j1.setEnRuine(False)

        self.assertFalse(Jeu.peut_defausser(j1,tg,(dneg,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(ddouble,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d2,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d3,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d4,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d6,[])))

        j1.setCartes(tg,c2)
        self.assertTrue(Jeu.peut_defausser(j1,tg,(Cartes.RIEN,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d5,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d8,[])))

        j1.setCartes(tg,c3)
        self.assertTrue(Jeu.peut_defausser(j1,tg,(d7,[])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[])))



        j1.setCartes(tg,c1)
        b1 = Bateau(1,1,p.it(5).lien(p.it(6)), Cartes.RIEN,Bateau.BateauType.TRANSPORT, False)
        b1.append(CartesGeneral(1,2,0,1,0,0,0,1,0,0))
        b1.save()
        d9 = CartesRessources(2,1,1,1,2) # Trop pour c1, preciser ce qui est retire du bateau
        d10 = CartesRessources(1,1,0,0,0) # Ok si on associe avec d1
        dneg = CartesRessources(3,-1,0,0,0) # negatif
        ddouble = CartesRessources(0.5,1.5,0,0,0) # pas entier
        dgen = CartesGeneral(1,0,0,0,0,0,0,1,0,0) # Carte developpement
        dgen2 = CartesGeneral(1,1,0,0,0,0,0,1,0,0) # Carte developpement
        d11 = CartesRessources(1,1,1,0,0) # Ok pour c1 si on associe avec tout le contenu du bateau
        d12 = CartesRessources(1,0,1,0,0) # Trop pour le bateau
        d13 = CartesRessources(1,2,0,1,0) # Cargaison du batea
        
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d9,[])))
        self.assertTrue(Jeu.peut_defausser(j1,tg,(d1,[(b1,d10)])))
        
#        j1.enRuine = True
#        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,d10)])))
#        # Joueur en ruine
#        j1.enRuine = False
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,dgen)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,dgen2)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,dneg)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,ddouble)])))
        self.assertTrue(Jeu.peut_defausser(j1,tg,(d11,[(b1,d13)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,d12)])))

        Jeu.defausser(j1,tg,(d1,[(b1,d10)]))
        self.assertEqual(j1.getCartes(tg), c1 - d1)

        b2 = Bateau.getBateau(1)
        self.assertEqual(b2.cargaison, CartesGeneral(0,1,0,1,0,0,0,1,0,0))
