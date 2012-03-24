# *-* coding: iso-8859-1 *-*
from plateau import *
from cartes import *
from redis import *
import joueurs

REDIS = redis.StrictRedis()

class Colonie:
    '''Suprise totale, cette classe représente les pions de type colonies et ville. Cette classe ne se préoccupe pas des règles du jeu (pas de vérifications avant de faire les actions).'''

    def __init__(self,jnum,int):
        '''Pose sur le terrain une colonie du joueur j à l'emplacement int.'''
        self.joueur = jnum
        self.position = int
        self.isVille = False
        self.deblayeurs = []
        self.deblayeurs24 = []



    def changer_proprietaire(self,jnum):
        ''' Modifie le propriétaire d'un batiment, si c'est une ville, elle redevient une colonie. Elle perd tous ses déblayeurs.'''
        self.joueur = jnum
        self.deblayeurs = []
        self.deblayeurs24 = []
        self.isVille = False
 
    def evolue(self):
        ''' Transforme la colonie en ville'''
        self.isVille = True
    
    def isCotier(self):
        ''' Renvoie vrai si la colonie est au bord de la mer.'''
        return self.position.isCotier()

    def ressources(self, bdd = REDIS):
        ''' Renvoie dans un tableau l'ensemble des ressources au format (numéro de pastille, ensemble des ressources acquises si ce numéro tombe, or acquis si ce numéro tombe).
         Par exemple, si la colonie est entourée par un hexagone Bois de pastille 4, un Argile de pastille 5 et un Or de pastille 5, la méthode renverra
         [(4,Cartes.BOIS,0), (5,Cartes.ARGILE,1)]'''
        t = []
        for i in range(10):
           u = self.ressources_from_past(i+3, bdd)
           if u != 0:
               t.append((i+3,u[0],u[1]))
        return t

    def ressources_from_past(self,past, bdd = REDIS):
        ''' Renvoie un 2 upplet contenant les ressources et le nombre de pépites d'or acquies si le nombre past tombe.'''
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
            if(not Voleur.isBrigande(h, bdd) and h.past == past):
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

    def save(self, bdd = REDIS):
        pos = 'I'+str(self.position.num)
        if(bdd.exists(pos+'colonie')):
            befJ = bdd.get(pos+'colonie')
            befjcol = 'J'+befJ+':colonies'
            befjvil = 'J'+befJ+':villes'
            befJ = int(befJ)
        else:
            befJ = 0
        if(befJ != self.joueur):
            bdd.set(pos+':colonie',self.joueur)
        bdd.set(pos+':isVille',self.isVille)
        jcol = 'J'+str(self.joueur)+':colonies'
        jvil = 'J'+str(self.joueur)+':villes'
        
        if(befJ != 0 and befJ != self.joueur):
            bdd.srem(befjcol,self.position.num)
            bdd.srem(befjvil,self.position.num)

        if self.isVille:    
            bdd.srem(jcol,self.position.num)
            bdd.sadd(jvil,self.position.num)
        else:
            bdd.srem(jvil,self.position.num)
            bdd.sadd(jcol,self.position.num)

    @staticmethod
    def getColonie(it, bdd = REDIS):
        key = 'I'+str(it.num)+':colonie'
        if bdd.exists(key):
            jnum = int(bdd.get(key))
            j = jnum
            c = Colonie(j,it)
            key2 = 'I'+str(it.num)+':isVille'
            c.isVille = (bdd.get(key2) == 'True')
            return c
        else:
            return 0

    @staticmethod
    def hasColonie(it, bdd = REDIS):
        return bdd.exists('I'+str(it.num)+':colonie')

    @staticmethod
    def getColonieJoueur(it, bdd = REDIS):
        num = bdd.get('I'+str(it.num)+':colonie')
        if num == None:
            return -1
        else:
            return int(num)

