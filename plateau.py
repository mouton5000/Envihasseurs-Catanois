# *-* coding: iso-8859-1 *-*
__all__ = ['Intersection', 'Plateau', 'Terre', 'Hexagone','HexaType', 'Arrete', 'CommerceType']

import random
import redis


REDIS = redis.StrictRedis()

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

    def __init__(self,num):
        self.num = num
        self.neigh = []
        self.liens = []
        self.hexagones = []

        self._isCotier = -1
        self._isTerrestre = -1
        self._isTerrestreOuCotier = -1

        self._isMaritime = -1
        self._isMaritimeOuCotier = -1
        
        self._isMarche = -1
        self._isPort = -1
        self._terre = -1

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
        if self._isCotier == -1:
            mer = False
            terre = False
            for h in self.hexagones:
                mer = mer or (h.etat == HexaType.MER)
                terre = terre or (h.etat != HexaType.MER)
            self._isCotier = (mer and terre)
        return self._isCotier
    
    def isTerrestre(self):
        '''# Renvoie vrai si l'intersection est dans la terre, pas au bord de la mer'''
        if self._isTerrestre == -1:
            mer = False 
            terre = False
            for h in self.hexagones:
                mer = mer or (h.etat == HexaType.MER)
                terre = terre or (h.etat != HexaType.MER)
            self._isTerrestre = (not(mer) and terre)
        return self._isTerrestre

    def isTerrestreOuCotier(self):
        ''' Renvoie vrai si l'intersection est sur terre, au bord de la mer ou pas'''
        if self._isTerrestreOuCotier == -1:
            self._isTerrestreOuCotier = False
            for h in self.hexagones:
                if (h.etat != HexaType.MER) : self._isTerrestreOuCotier = True
        return self._isTerrestreOuCotier

    def isMaritime(self):
        ''' Renvoie vrai si l'intersection est dans la mer, pas au bord de la mer'''
        if self._isMaritime == -1:
            mer = False
            terre = False
            for h in self.hexagones:
                mer = mer or (h.etat == HexaType.MER)
                terre = terre or (h.etat != HexaType.MER)
            self._isMaritime = (mer and not(terre))
        return self._isMaritime

    def isMaritimeOuCotier(self):
        ''' Renvoie vrai si l'intersection est dans la mer, au bord de la mer ou pas'''
        if self._isMaritimeOuCotier == -1:
            self._isMaritimeOuCotier = False
            for h in self.hexagones:
                if (h.etat == HexaType.MER) : self._isMaritimeOuCotier = True
        return self._isMaritimeOuCotier

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
        if self._isMarche == -1:
            self._isMarche = False
            for h in self.hexagones:
                if (h.isMarche() and self in h.lintp):
                    self._isMarche = True
        return self._isMarche
 
    


    def isPort(self):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type port, parmi les espaces de commerce'''
        if self._isPort == -1:
            self._isPort = False
            for h in self.hexagones:
                if (h.isPort() and self in h.lintp):
                    self._isPort = True
        return self._isPort



    def getTerre(self):
        ''' Renvoie la terre à laquelle appartient cette intersection, si elle est terrestre, 0 sinon '''
        if self._terre == -1:
            self._terre = 0
            for h in self.hexagones:
                if (h.etat != HexaType.MER) : self._terre = h.terre
        return self._terre

class Arrete:
    ''' Cette classe représente les liens entre les intersections, ou un côté d'un hexagone.'''

    def __init__(self,num,i1,i2):
        ''' Crée une arrête entre les deux intersections i1 et i2.'''
        self.num = num
        self.int1 = i1
        self.int2 = i2
        self.hexagones = []
        self.neigh = []
        self.neigh2 = []
    
        self._isCotier = -1
        self._isTerrestre = -1
        self._isTerrestreOuCotier = -1

        self._isMaritime = -1
        self._isMaritimeOuCotier = -1
        
        self._terre = -1


        i1.neigh.append(i2)
        i2.neigh.append(i1)
        i1.liens.append(self)
        i2.liens.append(self)

    def addHexa(self,h):
        ''' Ajoute h aux heagones de cette arrête'''
        if (not h in self.hexagones):
            self.hexagones.append(h)

    def __str__(self):
       return str(self.int1) + "--" + str(self.int2)
    
    def isCotier(self):
       ''' Renvoie vrai si l'arrête est au bord de la mer'''
       if self._isCotier == -1:
           mer = False
           terre = False
           for h in self.hexagones:
               mer = mer or (h.etat == HexaType.MER)
               terre = terre or (h.etat != HexaType.MER)
           self._isCotier = mer and terre
       return self._isCotier

    def isTerrestre(self):
        ''' Renvoie vrai si l'arrête est dans la terre, pas au bord de la mer'''
        if self._isTerrestre == -1:
            mer = False
            terre = False
            for h in self.hexagones:
                mer = mer or (h.etat == HexaType.MER)
                terre = terre or (h.etat != HexaType.MER)
            self._isTerrestre = not(mer) and terre
        return self._isTerrestre
    
    def isTerrestreOuCotier(self):
        '''# Renvoie vrai si l'arrête est dans la terre, au bord de la mer ou pas'''
        if self._isTerrestreOuCotier == -1:
            self._isTerrestreOuCotier = False
            for h in self.hexagones:
                if (h.etat != HexaType.MER) : self._isTerrestreOuCotier = True
        return self._isTerrestreOuCotier

    def isMaritime(self):
        ''' Renvoie vrai si l'arrête est en mer, pas au bord de la mer'''
        if self._isMaritime == -1:
            mer = False
            terre = False
            for h in self.hexagones:
                mer = mer or (h.etat == HexaType.MER)
                terre = terre or (h.etat != HexaType.MER)
            self._isMaritime = mer and not(terre)
        return self._isMaritime

    def isMaritimeOuCotier(self):
        ''' Renvoie vrai si l'arrête est en mer, au bord de la mer ou pas'''
        if self._isMaritimeOuCotier == -1:
            self._isMaritimeOuCotier = False
            for h in self.hexagones:
                if (h.etat == HexaType.MER) : self._isMaritimeOuCotier = True
        return self._isMaritimeOuCotier

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
        if self._terre == -1:
            self._terre = 0
            for h in self.hexagones:
                if (h.etat != HexaType.MER): 
                    self._terre = h.terre
                    return self._terre
            t1 = self.int1.getTerre()
            t2 = self.int2.getTerre()
            if t1 != 0:
                self._terre = t1
            elif t2 != 0:
                self._terre = t2
        return self._terre
            



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

    def __init__(self,num, i1,i2,i3,i4,i5,i6,t,p,comType=0,orientation=0):
        ''' Crée un hexagone entre les 6 intersection i1 à i6, de type t, avec une pastille p, de type de commerce ComType (si c'est une Mer -> Port, si c'est un désert -> marché), accessibles via les emplacements lintp. lintp doit être un sous ensemble de i1 i2 ... i6. Les arrêtes entre i1 i2, i2 i3 ... i6 i1 sont créées toutes seules.'''

        self.num = num
        self.int1 = i1
        self.int2 = i2
        self.int3 = i3
        self.int4 = i4
        self.int5 = i5
        self.int6 = i6
        self.etat = t
        self.past = p
        self.commerceType = comType
        self.ints = [i1,i2,i3,i4,i5,i6]
       
        if comType != 0: 
            if self.etat == HexaType.MER:
                self.lintp = [self.ints[orientation%6], self.ints[(orientation+1)%6]]
            else:
                self.lintp = [i1,i2,i3,i4,i5,i6]
        else:
            self.lintp = []


        i1.addHexa(self)
        i2.addHexa(self)
        i3.addHexa(self)
        i4.addHexa(self)
        i5.addHexa(self)
        i6.addHexa(self)
        self.liens = []
        for i in range(6):
            a = self.ints[i].lien(self.ints[(i+1)%6])
            if a == 0 :
                 a = Arrete(self.ints[i].num,self.ints[i],self.ints[(i+1)%6])
                 self.ints[i].liens.append(a)
                 self.ints[(i+1)%6].liens.append(a)
                 self.ints[i].neigh.append(self.ints[(i+1)%6])
                 self.ints[(i+1)%6].neigh.append(self.ints[i])
            self.liens.append(a)
            a.addHexa(self)

        self.neigh = 0

        self._isMaritimeCotier = -1
        self._isTerrestreCotier = -1
        self._isMaritime = -1
        self._isTerrestre = -1

    def __str__(self):
        return str(self.etat)+","+str(self.past)+","+str(self.int1) + "--" + str(self.int2) + "--" + str(self.int3) + "--" + str(self.int4) + "--" + str(self.int5) + "--" + str(self.int6) 
        
    def isMaritimeCotier(self):
        '''Renvoie vrai si cet exagone est marin, à côté de la terre'''
        if self._isMaritimeCotier == -1:
            cote = False
            for lien in self.liens:
                cote = cote or lien.isCotier()
            self._isMaritimeCotier = (self.etat==HexaType.MER) and cote
        return self._isMaritimeCotier
    
    def isTerrestreCotier(self):
        '''Renvoie vrai si cet exagone est terrestre, à côté de la mer'''
        if self._isTerrestreCotier == -1:
            cote = False
            for lien in self.liens:
                cote = cote or lien.isCotier()
            self._isTerrestreCotier = (self.etat!=HexaType.MER) and cote
        return self._isTerrestreCotier
    
    def isMaritime(self):
        '''Renvoie vrai si cet exagone est marin, pas à côté de la terre'''
        if self._isMaritime == -1:
            cote = False
            for lien in self.liens:
                cote = cote or lien.isCotier()
            self._isMaritime = (self.etat==HexaType.MER) and not(cote)
        return self._isMaritime
    
    def isTerrestre(self):
        '''Renvoie vrai si cet exagone est terrestre, pas à côté de la mer'''
        if self._isTerrestre == -1:
            cote = False
            for lien in self.liens:
                cote = cote or lien.isCotier()
            self._isTerrestre = (self.etat!=HexaType.MER) and not(cote)
        return self._isTerrestre

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

    
 
