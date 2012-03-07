# *-* coding: iso-8859-1 *-*
from plateau import *
from cartes import *
from redis import *

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

    def ressources(self):
        ''' Renvoie dans un tableau l'ensemble des ressources au format (numéro de pastille, ensemble des ressources acquises si ce numéro tombe, or acquis si ce numéro tombe).
         Par exemple, si la colonie est entourée par un hexagone Bois de pastille 4, un Argile de pastille 5 et un Or de pastille 5, la méthode renverra
         [(4,Cartes.BOIS,0), (5,Cartes.ARGILE,1)]'''
        t = []
        for i in range(10):
           u = self.ressources_from_past(i+3)
           if u != 0:
               t.append((i+3,u[0],u[1]))
        return t

    def ressources_from_past(self,past):
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
            if(h.isBrigande() == 0 and h.past == past):
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

    def save(self):
        pos = 'I'+str(self.position.num)
        if(REDIS.exists(pos+'colonie')):
            befJ = REDIS.get(pos+'colonie')
            befjcol = 'J'+befJ+':colonies'
            befjvil = 'J'+befJ+':villes'
            befJ = int(befJ)
        else:
            befJ = 0
        pipe = REDIS.pipeline()
        if(befJ != self.joueur):
            pipe.set(pos+':colonie',self.joueur)
        pipe.set(pos+':isVille',self.isVille)
        jcol = 'J'+str(self.joueur)+':colonies'
        jvil = 'J'+str(self.joueur)+':villes'
        
        if(befJ != 0 and befJ != self.joueur):
            pipe.srem(befjcol,self.position.num)
            pipe.srem(befjvil,self.position.num)

        if self.isVille:    
            pipe.srem(jcol,self.position.num)
            pipe.sadd(jvil,self.position.num)
        else:
            pipe.srem(jvil,self.position.num)
            pipe.sadd(jcol,self.position.num)
        pipe.execute()

    @staticmethod
    def getColonie(it):
        key = 'I'+str(it.num)+':colonie'
        if REDIS.exists(key):
            jnum = int(REDIS.get(key))
            j = jnum
            c = Colonie(j,it)
            key2 = 'I'+str(it.num)+':isVille'
            c.isVille = (REDIS.get(key2) == 'True')
            return c
        else:
            return 0