class Route:
    ''' Tout autant une surprise, cette classe est identifiée au pion de type route.'''

    def __init__(self,jnum,a):
        ''' Pose une route appartenant au joueur j sur l'arrête a.'''
        self.joueur = jnum
        self.position = a

    def changer_proprietaire(self,jnum):
        ''' Change le propriétaire de la route en j'''
        self.joueur = jnum

   
    def est_extremite(self, bdd = REDIS):
        ''' Vérifie si la route est une extrémité du réseau du joueur.'''
        i1 = self.position.int1
        i2 = self.position.int2
        col1 = Colonie.getColonie(i1, bdd)
        col2 = Colonie.getColonie(i2, bdd)
        if (col1 != 0 and col1.joueur != self.joueur) or (col2 != 0 and col2.joueur != self.joueur):
            return True
        ir1 = i1.neighb()
        b = True
        for i in ir1:
            if i2 != i:
                a = i.lien(i1)
                ar = Route.getRoute(a, bdd)
                b = b and (ar == 0 or ar.joueur != self.joueur)
        if b:
            return True
        b = True
        ir2 = i2.neighb()
        for i in ir2:
            if i1 != i:
                a = i.lien(i2)
                ar = Route.getRoute(a, bdd)
                b = b and (ar == 0 or ar.joueur != self.joueur)
        return b

    def rlplfr(self, bdd = REDIS):
        ''' Renvoie la route la plus longue qui commence en self.'''
        return self.rlplfrwb([], bdd)

    def voisins_routables(self,l, bdd = REDIS):
        ''' Renvoie l'ensemble des voisins de la route qui sont aussi des routes du meme joueur, et qui ne sont pas dans l, ou qui ne font pas faire un demi tour (par exemple sur un emplacement dhexagone, on a une étoile à 3 branches, si la dernière route de l est une de ces branche, que self en est une autre, alors la troisieme branche n'est pas un voisin routable'''
        a = self.position
        j = self.joueur
        ar = []
        for n in a.neighb():
            if not(n in l) and (len(l) == 0 or l[len(l)-1].lien(n) == 0):
                nr = Route.getRoute(n, bdd)
                if(nr != 0 and nr.joueur == j):
                    i = n.lien(a)
                    col = Colonie.getColonie(i, bdd)
                    if (col == 0 or col.joueur == j):
                        ar.append(nr)
        return ar

    def rlplfrwb(self,beginning, bdd = REDIS):
        ''' Renvoie la route la plus longue commençant par beginning, passant par self'''
        beg2 = beginning + [self.position]
        vr = self.voisins_routables(beginning, bdd)
        i = 0
        for r in vr:
            i = max(i,r.rlplfrwb(beg2, bdd))
        return i + 1
        
    def save(self, bdd = REDIS):
        pos = 'A'+str(self.position.num)+':route'
        if(bdd.exists(pos)):
            befJ = bdd.get(pos)
            befjrout = 'J'+befJ+':routes'
            befJ = int(befJ)
        else:
            befJ = 0
        if(befJ != self.joueur):
            bdd.set(pos,self.joueur)
        jrout = 'J'+str(self.joueur)+':routes'
        
        if(befJ != 0 and befJ != self.joueur):
            bdd.srem(befjrout,self.position.num)

        bdd.sadd(jrout,self.position.num)
    
    @staticmethod
    def getRoute(ar,bdd = REDIS):
        key = 'A'+str(ar.num)+':route'
        if bdd.exists(key):
            jnum = int(bdd.get(key))
            j = jnum
            return Route(j,ar)
        else:
            return 0

    @staticmethod
    def hasRoute(ar, bdd = REDIS):
        return bdd.exists('A'+str(ar.num)+':route')

    @staticmethod
    def getRouteJoueur(ar, bdd = REDIS):
        num = bdd.get('A'+str(ar.num)+':route')
        if num == None:
            return -1
        else:
            return int(num)



