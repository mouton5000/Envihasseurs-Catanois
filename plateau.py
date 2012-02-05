# *-* coding: iso-8859-1 *-*
import random

class HexaType:
   ''' Ensemble des etats de tuile, un port est une tuile MER, avec un port dessus. Un marche est une tuile DESERT avec un port dessus.'''
   MER = 'mer'
   BOIS = 'bois'
   ARGILE = 'argile'
   CAILLOU = 'caillou'
   BLE = 'ble'
   MOUTON = 'mouton'
   DESERT = 'desert'
   OR = 'or'

class CommerceType:
    ''' Ensemble des commerces disponnible. TOUS est le commerce avec une pastille "?". '''
    TOUS = 'commerce_tous'
    BOIS = 'commerce_bois'
    ARGILE = 'commerce_argile'
    CAILLOU = 'commerce_caillou'
    BLE = 'commerce_ble'
    MOUTON = 'commerce_mouton'

class Intersection:
    ''' Intersection entre 3 hexagones, ou 3 arretes. Chaque intersection est reperee par un numero.'''
    # num ; identifiant de l'intersection
    # neigh : intersections voisines de l'intersection
    # liens : arretes voisines de l'intersection
    # hexagones : hexagones voisins de l'intersection
    # colonie : colonie de l'intersection


    def __init__(self,num):
       self.num = num
       self.neigh = []
       self.liens = []
       self.hexagones = []
       self.colonie = 0

    def addNeighbour(self,i,a):
        ''' Ajoute l'intersection i à ses voisins, et l'arrête a à ses arrêtes voisines.'''
        if (a.int1 == i and a.int2 == self or a.int1 == self and a.int2 == i):
            self.neigh.append(i)
            self.liens.append(a)

    def addHexa(self,h):
       ''' Ajoute l'hexagone h aux hexagones de self'''
       if (not h in self.hexagones):
            self.hexagones.append(h)

    def __str__(self):
       return str(self.num)

    def lien(self,i):
        '''# Renvoie s'il existe l'unique arc qui relie self et i'''
        for a in self.liens:
            if(a.int1 == i and a.int2 == self or a.int1 == self and a.int2 == i):
                return a
        return 0

    def isCotier(self):
        ''' Renvoie vrai si l'intersection est au bord de la mer'''
        mer = False
        terre = False
        for h in self.hexagones:
            mer = mer or (h.etat == HexaType.MER)
            terre = terre or (h.etat != HexaType.MER)
        return mer and terre
    
    def isTerrestre(self):
        '''# Renvoie vrai si l'intersection est dans la terre, pas au bord de la mer'''
        mer = False 
        terre = False
        for h in self.hexagones:
            mer = mer or (h.etat == HexaType.MER)
            terre = terre or (h.etat != HexaType.MER)
        return not(mer) and terre

    def isTerrestreOuCotier(self):
        ''' Renvoie vrai si l'intersection est sur terre, au bord de la mer ou pas'''
        for h in self.hexagones:
            if (h.etat != HexaType.MER) : return True
        return False

    def isMaritime(self):
        ''' Renvoie vrai si l'intersection est dans la mer, pas au bord de la mer'''
        mer = False
        terre = False
        for h in self.hexagones:
            mer = mer or (h.etat == HexaType.MER)
            terre = terre or (h.etat != HexaType.MER)
        return mer and not(terre)

    def isMaritimeOuCotier(self):
        ''' Renvoie vrai si l'intersection est dans la mer, au bord de la mer ou pas'''
        for h in self.hexagones:
            if (h.etat == HexaType.MER) : return True
        return False

    def dist(self,i, force = False):
        ''' Renvoie la taille du chemin minimal reliant self et i. Si force est vrai, le calcul est refait, sinon on renvoie le résultat déjà enregistré.'''
        d = Distances.dist(self,i)
        if(d == -1 or force):
            Distances.computeDistances(self)
            d = Distances.dist(self,i)
        return d
  
    def neighb(self):
        ''' Renvoie tous les voisins de l'intersection'''
        return self.neigh

    def isMarche(self):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type marché, parmi les espaces de commerce'''
        for h in self.hexagones:
            if (h.isMarche() and self in h.lintp):
                return True
        return False
 
    def isMarcheNonBrigande(self):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type marché, parmi les espaces de commerce non occupé par un brigand'''
        for h in self.hexagones:
            if (h.isMarche() and h.voleur == 0 and self in h.lintp):
                return True
        return False
    
    def marcheNonBrigande(self):
        ''' Renvoie l'ensemble des hexagones cette intersection de type marché, parmi les espaces de commerce, non occupés par un brigand'''
        for h in self.hexagones:
            if (h.isMarche() and h.voleur == 0 and self in h.lintp):
                return h
        return 0
    
    def isPort(self):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type port, parmi les espaces de commerce'''
        for h in self.hexagones:
            if (h.isPort() and self in h.lintp):
                return True
        return False

    def isPortNonPirate(self):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type port, parmi les espaces de commerce, non occupé par un pirate'''
        for h in self.hexagones:
            if (h.isPort() and h.voleur == 0 and self in h.lintp):
                return True
        return False

    def portNonPirate(self):
        ''' Renvoie l'ensemble des hexagones de l'intersection de type port, parmi les espaces de commerce, non occupé par un pirate'''
        for h in self.hexagones:
            if (h.isPort() and h.voleur == 0 and self in h.lintp):
                return h
        return 0

    def getTerre(self):
        ''' Renvoie la terre à laquelle appartient cette intersection, si elle est terrestre, 0 sinon '''
        for h in self.hexagones:
            if (h.etat != HexaType.MER) : return h.terre
        return 0

