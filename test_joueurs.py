import unittest
from joueurs import *
from constructions import *
from plateau import *

class TestCartesRessources(unittest.TestCase):
    def setUp(self):
        
        it = []
        for i in range(0,125):
            it.append(Intersection(i))
        self.it = it
        self.h1 =  Hexagone(it[1], it[12],it[23],it[33],it[22],it[11], HexaType.BOIS,4)
        self.h2 =  Hexagone(it[2], it[13],it[24],it[34],it[23],it[12], HexaType.ARGILE,8)
        self.h3 =  Hexagone(it[3], it[14],it[25],it[35],it[24],it[13], HexaType.BLE,9)
        self.h4 =  Hexagone(it[4], it[15],it[26],it[36],it[25],it[14], HexaType.MER,0)
        self.h5 =  Hexagone(it[5], it[16],it[27],it[37],it[26],it[15], HexaType.MER,0)
        self.h6 =  Hexagone(it[6], it[17],it[28],it[38],it[27],it[16], HexaType.MER,0)
        self.h7 =  Hexagone(it[7], it[18],it[29],it[39],it[28],it[17], HexaType.MER,0,CommerceType.BOIS,[it[28],it[39]])
        self.h8 =  Hexagone(it[8], it[19],it[30],it[40],it[29],it[18], HexaType.MER,0)
        self.h9 =  Hexagone(it[9], it[20],it[31],it[41],it[30],it[19], HexaType.MER,0)
        self.h10 = Hexagone(it[10],it[11],it[22],it[42],it[31],it[20], HexaType.MER,0)
        
        self.h11 = Hexagone(it[22],it[33],it[43],it[53],it[52],it[42], HexaType.BLE,6)
        self.h12 = Hexagone(it[23],it[34],it[44],it[54],it[43],it[33], HexaType.DESERT,0,CommerceType.TOUS,[it[23],it[34],it[44],it[54],it[43],it[33]])
        self.h13 = Hexagone(it[24],it[35],it[45],it[55],it[44],it[34], HexaType.MOUTON,12)
        self.h14 = Hexagone(it[25],it[36],it[46],it[56],it[45],it[35], HexaType.MER,0)
        self.h15 = Hexagone(it[26],it[37],it[47],it[57],it[46],it[36], HexaType.MER,0)
        self.h16 = Hexagone(it[27],it[38],it[48],it[58],it[47],it[37], HexaType.CAILLOU,5)
        self.h17 = Hexagone(it[28],it[39],it[49],it[59],it[48],it[38], HexaType.MOUTON,8)
        self.h18 = Hexagone(it[29],it[40],it[50],it[60],it[49],it[39], HexaType.DESERT,0)
        self.h19 = Hexagone(it[30],it[41],it[51],it[61],it[50],it[40], HexaType.MER,0)
        self.h20 = Hexagone(it[31],it[42],it[52],it[62],it[51],it[41], HexaType.MER,0)
        
        self.h21 = Hexagone(it[43],it[54],it[65],it[75],it[64],it[53], HexaType.BOIS,5)
        self.h22 = Hexagone(it[44],it[55],it[66],it[76],it[65],it[54], HexaType.ARGILE,10)
        self.h23 = Hexagone(it[45],it[56],it[67],it[77],it[66],it[55], HexaType.DESERT,0)
        self.h24 = Hexagone(it[46],it[57],it[68],it[78],it[67],it[56], HexaType.MER,0)
        self.h25 = Hexagone(it[47],it[58],it[69],it[79],it[68],it[57], HexaType.MER,0)
        self.h26 = Hexagone(it[48],it[59],it[70],it[80],it[69],it[58], HexaType.BLE,12)
        self.h27 = Hexagone(it[49],it[60],it[71],it[81],it[70],it[59], HexaType.DESERT,0,CommerceType.TOUS,[it[49],it[60],it[71],it[81],it[70],it[59]])
        self.h28 = Hexagone(it[50],it[61],it[72],it[82],it[71],it[60], HexaType.BLE,6)
        self.h29 = Hexagone(it[51],it[62],it[73],it[83],it[72],it[61], HexaType.MER,0)
        self.h30 = Hexagone(it[52],it[53],it[64],it[84],it[73],it[62], HexaType.MER,0)
        
        self.h31 = Hexagone(it[64],it[75],it[85],it[95], it[94],it[84], HexaType.MOUTON,2)
        self.h32 = Hexagone(it[65],it[76],it[86],it[96], it[85],it[75], HexaType.OR,9)
        self.h33 = Hexagone(it[66],it[77],it[87],it[97], it[86],it[76], HexaType.MOUTON,4)
        self.h34 = Hexagone(it[67],it[78],it[88],it[98], it[87],it[77], HexaType.MER,0)
        self.h35 = Hexagone(it[68],it[79],it[89],it[99], it[88],it[78], HexaType.MER,0)
        self.h36 = Hexagone(it[69],it[80],it[90],it[100],it[89],it[79], HexaType.MER,0)
        self.h37 = Hexagone(it[70],it[81],it[91],it[101],it[90],it[80], HexaType.CAILLOU,10)
        self.h38 = Hexagone(it[71],it[82],it[92],it[102],it[91],it[81], HexaType.ARGILE,2)
        self.h39 = Hexagone(it[72],it[83],it[93],it[103],it[92],it[82], HexaType.MOUTON,6)
        self.h40 = Hexagone(it[73],it[84],it[94],it[104],it[93],it[83], HexaType.MER,0)
        
        self.h41 = Hexagone(it[85],it[96], it[106],it[115],it[105], it[95], HexaType.BLE,3)
        self.h42 = Hexagone(it[86],it[97], it[107],it[116],it[106], it[96], HexaType.ARGILE,6)
        self.h43 = Hexagone(it[87],it[98], it[108],it[117],it[107], it[97], HexaType.CAILLOU,11)
        self.h44 = Hexagone(it[88],it[99], it[109],it[118],it[108], it[98], HexaType.MER,0)
        self.h45 = Hexagone(it[89],it[100],it[110],it[119],it[109], it[99], HexaType.MER,0)
        self.h46 = Hexagone(it[90],it[101],it[111],it[120],it[110],it[100], HexaType.BOIS,8)
        self.h47 = Hexagone(it[91],it[102],it[112],it[121],it[111],it[101], HexaType.BOIS,9)
        self.h48 = Hexagone(it[92],it[103],it[113],it[122],it[112],it[102], HexaType.ARGILE,5)
        self.h49 = Hexagone(it[93],it[104],it[114],it[123],it[113],it[103], HexaType.MER,0)
        self.h50 = Hexagone(it[94],it[95], it[105],it[124],it[114],it[104], HexaType.MER,0)
        
        self.h51 = Hexagone(it[105],it[115], it[1], it[11],it[10],it[124], HexaType.MER,0)
        self.h52 = Hexagone(it[106],it[116], it[2], it[12],it[1], it[115], HexaType.MER,0,CommerceType.ARGILE,[it[1],it[12]])
        self.h53 = Hexagone(it[107],it[117], it[3], it[13],it[2], it[116], HexaType.MER,0)
        self.h54 = Hexagone(it[108],it[118], it[4], it[14],it[3], it[117], HexaType.MER,0)
        self.h55 = Hexagone(it[109],it[119], it[5], it[15],it[4], it[118], HexaType.MER,0)
        self.h56 = Hexagone(it[110],it[120], it[6], it[16],it[5], it[119], HexaType.MER,0)
        self.h57 = Hexagone(it[111],it[121], it[7], it[17],it[6], it[120], HexaType.MER,0,CommerceType.MOUTON, [it[120],it[111]])
        self.h58 = Hexagone(it[112],it[122], it[8], it[18],it[7], it[121], HexaType.MER,0)
        self.h59 = Hexagone(it[113],it[123], it[9], it[19],it[8], it[122], HexaType.MER,0)
        self.h60 = Hexagone(it[114],it[124], it[10],it[20],it[9], it[123], HexaType.MER,0)

        self.tg = Terre('Terre Gauche', [self.h1,self.h2,self.h3,self.h11,self.h12,self.h13,self.h21,self.h22,self.h23,self.h31,self.h32,self.h33,self.h41,self.h42,self.h43],[self.h51,self.h52,self.h53,self.h54,self.h4,self.h14,self.h24,self.h34,self.h35,self.h44,self.h60,self.h10,self.h20,self.h30,self.h40,self.h50])
        self.td = Terre('Terre Droite', [self.h16,self.h17,self.h18,self.h26,self.h27,self.h28,self.h37,self.h38,self.h39,self.h46,self.h47,self.h48],[self.h5,self.h6,self.h7,self.h8,self.h9,self.h15,self.h19,self.h25,self.h29,self.h36,self.h45,self.h49,self.h55,self.h56,self.h57,self.h58,self.h59])
        

        Jeu.des = []
        Jeu.joueurs_origine = [0,0]
        Jeu.terres = [self.tg,self.td]
    
        self.j1 = Jeu.get_joueur(1)
        self.j2 = Jeu.get_joueur(2)
        self.j3 = Jeu.get_joueur(3)
        self.j4 = Jeu.get_joueur(4)

        Jeu.JOUEURS = [self.j1, self.j2, self.j3, self.j4]

        self.j1.terres = [self.tg,self.td]
        self.j2.terres = [self.tg,self.td]
        self.j3.terres = [self.tg,self.td]
        self.j1.mains = [0,0]
        self.j2.mains = [0,0]
        self.j3.mains = [0,0]
        
        self.tg.deplacer_brigand(self.h23)
        self.tg.deplacer_pirate(self.h44)
        self.td.brigand.position.voleur = 0
        self.td.brigand = 0
        self.td.pirate.position.voleur = 0
        self.td.pirate = 0