class Bateau:
    ''' Classe identifiée au pion bateau'''

    class BateauType :
        ''' Ensemble des types de bateau qui existent'''
        VOILIER = 'bateauType_voilier'
        CARGO = 'bateauType_cargo'
        TRANSPORT = 'bateauType_transport'

    def __init__(self,num,jnum,a,carg,etat,aBouge):
        ''' Pose un bateau appartenant au joueur j sur l'arrête a'''
        self.num = num
        self.joueur = jnum
        self.position = a
        self.cargaison = carg
        self.etat = etat
        self.aBouge = aBouge
        self.fouilleurs = []
   
    def getCargaisonMax(self):
        if(self.etat == Bateau.BateauType.TRANSPORT):
            return 6
        else:
            return 10

    def getVitesse(self):
        if(self.etat == Bateau.BateauType.VOILIER):
            return 2
        else:
            return 1
 
    def evolue(self):
        ''' Transforme ce bateau en Cargo si c'est un bateau de transport, ou en voillier si c'est un cargo.'''
        if(self.etat == Bateau.BateauType.TRANSPORT):
             self.etat = Bateau.BateauType.CARGO
        elif self.etat == Bateau.BateauType.CARGO:
             self.etat = Bateau.BateauType.VOILIER

    def append(self,cartes):
        ''' Ajoute les cartes à la cargaison du bateau'''
        if (self.cargaison + cartes).size() <= self.getCargaisonMax():
            self.cargaison += cartes

    def remove(self,cartes):
        ''' Retire les cartes de la cargaison'''
        if(cartes <= self.cargaison):
           self.cargaison -= cartes

    def deplacer(self,a):
        ''' Pose ce bateau sur l'arrête a (sans se soucier de savoir s'il a le droit)'''
        self.position.bateau = 0
        self.position = a
        a.bateau = self

    def peut_recevoir_et_payer(self,cr,cp):
        ''' Vérifie si le bateau peut recevoir les cartes cr et donner (en même temps) les cartes cp.'''
        return cp <= self.cargaison and (self.cargaison + cr - cp).size() <= self.getCargaisonMax()

    def positions_colonisables(self):
        ''' Renvoie toutes les positions terrestres situées à deux hexagones d'un bateau sur la cote.'''
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

    def en_position_echange(self, bdd = REDIS):
        ''' Vérifie que le bateau est sur un emplacement où il peut échanger avec une terre : un port ou une colonie cotière'''
        i1 = self.position.int1
        i2 = self.position.int2
        col1 = Colonie.getColonie(i1, bdd)
        col2 = Colonie.getColonie(i2, bdd)
        j = joueurs.Joueur(self.joueur)
        return  ((col1 != 0 and col1.joueur == self.joueur) or (col2 != 0 and col2.joueur == self.joueur) or i1.isPort() or i2.isPort()) and j.aColoniseTerre(self.position.getTerre(), bdd) 
    
    def est_proche(self,terre):
        ''' Est vrai si le bateau est à un déplacement d'un emplacement cotier'''
        ints = []
        ints += [self.position.int1,self.position.int2]
        ints += self.position.int1.neighb()
        ints += self.position.int2.neighb()
        if(self.etat == Bateau.BateauType.VOILIER):
            for i in ints[:]:
                ints += i.neighb()
        for i in ints:
            if i.isTerrestreOuCotier() and i.getTerre() == terre:
                return True
        return False

    def save(self, bdd = REDIS):
        pos = 'B'+str(self.num)

        if(bdd.exists(pos+':position')):
            befA = bdd.get(pos+':position')
            befAboat = 'A'+befA+':bateaux'
            befA = int(befA)
        else:
            befA = 0

        if(befA != self.position.num):
            bdd.set(pos+':position',self.position.num)

        bdd.set(pos+':joueur',self.joueur)
        bdd.set(pos+':type',self.etat)
        self.cargaison.setTo(pos+":cargaison",bdd)
        bdd.set(pos+':aBouge', self.aBouge)

        aBoat = 'A'+str(self.position.num)+':bateaux'
        if(befA != 0 and befA != self.position.num):
            bdd.srem(befAboat,self.num)

        bdd.sadd(aBoat,self.num)
       
        jtrans = 'J'+str(self.joueur)+':transports'
        jtransPos = 'J'+str(self.joueur)+':transports:positions'
        jcarg = 'J'+str(self.joueur)+':cargos'
        jcargPos = 'J'+str(self.joueur)+':cargos:positions'
        jvoil = 'J'+str(self.joueur)+':voiliers'
        jvoilPos = 'J'+str(self.joueur)+':voiliers:positions'

        if self.etat == Bateau.BateauType.TRANSPORT:    
            bdd.sadd(jtrans,self.num)
            bdd.sadd(jtransPos,self.position.num)
        elif self.etat == Bateau.BateauType.CARGO:
            bdd.srem(jtrans,self.num)
            bdd.srem(jtransPos,self.position.num)
            bdd.sadd(jcarg,self.num)
            bdd.sadd(jcargPos,self.position.num)
        elif self.etat == Bateau.BateauType.VOILIER:
            bdd.srem(jtrans,self.num)
            bdd.srem(jtransPos,self.position.num)
            bdd.srem(jcarg,self.num)
            bdd.srem(jcargPos,self.position.num)
            bdd.sadd(jvoil,self.num)
            bdd.sadd(jvoilPos,self.position.num)

    @staticmethod
    def getBateau(num,bdd = REDIS):
        key = 'B'+str(num)
        if bdd.exists(key+':position') :
            a = Plateau.getPlateau().ar(int(bdd.get(key+':position')))
            jnum = int(bdd.get(key+':joueur'))
            carg = CartesGeneral.get(key+':cargaison',bdd)
            etat = bdd.get(key+':type')
            aBouge = (bdd.get(key+':aBouge') == 'True')
            return Bateau(num,jnum,a,carg,etat,aBouge)
        return 0

    @staticmethod
    def getBateaux(ar,bdd = REDIS):
        b = []
        bn = bdd.smembers('A'+str(ar.num)+':bateaux')
        for n in bn:
            b.append(Bateau.getBateau(int(n), bdd))
        return b

    @staticmethod
    def getBateauxNum(ar, bdd = REDIS):
        return bdd.smembers('A'+str(ar.num)+':bateaux')

