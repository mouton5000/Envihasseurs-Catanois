# *-* coding: iso-8859-1 *-*
from pions import *
from plateau import *
from cartes import *
from foret_action import *
import random
import functools
import redis

REDIS = redis.StrictRedis()

class Tarifs:
    COLONIE = CartesRessources(1,1,1,0,1)
    VILLE = CartesRessources(0,3,0,2,0)
    ROUTE = CartesRessources(1,0,1,0,0)
    BATEAU_TRANSPORT = CartesRessources(0,0,1,0,1)
    CARGO = CartesRessources(1,0,0,1,0)
    VOILIER = CartesRessources(1,0,0,0,2)
    DEVELOPPEMENT = CartesRessources(0,1,0,1,1)

def protection(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        peut_f = getattr(Jeu,'peut_' + f.__name__)
        if peut_f(*args,**kwargs):
            f(*args,**kwargs)
            return True
        else:
            return False

    return helper

class Des:

    NB_LANCES = 4

    @staticmethod
    def roll(bdd = REDIS):
        ''' Enregistre une liste de 4 lancés de dés dans la bdd '''
        dices = []
        for i in xrange(Des.NB_LANCES):
            dices.append(random.randint(2, 12))
        Des.save(dices,bdd)


    @staticmethod
    def getOrigin(bdd = REDIS):
        ''' Renvoie le nombre de lancés de dés, correspond donc en jeu de plateau au nombres de joueurs qui ont lancé les dés et donc au numéro du joueur, modulo le nombre de joueurs, qui a effectué le premiers des 4 derniers lancés. '''
        return int(bdd.get('dices:joueur_origine'))
    
    @staticmethod
    def setOrigin(num, bdd = REDIS):
        ''' Enregistre le nombre de lancés de dés depuis le début de la partie '''
        bdd.set('dices:joueur_origine',num)
    
    @staticmethod
    def incrOrigin(bdd = REDIS):
        ''' Incrémente le nombre de lancé de dés '''
        bdd.incr('dices:joueur_origine',Des.NB_LANCES)

    @staticmethod
    def save(dices, bdd = REDIS):
        ''' Sauvegarde un lancé de 4 dés '''
        bdd.delete('dices')
        bdd.rpush('dices',*dices)
        Des.incrOrigin(bdd)

    @staticmethod
    def getDices(bdd = REDIS):
        ''' Renvoie les 4 derniers lancés de dés '''
        a =  bdd.lrange('dices',0,-1)
        dices = [int(i) for i in a]
        return dices

class Joueur:
    ''' Classe représentant un joueur, avec ses pions (construction, bateau), permettant de récupérer les informations relatives à ce joueur, voire d'en modifier.'''
    def __init__(self,num):
        self.num = num

    def setCartes(self,terre,cartes, bdd = REDIS):
        ''' Associe à la main du joueur sur cette terre les cartes données en paramètre'''
        cartes.setTo('J'+str(self.num)+':T'+str(terre.num), bdd)

    def getCartes(self,terre, bdd = REDIS):
        ''' Renvoie la main du joueur sur cette terre'''
        return CartesGeneral.get('J'+str(self.num)+':T'+str(terre.num), bdd)
    
    def payer(self,terre, cartes, bdd = REDIS):
        ''' Déduis de la main du joueur sur cette terre les cartes données en paramètre'''
        self.setCartes(terre,self.getCartes(terre,bdd) - cartes, bdd)

    def recevoir(self,terre,cartes, bdd = REDIS):
        ''' Ajoute à la main du joeuur sur cette terre les cartes données en paramètre'''
        self.payer(terre,cartes*(-1), bdd)

    def peut_payer(self,terre,cartes, bdd = REDIS):
        ''' Vérifie si la main du joeuur sur cette terre peut payer la quantité donnée en paramètre'''
        return cartes <= self.getCartes(terre, bdd)
    
    def ressource_aleatoire(self,terre, bdd = REDIS):
        ''' Ajoute à la main du joueur sur cette terre une carte de ressource aléatoire'''
        carte = CartesRessources.get_random_ressource(bdd)
        self.setCartes(terre,self.getCartes(terre, bdd) + carte, bdd)

    def getOr(self,terre, bdd = REDIS):
        ''' Renvoie la quantité d'or du joueur présente sur cette terre'''
        return int(bdd.get('J'+str(self.num)+':T'+str(terre.num)+':or'))

    def setOr(self,terre, nb, bdd = REDIS):
        ''' Définit la quantité d'or du joueur présente sur cette terre'''
        bdd.set('J'+str(self.num)+':T'+str(terre.num)+':or', nb)

    def addOr(self,terre,nb, bdd = REDIS):
        ''' Ajoute au stock d'or du joeuur sur cette terre nb lingots d'or'''
        self.setOr(terre, self.getOr(terre, bdd) + nb, bdd)

    def payerOr(self,terre, bdd = REDIS):
        ''' Déduis du stock d'or du joueur sur cette terre un lingot d'or'''
        self.addOr(terre,-1, bdd)

    def aColoniseTerre(self,terre, bdd = REDIS):
        return bdd.sismember('J'+str(self.num)+':terres', terre.num)
    
    def addTerre(self,terre, bdd = REDIS):
        ''' Ajoute une terre aux terres colonisées du joueur'''
        bdd.sadd('J'+str(self.num)+':terres',terre.num)
        self.setCartes(terre,Cartes.RIEN, bdd)
        self.setOr(terre,0, bdd)
        self.set_chevalliers(terre,0, bdd)
        self.set_route_la_plus_longue(terre,0, bdd)
        self.setStaticPoints(terre,0, bdd)
        terre.addJoueur(self, bdd)

    def getTerres(self, bdd = REDIS):
        l = bdd.smembers('J'+str(self.num)+':terres')
        t = []
        for i in l:
            t.append(Plateau.getPlateau().ter(int(i)))
        return t

    def piocher_developpement(self, terre, bdd = REDIS):
        ''' Ajoute à la main du joueur sur cette terre une carte de développement aléatoire'''
        i = random.Random().randint(1,5)
        if (i == 1):
            carte = Cartes.CHEVALLIER
        elif i == 2:
            carte = Cartes.MONOPOLE
        elif i == 3:
            carte = Cartes.POINT_VICTOIRE
        elif i == 4:
            carte = Cartes.DECOUVERTE
        elif i == 5:
            carte = Cartes.CONSTRUCTION_ROUTES
        self.recevoir(terre,carte, bdd)
        return carte

    def contient_commerce_utilisable(self,terre,comType, bdd = REDIS):
        ''' Vérifie si le joueur contient sur cette terre un commerce de type comType'''
        for c in self.getBatiments(bdd):
            c = int(c)
            intersection = Plateau.getPlateau().it(c)
            ms = Voleur.marcheNonBrigande(intersection, bdd)
            ps = Voleur.portNonPirate(intersection, bdd)
            if ms != 0:
                for m in ms:
                    if m.commerceType == comType:
                        return True
            if ps != 0:
                for p in ps:
                    if p.commerceType == comType:
                        return True
        return False


    def recolter_ressources(self,des, bdd = REDIS):
        ''' Récolte les ressources du joueur en fonction du lancé de dés, sur toutes les terres'''
        for c in self.getBatiments(bdd):
            c = int(c)
            it = Plateau.getPlateau().it(c)
            terre = it.getTerre()
            res = Colonie.getColonie(it,bdd).ressources_from_past(des,bdd)
            if (res != 0):
                self.addOr(terre,res[1], bdd)
                self.recevoir(terre,res[0], bdd) 

    def getBateaux(self, bdd = REDIS):
        ''' Renvoie les identifiants des bateaux du joueur, tout type confondu'''
        return self.getBateauxTransport(bdd).union(self.getCargos(bdd)).union(self.getVoiliers(bdd))
    
    def getBateauxTransport(self, bdd = REDIS):
        return bdd.smembers('J'+str(self.num)+':transports')

    def getCargos(self, bdd = REDIS):
        return bdd.smembers('J'+str(self.num)+':cargos')
    
    def getVoiliers(self, bdd = REDIS):
        return bdd.smembers('J'+str(self.num)+':voiliers')
    
    
    def getBateauxTransportPositions(self, bdd = REDIS):
        ''' Renvoie les arretes où se trouvent les bateaux du joueur, tout type confondu'''
        return bdd.smembers('J'+str(self.num)+':transports:positions')

    def getCargosPositions(self, bdd = REDIS):
        return bdd.smembers('J'+str(self.num)+':cargos:positions')
    
    def getVoiliersPositions(self, bdd = REDIS):
        return bdd.smembers('J'+str(self.num)+':voiliers:positions')
    
    def getBateauxPositions(self, bdd = REDIS):
        ''' Renvoie les bateaux du joueur, tout type confondu'''
        return self.getBateauxTransportPositions(bdd).union(self.getCargosPositions(bdd)).union(self.getVoiliersPositions(bdd))

    def getColonies(self, bdd = REDIS):
        ''' Renvoie tous les intersection où se trouvent les colonies du joueur'''
        return bdd.smembers('J'+str(self.num)+':colonies')

    def getVilles(self, bdd = REDIS):
        ''' Renvoie tous les intersection où se trouvent les villes du joueur'''
        return bdd.smembers('J'+str(self.num)+':villes')
    
    def getRoutes(self, bdd = REDIS):
        ''' Renvoie tous les arretes où se trouvent les routes du joueur'''
        return bdd.smembers('J'+str(self.num)+':routes')

    def getBatiments(self, bdd = REDIS):
        ''' Renvoie toutes les intersection où se trouvent les batiments du joueur, tout type confondu'''
        return self.getColonies(bdd).union(self.getVilles(bdd))
    
    def set_chevalliers(self,terre, nb, bdd = REDIS):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        bdd.set('J'+str(self.num)+':T'+str(terre.num)+':armee', nb)
                 
    def add_chevallier(self,terre, bdd = REDIS):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        return int(bdd.incr('J'+str(self.num)+':T'+str(terre.num)+':armee'))
 
    def get_chevalliers(self,terre, bdd = REDIS):
        ''' Renvoie l'armée du joueur sur cette terre'''
        if self.getEnRuine(bdd):
            return 0
        return int(bdd.get('J'+str(self.num)+':T'+str(terre.num)+':armee'))
   
    def set_deplacement_voleur(self,terre, dep, bdd = REDIS):
        ''' Indique que sur cette terre, le joueur doit déplacer le voleur'''
        bdd.set('J'+str(self.num)+':T'+str(terre.num)+':deplacement_voleur', dep)
 
    def get_deplacement_voleur(self,terre, bdd = REDIS):
        ''' Renvoie vrai si sur cette terre, le joueur doit déplacer le voleur'''
        return bdd.get('J'+str(self.num)+':T'+str(terre.num)+':deplacement_voleur') == 'True'
         
    def get_carte_armee_la_plus_grande(self,terre, bdd = REDIS):
        ''' Renvoie vrai si le joueur a l'armée la plus grande sur cette terre'''
        u = Jeu.get_armee_la_plus_grande(terre, bdd)
        return u!=0 and u[0] == self.num
 
    def get_route_la_plus_longue(self,terre, bdd = REDIS):
        ''' Renvoie la taille de la route la plus longue du joueur sur cette terre'''
        if self.getEnRuine(bdd):
            return 0
        return int(bdd.get('J'+str(self.num)+':T'+str(terre.num)+':rlpl'))
 
    def set_route_la_plus_longue(self,terre, l, bdd = REDIS):
        ''' Définie la route la plus longue sur cette terre comme étant de taille l'''
        bdd.set('J'+str(self.num)+':T'+str(terre.num)+':rlpl',l)

    def recalcul_route_la_plus_longue(self,terre, bdd = REDIS):
        ''' Calcule la route la plus longue de ce joueur sur cette terre. Si elle est déjà calculée alors renvoie juste la valeur déjà calculée '''
        if self.getEnRuine(bdd):
            self.set_route_la_plus_longue(terre,0, bdd)
            return
        if self.aColoniseTerre(terre, bdd):
                i = 0
                for arn in self.getRoutes(bdd):
                    ar = Plateau.getPlateau().ar(int(arn))
                    r = Route.getRoute(ar,bdd)
                    if ar.getTerre() == terre and r.est_extremite(bdd):
                        i = max(i, r.rlplfr(bdd))
                self.set_route_la_plus_longue(terre,i, bdd)
                       
    def get_carte_route_la_plus_longue(self,terre, bdd = REDIS):
        ''' Vérifie si ce joueur a la carte de la route al plus longue sur cette terre'''
        u = Jeu.get_route_la_plus_longue(terre, bdd)
        return u!=0 and u[0]== self.num

    def addStaticPoints(self,terre,nb, bdd = REDIS):
        ''' Ajoute nb points aux points statiques (ie batiments) de cette terre'''
        if self.getEnRuine(bdd):
            return 
        bdd.incr('J'+str(self.num)+':T'+str(terre.num)+':points',nb)

    def getStaticPoints(self,terre, bdd = REDIS):
        if self.getEnRuine(bdd):
            return 0
        return int(bdd.get('J'+str(self.num)+':T'+str(terre.num)+':points'))
    
    def setStaticPoints(self,terre, nb, bdd = REDIS):
        if self.getEnRuine(bdd):
            return 
        bdd.set('J'+str(self.num)+':T'+str(terre.num)+':points', nb)

    def getPoints(self,terre, bdd = REDIS):
        ''' Calcule le nombre de points de ce joueur sur cette terre'''
        if self.getEnRuine(bdd) or not self.aColoniseTerre(terre,bdd):
            return 0
        return self.getVisiblePoints(terre,bdd) + self.getCartes(terre, bdd).get_cartes_de_type(Cartes.POINT_VICTOIRE)
    
    def getVisiblePoints(self,terre, bdd = REDIS):
        ''' Calcule le nombre de points de ce joueur sur cette terre'''
        if self.getEnRuine(bdd) or not self.aColoniseTerre(terre, bdd):
            return 0
        p = 0
        if (self.get_carte_route_la_plus_longue(terre, bdd)):
            p += 2
        if (self.get_carte_armee_la_plus_grande(terre, bdd)):
            p += 2
        return self.getStaticPoints(terre, bdd) + p

    def addRoot(self):
        return ForetAction.setNewRoot(self) 
    
    def addFirstRoot(self):
        return ForetAction.setNewFirstRoot(self) 

    def addNextRoot(self,root):
        return ForetAction.setNewNextRoot(root,self) 

    @staticmethod
    def setNbJoueurs(nb, bdd = REDIS):
        bdd.set('NombreJoueurs',nb)
        
    @staticmethod
    def getNbJoueurs(bdd = REDIS):
        return int(bdd.get('NombreJoueurs'))

    def setEnRuine(self,ruine, bdd = REDIS):
        bdd.set('J'+str(self.num)+':ruine',ruine)
    
    def getEnRuine(self, bdd = REDIS):
        return bdd.get('J'+str(self.num)+':ruine') == 'True'

    def ruiner(self, bdd = REDIS):
        self.setEnRuine(True,bdd)
        for t in self.getTerres(bdd):
            self.setStaticPoints(t,0,bdd)
            Jeu.recalcul_route_la_plus_longue(t,bdd)
            Jeu.recalcul_armee_la_plus_grande(t,bdd)

class Jeu:

    @staticmethod
    def get_all_joueurs(bdd = REDIS):
        i = Joueur.getNbJoueurs(bdd)
        joueurs = []
        for j in xrange(i):
            joueurs.append(Joueur(j+1))
        return joueurs

    # Renvoie le joueur qui possède la route la plus longue sur la terre terre et sa longueur.
    @staticmethod
    def get_route_la_plus_longue(terre, bdd = REDIS):
        j = bdd.get('T'+str(terre.num)+':carte_rlpl:joueur')
        l = bdd.get('T'+str(terre.num)+':carte_rlpl:longueur')
        if j != None and l != None:
            return (int(j),int(l))
        else:
            return 0

    @staticmethod
    def set_route_la_plus_longue(terre,j,n, bdd = REDIS):
        bdd.set('T'+str(terre.num)+':carte_rlpl:joueur',j)
        bdd.set('T'+str(terre.num)+':carte_rlpl:longueur',n)
    
    @staticmethod
    def delete_route_la_plus_longue(terre, bdd = REDIS):
        bdd.delete('T'+str(terre.num)+':carte_rlpl:joueur')
        bdd.delete('T'+str(terre.num)+':carte_rlpl:longueur')

    # Vérifie si j a une route plus longue que la route la plus longue sur la terre terre. Si la route actuelle est nulle, alors vérifie si j a une route de plus de 5 troncons. Si c'est le cas, j prend la plus du joueur actuellement en position
    @staticmethod
    def challenge_route_la_plus_longue(j,terre, bdd = REDIS):
            n = j.get_route_la_plus_longue(terre, bdd)
            if n>=5:
                u = Jeu.get_route_la_plus_longue(terre,bdd)
                if u == 0 or  n > u[1]:
                    Jeu.set_route_la_plus_longue(terre,j.num,n,bdd)
                    
    # Recalcule qui parmi les colons de la terre a la carte de route la plus longue. Si il y a égalité, si la route la plus longue est identique à celle précédemment inscrite dans la base de données, alors elle est conservée, sinon, la carte est retirée du jeu jusqu'à ce que ait un montant plus important.
    @staticmethod
    def recalcul_route_la_plus_longue(terre, bdd = REDIS):
        jt = terre.getJoueurs(bdd)
        rlpl = 0
        jmax = []
        for jtn in jt:
            j = Joueur(int(jtn))
            rlplj = j.get_route_la_plus_longue(terre,bdd)
            if rlplj > rlpl:
                rlpl = rlplj
                jmax = [j.num]
            elif rlplj == rlpl:
                jmax.append(j.num)
        if len(jmax) == 1 and rlpl >= 5:
            Jeu.set_route_la_plus_longue(terre,jmax[0],rlpl,bdd)
        else:
            t = Jeu.get_route_la_plus_longue(terre,bdd)
            if t != 0  and (t[1] > rlpl or not t[0] in jmax):
                Jeu.delete_route_la_plus_longue(terre,bdd)
                


    # Renvoie le joueur qui possède l'armee la plus grande sur la terre terre et sa longueur.
    @staticmethod
    def get_armee_la_plus_grande(terre, bdd = REDIS):
        j = bdd.get('T'+str(terre.num)+':carte_alpg:joueur')
        s = bdd.get('T'+str(terre.num)+':carte_alpg:taille')
        if j != None and s != None:
            return (int(j),int(s))
        else:
            return 0

    @staticmethod
    def set_armee_la_plus_grande(terre,j,s, bdd = REDIS):
        bdd.set('T'+str(terre.num)+':carte_alpg:joueur',j)
        bdd.set('T'+str(terre.num)+':carte_alpg:taille',s)
    
    @staticmethod
    def delete_armee_la_plus_grande(terre, bdd = REDIS):
        bdd.delete('T'+str(terre.num)+':carte_alpg:joueur')
        bdd.delete('T'+str(terre.num)+':carte_alpg:taille')

                
    # Vérifie si j a une armee plus grande que la armee la plus grande sur la terre terre. Si l'armee actuelle est nulle, alors vérifie si j a une armee de plus de 3 chevalliers. Si c'est le cas, j prend la plus du joueur actuellement en position
    @staticmethod
    def challenge_armee_la_plus_grande(j,terre, bdd = REDIS):
        n = j.get_chevalliers(terre,bdd)
        if n>=3:
            u = Jeu.get_armee_la_plus_grande(terre,bdd)
            if u == 0 or  n > u[1]:
                Jeu.set_armee_la_plus_grande(terre,j.num,n,bdd)
    
    # Recalcule qui parmi les colons de la terre a la carte de route la plus longue. Si il y a égalité, si la route la plus longue est identique à celle précédemment inscrite dans la base de données, alors elle est conservée, sinon, la carte est retirée du jeu jusqu'à ce que ait un montant plus important.
    @staticmethod
    def recalcul_armee_la_plus_grande(terre, bdd = REDIS):
        jt = terre.getJoueurs(bdd)
        armee = 0
        jmax = []
        for jtn in jt:
            j = Joueur(int(jtn))
            armeej = j.get_chevalliers(terre,bdd)
            if armeej > armee:
                armee = armeej
                jmax = [j.num]
            elif armeej == armee:
                jmax.append(j.num)
        if len(jmax) == 1 and armee >= 3:
            Jeu.set_armee_la_plus_grande(terre,jmax[0],armee,bdd)
        else:
            t = Jeu.get_armee_la_plus_grande(terre,bdd)
            if t != 0  and (t[1] > armee or not t[0] in jmax):
                Jeu.delete_armee_la_plus_grande(terre,bdd)

# -----------------------------------------------------
#    Actions de la nuit
# -----------------------------------------------------

    @staticmethod
    def designer_deplaceur_de_voleur(bdd = REDIS):
        p = Plateau.getPlateau()
        for terre in p.terres:
            js = terre.getJoueurs(bdd)
            for jn in js:
                j = Joueur(int(jn))
                j.set_deplacement_voleur(terre,False,bdd)

        des = Des.getDices(bdd)
        origin = Des.getOrigin(bdd)
        for terre in p.terres:
            js = []
            for jns in terre.getJoueurs(bdd):
                j = Joueur(int(jns))
                if(not j.getEnRuine(bdd)):
                    js.append(j)
            for i in range(0,Des.NB_LANCES):
                if des[i] == 7:
                    js[(i+origin)%len(js)].set_deplacement_voleur(terre,True,bdd)

# -----------------------------------------------------
#    Actions dans la journee
# -----------------------------------------------------





    @staticmethod
    def peut_construire_colonie(j,intersection, bdd = REDIS):
        ''' Un joueur peut construire une colonie si il n'est aps en ruine, si il ne la construit pas a un emplacement voisin d'une autre colonie, si il la construit sur un emplacement voisin d'une de ses routes, si cet emplacement est sur terre et si il peut payer la construiction.'''
        col = Colonie.hasColonie(intersection, bdd)
        if not j.getEnRuine(bdd) and not col and not intersection.isMaritime() and j.peut_payer(intersection.getTerre(), Tarifs.COLONIE,bdd):
    
            for i in intersection.neigh:
                if Colonie.hasColonie(i,bdd):
                    return False
            for a in intersection.liens:
                jrout = Route.getRouteJoueur(a,bdd)
                if jrout == j.num:
                    return True
        return False

    @staticmethod
    @protection
    def construire_colonie(j, intersection, bdd = REDIS):
        ''' Pose une nouvelle colonie du joueur j sur l'intersection si il en a la possibilité, et effectue le paiement.'''
        c = Colonie(j.num, intersection)
        terre = intersection.getTerre()
        j.payer(terre, Tarifs.COLONIE,bdd)
        j.addStaticPoints(terre,1,bdd)

        c.save(bdd)
        for a in intersection.liens:
            jrout = Route.getRouteJoueur(a,bdd)
            if jrout != 0 and jrout != j.num:
                Joueur(jrout).recalcul_route_la_plus_longue(terre,bdd)
        Jeu.recalcul_route_la_plus_longue(terre,bdd)

    @staticmethod
    def peut_construire_route(j, arrete, construction_route = False, bdd = REDIS):
        ''' Un joueur j peut construire une route sur l'arrete si il n'est pas en ruine, si il n'existe pas déjà de route non en ruine sur cet emplacement, si cette arrete est terrestre, si il peut payer ou s'il a jouer une carte développement de construction de route, et s'il existe une colonie ou une route voiine à cette arrete.'''
        rout = Route.hasRoute(arrete,bdd)
        if not j.getEnRuine(bdd) and not rout and not arrete.isMaritime() and (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.ROUTE,bdd)):
            jcol1 = Colonie.getColonieJoueur(arrete.int1,bdd)
            jcol2 = Colonie.getColonieJoueur(arrete.int2,bdd)
            if (jcol1 == j.num) or (jcol2 == j.num):
                return True
            for a in arrete.neighb():
                jrout = Route.getRouteJoueur(a,bdd)
                if (jrout == j.num):
                    return True
        return False

    @staticmethod
    def construire_route(j,arrete, construction_route = False, bdd = REDIS):
        ''' Pose, si c'est possible, une route du joueur j sur l'arrete et effectue le paiement.'''
        if Jeu.peut_construire_route(j,arrete, construction_route,bdd):
            r = Route(j.num,arrete)
            terre = arrete.getTerre()
            if not construction_route:
                j.payer(terre,Tarifs.ROUTE,bdd)
            r.save(bdd)
            j.recalcul_route_la_plus_longue(terre,bdd)
            Jeu.challenge_route_la_plus_longue(j,terre,bdd)
            return True
        else:
            return False

    @staticmethod
    def peut_evoluer_colonie(j, intersection, bdd = REDIS):
        ''' Un joueur j peut faire evoluer une colonie si il n'est pas en ruine, si elle est a lui et si il peyt payer le cout de l'évolution'''
        colonie = Colonie.getColonie(intersection,bdd)
        if colonie == 0:
            return False
        return not j.getEnRuine(bdd) and not colonie.isVille and colonie.joueur == j.num and j.peut_payer(intersection.getTerre(), Tarifs.VILLE,bdd)

    @staticmethod
    @protection
    def evoluer_colonie(j,intersection, bdd = REDIS):
        ''' Evolue si c'est possible la colonie, via le joueur j et effectue le paiement'''
        colonie = Colonie.getColonie(intersection,bdd)
        colonie.evolue()
        terre = intersection.getTerre()
        j.payer(terre,Tarifs.VILLE,bdd)
        j.addStaticPoints(terre,1,bdd)
        colonie.save(bdd)
    
    @staticmethod
    def peut_recolter_ressources(des, bdd = REDIS):
        ''' On peut lancer la récolte des réssources si les dés sont entre 2 et 12'''
        if des < 2 or des == 7 or des > 12:
            return False
        else:
            return True

    @staticmethod
    @protection
    def recolter_ressources(des, bdd = REDIS):
        ''' Effectue pour tous les joueurs sur toutes les terres la récolte des ressources sauf s'ils sont en ruine'''
        for j in Jeu.get_all_joueurs(bdd):
            if not j.getEnRuine(bdd): 
                j.recolter_ressources(des,bdd)
    
    @staticmethod
    def peut_acheter_ressource(j,terre,carte, bdd = REDIS):
        ''' Un joueur j sur cette terre peut acheter contre un lingot d'or une carte de type carte, si il n'est pas en ruien, si il possède au moins un lingot et si carte est une carte de ressource'''
        return not j.getEnRuine(bdd) and j.aColoniseTerre(terre,bdd) and j.getOr(terre,bdd) > 0 and carte.est_ressource() and carte.size() == 1 and carte.est_physiquement_possible()

    @staticmethod
    @protection
    def acheter_ressource(j,terre, carte, bdd = REDIS):
        ''' Effectue via le joueur j sur cette terre l'achat de cette carte si il est possible'''
        j.payerOr(terre,bdd)
        j.recevoir(terre,carte,bdd)