#(51) (52)   (53)  (54)  (55)  (56)  (57)  (58)  (59)  (60)  
#    1 P   2     3     4     5     6     7     8     9    10-

# 11(1) 12(2) 13(3) 14(4) 15(5) 16(6) 17(7) 18(8) 19(9) 20(10)11 
# 22 x  23  x 24 x  25    26    27    28 P  29    30    31    22

#(11)33(12)34(13)35(14)36(15)37(16)38(17)39(18)40(19)41(20)42
# x  43 xM 44 x  45    46    47  x 48  x 49 x  50    51    52

# 53(21)54(22)55(23)56(24)57(25)58(26)59(27)60(28)61(29)62(30)53
# 64 x  65 x  66 x  67    68    69 x  70 xM 71 x  72    73    64

#(31)75(32)76(33)77(34)78(35)79(36)80(37)81(38)82(39)83(40)84
# x  85 x  86 x  87    88    89    90 x  91 x  92 x  93    94

# 95(41)96(42)97(43)98(44)99(45)100 x 101 x 102 x 103   104   95 ( (46) (47) (48)  (49)  (50) )
# 105x 106 x 107 x 108   109    110   111   112   113   114   105

#   115  116   117   118    119   120P  121   122   123   124
#    1     2     3     4     5     6     7     8     9    10
#       

    def tearDown(self):
        for i in self.it:
            i.colonie = 0
            for a in i.liens :
                a.route = 0
                a.bateau = 0
        
        Jeu.JOUEURS = [self.j1, self.j2, self.j3, self.j4]

        Jeu.des = []
        Jeu.joueurs_origine = [0,0]
        Jeu.terres = [self.tg,self.td]
    

        for j in [self.j1,self.j2,self.j3]:
            j.colonies = []
            j.villes = []
            j.routes = []
            j.bateaux_transport = []
            j.cargo = []
            j.voilier = []
        self.tg.deplacer_brigand(self.h23)
        self.tg.deplacer_pirate(self.h44)
        if self.td.brigand != 0:
            self.td.brigand.position.voleur = 0
            self.td.brigand = 0
        if self.td.pirate != 0:
            self.td.pirate.position.voleur = 0
            self.td.pirate = 0
                            
# 2 niveaux de tests : le niveau joueur et le niveau conflits. Quand un joueur joue il a deja des restrictions de son jeu (par exemple, pas question de lui proposer de construire une colonie n'importe ou). A ce niveau, toute verite autre que celle de la racine de l'arbre d'action est virtuelle. Le niveau des conflits s'occupe de realiser les actions des arbres d'action et va donc devoir faire plus de verification. Par exemple, on ne peut pas empecher un joueur de deaplcer un bateau sur l'emplacement d'un autre bateau car il est possible que ce dernier soit deplace avant et laisse son emplacement disponible. Donc cette verification ne peut se faire que pendant la phase de resolution.
#
# Donc pour chaque test : on separe bien les verifications de type "pendant que le joueur joue" et creation des actions virtuelles de l'arbre d'un cote, et "pendant que le joueur dort" et actions irreversibles de l'autre.

# Un joueur possede un arbre dont : la racine contient l'etat du jeu le matin, et le reste de l'arbre contient des actions virtuelle. Pour connaitre l'etat du jeu a un endroit donne de l'abre, il faut calculer toutes les actions entre la racine et le noeud.

# Attention a respecter le partage des ressources et des actions entre chaque terre.
# 4 joueurs placent leur colonies et route
#   Ils doivent le faire selon les regles, dans l'ordre, avec colonie sur terre et route sur terre, accolees, et sur des cases reglementaires (pas occupees, et par a 1 case d'une autre colonie). Ils peuvent aussi construire un bateau a la place de la route
## Les joueurs construisent. Ils doivent avoir assez de ressources, et construire sur des cases reglementaire.
## Les joueurs deplacent leurs bateaux : pirate, superposition.
## Les joueurs achetent des cartes developpement : assez de ressource
## Les joueurs echangent avec leurs bateaux : au bon endroit, et conservation des biens
## Les joueurs recoltent leur ressources : lancement des des, autre que 7, recolte des ressources en fonction des villages et des villes, et des brigands. Recolte de l'or
## Les joueurs utilisent le voleur : Seuelement si un 7, defausse, vol et deplacement du brigand ou du pirate, 
## Les joueurs utilisent leur cartes de developpement : chevallier + Deplacement du voleur, monopole, decouverte, construction de route. 
# Les joueurs regardent les routes les plus longue et les armees les plus grandes
# Les joueurs comptent leur points : en fonction des terres et des bonus 
# Les joueurs tombent en ruine, les autres fouillent les ruines : respect des delais et des rachats et disparitions des ruines. Epaves
## Les joueurs echangent entre eux et avec leur port : en fonction du pirate, du type de port.
## Les joueurs colonisent d'autres terres
## Les joueurs se defaussent
#
#
# Les joueurs proposent des actions et reglent les conflits
#
#


# 4 joueurs placent leur colonies et route
#   Ils doivent le faire selon les regles, dans l'ordre, avec colonie sur terre et route sur terre, accolees, et sur des cases reglementaires (pas occupees, et par a 1 case d'une autre colonie). Ils peuvent aussi construire un bateau a la place de la route. Ils doivent tout poser sur la bonne terre (ici la gauche).

## :s/\(j\d,\)\(\d\+\),\(\d\+\)/$1self.it[$2],self.it[$3]
    """
    def test_pose_initiale(self):
        j1 = Jeu.get_joueur(1)
        j2 = Jeu.get_joueur(2)
        j3 = Jeu.get_joueur(3)
        self.assertEqual(Jeu.joueur_courrant(),j1)
        self.assertTrue(Jeu.peut_poser_colonieR(j1,44,55))
        self.assertFalse(Jeu.peut_poser_colonieR(j2,44,55))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,36,25))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,70,81))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,29,18))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,24,55))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,45,46))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,25,36))
        self.assertTrue(Jeu.peut_poser_colonieB(j1,25,36))
        Jeu.poser_colonieR(j1,44,55)
        self.asserEqual(len(j1.colonies),1)
        self.asserEqual(len(j1.routes),1)
        self.assertEqual(Jeu.joueur_courrant(),j2)
        self.assertFalse(Jeu.peut_poser_colonieR(j2,44,54))
        self.assertFalse(Jeu.peut_poser_colonieR(j2,34,44))
        self.assertFalse(Jeu.peut_poser_colonieR(j2,55,44))
        self.assertFalse(Jeu.peut_poser_colonieR(j2,55,45))
        self.assertFalse(Jeu.peut_poser_colonieR(j3,71,81))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,71,81))
        self.assertTrue(Jeu.peut_poser_colonieB(j2,64,84))
        self.assertFalse(Jeu.peut_poser_colonieR(j2,64,84))
        self.assertTrue(Jeu.peut_poser_colonieB(j1,25,36))
        self.asserEqual(len(j2.colonies),1)
        self.asserEqual(len(j2.routes),0)
        self.asserEqual(len(j2.bateaux),1)
        Jeu.poser_colonieB(j2,64,84)
        self.assertFalse(Jeu.distribuerPremiereRessources())
        self.assertEqual(Jeu.joueur_courrant(),j3)
        self.assertFalse(Jeu.peut_poser_colonieR(j2,23,34))
        self.assertFalse(Jeu.peut_poser_colonieR(j1,23,34))
        self.assertTrue(Jeu.peut_poser_colonieR(j3,23,34))
        self.assertFalse(Jeu.peut_poser_colonieR(j3,64,84))
        self.assertFalse(Jeu.peut_poser_colonieB(j3,64,84))
        Jeu.poser_colonieR(j3,106,116)
        self.assertEqual(Jeu.joueur_courrant(),j3)
        Jeu.poser_colonieR(j3,67,77)
        self.assertEqual(Jeu.joueur_courrant(),j2)
        Jeu.poser_colonieR(j2,22,33)
        Jeu.poser_colonieR(j1,24,35)
        self.assertTrue(j1.choisir_FColonie(24))
        self.assertFalse(Jeu.distribuerPremiereRessources())
        self.assertTrue(j2.choisir_FColonie(64))
        self.assertFalse(Jeu.distribuerPremiereRessources())
        self.assertTrue(j3.choisir_FColonie(67))
        self.asserEqual(len(j1.colonies),2)
        self.asserEqual(len(j1.routes),2)
        self.asserEqual(len(j1.bateaux),0)
        self.asserEqual(len(j2.colonies),2)
        self.asserEqual(len(j2.routes),1)
        self.asserEqual(len(j2.bateaux),1)
        self.asserEqual(le0n(j3.colonies),2)
        self.asserEqual(len(j3.routes),2)
        self.asserEqual(len(j3.bateaux),0)
        

        self.assertTrue(Jeu.distribuerPremiereRessources())
        
        self.assertEqual(j1.ressources(tg), CartesRessources(1,1,0,0,1))
        self.assertEqual(j1.ressources(td), Cartes.RIEN)
        self.assertEqual(j2.ressources(tg), CartesRessources(0,0,1,0,1))
        self.assertEqual(j2.ressources(td), Cartes.RIEN)
        self.assertEqual(j3.ressources(tg), Cartes.RIEN)
        self.assertEqual(j3.ressources(td), Cartes.RIEN)
    """