class Arrete:
    ''' Cette classe représente les liens entre les intersections, ou un côté d'un hexagone.'''

    def __init__(self,i1,i2):
        ''' Crée une arrête entre les deux intersections i1 et i2.'''
        self.int1 = i1
        self.int2 = i2
        self.hexagones = []
        i1.addNeighbour(i2,self)
        i2.addNeighbour(i1,self)
        self.route = 0
        self.bateau = 0
        self.neigh = []
        self.neigh2 = []
    
    def addHexa(self,h):
        ''' Ajoute h aux heagones de cette arrête'''
        if (not h in self.hexagones):
            self.hexagones.append(h)

    def __str__(self):
       return str(self.int1) + "--" + str(self.int2)
    
    def isCotier(self):
       ''' Renvoie vrai si l'arrête est au bord de la mer'''
       mer = False
       terre = False
       for h in self.hexagones:
           mer = mer or (h.etat == HexaType.MER)
           terre = terre or (h.etat != HexaType.MER)
       return mer and terre

    def isTerrestre(self):
        ''' Renvoie vrai si l'arrête est dans la terre, pas au bord de la mer'''
        mer = False
        terre = False
        for h in self.hexagones:
            mer = mer or (h.etat == HexaType.MER)
            terre = terre or (h.etat != HexaType.MER)
        return not(mer) and terre
    
    def isTerrestreOuCotier(self):
        '''# Renvoie vrai si l'arrête est dans la terre, au bord de la mer ou pas'''
        for h in self.hexagones:
            if (h.etat != HexaType.MER) : return True
        return False

    def isMaritime(self):
        ''' Renvoie vrai si l'arrête est en mer, pas au bord de la mer'''
        mer = False
        terre = False
        for h in self.hexagones:
            mer = mer or (h.etat == HexaType.MER)
            terre = terre or (h.etat != HexaType.MER)
        return mer and not(terre)

    def isMaritimeOuCotier(self):
        ''' Renvoie vrai si l'arrête est en mer, au bord de la mer ou pas'''
        for h in self.hexagones:
            if (h.etat == HexaType.MER) : return True
        return False

    def neighb(self, force = False):
        ''' Renvoie les voisins de cette arrête. Si force est vrai, les voisins sont recalculés.'''
        if self.neigh == [] or force:
            n = []
            for inti in [self.int1,self.int2]:
                for i in inti.neigh:
                    a = i.lien(inti)
                    if(a!=self):
                        n.append(a)
                self.neigh = n
            return n
        else:
            return self.neigh

    def doubleNeighb(self, force = False):
        ''' Renvoie les voisins à une distance 2, si force est vrai, alors ce calcul est refait.'''
        if self.neigh2 == [] or force:
            neigh = self.neighb(force)
            n2 = neigh[:]
            for a in neigh:
                for a2 in a.neighb(force):
                    if not (a2 == self or a2 in n2):
                        n2.append(a2)
            return n2


    def dist(self,a,force = False):
        ''' Renvoie la distance entre self et a, force à True force le calcul à être refait.'''
        d = Distances.dist(self,a)
        if(d == -1 or force):
            Distances.computeDistances(self)
            d = Distances.dist(self,a)
        return d
      
      
    def getTerre(self):
        ''' Renvoie la terre à laquelle appartient cette arrête, si elle est terrestre, sinon 0.'''
        for h in self.hexagones:
           if (h.etat != HexaType.MER) : return h.terre
        t1 = self.int1.getTerre()
        t2 = self.int2.getTerre()
        if t1 != 0:
            return t1
        elif t2 != 0:
            return t2
        return 0


    def est_pirate(self):
        '''Renvoie vrai si l'arrete est occupée par le pirate'''
        for h in self.hexagones:
            if (h.etat == HexaType.MER and h.voleur != 0):
                return True
        return False

    def lien(self,a):
        '''Renvoie vrai si l'arrete est occupée par le pirate'''
        if a != self:
            if a.int1 == self.int1 or a.int2 == self.int1:
                return self.int1
            elif a.int1 == self.int2 or a.int2 == self.int2:
                return self.int2
        return 0
        