# On suppose que chaque ile est separee d'au moins 2 arrete. Ca evite des ambiguites au niveau de la terre de construction.
    @staticmethod
    def peut_construire_bateau(j,arrete,construction_route = False, bdd = REDIS):
        ''' Le joueur j peut poser un bateau sur l'arrete si il n'est pas en ruine, et s'il l'arrete est maritime et s'il peyt payer ou s'il a joué une carte de développement construction de route, et si il existe une colonie cotiere voisine de l'arrete.'''
        terre = arrete.getTerre()
        # Si l'arrete n'a pas de terre, elle n'est surement pas reliée à la terre
        if terre == 0:
            return False
        if not j.getEnRuine(bdd) and arrete.isMaritimeOuCotier() and (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.BATEAU_TRANSPORT,bdd)):
            col1 = Colonie.getColonie(arrete.int1,bdd)
            col2 = Colonie.getColonie(arrete.int2,bdd)
            if (col1 != 0 and col1.joueur == j.num) or (col2 != 0 and col2.joueur == j.num):
                return True
        return False
    
    @staticmethod
    def construire_bateau(j,arrete, construction_route = False, bdd = REDIS):
        ''' Pose, si c'est possible un bateau du joueur j sur l'arrete et effectue le paiement.'''
        if Jeu.peut_construire_bateau(j,arrete, construction_route,bdd):
            i = bdd.get('lastBateauId')
            if i == None:
                i = 1
                bdd.set('lastBateauId',1)
            b = Bateau(i,j.num,arrete,Cartes.RIEN,Bateau.BateauType.TRANSPORT,False)
            if not construction_route:
                j.payer(arrete.getTerre(),Tarifs.BATEAU_TRANSPORT,bdd)

            b.save(bdd)
            bdd.incr('lastBateauId')
            return True
        else:
            return False
    

    @staticmethod
    def peut_deplacer_bateau(j,bateau,arrete, bdd = REDIS):
        ''' Le joueur j peut déplacer un bateau sur une arrete, si il n'est pas en ruine, si le bateau appartient à ce joueur, si le bateau n'est pas abordé par un bateau pirate, si il souhaite se déplacer sur une arrete maritime, si cette arrete est voisine de la position actuelle du bateau ou a 2 déplacements pour un voillier, et si ce bateau n'a pas déjà bougé'''
        if bateau == 0:
            return False
        return not j.getEnRuine(bdd) and bateau.joueur == j.num and not Voleur.est_pirate(bateau.position,bdd) and arrete.isMaritimeOuCotier() and (arrete in bateau.position.neighb() or (bateau.etat == Bateau.BateauType.VOILIER and arrete in bateau.position.doubleNeighb() )) and not bateau.aBouge
    
    @staticmethod
    @protection
    def deplacer_bateau(j,bateau,arrete, bdd = REDIS):
        ''' Déplace si c'est possible le bateau via le joueur j sur l'arrete'''
        bateau.deplacer(arrete)
        bateau.aBouge = True
        bateau.save(bdd)

    @staticmethod
    def peut_echanger_bateau(j,bateau,ct,cb, bdd = REDIS):
        ''' Le joueur j peut échanger avec ce bateau ct cartes de la terre où se trouve le bataeu vers le bateau et cb cartes du bateau vers la terre si il n'est pas en ruine, si le bateau appartient au joueur, si le bateau est sur une zone d'échange (colonie cotiere ou port), si il a assez de ressource sur la terre et dans le bateau et si les échanges sont des nombres entiers naturels.'''
        return not j.getEnRuine(bdd) and j.num == bateau.joueur and bateau.en_position_echange(bdd) and j.peut_payer(bateau.position.getTerre(), ct,bdd) and bateau.peut_recevoir_et_payer(ct,cb) and ct.est_physiquement_possible() and cb.est_physiquement_possible()

    @staticmethod
    @protection
    def echanger_bateau(j,bateau,ct,cb, bdd = REDIS):
        ''' Echange si c'est possible des cartes entre la cargaison du bateau et la main de j sur la terre où se trouve le bateau, ct cartes depuis la terre vers le bateau et cb depuis le bateau'''
        terre = bateau.position.getTerre()
        j.payer(terre,ct,bdd)
        j.recevoir(terre,cb,bdd)
        bateau.remove(cb)
        bateau.append(ct)
        bateau.save(bdd)
    
    @staticmethod
    def peut_evoluer_bateau(j,bateau, bdd = REDIS):
        ''' Le joueur j peut faire evoluer le bateau si il n'est pas en ruine, si le bateau est a lui, si le bateau est en zone d'échange, si le bateau n'est pas un voilier et si il peut payer l'évolution.'''
        return not j.getEnRuine(bdd) and j.num == bateau.joueur and bateau.en_position_echange(bdd) and ((bateau.etat == Bateau.BateauType.TRANSPORT and j.peut_payer(bateau.position.getTerre(), Tarifs.CARGO,bdd)) or (bateau.etat == Bateau.BateauType.CARGO and j.peut_payer(bateau.position.getTerre(), Tarifs.VOILIER,bdd)))

    
    @staticmethod
    @protection
    def evoluer_bateau(j,bateau, bdd = REDIS):
        ''' Evolue, si c'est possible le bateau via le joueur j et effectue le paiement'''
        terre = bateau.position.getTerre()
        if(bateau.etat == Bateau.BateauType.TRANSPORT):
            bateau.evolue()
            j.payer(terre,Tarifs.CARGO,bdd)
            bateau.save(bdd)
        elif bateau.etat == Bateau.BateauType.CARGO :
            bateau.evolue()
            j.payer(terre,Tarifs.VOILIER,bdd)
            bateau.save(bdd)
        else:
            return False

    @staticmethod
    def peut_acheter_carte_developpement(j,terre, bdd = REDIS):
        ''' Un joueur j peut acheter une carte de développement sur la terre si il peut la payer'''
        return not j.getEnRuine(bdd) and j.aColoniseTerre(terre,bdd) and j.peut_payer(terre,Tarifs.DEVELOPPEMENT,bdd)
   
    @staticmethod
    @protection 
    def acheter_carte_developpement(j,terre, bdd = REDIS):
        ''' Pioche pour le joueur j sur cette terre, une carte de développement si c'est possible, et effectue le paiement.'''
        j.payer(terre,Tarifs.DEVELOPPEMENT,bdd)
        return j.piocher_developpement(terre,bdd)

    @staticmethod
    def peut_coloniser(j,bateau,position,transfert, bdd = REDIS):
        if not j.getEnRuine(bdd) and j.num == bateau.joueur and transfert.est_physiquement_possible() and transfert <= (bateau.cargaison-Tarifs.COLONIE) and Tarifs.COLONIE <= bateau.cargaison and position.isTerrestreOuCotier() and not j.aColoniseTerre(position.getTerre(),bdd):
            col = Colonie.getColonie(position,bdd)
            if col != 0:
                return False
            for i in position.neighb():
                col = Colonie.getColonie(i,bdd)
                if col != 0:
                    return False
            return position in bateau.positions_colonisables()
        else:
            return False


    @staticmethod
    @protection
    def coloniser(j,bateau,position,transfert, bdd = REDIS):
            Colonie(j.num,position).save(bdd)
            terre = position.getTerre()
            j.addTerre(terre,bdd)
            j.addStaticPoints(terre,1,bdd)
            j.recevoir(terre,transfert,bdd)
            bateau.remove(Tarifs.COLONIE + transfert)
            bateau.save(bdd)

    @staticmethod
    def peut_echanger(j1,j2,terre,c1,c2, bdd = REDIS):
        ''' Le joueur j1 peut echanger avec le joueur j2 sur la terre, des cartes c1 du joueur j1 vers j2 et c2 du joueur j2 vers j1 si aucun joueur n'est en ruine, si sur cette terre ils peuvent payer cette somme, si c1 et c2 sont des entiers naturels, et uniquement des ressources (pas carte de développement), '''
        return not j1.getEnRuine(bdd) and not j2.getEnRuine(bdd) and j1.aColoniseTerre(terre,bdd) and j2.aColoniseTerre(terre,bdd) and j1.peut_payer(terre,c1,bdd) and j2.peut_payer(terre,c2,bdd) and c1.est_ressource() and c2.est_ressource() and c1.est_physiquement_possible() and c2.est_physiquement_possible()

    @staticmethod
    @protection
    def echanger(j1,j2,terre,c1,c2, bdd = REDIS):
        ''' Effectue si il est possible un échange de cartes entre j1 et j2 sur cette terre, avec j1 donnant c1 cartes et j2 donnant c2 cartes.'''
        j1.payer(terre,c1,bdd)
        j1.recevoir(terre,c2,bdd)
        j2.payer(terre,c2,bdd)
        j2.recevoir(terre,c1,bdd)
    
    @staticmethod
    def peut_echanger_classique(j,terre,t1,t2, bdd = REDIS):
        ''' Un joueur j peut effectuer un echange classique (4 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a colonisé la terre et si il peut payer 4 cartes de t1'''
        return not j.getEnRuine(bdd) and t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.aColoniseTerre(terre,bdd) and j.peut_payer(terre,t1*4,bdd)

    @staticmethod
    @protection
    def echanger_classique(j,terre,t1,t2, bdd = REDIS):
        ''' Effectue s'il est possible un échange classique de cartes (4 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*4,bdd)
        j.recevoir(terre,t2,bdd)
    
    @staticmethod
    def peut_echanger_commerce_tous(j,terre,t1,t2, bdd = REDIS):
        ''' Un joueur j peut effectuer un echange de commerce '?' (3 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce de type '?' et si il peut payer 3 cartes de t1'''

        return not j.getEnRuine(bdd) and t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and j.aColoniseTerre(terre,bdd) and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.peut_payer(terre,t1*3,bdd) and j.contient_commerce_utilisable(terre,CommerceType.TOUS,bdd)
    
    @staticmethod
    @protection
    def echanger_commerce_tous(j,terre,t1,t2, bdd = REDIS):
        ''' Effectue s'il est possible un échange commerce '?' de cartes (3 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*3,bdd)
        j.recevoir(terre,t2,bdd)
    
    @staticmethod
    def peut_echanger_commerce(j,terre,t1,t2, bdd = REDIS):
        ''' Un joueur j peut effectuer un echange de commerce spécialisé (2 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce spécialisé en le type t1 et si il peut payer 2 cartes de t1'''
        if not j.getEnRuine(bdd) and t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and j.aColoniseTerre(terre,bdd) and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.peut_payer(terre,t1*2,bdd):
            if t1 == Cartes.ARGILE:
                comType = CommerceType.ARGILE
            elif t1 == Cartes.BOIS:
                comType = CommerceType.BOIS
            elif t1 == Cartes.BLE:
                comType = CommerceType.BLE
            elif t1 == Cartes.CAILLOU:
                comType = CommerceType.CAILLOU
            elif t1 == Cartes.MOUTON:
                comType = CommerceType.MOUTON
            else:
                comType = 0
            
            return j.contient_commerce_utilisable(terre,comType,bdd)
        return False
    
    @staticmethod
    @protection
    def echanger_commerce(j,terre,t1,t2, bdd = REDIS):
        ''' Effectue s'il est possible un échange de commerce spécialisé de cartes (2 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*2,bdd)
        j.recevoir(terre,t2,bdd)


    @staticmethod
    def peut_jouer_decouverte(joueur,terre,cartes, bdd = REDIS):
        return not joueur.getEnRuine(bdd) and Cartes.DECOUVERTE <= joueur.getCartes(terre,bdd) and joueur.aColoniseTerre(terre,bdd) and cartes.size() == 2 and cartes.est_ressource() and cartes.est_physiquement_possible()

    @staticmethod
    @protection
    def jouer_decouverte(joueur,terre,cartes, bdd = REDIS):
            joueur.recevoir(terre,cartes,bdd)
            joueur.payer(terre,Cartes.DECOUVERTE,bdd)

    @staticmethod
    def peut_jouer_monopole(joueur,terre,t1, jvols, bdd = REDIS):
        if joueur.getEnRuine(bdd):
            return False
        b = Cartes.MONOPOLE <= joueur.getCartes(terre,bdd) and joueur.aColoniseTerre(terre,bdd) and t1.est_ressource() and t1.size() == 1 and t1.est_physiquement_possible() and len(jvols) <= 3 and not joueur in jvols

        for j in jvols:
            b = b and j.aColoniseTerre(terre,bdd) and not j.getEnRuine(bdd)

        return b

    @staticmethod
    @protection
    def jouer_monopole(joueur,terre,t1,jvols, bdd = REDIS):
        i = 0
        for j in jvols:
            r =  j.getCartes(terre,bdd).get_cartes_de_type(t1)
            i += r
            j.payer(terre,t1*r,bdd)
        joueur.recevoir(terre,t1*i,bdd)


    @staticmethod
    def peut_jouer_construction_routes(joueur,terre,isFirstRoute,a1,isSecondRoute,a2, bdd = REDIS):


        return not joueur.getEnRuine(bdd) and a1 != a2 and Cartes.CONSTRUCTION_ROUTES <= joueur.getCartes(terre,bdd) and joueur.aColoniseTerre(terre,bdd) and (a1.getTerre() == terre or a1.int1.getTerre() == terre or a1.int2.getTerre() == terre) and (a2.getTerre() == terre or a2.int1.getTerre() == terre or a2.int2.getTerre() == terre) and ((isFirstRoute and a1.isTerrestreOuCotier() and Jeu.peut_construire_route(joueur,a1,True,bdd)) or (not(isFirstRoute) and a1.isMaritimeOuCotier() and Jeu.peut_construire_bateau(joueur,a1,True,bdd))) and ((isSecondRoute and a2.isTerrestreOuCotier() and Jeu.peut_construire_route(joueur,a2,True,bdd)) or (not(isSecondRoute) and a2.isMaritimeOuCotier() and Jeu.peut_construire_bateau(joueur,a2,True,bdd))) and ((isFirstRoute and a1.isTerrestreOuCotier() and Jeu.peut_construire_route(joueur,a1,True,bdd)) or (not(isFirstRoute) and a1.isMaritimeOuCotier() and Jeu.peut_construire_bateau(joueur,a1,True,bdd))) and ((isSecondRoute and a2.isTerrestreOuCotier() and Jeu.peut_construire_route(joueur,a2,True,bdd)) or (not(isSecondRoute) and a2.isMaritimeOuCotier() and Jeu.peut_construire_bateau(joueur,a2,True,bdd)))

    @staticmethod
    @protection
    def jouer_construction_routes(joueur,terre,isFirstRoute,a1,isSecondRoute,a2, bdd = REDIS):
        joueur.payer(terre,Cartes.CONSTRUCTION_ROUTES,bdd)
        if isFirstRoute:
            Jeu.construire_route(joueur,a1,True,bdd)
        else:
            Jeu.construire_bateau(joueur,a1,True,bdd)
        if isSecondRoute:
            Jeu.construire_route(joueur,a2,True,bdd)
        else:
            Jeu.construire_bateau(joueur,a2,True,bdd)

    @staticmethod
    def peut_defausser(joueur,terre,cartes, bdd = REDIS):
        if not joueur.getEnRuine(bdd) and 7 in Des.getDices(bdd) and joueur.aColoniseTerre(terre,bdd):
            c = joueur.getCartes(terre,bdd)
            rs = c.ressources_size()


            bs = []
            for bn in joueur.getBateaux(bdd):
                b = Bateau.getBateau(int(bn),bdd)
                if b.est_proche(terre):
                    bs.append(b.num)
                    rs += b.cargaison.ressources_size()
            if rs <= 7:
                return cartes == (Cartes.RIEN,[])
            
            res = cartes[0]
            cargs = cartes[1]

            ds = rs/2 + rs%2 # ressource arrondi au superieur
            rs2 = rs - ds

            while rs2 > 7:
                ds += rs2/2 + rs2%2 # ressource arrondi au superieur
                rs2 = rs - ds
            if res <= c and res.est_ressource() and res.est_physiquement_possible():
                ss = res.ressources_size()
                for cb in cargs:
                    if cb[0].num in bs and cb[1] <= cb[0].cargaison and cb[1].est_physiquement_possible() and cb[1].est_ressource():
                        ss += cb[1].ressources_size()
                    else:
                        return False
                return ss == ds
        return False

    @staticmethod
    @protection
    def defausser(joueur,terre,cartes, bdd = REDIS):
        joueur.payer(terre,cartes[0],bdd)
        for cb in cartes[1]:
            cb[0].remove(cb[1])
            cb[0].save(bdd)

    
    @staticmethod
    def positions_possibles_voleur(joueur,terre,voleur, bdd = REDIS):
        if voleur == 0:
            return []
        b = voleur.etat == Voleur.VoleurType.PIRATE
        if not b:
            hexs = terre.hexagones[:]
        else:
            hexs = terre.espaceMarin[:]
        if voleur.position != 0:
            hexs.remove(voleur.position)
        possibilite = []
        if b:
            for h in hexs:
                if h.commerceType!= 0:
                    for i in h.ints:
                        col = Colonie.getColonie(i,bdd)
                        if (col != 0) and (col.joueur != joueur.num):
                            possibilite.append((h,col.joueur))
                for a in h.liens:
                    for bat in Bateau.getBateaux(a,bdd):
                        if (bat != 0) and (bat.joueur != joueur.num):
                            possibilite.append((h,bat.joueur))
            if possibilite == []:
                return [(0,0)]
        else:
            for h in hexs:
                for i in h.ints:
                    col = Colonie.getColonie(i,bdd)
                    if (col != 0) and (col.joueur != joueur.num):
                            possibilite.append((h,col.joueur))
            if possibilite == []:
                for h in voleur.position.terre.hexagones:
                    if h.etat == HexaType.DESERT and h.commerceType == 0:
                        possibilite.append((h,0))
        return possibilite 



    @staticmethod
    def peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,chevallier = False, bdd = REDIS):
        if not joueur.getEnRuine(bdd) and (joueur.get_deplacement_voleur(terre,bdd) or chevallier) and (hex == 0 or hex.terre == terre):
            if voleurType == Voleur.VoleurType.BRIGAND:
                voleur = Voleur.getBrigand(terre,bdd)
            else:
                voleur = Voleur.getPirate(terre,bdd)
            if jvol == 0:
                t = (hex, 0)
            else:
                t = (hex, jvol.num)
            return joueur.aColoniseTerre(terre,bdd) and t in Jeu.positions_possibles_voleur(joueur,terre,voleur,bdd)
        return False

    @staticmethod
    def voler(j1,terre,j2, bdd = REDIS):
        ressources_terrestres = j2.getCartes(terre,bdd)
        nc = ressources_terrestres.ressources_size()
        ressources_bateaux = []
        s = nc
        for bn in j2.getBateaux(bdd):
            b = Bateau.getBateau(int(bn),bdd)
            if b.en_position_echange(bdd) and b.position.getTerre() == terre:
                n = b.cargaison.size()
                ressources_bateaux.append((n,b))
                s+=n
        if s == 0:
            return
        u = random.randint(1,s)
        if u <= nc:
            c = ressources_terrestres.carte(u)
            j2.payer(terre,c,bdd)
            j1.recevoir(terre,c,bdd)
        else:
            u-=nc
            for rb in ressources_bateaux:
                if u <= rb[0]:
                    c = rb[1].cargaison.carte(u)
                    rb[1].remove(c)
                    rb[1].save(bdd)
                    j1.recevoir(terre,c,bdd)
                    return
                else:
                    u -= rb[0]

    @staticmethod
    def deplacer_voleur(joueur,terre,voleurType,hex,jvol, chevallier = False, bdd = REDIS):
        if Jeu.peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,chevallier,bdd):
            if voleurType == Voleur.VoleurType.BRIGAND:
                voleur = Voleur.getBrigand(terre,bdd)
            else:
                voleur = Voleur.getPirate(terre,bdd)
            voleur.deplacer(hex)
            voleur.save(bdd)
            Jeu.voler(joueur,terre,jvol,bdd)
            if not chevallier:
                joueur.set_deplacement_voleur(terre,False,bdd)
            return True
        else:
            return False
                
    @staticmethod
    def peut_jouer_chevallier(joueur,terre,voleurType, hex,jvol, bdd = REDIS):
        return not joueur.getEnRuine(bdd) and Cartes.CHEVALLIER <= joueur.getCartes(terre,bdd) and joueur.aColoniseTerre(terre,bdd) and Jeu.peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,True,bdd)

    @staticmethod
    @protection
    def jouer_chevallier(joueur,terre,voleurType, hex,jvol, bdd = REDIS):
            joueur.add_chevallier(terre,bdd)
            joueur.payer(terre,Cartes.CHEVALLIER,bdd)
            Jeu.challenge_armee_la_plus_grande(joueur,terre,bdd)
            Jeu.deplacer_voleur(joueur,terre,voleurType,hex,jvol,True,bdd)


if __name__ == '__main__':
    j = Joueur("1")