# Les joueurs construisent. Ils doivent avoir assez de ressources, et construire sur des cases reglementaire.

#                                                  

# test de construction de colonie, route et bateau

    def test_construire(self):
        j1 = self.j1
        j2 = self.j2

        i44 = self.it[44] 
        i55 = self.it[55]
        i66 = self.it[66]
        i68 = self.it[68]
        i87 = self.it[87]
        a44 = i44.lien(i55)
        a55 = i55.lien(i66)
        c1 = Colonie(j1,i44)
        r1 = Route(j1,a44)
        r2 = Route(j1,a55)
        j1.setCartes(self.tg,Tarifs.COLONIE)
        self.assertTrue(Jeu.peut_construire_colonie(j1,i66)) # Ok
        self.assertFalse(Jeu.peut_construire_colonie(j1,i44))# Il y a deja une colonie
        self.assertFalse(Jeu.peut_construire_colonie(j1,i55))# Il y a une colonie a 1 case
        self.assertFalse(Jeu.peut_construire_colonie(j1,i87))# Il n'y a aucun lien
        self.assertFalse(Jeu.peut_construire_colonie(j1,i68))# C'est la mer
        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_colonie(j1,i66)) # Plus assez de ressources
        
        i75 = self.it[75] 
        i64 = self.it[64] 
        i53 = self.it[53] 
        a75 = i75.lien(i64)
        a64 = i64.lien(i53)
        j1.setCartes(self.tg,Tarifs.COLONIE)
        c2 = Colonie(j2,i75)
        r3 = Route(j2,a75)
        r4 = Route(j2,a64)
        self.assertFalse(Jeu.peut_construire_colonie(j1,i75)) # Colonie adverse
        self.assertFalse(Jeu.peut_construire_colonie(j1,i64)) # Colonie adverse a une case
        self.assertFalse(Jeu.peut_construire_colonie(j1,i53)) # Relie a une route mais adverse

        i54 = self.it[54] 
        i65 = self.it[65] 
        a65 = i65.lien(i54)
        a54 = i54.lien(i44)
        r5 = Route(j2,a65)
        r6 = Route(j2,a54)
        self.assertFalse(Jeu.peut_construire_colonie(j1,i65)) # Relie a une route mais colonie adverse a une case
        
        i = len(j1.colonies)
        Jeu.construire_colonie(j1,i66)
        self.assertEqual(len(j1.colonies),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
        
        j1.setCartes(self.tg,Tarifs.ROUTE)
        i66 = self.it[66] 
        i23 = self.it[23] 
        i75 = self.it[75] 
        i77 = self.it[77] 
        i67 = self.it[67] 
        i78 = self.it[78] 
        i34 = self.it[34] 
        i85 = self.it[85] 
        i56 = self.it[56] 
        a66 = i66.lien(i77)
        a23 = i23.lien(i34)
        a85 = i75.lien(i85)
        a77 = i77.lien(i67)
        a67 = i67.lien(i78)
        a56 = i67.lien(i56)
        a34 = i44.lien(i34)
        self.assertTrue(Jeu.peut_construire_route(j1,a66))  # ok relie a une route
        self.assertTrue(Jeu.peut_construire_route(j1,a34))  # ok relie a une colonie
        self.assertFalse(Jeu.peut_construire_route(j1,a55)) # existe deja
        self.assertFalse(Jeu.peut_construire_route(j1,a23)) # relie a rien
        self.assertFalse(Jeu.peut_construire_route(j1,a85)) # relie seulement a l'ennemi
        r7 = Route(j1,a66)
        r8 = Route(j1,a77)
        self.assertFalse(Jeu.peut_construire_route(j1,a67)) # c'est la mer
        self.assertFalse(Jeu.peut_construire_route(j1,a66)) # existe deja
        self.assertTrue(Jeu.peut_construire_route(j1,a56)) # cotier

        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_route(j1,a56)) # manque de ressource
        j1.setCartes(self.tg,Tarifs.ROUTE)
        self.assertTrue(Jeu.peut_construire_route(j1,a56))
        i = len(j1.routes)
        Jeu.construire_route(j1,a56)
        self.assertEqual(len(j1.routes),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)

        j1.setCartes(self.tg,Tarifs.BATEAUX_TRANSPORT)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a67)) # Aucun lien


        c3 = Colonie(j1,i67)
        self.assertTrue(Jeu.peut_construire_bateau(j1,a67)) # ok

        i52 = self.it[52]
        a53 = i53.lien(i52)
        c4 = Colonie(j2,i53)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a53)) # relie mais a un adversaire

        a2 = self.it[2].lien(self.it[116])
        self.assertFalse(Jeu.peut_construire_bateau(j1,a2)) # relie a rien
        self.assertFalse(Jeu.peut_construire_bateau(j1,a34)) # relie mais terrestre
        
        Colonie(j1,self.it[2])
        Bateau(j2,a2)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a2)) # emplacement occupe
        
        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_construire_bateau(j1,a67))
        j1.setCartes(self.tg,Tarifs.BATEAUX_TRANSPORT)
        i = len(j1.bateaux_transport)
        Jeu.construire_bateau(j1,a67)
        self.assertEqual(len(j1.bateaux_transport),i+1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)


# test d'evolution d'une colonie en ville

    def test_evoluer_colonie(self):

        j1 = Jeu.get_joueur(1)
        c1 = Colonie(j1,self.it[44])
        j2 = self.j2
        c2 = Colonie(j2,self.it[75])

        j1.setCartes(self.tg,Tarifs.VILLE)
        self.assertTrue(Jeu.peut_evoluer_colonie(j1,c1))
        self.assertFalse(Jeu.peut_evoluer_colonie(j1,c2)) # Colonie adverse
        j1.setCartes(self.tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_evoluer_colonie(j1,c1)) # Pas assez ressource
        j1.setCartes(self.tg,Tarifs.VILLE)
        self.assertTrue(Jeu.peut_evoluer_colonie(j1,c1))
        i = len(j1.villes)
        j = len(j1.colonies)
        Jeu.evoluer_colonie(j1,c1)
        self.assertEqual(len(j1.villes),i+1)
        self.assertEqual(len(j1.colonies),j-1)
        self.assertEqual(j1.getCartes(self.tg),Cartes.RIEN)
   
 
    def test_deplacer_bateaux(self):
        
        j1 = self.j1
        j2 = self.j2
        
        i46 = self.it[46] 
        i56 = self.it[56] 
        i67 = self.it[67]
        i78 = self.it[78]
        i57 = self.it[57]
        i68 = self.it[68]
        i77 = self.it[77]
        i45 = self.it[45]
        i35 = self.it[35]
        i55 = self.it[55]
        
        a46 = i46.lien(i56)
        a56 = i56.lien(i67)
        a67 = i67.lien(i78)
        a78 = i78.lien(i68)
        a68 = i68.lien(i57)
        a57 = i57.lien(i46)
        a77 = i67.lien(i77)
        a45 = i35.lien(i45)
        a55 = i45.lien(i55)


        b1 = Bateau(j1,a46)
        b12 = Bateau(j1,a56)
        b13 = Bateau(j1,a45)
        b2 = Bateau(j2,a57)

        self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a77)) # Trop loin
        self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a57,True)) # Deja un bateau adverse
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b1,a57)) # Bateau adverse qui peut se deplacer
        self.assertFalse(Jeu.peut_deplacer_bateau(j1,b1,a56)) # Bateau allie
        self.assertFalse(Jeu.peut_deplacer_bateau(j1,b13,a55)) # En pleine terre
        self.assertTrue(Jeu.peut_deplacer_bateau(j1,b12,a77)) # cotier
        self.tg.deplacer_pirate(self.h24)
        self.assertFalse(Jeu.peut_deplacer_bateau(j1,b12,a77)) # Pirate
        self.tg.deplacer_pirate(self.h44)
        
        Jeu.deplacer_bateau(j1,b12,a77)
        self.assertFalse(Jeu.peut_deplacer_bateau(j1,b12,a56)) # a deja bouge
               

 
    def test_acheter_developpement(self):        
        

        j1 = self.j1
        tg = self.tg 
        j1.setCartes(tg,Tarifs.DEVELOPPEMENT)
        self.assertTrue(Jeu.peut_acheter_carte_developpement(j1,tg))
        j1.setCartes(tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_acheter_carte_developpement(j1,tg))
        j1.setCartes(tg,Tarifs.DEVELOPPEMENT)


