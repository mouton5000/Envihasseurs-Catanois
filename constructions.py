# *-* coding: iso-8859-1 *-*
from plateau import *
from cartes import *

# Suprise totale, cette classe représente les pions de type colonies et ville. Cette classe ne se préoccupe pas des règles du jeu (pas de vérifications avant de faire les actions).
class Colonie:

	# Pose sur le terrain une colonie du joueur j à l'emplacement int.
    def __init__(self,j,int):
       self.joueur = j
       self.position = int
       int.colonie = self
       self.isVille = False
       j.colonies.append(self)
       self.deblayeurs = []
       self.deblayeurs24 = []
   
    def changer_proprietaire(self,j):
        if self.isVille:
            self.joueur.villes.remove(self)
        else:
            self.joueur.colonies.remove(self)
        self.joueur = j
        j.colonies.append(self)
        self.deblayeurs = []
        self.deblayeurs24 = []
        self.isVille = False
 
	# Transforme la colonie en ville
    def evolue(self):
        self.isVille = True
        self.joueur.colonies.remove(self)
        self.joueur.villes.append(self)
    
	# Renvoie vrai si la colonie est au bord de la mer.
    def isCotier(self):
        return self.position.isCotier()

	# Renvoie dans un tableau l'ensemble des ressources au format (numéro de pastille, ensemble des ressources acquises si ce numéro tombe, or acquis si ce numéro tombe).
	# Par exemple, si la colonie est entourée par un hexagone Bois de pastille 4, un Argile de pastille 5 et un Or de pastille 5, la méthode renverra
	# [(4,Cartes.BOIS,0), (5,Cartes.ARGILE,1)]
    def ressources(self):
    	t = []
        for i in range(10):
           u = self.ressources_from_past(i+3)
           if u != 0:
               t.append((i+3,u[0],u[1]))
        return t

	# Renvoie un 2 upplet contenant les ressources et le nombre de pépites d'or acquies si le nombre past tombe.
    def ressources_from_past(self,past):
        t = []
        bois = 0
        argile = 0
        ble = 0
        mouton = 0
        caillou = 0
        aur = 0
        if self.isVille:
            i = 2
        else:
            i = 1
        for h in self.position.hexagones:
            if(h.voleur == 0 and h.past == past):
                if (h.etat == HexaType.BOIS):
                    bois += i
                elif h.etat == HexaType.ARGILE:
                    argile += i
                elif h.etat == HexaType.BLE:
                    ble += i
                elif h.etat == HexaType.OR:
                    aur += i
                elif h.etat == HexaType.CAILLOU:
                    caillou += i
                elif h.etat == HexaType.MOUTON:
                    mouton += i
        if (bois != 0 or argile != 0 or ble != 0 or aur != 0 or caillou != 0 or mouton != 0):
            return (CartesRessources(argile,ble,bois,caillou,mouton),aur)
        else:
            return 0

# Tout autant une surprise, cette classe est identifiée au pion de type route.
class Route:

	# Pose une route appartenant au joueur j sur l'arrête a.
    def __init__(self,j,a):
        self.joueur = j
        self.position = a
        a.route = self
        j.routes.append(self)

    def changer_proprietaire(self,j):
        self.joueur.routes.remove(self)
        self.joueur = j
        j.routes.append(self)

    def voisins_routables(self,l):
        a = self.position
        j = self.joueur
        ar = []
        for n in a.neighb():
            if(n.route != 0 and n.route.joueur == j):
                i = n.lien(a)
                if (i.colonie == 0 or i.colonie.joueur == j) and not(n.route in l) and (len(l) == 0 or l[len(l)-1].position.lien(n) == 0):
                    ar.append(n.route)
        return ar

   
    def est_extremite(self):
        i1 = self.position.int1 
        i2 = self.position.int2
        if (i1.colonie != 0 and i1.colonie.joueur != self.joueur) or (i2.colonie != 0 and i2.colonie.joueur != self.joueur):
            return True
        ir1 = i1.neighb()
        b = True
        for i in ir1:
            if i2 != i:
                a = i.lien(i1)
                b = b and (a.route == 0 or a.route.joueur != self.joueur)
        if b:
            return True
        b = True
        ir2 = i2.neighb()
        for i in ir2:
            if i1 != i:
                a = i.lien(i2)
                b = b and (a.route == 0 or a.route.joueur != self.joueur)
        return b

    # Renvoie la route la plus longue qui commence en  self.
    def rlplfr(self):
        return self.rlplfrwb([])

    def rlplfrwb(self,beginning):
        beg2 = beginning + [self]
        vr = self.voisins_routables(beginning)
        i = 0
        for r in vr:
            i = max(i,r.rlplfrwb(beg2))
        return i + 1
        