class Hexagone:
    ''' Cette classe correspond à un hexagone du terrain.'''

    def __init__(self,i1,i2,i3,i4,i5,i6,t,p,comType=0,lintp=[]):
        ''' Crée un hexagone entre les 6 intersection i1 à i6, de type t, avec une pastille p, de type de commerce ComType (si c'est une Mer -> Port, si c'est un désert -> marché), accessibles via les emplacements lintp. lintp doit être un sous ensemble de i1 i2 ... i6. Les arrêtes entre i1 i2, i2 i3 ... i6 i1 sont créées toutes seules.'''
        self.int1 = i1
        self.int2 = i2
        self.int3 = i3
        self.int4 = i4
        self.int5 = i5
        self.int6 = i6
        self.etat = t
        self.past = p
        self.commerceType = comType
        self.lintp = lintp
        i1.addHexa(self)
        i2.addHexa(self)
        i3.addHexa(self)
        i4.addHexa(self)
        i5.addHexa(self)
        i6.addHexa(self)
        self.liens = []
        self.ints = [i1,i2,i3,i4,i5,i6]
        for i in range(6):
            a = self.ints[i].lien(self.ints[(i+1)%6])
            if a == 0 :
                 a = Arrete(self.ints[i],self.ints[(i+1)%6])
            self.liens.append(a)
            a.addHexa(self)

        self.voleur = 0
        self.neigh = 0

    def __str__(self):
        return str(self.etat)+","+str(self.past)+","+str(self.int1) + "--" + str(self.int2) + "--" + str(self.int3) + "--" + str(self.int4) + "--" + str(self.int5) + "--" + str(self.int6) 
        
    def isMaritimeCotier(self):
        '''Renvoie vrai si cet exagone est marin, à côté de la terre'''
        cote = False
        for lien in self.liens:
            cote = cote or lien.isCotier()
        return (self.etat==HexaType.MER) and cote
    
    def isTerrestreCotier(self):
        '''Renvoie vrai si cet exagone est terrestre, à côté de la mer'''
        cote = False
        for lien in self.liens:
            cote = cote or lien.isCotier()
        return (self.etat!=HexaType.MER) and cote
    
    def isMaritime(self):
        '''Renvoie vrai si cet exagone est marin, pas à côté de la terre'''
        cote = False
        for lien in self.liens:
            cote = cote or lien.isCotier()
        return (self.etat==HexaType.MER) and not(cote)
    
    def isTerrestre(self):
        '''Renvoie vrai si cet exagone est terrestre, pas à côté de la mer'''
        cote = False
        for lien in self.liens:
            cote = cote or lien.isCotier()
        return (self.etat!=HexaType.MER) and not(cote)

    def isMarche(self):
        ''' REnvoie vrai si cet hexagone est un marché'''
        return self.commerceType != 0 and self.etat != HexaType.MER
    
    def isPort(self):
        ''' REnvoie vrai si cet hexagone est un port'''
        return self.commerceType != 0 and self.etat == HexaType.MER

    def neighb(self,force = False):
        ''' REnvoie les voisins de cet hexagone, force à True force le recalcul.'''
        if self.neigh == 0 or force:
            hf = []
            for i in self.ints:
                for h in i.hexagones:
                    if h != self and not h in hf:
                        hf.append(h)
            self.neigh == hf
            return hf
        else:
            return self.neigh
            