# test les echanges entre terre et bateau, et les evolutions de bateau
    def test_echanger_evoluer_bateau(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        self.j1.terres = [tg]
        self.j2.terres = [tg]
        cartes = CartesGeneral(3,3,3,3,3,1,0,0,1,2)
        self.j1.mains = [cartes]
        self.j2.mains = [CartesGeneral(5,5,5,5,5,5,5,5,5,5)]

        i56 = self.it[56]
        i108 = self.it[108]
        i52 = self.it[52]
        a56 = i56.lien(self.it[46])
        a4 = self.it[4].lien(self.it[15])
        a108 = i108.lien(self.it[117])
        a35 = self.it[35].lien(self.it[45])
        a1 = self.it[1].lien(self.it[12]) 
        a39 = self.it[39].lien(self.it[28])
        a52 = i52.lien(self.it[62])

        b1 = Bateau(j1,a56)
        b2 = Bateau(j1,a4)
        b3 = Bateau(j1,a108)
        b4 = Bateau(j1,a35)
        b5 = Bateau(j1,a1)
        b6 = Bateau(j1,a39)
        b7 = Bateau(j2,a52)

        c = CartesGeneral(1,2,0,0,1,1,1,0,0,0)
        b1.append(c)
        b2.append(c)
        b3.append(c)
        b4.append(c)
        b5.append(c)
        b6.append(c)
        b7.append(c)

        c1 = Colonie(j1,i56)
        c2 = Colonie(j2,i108)
        c3 = Colonie(j1,i52)
        
        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b1)) # OK touche une colonie
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b2)) # En pleine mer
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b3)) # Colonie ennemie
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b4)) # Relie a rien
        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b5)) # Ok touche un port
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b6)) # Port mais sur une terre non colonisee
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b7)) # Pas un bateau allie
        j1.setCartes(tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1)) # Pas assez ressource
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5)) # 
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
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb)) # OK touche une colonie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b2,cecht,cechb)) # En pleine mer
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b3,cecht,cechb)) # Colonie ennemie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b4,cecht,cechb)) # Relie a rien
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb)) # Ok touche un port
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b6,cecht,cechb)) # Port mais sur une terre non colonisee
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b7,cecht,cechb)) # Pas un bateau allie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch1,cechb)) # Trop de ressources demandees, le bateau est plein
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch2,cechb)) # Trop de ressources demandees la colonie n'a pas tout ca
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbtoomuch)) # Trop de ressources demandees, le bateau n'a pas tout ca
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtneg,cechb)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtdouble,cechb)) # Echange non entier
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbdouble)) # Echange non entier

        j1.setCartes(tg,Tarifs.CARGO)
        Jeu.evoluer_bateau(j1,b1)
        self.assertEqual(j1.getCartes(tg),Cartes.RIEN)
        self.assertEqual(b1.etat, Bateau.BateauType.CARGO)
        j1.setCartes(tg,cartes)

        Jeu.echanger_bateau(j1,b1,cecht,cechb)
        self.assertEqual(j1.getCartes(tg),cartes - cecht + cechb)
        self.assertEqual(b1.cargaison,c + cecht - cechb)
        j1.recevoir(tg,cecht - cechb)
        b1.append(cechb - cecht)


        b2.evolue()
        b3.evolue()
        b4.evolue()
        b5.evolue()
        b6.evolue()
        b7.evolue()

        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b1)) # OK touche une colonie
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b2)) # En pleine mer
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b3)) # Colonie ennemie
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b4)) # Relie a rien
        self.assertTrue(Jeu.peut_evoluer_bateau(j1,b5)) # Ok touche un port
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b6)) # Port mais sur une terre non colonisee
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b7)) # Pas un bateau allie
        j1.setCartes(tg,Cartes.RIEN)
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1)) # Pas assez ressource
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5)) # 
        j1.setCartes(tg,cartes) 

        cecht = CartesGeneral(2,2,0,0,0,0,0,0,0,1) 
        cechb = CartesGeneral(0,0,0,0,1,1,0,0,0,0) 
        cechttoomuch1 = CartesGeneral(2,2,2,2,0,0,0,0,0,1) 
        cechttoomuch2 = CartesGeneral(0,0,0,0,0,0,0,1,0,0) 
        cechbtoomuch = CartesGeneral(2,0,0,0,0,0,0,0,0,0) 
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb)) # OK touche une colonie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b2,cecht,cechb)) # En pleine mer
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b3,cecht,cechb)) # Colonie ennemie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b4,cecht,cechb)) # Relie a rien
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb)) # Ok touche un port
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b6,cecht,cechb)) # Port mais sur une terre non colonisee
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b7,cecht,cechb)) # Pas un bateau allie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch1,cechb)) # Trop de ressources demandees, le bateau est plein
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch2,cechb)) # Trop de ressources demandees la colonie n'a pas tout ca
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbtoomuch)) # Trop de ressources demandees, le bateau n'a pas tout ca
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtneg,cechb)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtdouble,cechb)) # Echange non entier
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbdouble)) # Echange non entier

        j1.setCartes(tg,Tarifs.VOILIER)
        Jeu.evoluer_bateau(j1,b1)
        self.assertEqual(j1.getCartes(tg),Cartes.RIEN)
        self.assertEqual(b1.etat, Bateau.BateauType.VOILIER)
        j1.setCartes(tg,cartes)
        
        Jeu.echanger_bateau(j1,b1,cecht,cechb)
        self.assertEqual(j1.getCartes(tg),cartes - cecht + cechb)
        self.assertEqual(b1.cargaison,c + cecht - cechb)
        j1.recevoir(tg,cecht - cechb)
        b1.append(cechb - cecht)
        
        b2.evolue()
        b3.evolue()
        b4.evolue()
        b5.evolue()
        b6.evolue()
        b7.evolue()

        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b1)) # Un voilier ne peut evoluer
        self.assertFalse(Jeu.peut_evoluer_bateau(j1,b5)) # 

        cecht = CartesGeneral(2,2,0,0,0,0,0,0,0,1) 
        cechb = CartesGeneral(0,0,0,0,1,1,0,0,0,0) 
        cechttoomuch1 = CartesGeneral(2,2,2,2,0,0,0,0,0,1) 
        cechttoomuch2 = CartesGeneral(0,0,0,0,0,0,0,1,0,0) 
        cechbtoomuch = CartesGeneral(2,0,0,0,0,0,0,0,0,0) 
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b1,cecht,cechb)) # OK touche une colonie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b2,cecht,cechb)) # En pleine mer
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b3,cecht,cechb)) # Colonie ennemie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b4,cecht,cechb)) # Relie a rien
        self.assertTrue(Jeu.peut_echanger_bateau(j1,b5,cecht,cechb)) # Ok touche un port
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b6,cecht,cechb)) # Port mais sur une terre non colonisee
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b7,cecht,cechb)) # Pas un bateau allie
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch1,cechb)) # Trop de ressources demandees, le bateau est plein
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechttoomuch2,cechb)) # Trop de ressources demandees la colonie n'a pas tout ca
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbtoomuch)) # Trop de ressources demandees, le bateau n'a pas tout ca
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtneg,cechb)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cechtdouble,cechb)) # Echange non entier
        self.assertFalse(Jeu.peut_echanger_bateau(j1,b1,cecht,cechbdouble)) # Echange non entier