class Terre:
    ''' Cette classe représente un ensemble d'hexagones regroupés pour former une terre avec un espace maritime.'''

    def __init__(self,num,nom,hexsTerre,hexsMer):
        ''' Crée un terre de nom nom en regroupant les hexagones terrestres dans hexsTerre et les marins dans hexsMer'''
        self.num = num
        self.hexagones = hexsTerre
        self.espaceMarin = hexsMer
        self.nom = nom

        for h in hexsTerre:
            h.terre = self
       
        for h in hexsMer:
            h.terre = self

        # Attention voleurs à initialiser dans la BDD directement

    def addJoueur(self, j, bdd = REDIS):
        ''' Ajoute le joueur j aux joueur ayant colonisé cette terre'''
        bdd.rpush('T'+str(self.num)+':joueurs',j.num)

    def getJoueurIndex(self, j, bdd = REDIS):
        ''' Renvoie le rang du joueur parmi les colon de cette terre'''
        js = self.getJoueurs(bdd)
        return js.index(str(j.num))
    
    def getJoueur(self,index, bdd = REDIS):
        ''' Renvoie le joueur en position index sur cette terre '''
        return bdd.lindex('T'+str(self.num)+':joueurs',index)
    
    def getJoueurs(self, bdd = REDIS):
        ''' Renvoie tous les joueurs ayant colonisé cette terre '''
        return bdd.lrange('T'+str(self.num)+':joueurs',0,-1)
    

    def getNbJoueurs(self, bdd = REDIS): 
        ''' Renvoie le nombre de joueurs ayant colonisé cette terre'''
        return bdd.llen('T'+str(self.num)+':joueurs')


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