class Voleur:
    ''' Classe représentant le pion voleur.'''
    
    class VoleurType:
        ''' Les type de voleur : briguand sur terre, pirate sur mer'''
        BRIGAND = 'voleur_brigand'
        PIRATE = 'voleur_pirate'

    def __init__(self,hex,etat,terre):
        ''' Pose un voleur de type etat, sur l'hexagone hex.'''
        self.position = hex
        self.etat = etat
        self.terre = terre

    def deplacer(self,hex):
        ''' Déplace le voleur sur l'hexagone hex'''
        if hex == 0 or hex.terre == self.terre:
            self.position = hex

    def save(self, bdd = REDIS):
        if(self.etat == Voleur.VoleurType.BRIGAND):
            bdd.set("T"+str(self.terre.num)+":brigand:position",self.position.num)
        else:
            if self.position == 0:
                n = 0
            else:
                n = self.position.num 
            bdd.set("T"+str(self.terre.num)+":pirate:position",n)

    @staticmethod
    def getBrigand(terre, bdd = REDIS):
        hexIdStr = bdd.get("T"+str(terre.num)+":brigand:position")
        if hexIdStr != None:
            hexId = int(hexIdStr)
            if hexId == 0:
                hex = 0
            else:
                hex = Plateau.getPlateau().hexa(hexId)
            return Voleur(hex,Voleur.VoleurType.BRIGAND,terre) 
        return 0

    @staticmethod
    def getPirate(terre, bdd = REDIS):
        hexIdStr = bdd.get("T"+str(terre.num)+":pirate:position")
        if hexIdStr != None:
            hexId = int(hexIdStr)
            if hexId == 0:
                hex = 0
            else:
                hex = Plateau.getPlateau().hexa(hexId)
            return Voleur(hex,Voleur.VoleurType.PIRATE,terre)
        return 0

    @staticmethod
    def isMarcheNonBrigande(intersection, bdd = REDIS):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type marché, parmi les espaces de commerce non occupé par un brigand'''
        for h in intersection.hexagones:
            if (h.isMarche() and intersection in h.lintp and not Voleur.isBrigande(h, bdd)):
                return True
        return False
    
    @staticmethod
    def marcheNonBrigande(intersection, bdd = REDIS):
        ''' Renvoie l'ensemble des hexagones cette intersection de type marché, parmi les espaces de commerce, non occupés par un brigand'''
        marches = []
        for h in intersection.hexagones:
            if (h.isMarche() and intersection in h.lintp and not Voleur.isBrigande(h, bdd)):
                marches.append(h)
        return marches

    @staticmethod
    def isPortNonPirate(intersection, bdd = REDIS):
        ''' Renvoie vrai si l'intersection est sur un hexagone de type port, parmi les espaces de commerce, non occupé par un pirate'''
        for h in intersection.hexagones:
            if (h.isPort() and intersection in h.lintp and not Voleur.isPirate(h, bdd)):
                return True
        return False

    @staticmethod
    def portNonPirate(intersection, bdd = REDIS):
        ''' Renvoie l'ensemble des hexagones de l'intersection de type port, parmi les espaces de commerce, non occupé par un pirate'''
        ports = []
        for h in intersection.hexagones:
            if (h.isPort() and intersection in h.lintp and not Voleur.isPirate(h, bdd)):
                ports.append(h)
        return ports
    
    @staticmethod
    def est_pirate(arrete, bdd = REDIS):
        '''Renvoie vrai si l'arrete est occupée par le pirate'''
        for h in arrete.hexagones:
            if (h.etat == HexaType.MER and Voleur.isPirate(h, bdd)):
                return True
        return False

    @staticmethod
    def isBrigande(h, bdd = REDIS):
        v = Voleur.getBrigand(h.terre, bdd)
        return v != 0 and v.position.num == h.num
    
    @staticmethod
    def isPirate(h, bdd = REDIS):
        v = Voleur.getPirate(h.terre, bdd)
        return v != 0 and v.position.num == h.num