# Les joueurs echangent entre eux.
    def test_echanger_joueur(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        self.j1.terres = [tg]
        self.j2.terres = [tg,td]
        c1 = CartesGeneral(3,0,3,3,3,1,0,0,0,0)
        c2g = CartesRessources(3,3,3,1,0)
        c2d = CartesRessources(1,0,0,1,0)
        self.j1.mains = [c1]
        self.j2.mains = [c2g,c2d]
        
        c1ech1 = CartesRessources(1,0,0,0,0)
        c1ech2 = CartesRessources(0,1,0,0,0)
        c1ech3 = CartesGeneral(1,0,0,0,0,1,0,0,0,0)
        c1ech1neg = CartesRessources(1,-1,0,0,0)
        c1ech1double = CartesRessources(0.5,0,0,0,0)
        c2ech = CartesRessources(0,0,0,1,0)
        c2echneg = CartesRessources(0,0,0,1,-1)
        c2echdouble = CartesRessources(0,0,0,0.5,0)


        self.assertTrue(Jeu.peut_echanger(j1,j2,tg,c1ech1,c2ech)) # Ok
        self.assertFalse(Jeu.peut_echanger(j1,j2,tg,c1ech2,c2ech)) # J1 n'a pas la somme requise
        self.assertFalse(Jeu.peut_echanger(j1,j2,tg,c1ech3,c2ech)) # J1 offre des cartes de developpement  
        self.assertFalse(Jeu.peut_echanger(j1,j2,td,c1ech3,c2ech)) # J1 n'est pas sur td
        self.assertFalse(Jeu.peut_echanger(j1,j2,tg,c1ech1neg,c2ech)) # Echange Negatif
        self.assertFalse(Jeu.peut_echanger(j1,j2,tg,c1ech1double,c2ech)) # Echange non entier
        self.assertFalse(Jeu.peut_echanger(j1,j2,tg,c1ech1,c2echneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger(j1,j2,tg,c1ech1,c2echdouble)) # Echante non entier

        Jeu.echanger(j1,j2,tg,c1ech1,c2ech)
        self.assertEqual(j1.getCartes(tg),c1 - c1ech1 + c2ech)        
        self.assertEqual(j2.getCartes(tg),c2g + c1ech1 - c2ech)        


# Les joueurs echangent avec les ports et marche.
    def test_echanger_commerce(self):
        
        j1 = self.j1
        tg = self.tg
        td = self.td
        port = self.h52
        marche = self.h12
        self.j1.terres = [tg]
        c1 = CartesRessources(3,8,4,4,4)
        cneg = CartesRessources(-1,2,0,0,0)
        cdouble = CartesRessources(0.5,0.5,0,0,0)
        self.j1.mains = [c1]
        
        self.tg.deplacer_brigand(self.h23)
        self.tg.deplacer_pirate(self.h44)
        
        self.assertTrue(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertFalse(Jeu.peut_echanger_classique(j1,td,Cartes.BOIS,Cartes.ARGILE)) # Pas la bonne Terre
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Aucun Commerce
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Aucun Commerce.
        self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.ARGILE,Cartes.BOIS)) # Pas assez de argile
        self.assertFalse(Jeu.peut_echanger_classique(j1,tg,cneg,Cartes.BOIS)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_classique(j1,tg,cdouble,Cartes.BOIS)) # Echante non entier
        self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,cneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_classique(j1,tg,Cartes.BOIS,cdouble)) # Echange non entier
        
        Jeu.echanger_classique(j1,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j1.getCartes(tg), CartesRessources(4,8,0,4,4))

        c1 = CartesRessources(2,6,3,3,3)
        self.j1.mains = [c1]
        self.tg.deplacer_brigand(self.h23)
        self.tg.deplacer_pirate(self.h44)
        
        Colonie(j1,self.it[1])
        port.commerceType = CommerceType.TOUS
        self.assertTrue(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,td,Cartes.BOIS,Cartes.ARGILE)) # Pas la bonne terre
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.ARGILE,Cartes.BLE)) # Pas assez de ressource
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,cneg,Cartes.BOIS)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,cdouble,Cartes.BOIS)) # Echante non entier
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,cneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,cdouble)) # Echange non entier
        self.tg.deplacer_pirate(self.h52)
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Piate

        self.tg.deplacer_pirate(self.h44)
        Jeu.echanger_commerce_tous(j1,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j1.getCartes(tg), CartesRessources(3,6,0,3,3))

        c1 = CartesRessources(1,4,2,2,2)
        self.j1.mains = [c1]
        port.commerceType = CommerceType.BOIS
        self.assertTrue(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertFalse(Jeu.peut_echanger_commerce(j1,td,Cartes.BOIS,Cartes.ARGILE)) # Pas la bonne terre
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.ARGILE,Cartes.BLE)) # Pas assez de ressource
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,cneg,Cartes.BOIS)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,cdouble,Cartes.BOIS)) # Echante non entier
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,cneg)) # Echange negatif
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,cdouble)) # Echange non entier
        self.tg.deplacer_pirate(self.h52)
        self.assertFalse(Jeu.peut_echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE)) # Pirate

        self.tg.deplacer_pirate(self.h44)
        Jeu.echanger_commerce(j1,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j1.getCartes(tg), CartesRessources(2,4,0,2,2))
        
        j2 = self.j2
        tg = self.tg
        self.j2.terres = [tg]
        c2 = CartesRessources(2,3,3,3,3)
        self.j2.mains = [c2]
        
        Colonie(j2,self.it[33])
        marche.commerceType = CommerceType.TOUS
        self.assertTrue(Jeu.peut_echanger_commerce_tous(j2,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j2,tg,Cartes.ARGILE,Cartes.BLE)) ## Pas assez de ressource

        self.tg.deplacer_brigand(self.h12)
        self.assertFalse(Jeu.peut_echanger_commerce_tous(j2,tg,Cartes.BOIS,Cartes.ARGILE)) # Brigand
        
        self.tg.deplacer_brigand(self.h23)
        Jeu.echanger_commerce_tous(j2,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j2.getCartes(tg), CartesRessources(3,3,0,3,3))

        c2 = CartesRessources(1,2,2,2,2)
        self.j2.mains = [c2]
        marche.commerceType = CommerceType.BOIS
        self.assertTrue(Jeu.peut_echanger_commerce(j2,tg,Cartes.BOIS,Cartes.ARGILE))
        self.assertFalse(Jeu.peut_echanger_commerce(j2,tg,Cartes.ARGILE,Cartes.BLE)) # Pas assez de ressource

        self.tg.deplacer_brigand(self.h12)
        self.assertFalse(Jeu.peut_echanger_commerce(j2,tg,Cartes.BOIS,Cartes.ARGILE)) # Brigand
        
        self.tg.deplacer_brigand(self.h23)
        Jeu.echanger_commerce(j2,tg,Cartes.BOIS,Cartes.ARGILE)
        self.assertEqual(j2.getCartes(tg), CartesRessources(2,2,0,2,2))