# Classe identifiée au pion bateau
class Bateau:

	# Ensemble des types de bateau qui existent
    class BateauType :
        VOILIER = 'bateauType_voilier'
        CARGO = 'bateauType_cargo'
        TRANSPORT = 'bateauType_transport'

	# Pose un bateau appartenant au joueur j sur l'arrête a
    def __init__(self,j,a):
        self.joueur = j
        self.position = a
        a.bateau = self
        self.cargaison = CartesGeneral(0,0,0,0,0,0,0,0,0,0)
        self.etat = Bateau.BateauType.TRANSPORT
        self.cargaisonMax = 6
        self.vitesse = 1
        self.enEpave = False
        j.bateaux_transport.append(self)
        self.aBouge = False
    
	# Transforme ce bateau en Cargo si c'est un bateau de transport, ou en voillier si c'est un cargo.
    def evolue(self):
        if(self.etat == Bateau.BateauType.TRANSPORT):
             self.etat = Bateau.BateauType.CARGO
             self.cargaisonMax = 10
             self.joueur.bateaux_transport.remove(self)
             self.joueur.cargo.append(self)
        elif self.etat == Bateau.BateauType.CARGO:
             self.etat = Bateau.BateauType.VOILIER
             self.vitesse = 2
             self.joueur.cargo.remove(self)
             self.joueur.voilier.append(self)

	# Ajoute les cartes à la cargaison du bateau
    def append(self,cartes):
        if (self.cargaison + cartes).size() <= self.cargaisonMax:
            self.cargaison += cartes

	# Retire les cartes de la cargaison
    def remove(self,cartes):
        if(cartes <= self.cargaison):
           self.cargaison -= cartes

	# Pose ce bateau sur l'arrête a (sans se soucier de savoir s'il a le droit)
    def deplacer(self,a):
        self.position.bateau = 0
        self.position = a
        a.bateau = self

	# Vérifie si le bateau peut recevoir les cartes cr et donner (en même temps) les cartes cp.
    def peut_recevoir_et_payer(self,cr,cp):
        return cp <= self.cargaison and (self.cargaison + cr - cp).size() <= self.cargaisonMax

	# Renvoie toutes les positions terrestres situées à deux hexagones d'un bateau sur la cote.
    def positions_colonisables(self):
        hc = []
        for i in [self.position.int1, self.position.int2]:
            for h in i.hexagones:
                if h.etat != HexaType.MER and not h in hc:
                    hc.append(h)


        hf = hc[:]
        for h in hc:
            for hp in h.neighb():
                if hp.etat != HexaType.MER and not hp in hf:
                    hf.append(hp)

        intf = []
        for h in hf:
            for pos in h.ints:
                if not pos in intf:
                    intf.append(pos)
        return intf

	# Vérifie que le bateau est sur un emplacement où il peut échanger avec une terre : un port ou une colonie cotière
    def en_position_echange(self):
        i1 = self.position.int1
        i2 = self.position.int2
        return  ((i1.colonie != 0 and i1.colonie.joueur == self.joueur) or (i2.colonie != 0 and i2.colonie.joueur == self.joueur) or i1.isPort() or i2.isPort()) and self.position.getTerre() in self.joueur.terres 
    
    def est_proche(self,terre):
        ints = []
        ints += [self.position.int1,self.position.int2]
        ints += self.position.int1.neighb()
        ints += self.position.int2.neighb()
        if(self.etat == Bateau.BateauType.VOILIER):
            for i in ints[:]:
                ints += i.neighb()
        for i in ints:
            if i.isTerrestreOuCotier():
                return True
        return False