class Plateau:
    PLATEAU = 0 
    
    def __init__(self):
        self.intersections = []
        self.arretes = []
        self.hexagones = []
        self.terres = []
  
    def reinit(self): 
        self.intersections = []
        self.arretes = []
        self.hexagones = []
        self.terres = []

    @staticmethod
    def getPlateau():
        if Plateau.PLATEAU == 0:
            Plateau.PLATEAU = Plateau()
        return Plateau.PLATEAU

    def it(self,index):
        return self.intersections[index-1]

    def ar(self,index):
        return self.arretes[index-1]

    def hexa(self,index):
        return self.hexagones[index-1]

    def ter(self,index):
        return self.terres[index-1]

    def build(self, h,l, hs, terres):
        ''' Construit les intersections et les arrêtes d'un plateau de hauteur h et largeur l, puis les hexagones dont
            la description est donnée dans hs comme tuple de (type, pastille, type de commerce, orientation de commerce)
            Si le type de commerce est 0, alors ce n'est ni un port, ni un commerce.'''
        for i in xrange(h*l):
            self.intersections.append(Intersection(i+1))

        for j in xrange(h*l):

            i = j+1
            it = self.it(i)
            indUp = Plateau.up(j,h,l)
            i1 = self.it(indUp+1)
            a1 = Arrete(i,it,i1)

            self.arretes.append(a1)

        b = True
        for j in xrange(h*l):
            i = j+1
            
            it = self.it(i)
            k1 = j%l
            k2 = j/l
            if b:
                ind = Plateau.right(j,h,l)
                i3 = self.it(ind+1)
                a3 = Arrete(j/2 + h*l + 1,it,i3)
                self.arretes.append(a3)

            if (j+1)%l != 0:
                b = not b

        b = True
        k = 0
        for j in xrange(h*l):
            if b:
                i1 = j
                i2 = Plateau.right(i1,h,l)
                i3 = Plateau.up(i2,h,l)
                i4 = Plateau.up(i3,h,l)
                i5 = Plateau.left(i4,h,l)
                i6 = Plateau.down(i5,h,l)
                
                it1 = self.it(i1+1)
                it2 = self.it(i2+1)
                it3 = self.it(i3+1)
                it4 = self.it(i4+1)
                it5 = self.it(i5+1)
                it6 = self.it(i6+1)

                ts = hs[k]
                hexag = Hexagone(k+1,it1,it2,it3,it4,it5,it6,*ts)

                k += 1
                self.hexagones.append(hexag)
            if (j+1)%l != 0:
                b = not b

        k = 0
        for t in terres:
            nom = t[0]
            hexsTerre = []
            hexsMer = []
            for j in t[1]:
                hexsTerre.append(self.hexa(j))
            for j in t[2]:
                hexsMer.append(self.hexa(j))
            ter = Terre(k+1,nom,hexsTerre,hexsMer)
            self.terres.append(ter)
            k += 1
        
    @staticmethod
    def right(j,h,l):
        k1 = j%l
        k2 = j/l
        return (k1+1)%l+k2*l
    
    @staticmethod
    def left(j,h,l):
        k1 = j%l
        k2 = j/l
        return (k1-1)%l+k2*l

    @staticmethod
    def up(j,h,l):
        return (j+l)%(l*h)

    @staticmethod
    def down(j,h,l):
        return (j-l)%(l*h)

if __name__ == '__main__':
        
    p = Plateau.getPlateau()

    mer = HexaType.MER
    arg = HexaType.ARGILE
    bois = HexaType.BOIS
    aur = HexaType.OR
    des = HexaType.DESERT

    p.build(4,4, 
    [(mer,0,0,0),(mer,0,0,0),(arg,12,0,0),(mer,0,CommerceType.BLE,4),(bois,4,0,0),(aur,6,0,0),(des,0,CommerceType.TOUS,0),(mer,0,0,0)],
    [('Antaria',[3,5],[1]),('Hemenos',[6,7],[2,4,8])])
#for t in p.terres:
#    print t.num, [str(h.num) for h in t.hexagones], [str(h.num) for h in t.espaceMarin]

    for i in p.intersections:
         print i.num, [str(j) for j in i.neigh], [str(j) for j in i.liens]