class Voleur:
    ''' Classe représentant le pion voleur.'''
    
    class VoleurType:
        ''' Les type de voleur : briguand sur terre, pirate sur mer'''
        BRIGAND = 'voleur_brigand'
        PIRATE = 'voleur_pirate'

    def __init__(self,hex,etat):
        ''' Pose un voleur de type etat, sur l'hexagone hex.'''
        self.position = hex
        hex.voleur = self
        self.etat = etat

    def deplacer(self,hex):
        ''' Déplace le voleur sur l'hexagone hex'''
        if self.position != 0:
            self.position.voleur = 0
        self.position = hex
        hex.voleur = self
       

class Terre:
    ''' Cette classe représente un ensemble d'hexagones regroupés pour former une terre avec un espace maritime.'''

    def __init__(self,nom,hexsTerre,hexsMer):
        ''' Crée un terre de nom nom en regroupant les hexagones terrestres dans hexsTerre et les marins dans hexsMer'''
        self.hexagones = hexsTerre
        self.espaceMarin = hexsMer
        self.nom = nom
        self.joueurs = []


        for h in hexsTerre:
            h.terre = self
        for h in hexsTerre:
            if h.etat == HexaType.DESERT and not h.isMarche():
                self.brigand = Voleur(h,Voleur.VoleurType.BRIGAND)
                break
        i = random.randint(0,len(hexsMer)-1)
        self.pirate = Voleur(hexsMer[i],Voleur.VoleurType.PIRATE)
        for h in hexsMer:
            h.terre = self

    def addJoueur(self, j):
        ''' Ajoute le joueur j aux joueur ayant colonisé cette terre'''
        self.joueurs.append(j)
        j.terre.append(self)

    def deplacer_voleur(self,vT,h):
        ''' Déplace le voleur de type vT de cette terre sur l'hexagone h'''
        if vT == Voleur.VoleurType.BRIGAND:
            self.deplacer_brigand(h)
        elif vT == Voleur.VoleurType.PIRATE:
            self.deplacer_pirate(h)

    def deplacer_brigand(self,h):
        '''Déplace le brigand de cette terre sur l'hexagone h'''
        self.brigand.deplacer(h)

    def deplacer_pirate(self,h):
        '''Déplace le pirate de cette terre sur l'hexagone h'''
        self.pirate.deplacer(h)



class Distances:
    ''' Classe qui gère le calcule des distances entre arrêtes ou intersection (l'algo est le même).'''

    dists = []
    
    def dist(e1,e2):
        if e1 == e2:
            return 0
        for e in Distances.dists :
            if (e[0] == e1 and e[1] == e2) or (e[0] == e2 and e[1] == e1):
                return e[2]
        return -1
    dist = staticmethod(dist)

    def computeDistances(elem):
        
        elemAVoir = [elem]
        elemVus = []
        b = False

        for eGl in elemAVoir:
            d = 1
            ints = [eGl]
            dejavu = []
            suivants = []
            while(ints != []):
                for e in ints:
                    dejavu.append(e)
                    for n in e.neighb():
                        if not(n in dejavu) and not(n in suivants):
                            if not b:
                                elemAVoir.append(n)
                            if (not n in elemVus):
                                Distances.dists.append((eGl,n,d))
                            suivants.append(n)
                d += 1
                ints = suivants
                suivants = []
            b = True
            elemVus.append(eGl)
    computeDistances = staticmethod(computeDistances)