# Les joueurs recoltent leur ressources : lancement des des, autre que 7, recolte des ressources en fonction des villages et des villes, et des brigands. Recolte de l'or
    def test_recolter_ressources(self):
        
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.terres = [tg]
        j2.terres = [tg,td]
        c = Cartes.RIEN
        j1.mains = [c]
        j1.aur = [0]
        j2.mains = [c,c]
        j2.aur = [0,0]
    
        c1 = Colonie(j1,self.it[1]) # 4 : Bois Port Mer
        c2 = Colonie(j1,self.it[54])# 5 : Bois, 10 : Argile Marche
        c3 = Colonie(j1,self.it[66])# 10 : Argile, 4 : Mouton, Desert
        c4 = Colonie(j1,self.it[85])# 2 : Mouton, 9 : Or, 3 : Ble
        c3.evolue()

        self.tg.deplacer_brigand(self.h3)
        self.td.brigand = Voleur(self.h27,Voleur.VoleurType.BRIGAND)
        
        self.assertFalse(Jeu.peut_recolter_ressources(-1))
        self.assertFalse(Jeu.peut_recolter_ressources(0))
        self.assertFalse(Jeu.peut_recolter_ressources(1))
        self.assertFalse(Jeu.peut_recolter_ressources(7))
        self.assertFalse(Jeu.peut_recolter_ressources(13))
        self.assertTrue(Jeu.peut_recolter_ressources(2))
        self.assertTrue(Jeu.peut_recolter_ressources(10))

        self.j1.mains = [c]
        Jeu.recolter_ressources(4)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,1,0,2))
        self.j1.mains = [c]
        Jeu.recolter_ressources(10)
        self.assertEqual(j1.getCartes(tg),CartesRessources(3,0,0,0,0))
        self.j1.mains = [c]
        Jeu.recolter_ressources(9)
        self.assertEqual(j1.getCartes(tg),c)
        self.assertEqual(j1.getOr(tg),1)

        j1.aur = [0]
        
        self.j1.mains = [c]
        tg.deplacer_brigand(self.h1)
        Jeu.recolter_ressources(4)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,0,0,2))
        
        self.j1.mains = [c]
        tg.deplacer_brigand(self.h33)
        Jeu.recolter_ressources(4)
        self.assertEqual(j1.getCartes(tg),CartesRessources(0,0,1,0,0))



        c6 = Colonie(j2,self.it[64])# 5 : Bois, 2 ; Mouton Mer
        c7 = Colonie(j2,self.it[102]) # Terre Droite #  2 : Argile, 5 : Argile, 9: bois

        
        self.j2.mains = [c,c]
        Jeu.recolter_ressources(5)
        self.assertEqual(j2.getCartes(tg),CartesRessources(0,0,1,0,0))
        self.assertEqual(j2.getCartes(td),CartesRessources(1,0,0,0,0))
        
        self.j1.mains = [c] 
        j1.aur = [0]
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))
        j1.aur = [1]
        self.assertTrue(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(1,1,0,0,0)))
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(-1,2,0,0,0)))
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,CartesRessources(0.5,0.5,0,0,0)))
        Jeu.acheter_ressource(j1,tg, Cartes.BLE)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)
        self.assertFalse(Jeu.peut_acheter_ressource(j1,tg,Cartes.BLE))