class Route:
    ''' Tout autant une surprise, cette classe est identifiée au pion de type route.'''

    def __init__(self,jnum,a):
        ''' Pose une route appartenant au joueur j sur l'arrête a.'''
        self.joueur = jnum
        self.position = a

    def changer_proprietaire(self,jnum):
        ''' Change le propriétaire de la route en j'''
        self.joueur = jnum

   
    def est_extremite(self):
        ''' Vérifie si la route est une extrémité du réseau du joueur.'''
        i1 = self.position.int1
        i2 = self.position.int2
        col1 = Colonie.getColonie(i1)
        col2 = Colonie.getColonie(i2)
        if (col1 != 0 and col1.joueur != self.joueur) or (col2 != 0 and col2.joueur != self.joueur):
            return True
        ir1 = i1.neighb()
        b = True
        for i in ir1:
            if i2 != i:
                a = i.lien(i1)
                print a
                ar = Route.getRoute(a)
                b = b and (ar == 0 or ar.joueur != self.joueur)
        if b:
            return True
        b = True
        ir2 = i2.neighb()
        for i in ir2:
            if i1 != i:
                a = i.lien(i2)
                ar = Route.getRoute(a)
                b = b and (ar == 0 or ar.joueur != self.joueur)
        return b

    def rlplfr(self):
        ''' Renvoie la route la plus longue qui commence en self.'''
        return self.rlplfrwb([])

    def voisins_routables(self,l):
        ''' Renvoie l'ensemble des voisins de la route qui sont aussi des routes du meme joueur, et qui ne sont pas dans l, ou qui ne font pas faire un demi tour (par exemple sur un emplacement dhexagone, on a une étoile à 3 branches, si la dernière route de l est une de ces branche, que self en est une autre, alors la troisieme branche n'est pas un voisin routable'''
        a = self.position
        j = self.joueur
        ar = []
        for n in a.neighb():
            if not(n in l) and (len(l) == 0 or l[len(l)-1].lien(n) == 0):
                nr = Route.getRoute(n)
                if(nr != 0 and nr.joueur == j):
                    i = n.lien(a)
                    col = Colonie.getColonie(i)
                    if (col == 0 or col.joueur == j):
                        ar.append(nr)
        return ar

    def rlplfrwb(self,beginning):
        ''' Renvoie la route la plus longue commençant par beginning, passant par self'''
        beg2 = beginning + [self.position]
        vr = self.voisins_routables(beginning)
        i = 0
        for r in vr:
            i = max(i,r.rlplfrwb(beg2))
        print self.position.num, str(self.position)+"   ", [str(a) for a in beginning], i
        return i + 1
        
    def save(self):
        pos = 'A'+str(self.position.num)+':route'
        if(REDIS.exists(pos)):
            befJ = REDIS.get(pos)
            befjrout = 'J'+befJ+':routes'
            befJ = int(befJ)
        else:
            befJ = 0
        pipe = REDIS.pipeline()
        if(befJ != self.joueur):
            pipe.set(pos,self.joueur)
        jrout = 'J'+str(self.joueur)+':routes'
        
        if(befJ != 0 and befJ != self.joueur):
            pipe.srem(befjrout,self.position.num)

        pipe.sadd(jrout,self.position.num)
        pipe.execute()
    
    @staticmethod
    def getRoute(ar):
        key = 'A'+str(ar.num)+':route'
        if REDIS.exists(key):
            jnum = int(REDIS.get(key))
            j = jnum
            return Route(j,ar)
        else:
            return 0

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

    def en_position_echange(self):
        ''' Vérifie que le bateau est sur un emplacement où il peut échanger avec une terre : un port ou une colonie cotière'''
        i1 = self.position.int1
        i2 = self.position.int2
        col1 = Colonie.getColonie(i1)
        col2 = Colonie.getColonie(i2)
        return  ((col1 != 0 and col1.joueur == self.joueur) or (col2 != 0 and col2.joueur == self.joueur) or i1.isPort() or i2.isPort()) and self.joueur.aColonise(self.position.getTerre()) 
    
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

    def save(self):
        pos = 'B'+str(self.num)

        if(REDIS.exists(pos+':position')):
            befA = REDIS.get(pos+':position')
            befAboat = 'A'+befA+':bateaux'
            befA = int(befA)
        else:
            befA = 0

        pipe = REDIS.pipeline()
        if(befA != self.position.num):
            pipe.set(pos+':position',self.position.num)

        pipe.set(pos+':joueur',self.joueur)
        pipe.set(pos+':type',self.etat)
        self.cargaison.setTo(pos+":cargaison")
        pipe.set(pos+':aBouge', self.aBouge)

        aBoat = 'A'+str(self.position.num)+':bateaux'
        if(befA != 0 and befA != self.position.num):
            pipe.srem(befAboat,self.num)

        pipe.sadd(aBoat,self.num)
       
        jtrans = 'J'+str(self.joueur)+':transports'
        jtransPos = 'J'+str(self.joueur)+':transports:positions'
        jcarg = 'J'+str(self.joueur)+':cargos'
        jcargPos = 'J'+str(self.joueur)+':cargos:positions'
        jvoil = 'J'+str(self.joueur)+':voiliers'
        jvoilPos = 'J'+str(self.joueur)+':voiliers:positions'

        if self.etat == Bateau.BateauType.TRANSPORT:    
            pipe.sadd(jtrans,self.num)
            pipe.sadd(jtransPos,self.position.num)
        elif self.etat == Bateau.BateauType.CARGO:
            pipe.srem(jtrans,self.num)
            pipe.srem(jtransPos,self.position.num)
            pipe.sadd(jcarg,self.num)
            pipe.sadd(jcargPos,self.position.num)
        elif self.etat == Bateau.BateauType.VOILIER:
            pipe.srem(jtrans,self.num)
            pipe.srem(jtransPos,self.position.num)
            pipe.srem(jcarg,self.num)
            pipe.srem(jcargPos,self.position.num)
            pipe.sadd(jvoil,self.num)
            pipe.sadd(jvoilPos,self.position.num)
        pipe.execute()

    @staticmethod
    def getBateau(num):
        key = 'B'+str(num)
        if REDIS.exists(key+':position') :
            a = Plateau.getPlateau().ar(int(REDIS.get(key+':position')))
            j = int(REDIS.get(key+':joueur'))
            carg = CartesGeneral.get(key+':cargaison')
            etat = REDIS.get(key+':type')
            aBouge = (REDIS.get(key+':aBouge') == 'True')
            return Bateau(num,j,a,carg,etat,aBouge)
        return 0