# Les joueurs colonisent d'autres terres

    def test_coloniser(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.terres = [tg]
        j2.terres = [tg,td]
        c = Cartes.RIEN
        j1.mains = [c]
        j1.aur = [0]
        j1.chevalliers = [0]
        j1.deplacement_voleur = [False]
        j2.mains = [c,c]
        j2.aur = [0,0]
        j2.chevalliers = [0,0]
        j2.deplacement_voleur = [False,False]
          
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

        i47 = self.it[47] # Point de colonisation
        i60 = self.it[60] # Colonisation trop lointaine
        i57 = self.it[57] # Pour le bateau
        i46 = self.it[46] # Pour le bateau (2)
        a1 = i47.lien(i57)
        a12 = i57.lien(i46)
        i48 = self.it[48] # Pour aller plus loin
        i58 = self.it[58] # Pour aller plus loin
        i38 = self.it[38] # Pour mettre une colonie de j2
        i93 = self.it[93] # Bteau du joueur 2
        i104 = self.it[104] # Bateau du joueur 2
        a2 = i93.lien(i104)
        
        b1 = Bateau(j1,a1)
        b2 = Bateau(j2,a2)

        carg1 = CartesRessources(1,1,1,0,1) # Juste assez pour coloniser
        carg2 = CartesGeneral(3,1,3,0,1,1,0,0,1,0) # Juste assez pour coloniser et transferer
        carg3 = CartesRessources(1,1,0,0,1) # Cargaison pas suffisante
        transf1toomuch = Cartes.BLE # Plus de ressource dans le bateau
        transf1neg = Cartes.BLE * -1 # Transfert nefatif
        transf2 = CartesGeneral(1,0,2,0,0,1,0,0,0,0) # Juste assez pour coloniser et transferer
        transf2double = Cartes.BOIS * 0.5 # Transfert non entier

        b1.cargaison = carg1
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i47,Cartes.RIEN))
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i48,Cartes.RIEN))
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i60,Cartes.RIEN)) # Trop loin
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i57,Cartes.RIEN)) # Dans l'eau
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i47,transf1toomuch)) # Transfert trop eleve
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i47,transf1neg)) # Transfert negatif
        

        b1.cargaison = carg3
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i47,Cartes.RIEN)) # Pas assez de cargaison
        
        b2.cargaison = carg1
        self.assertFalse(Jeu.peut_coloniser(j1,b2,i93,Cartes.RIEN)) # Pas le bon bateau

        b1.cargaison = carg2
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i47,transf2))
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i47,transf2double)) # Transfert non entier

        j1.terres = [tg,td]
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i47,transf2)) # La terre est deja colonisee
        
        j1.terres = [tg]
        c = Colonie(j2,i47)    
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i47,transf2)) # Il y a une colonie a cet emplacement
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i58,transf2)) # Il y a une colonie voisine
        self.assertTrue(Jeu.peut_coloniser(j1,b1,i48,transf2)) # Il y a une colonie voisine

        b1.deplacer(a12)
        self.assertFalse(Jeu.peut_coloniser(j1,b1,i48,transf2)) # Le bateau n'est pas cotier
        b1.deplacer(a1)
        Jeu.coloniser(j1,b1,i48,transf2)
        

        self.assertNotEqual(j1.getTerreIndex(td),-1)
        self.assertEqual(j1.getCartes(td),transf2)
        self.assertEqual(j1.getOr(td),0)
        self.assertEqual(j1.get_deplacement_voleur(td),False)
        self.assertEqual(j1.get_chevalliers(td),0)
        self.assertEqual(b1.cargaison,carg2 - transf2 - Tarifs.COLONIE )
        self.assertEqual(len(j1.colonies),1)
        self.assertEqual(len(j1.routes),0)

    def test_deplacer_voleur(self):
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.terres = [tg]
        j2.terres = [tg,td]

        self.tg.deplacer_brigand(self.h23)
        self.tg.deplacer_pirate(self.h44)
        self.td.brigand = Voleur(self.h27,Voleur.VoleurType.BRIGAND)
        self.td.pirate = Voleur(self.h8,Voleur.VoleurType.PIRATE)

        br = Voleur.VoleurType.BRIGAND
        pr = Voleur.VoleurType.PIRATE
        
        Jeu.des = [7,6,4,3]
        Jeu.terres = [tg,td]
        Jeu.joueurs_origine = [0,0]
        j1.deplacement_voleur = True

        # Deplacement du voleur s'il n'y a aucun autre joueur sur la terre privee de l'hexagone actuellement occupe : l'hexagone choisi doit alors etre un desert, si c'est le brigand, nul si c'est un pirate et le joueur vole nul.

        # Aucun joueur sur l'ile
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h1,0)) # Non desert
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h12,0)) # Desert mais Marche
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h39,0)) # Autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h15,0)) # Mer
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,j2)) # Il ne faut pas de joueur

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,0,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,0)) # Il ne faut pas d hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,j2)) # Il ne faut pas de joueur
        
        # Un seul joueur sur l'ile 
        
        Colonie(j1,self.it[24])
        Bateau(j1,self.it[15].lien(self.it[26]))

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h1,0)) # Non desert
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h12,0)) # Desert mais Marche
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h39,0)) # Autre terre        
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h15,0)) # Mer
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,j2)) # Il ne faut pas de joueur

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,0,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,0)) # Il ne faut pas d hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,j2)) # Il ne faut pas de joueur

        #Deux joueurs sur l ile mais le voleur est sur le seul hexagone occupe par le deuxieme joueur

        Colonie(j2,self.it[108]) # Colonie cotiere pas sur un port
        b2 = Bateau(j2,self.it[108].lien(self.it[98])) #Bateau Cotier

        tg.deplacer_brigand(self.h43)
        tg.deplacer_pirate(self.h44)


        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h43,0)) # Aucun deplacement
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h1,0)) # Non desert
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h12,0)) # Desert mais Marche
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h39,0)) # Autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h15,0)) # Mer
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,j2)) # Il ne faut pas d hexagone

        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,0,0))
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,0)) # Il ne faut pas d hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h44,0)) # Aucun deplacement
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,j2)) # Il ne faut pas de joueur        
        # Brigand
        # Deplacement sur un hexagone sans joueur
        # Deplacement sur le meme hexagone
        # Deplacement dans la mer
        # Deplacements sur une autre terre

        tg.deplacer_brigand(self.h23)
        
        Colonie(j2,self.it[55]) # Colonie cotiere pas sur un port

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,0,j2)) # Pas d'hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h43,0)) # Pas de joueur
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h1,j2)) # Le joueur 2 n'est pas la
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h23,j2)) # Le voleur ne bouge pas
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h44,j2)) # Deplacement en mer
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,br,self.h43,j2))
        
        Jeu.des = [7,6,4,3]
        Jeu.joueurs_origine = [1,0]
        j1.deplacement_voleur = False
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h43,j2)) # Ce n'est pas a son our
        Jeu.des = [5,6,4,3]
        Jeu.joueurs_origine = [0,0]
        j1.deplacement_voleur = False
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h43,j2)) # Ce n'est pas a son our
        Jeu.des = [7,6,4,3]
        Jeu.joueurs_origine = [0,0]
        j1.deplacement_voleur = True

        Colonie(j2,self.it[69]) # Colonie cotiere pas sur un port
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,br,self.h26,j2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,br,self.h26,j2)) # Deplacement sur une autre terre
        
        # Pirate
        # Deplacement sur un hexagone sans colonie ni bateau
        # Deplacement sur le meme hexagone
        # Deplacement sur la terre
        # Deplacements sur une autre terre
        # Deplacement du voleur s'il n'y a aucun autre bateau ou colonie cotier sur la terre privee de l'hexagone occupe
        # Deplacement du pirate s il avait disparu

        b2.deplacer(self.it[14].lien(self.it[4]))
        tg.deplacer_pirate(self.h54)
        Bateau(j2,self.it[30].lien(self.it[41]))

        Colonie(j2,self.it[1]) 
        Colonie(j2,self.it[111])

        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,0,j2)) # Pas d'hexagone
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h52,0)) # Pas de joueur
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h53,j2)) # Le joueur 2 n'est pas la
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h54,j2)) # Le voleur ne bouge pas
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h22,j2)) # Deplacement en terre
        
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h52,j2))
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,j2))
        
        Jeu.des = [7,6,4,3]
        Jeu.joueurs_origine = [1,0]
        j1.deplacement_voleur = False
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h52,j2)) # Ce n'est pas a son our
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,j2)) # Ce n'est pas a son our
        Jeu.des = [5,6,4,3]
        Jeu.joueurs_origine = [0,0]
        j1.deplacement_voleur = False
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h52,j2)) # Ce n'est pas a son our
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,j2)) # Ce n'est pas a son our

        Jeu.des = [7,6,4,3]
        Jeu.joueurs_origine = [0,0]
        j1.deplacement_voleur = True
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h57,j2)) # Deplacement sur une autre terre
        self.assertFalse(Jeu.peut_deplacer_voleur(j1,td,pr,self.h57,j2)) # Deplacement sur une autre terre
 
        tg.deplacer_pirate(self.h44)
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h52,j2))
        self.assertTrue(Jeu.peut_deplacer_voleur(j1,tg,pr,self.h4,j2))
 
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
        j1.mains = [c0]
        j1.aur = [0]
        j2.mains = [c0,c0]
        j2.aur = [2,1]

        
        j1.mains = [c0]
        j1.aur = [0]
        j2.mains = [c0,c0]
        j2.aur = [2,1]
        
        j1.deplacement_voleur = True
        Jeu.deplacer_voleur(j1,tg,br,self.h43,j2)

        self.assertEqual(tg.brigand.position,self.h43)
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c0)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j2.getOr(tg),2)
        self.assertEqual(j2.getOr(td),1)

        j2.setCartes(tg,c2)
        j1.deplacement_voleur = True
        Jeu.deplacer_voleur(j1,tg,br,self.h23,j2)

        self.assertEqual(tg.brigand.position,self.h23)
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c2)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j2.getOr(tg),2)
        self.assertEqual(j2.getOr(td),1)

        j2.setCartes(tg,cch)
        j1.setCartes(tg,c0)
        j1.deplacement_voleur = True
        Jeu.deplacer_voleur(j1,tg,pr,self.h4,j2)

        self.assertEqual(tg.pirate.position,self.h4)
        self.assertEqual(j2.getCartes(tg),cch)
        self.assertEqual(j1.getCartes(tg),c0)
        self.assertEqual(j1.getOr(tg),0)
        self.assertEqual(j2.getOr(tg),2)
        self.assertEqual(j2.getOr(td),1)

        # Vol d un bateau
        j1.mains = [c0]
        j2.mains = [c0,c0]
        b2.deplacer(self.it[1].lien(self.it[115]))
        b2.cargaison = Cartes.BLE
        j1.deplacement_voleur = True
        Jeu.deplacer_voleur(j1,tg,br,self.h43,j2)
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)
        self.assertEqual(b2.cargaison,c0)

        # Vol d un bateau
        j1.mains = [c0]
        j2.mains = [c0,c0]
        b2.deplacer(self.it[108].lien(self.it[118]))
        b2.cargaison = Cartes.BLE
        j1.deplacement_voleur = True
        Jeu.deplacer_voleur(j1,tg,br,self.h23,j2)
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),Cartes.BLE)
        self.assertEqual(b2.cargaison,c0)

        # Vol d un joueur qui n a rien, le bateau est mal place
        j1.mains = [c0]
        j2.mains = [c0,c0]
        b2.deplacer(self.it[14].lien(self.it[4]))
        b2.cargaison = Cartes.BLE
        j1.deplacement_voleur = True
        Jeu.deplacer_voleur(j1,tg,br,self.h43,j2)
        self.assertEqual(j2.getCartes(tg),c0)
        self.assertEqual(j1.getCartes(tg),c0)
        self.assertEqual(b2.cargaison,Cartes.BLE)

    def test_defausser(self):
        j1 = self.j1
        tg = self.tg
        j1.terres = [tg]
         
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

        Jeu.des = [3,6,5,1]
        j1.setCartes(tg,c1)
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[])))
        Jeu.des = [3,7,5,1]
        self.assertTrue(Jeu.peut_defausser(j1,tg,(d1,[])))
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
        b1 = Bateau(j1,self.it[15].lien(self.it[26]))
        b1.append(CartesGeneral(1,2,0,1,0,0,0,1,0,0))
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
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,dgen)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,dgen2)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,dneg)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,ddouble)])))
        self.assertTrue(Jeu.peut_defausser(j1,tg,(d11,[(b1,d13)])))
        self.assertFalse(Jeu.peut_defausser(j1,tg,(d1,[(b1,d12)])))

        Jeu.defausser(j1,tg,(d1,[(b1,d10)]))
        self.assertEqual(j1.getCartes(tg), c1 - d1)
        self.assertEqual(b1.cargaison, CartesGeneral(0,1,0,1,0,0,0,1,0,0))


    def test_jouer_chevalliers(self):

        # Le joueur 1 joue une carte de chevallier si il en a en main et s'il ne l'a pas achete recemment. Il l'ajoute a son armee locale et deplace le voleur.
        
        j1 = self.j1
        j2 = self.j2
        tg = self.tg
        td = self.td
        j1.terres = [tg]
        j2.terres = [tg,td]

        Colonie(j2,self.it[86]) 
        Colonie(j2,self.it[81]) 
        
        self.tg.deplacer_brigand(self.h23)
        self.td.brigand = Voleur(self.h26,Voleur.VoleurType)
        
        br = Voleur.VoleurType.BRIGAND
        # Aucun test pour voleur ici, ils sont deja fait dans deplacer voleur, les regles sont les memes

        c1 = CartesDeveloppement(3,0,0,0,0)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(0,1,1,1,1)
        
        j2.setCartes(tg,Cartes.RIEN)
        j2.setCartes(td,Cartes.RIEN)

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,td,br,self.h37,j2))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_chevallier(j1,tg,br,self.h32,j2))

        j1.setCartes(tg,c1)
        j1.chevalliers = [0]
        Jeu.jouer_chevallier(j1,tg,br,self.h32,j2)
        self.assertEqual(tg.brigand.position,self.h32)
        self.assertEqual(j1.chevalliers,[1])

    def test_peut_jouer_decouverte(self):
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.terres = [tg]

        c1 = CartesDeveloppement(0,0,0,3,0)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,1,1,0,1)
        
        d1 = CartesRessources(1,1,0,0,0)
        dneg = CartesRessources(-1,1,1,1,0)
        ddouble = CartesRessources(0.5,1.5,0,0,0)
        d2 = CartesRessources(1,1,0,0,1)
        d3 = CartesRessources(1,0,0,0,0)
        d4 = CartesGeneral(1,0,0,0,0,1,0,0,0,0)
        d5 = CartesGeneral(1,0,1,0,0,1,0,0,0,0)

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_decouverte(j1,tg,d1))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,td,d1))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,dneg))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,ddouble))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d2))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d3))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d4))
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d5))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_decouverte(j1,tg,d1))

        j1.setCartes(tg,c1)
        j1.aur = [0]
        Jeu.jouer_decouverte(j1,tg,d1)
        self.assertEqual(j1.getCartes(tg),d1 + Cartes.DECOUVERTE * 2)
        self.assertEqual(j1.aur,[0])
        
    def test_peut_jouer_construction_routes(self):


        # le test sur la construction de route n est pas fait ici
        j1 = self.j1
        tg = self.tg
        td = self.td
        j1.terres = [tg]

        Colonie(j1,self.it[23])
        Route(j1,self.it[23].lien(self.it[34])) 

        c1 = CartesDeveloppement(0,0,0,0,3)
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,1,1,1,0)
        
        a1 = self.it[23].lien(self.it[12])
        a2 = self.it[34].lien(self.it[44])

        j1.setCartes(tg,c1)
        self.assertTrue(Jeu.peut_jouer_construction_routes(j1,tg,a1,a2))
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,td,a1,a2))
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,a1,a1))
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,a1,a2))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,a1,a2))

        j1.terres = [tg,td]
        Colonie(j1,self.it[49])
        a3 = self.it[49].lien(self.it[59])
        j1.setCartes(tg,c1)
        self.assertFalse(Jeu.peut_jouer_construction_routes(j1,tg,a1,a3))

        j1.setCartes(tg,c1)
        Jeu.jouer_construction_routes(j1,tg,a1,a2)
        self.assertEqual(j1.getCartes(tg),Cartes.CONSTRUCTION_ROUTES * 2)
        self.assertTrue(a1.route != 0)
        self.assertTrue(a2.route != 0)
        self.assertTrue(a1.route.joueur == j1)
        self.assertTrue(a2.route.joueur == j1)




    def test_peut_jouer_monopole(self):

        j1 = self.j1
        j2 = self.j2
        j3 = self.j3
        j4 = self.j4
        j5 = Joueur(5)
        j6 = Joueur(6)

        tg = self.tg
        td = self.td

        j1.terres = [tg]
        j2.terres = [tg,td]
        j3.terres = [tg]
        j4.terres = [tg]
        j5.terres = [tg]
        j6.terres = [td]

        j1.mains = [0]
        j2.mains = [0,0]
        j3.mains = [0]
        j4.mains = [0]
        j5.mains = [0]
        j6.mains = [0]
        
        r = Cartes.ARGILE
        rch = Cartes.CHEVALLIER
        
        c1 = Cartes.MONOPOLE
        c2 = Cartes.RIEN
        c3 = CartesDeveloppement(1,0,1,1,1)
        c4 = CartesGeneral(2,0,0,0,1,0,1,0,0,0)
        c5 = CartesRessources(2,0,0,0,0)

        j1.setCartes(tg,c1)
        j2.setCartes(tg,c4)
        j2.setCartes(td,c5)
        j3.setCartes(tg,c4)
        j4.setCartes(tg,c4)
        j5.setCartes(tg,c4)
        j6.setCartes(td,c4)
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j1,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4,j5]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j6]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,rch,[j2,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,td,rch,[j2,j6]))

        j2.setCartes(tg,c2)
        j3.setCartes(tg,c2)
        j4.setCartes(tg,c2)
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertTrue(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        
        j1.setCartes(tg,c2)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[]))
        j1.setCartes(tg,c3)
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3,j4]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2,j3]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[j2]))
        self.assertFalse(Jeu.peut_jouer_monopole(j1,tg,r,[]))

        j1.setCartes(tg,c1)
        j2.setCartes(tg,c5)
        j3.setCartes(tg,c5)
        j4.setCartes(tg,c5)
        Jeu.jouer_monopole(j1,tg,r,[j2,j3,j4])
        self.assertEqual(j1.getCartes(tg),c1 + Cartes.ARGILE*6)

        self.assertEqual(j2.getCartes(tg).get_cartes_de_type(r), 0)
        self.assertEqual(j3.getCartes(tg).get_cartes_de_type(r), 0)
        self.assertEqual(j4.getCartes(tg).get_cartes_de_type(r), 0)
    ''' 
    def test_louer_route(self):

        # Un joueur peut louer une route si il est en mesure de la construire a cet endroit, que la route n'est pas a lui ou q'il ne l'a pas deja louee, qu'il a assez de ressource pour payer.


        j1 = self.j1
        j2 = self.j2

        tg = self.tg
        td = self.td

        j1.terres = [tg]
        j2.terres = [tg,td]

        j1.mains = [0]
        j2.mains = [0,0]
        
        p1 = Cartes.RIEN
        p2 = CartesRessources(1,0,0,0,0)
        p3 = CartesRessources(1,2,0,0,0)        

        c1 = CartesRessources(1,1,1,0,0) # Ok avec p1 et p2
        cneg = CartesRessources(1,-1,2,0,0)
        cdouble = CartesRessources(1,0.5,1.5,0,0)
        c2 = CartesRessources(1,2,0,0,0) # Ok avec les 3
        c3 = CartesRessources(1,0,0,0,0) # Pas ok, moins de 3 ressources
        c4 = Cartes.RIEN # Pas asssez de ressources
        c5 = CartesRessources(1,3,0,0,0) # trop de ressources
        c6 = CartesRessources(1,2,1,0,0) # Trop de ressources
        
        c7 = CartesRessources(5,5,5,5,5) # Ressources en main

        # Aucun test de position de route

        Colonie(j1,self.it[34])
        r1 = Route(j1,self.it[34].lien(self.it[24]))
        r2 = Route(j2,self.it[24].lien(self.it[13]))
        r3 = Route(j2,self.it[34].lien(self.it[44]))

        j1.setCartes(tg,c7)
        r2.prixLocation = p1
        self.assertTrue(Jeu.peut_louer_route(j1,r2,c1))
        self.assertTrue(Jeu.peut_louer_route(j1,r2,c2))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,cneg))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,cdouble))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c3))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c4))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c5))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c6))
        

        j1.setCartes(tg,c4)
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c1))
        j1.setCartes(tg,c1)
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c2))

        j1.setCartes(tg,c7)
        r2.prixLocation = p2
        self.assertTrue(Jeu.peut_louer_route(j1,r2,c1))
        self.assertTrue(Jeu.peut_louer_route(j1,r2,c2))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,cneg))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,cdouble))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c3))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c4))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c5))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c6))
        
        j1.setCartes(tg,c7)
        r2.prixLocation = p3
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c1))
        self.assertTrue(Jeu.peut_louer_route(j1,r2,c2))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,cneg))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,cdouble))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c3))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c4))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c5))
        self.assertFalse(Jeu.peut_louer_route(j1,r2,c6))

        r3.prixLocation = p1
        r3.locataires = [j1]
        self.assertFalse(Jeu.peut_louer_route(j1,r3,c1))

        r1.prixLocation = p1
        self.assertFalse(Jeu.peut_louer_route(j1,r1,c1))

        r2.prixLocation = p1
        Jeu.louer_route(j1,r2,c1)
        self.assertEqual(j1.getCartes(tg),c7-c1)
        self.assertEqual(j2.getCartes(tg),c1)
        self.assertEqual(r2.locataires,[j1])
    '''

    def test_route_la_plus_longue(self):
        j1 = self.j1
        j2 = self.j2

        tg = self.tg
        td = self.td

        j1.terres = [tg,td]
        j2.terres = [tg,td]

        Route(j1,self.it[33].lien(self.it[43]))
        Route(j1,self.it[43].lien(self.it[54]))
        Route(j1,self.it[54].lien(self.it[65]))
        Route(j1,self.it[65].lien(self.it[75]))
        Route(j1,self.it[75].lien(self.it[85]))
        Route(j1,self.it[85].lien(self.it[96]))
        Route(j1,self.it[65].lien(self.it[76]))
        Route(j1,self.it[76].lien(self.it[86]))
        Route(j1,self.it[86].lien(self.it[96]))
        Route(j1,self.it[54].lien(self.it[44]))
        Route(j1,self.it[44].lien(self.it[55]))
        Route(j1,self.it[55].lien(self.it[66]))
        
        Route(j1,self.it[107].lien(self.it[117]))
        Route(j1,self.it[117].lien(self.it[108]))
        Route(j1,self.it[108].lien(self.it[98]))


        Route(j1,self.it[27].lien(self.it[37]))
        Route(j1,self.it[37].lien(self.it[47]))
        Route(j1,self.it[47].lien(self.it[58]))
        Route(j1,self.it[58].lien(self.it[69]))
        Route(j1,self.it[69].lien(self.it[80]))
        Route(j1,self.it[80].lien(self.it[90]))
        Route(j1,self.it[90].lien(self.it[100]))
        Route(j1,self.it[100].lien(self.it[110]))
        Route(j1,self.it[110].lien(self.it[120]))
        Route(j1,self.it[120].lien(self.it[111]))
        
        self.assertEqual(j1.route_la_plus_longue(tg),9)
        self.assertEqual(j1.route_la_plus_longue(td),10)

        Colonie(j2,self.it[65])
        self.assertEqual(j1.route_la_plus_longue(tg),6)


if __name__ == '__main__':
    unittest.main()
