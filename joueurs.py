# *-* coding: iso-8859-1 *-*
from constructions import *
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

class Joueur:
    ''' Classe représentant un joueur, avec ses pions (construction, bateau), permettant de récupérer les informations relatives à ce joueur, voire d'en modifier.'''
    def __init__(self,num):
        self.num = num
        self.deplacement_voleur = []
        self.routes_les_plus_longues = []
        self.enRuine = False

    def setCartes(self,terre,cartes):
        ''' Associe à la main du joueur sur cette terre les cartes données en paramètre'''
        cartes.setTo('J'+str(self.num)+':T'+str(terre.num))

    def getCartes(self,terre):
        ''' Renvoie la main du joueur sur cette terre'''
        return CartesGeneral.get('J'+str(self.num)+':T'+str(terre.num))
    
    def payer(self,terre, cartes):
        ''' Déduis de la main du joueur sur cette terre les cartes données en paramètre'''
        self.setCartes(terre,self.getCartes(terre) - cartes)

    def recevoir(self,terre,cartes):
        ''' Ajoute à la main du joeuur sur cette terre les cartes données en paramètre'''
        self.payer(terre,cartes*(-1))

    def peut_payer(self,terre,cartes):
        ''' Vérifie si la main du joeuur sur cette terre peut payer la quantité donnée en paramètre'''
        return cartes <= self.getCartes(terre)
    
    def ressource_aleatoire(self,terre):
        ''' Ajoute à la main du joueur sur cette terre une carte de ressource aléatoire'''
        carte = CartesRessources.get_random_ressource()
        self.setCartes(terre,self.getCartes(terre) + carte)

    def getOr(self,terre):
        ''' Renvoie la quantité d'or du joueur présente sur cette terre'''
        return int(REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':or'))

    def setOr(self,terre, nb):
        ''' Définit la quantité d'or du joueur présente sur cette terre'''
        REDIS.set('J'+str(self.num)+':T'+str(terre.num)+':or', nb)

    def addOr(self,terre,nb):
        ''' Ajoute au stock d'or du joeuur sur cette terre nb lingots d'or'''
        self.setOr(terre, self.getOr(terre) + nb)

    def payerOr(self,terre):
        ''' Déduis du stock d'or du joueur sur cette terre un lingot d'or'''
        self.addOr(terre,-1)

    def aColoniseTerre(self,terre):
        return REDIS.sismember('J'+str(self.num)+':terres', terre.num)
    
    def addTerre(self,terre):
        ''' Ajoute une terre aux terres colonisées du joueur'''
        REDIS.sadd('J'+str(self.num)+':terres',terre.num)
        self.setCartes(terre,Cartes.RIEN)
        self.setOr(terre,0)
        REDIS.set('J'+str(self.num)+':T'+str(terre.num)+':chevalliers',0)



    def piocher_developpement(self, terre):
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
        self.recevoir(terre,carte)
        return carte

    def contient_commerce_utilisable(self,terre,comType):
        ''' Vérifie si le joueur contient sur cette terre un commerce de type comType'''
        for c in self.getBatiments():
            c = int(c)
            intersection = Plateau.getPlateau().it(c)
            ms = intersection.marcheNonBrigande()
            ps = intersection.portNonPirate()
            if ms != 0:
                for m in ms:
                    if m.commerceType == comType:
                        return True
            if ps != 0:
                for p in ps:
                    if p.commerceType == comType:
                        return True
        return False


    def recolter_ressources(self,des):
        ''' Récolte les ressources du joueur en fonction du lancé de dés, sur toutes les terres'''
        for c in self.getBatiments():
            c = int(c)
            it = Plateau.getPlateau().it(c)
            terre = it.getTerre()
            res = Colonie.getColonie(it).ressources_from_past(des)
            if (res != 0):
                self.addOr(terre,res[1])
                self.recevoir(terre,res[0]) 

    def getBateaux(self):
        ''' Renvoie les identifiants des bateaux du joueur, tout type confondu'''
        return self.getBateauxTransport() + self.getCargos() + self.getVoiliers()
    
    def getBateauxTransport(self):
        return REDIS.smembers('J'+str(self.num)+':transports')

    def getCargos(self):
        return REDIS.smembers('J'+str(self.num)+':cargos')
    
    def getVoiliers(self):
        return REDIS.smembers('J'+str(self.num)+':voiliers')
    
    
    def getBateauxTransportPositions(self):
        ''' Renvoie les arretes où se trouvent les bateaux du joueur, tout type confondu'''
        return REDIS.smembers('J'+str(self.num)+':transports:positions')

    def getCargosPositions(self):
        return REDIS.smembers('J'+str(self.num)+':cargos:positions')
    
    def getVoiliersPositions(self):
        return REDIS.smembers('J'+str(self.num)+':voiliers:positions')
    
    def getBateauxPositions(self):
        ''' Renvoie les bateaux du joueur, tout type confondu'''
        return self.getBateauxTransportPositions() + self.getCargosPositions() + self.getVoiliersPositions()

    def getColonies(self):
        ''' Renvoie tous les intersection où se trouvent les colonies du joueur'''
        return REDIS.smembers('J'+str(self.num)+':colonies')

    def getVilles(self):
        ''' Renvoie tous les intersection où se trouvent les villes du joueur'''
        return REDIS.smembers('J'+str(self.num)+':villes')
    
    def getRoutes(self):
        ''' Renvoie tous les arretes où se trouvent les routes du joueur'''
        return REDIS.smembers('J'+str(self.num)+':routes')

    def getBatiments(self):
        ''' Renvoie toutes les intersection où se trouvent les batiments du joueur, tout type confondu'''
        return self.getColonies().union(self.getVilles())
    
    def set_chevalliers(self,terre, nb):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        REDIS.set('J'+str(self.num)+':T'+str(terre.num)+':armee', nb)
                 
    def add_chevallier(self,terre):
        ''' Ajoute un chevallier à l'armée du joueur sur cette terre'''
        return int(REDIS.incr('J'+str(self.num)+':T'+str(terre.num)+':armee'))
 
    def get_chevalliers(self,terre):
        ''' Renvoie l'armée du joueur sur cette terre'''
        return int(REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':armee'))
    
    def get_carte_armee_la_plus_grande(self,terre):
        ''' Renvoie vrai si le joueur a l'armée la plus grande sur cette terre'''
        u = Jeu.get_armee_la_plus_grande(terre)
        return u!=0 and u[0] == self
 
    def get_deplacement_voleur(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.deplacement_voleur[i]
        else:
            return 0

    def get_deplacement_voleur(self,terre):
        ''' Renvoie si oui ou non, le joueur doit déplacer le voleur dans la journée sur cette terre.'''
        return (REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':deplacementVoleur') == 'True')

    def set_deplacement_voleur(self,terre,dep):
        ''' Définie si oui ou non, le joueur doit déplacer le voleur dans la journée sur cette terre.'''
        REDIS.set('J'+str(self.num)+':T'+str(terre.num)+':deplacementVoleur', False)


    def get_route_la_plus_longue(self,terre):
        ''' Renvoie la taille de la route la plus longue du joueur sur cette terre'''
        return int(REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':rlpl'))
 
    def set_route_la_plus_longue(self,terre, l):
        ''' Définie la route la plus longue sur cette terre comme étant de taille l'''
        REDIS.set('J'+str(self.num)+':T'+str(terre.num)+':rlpl',l)

    def recalcul_route_la_plus_longue(self,terre):
        ''' Calcule la route la plus longue de ce joueur sur cette terre. Si elle est déjà calculée alors renvoie juste la valeur déjà calculée '''
        if self.aColoniseTerre(terre):
                i = 0
                for ar in self.getRoutes():
                    ar = Plateau.getPlateau().ar(int(ar))
                    r = Route.getRoute(ar)
                    if ar.getTerre() == terre and r.est_extremite():
                        i = max(i, r.rlplfr())
                self.set_route_la_plus_longue(terre,i)
                       
    def get_carte_route_la_plus_longue(self,terre):
        ''' Vérifie si ce joueur a la carte de la route al plus longue sur cette terre'''
        u = Jeu.get_route_la_plus_longue(terre)
        return u!=0 and u[0]== self

    def addStaticPoints(self,terre,nb):
        ''' Ajoute nb points aux points statiques (ie batiments) de cette terre'''
        REDIS.incr('J'+str(self.num)+':T'+str(terre.num)+':points',nb)

    def getStaticPoints(self,terre):
        return int(REDIS.get('J'+str(self.num)+':T'+str(terre.num)+':points'))
    
    def setStaticPoints(self,terre, nb):
        REDIS.set('J'+str(self.num)+':T'+str(terre.num)+':points', nb)

    def getPoints(self,terre):
        ''' Calcule le nombre de points de ce joueur sur cette terre'''
        if self.enRuine:
            return 0
        i = self.getTerreIndex(terre)
        p = 0
        if (self.get_carte_route_la_plus_longue(terre)):
            p += 2
        if (self.get_carte_armee_la_plus_grande(terre)):
            p += 2
        if i!=-1:
            return self.getStaticPoints(terre) + self.getCartes(terre).get_cartes_de_type(Cartes.POINT_VICTOIRE) + p

    def addRoot(self):
        return ForetAction.setNewRoot(self) 
    
    def addFirstRoot(self):
        return ForetAction.setNewFirstRoot(self) 

    def addNextRoot(self,root):
        return ForetAction.setNewNextRoot(root,self) 

class Jeu:

# -----------------------------------------------------
#    Actions dans la journee
# -----------------------------------------------------

    @staticmethod
    def get_all_joueurs():
        i = int(REDIS.get('NombreJoueurs'))
        joueurs = []
        for j in xrange(i):
            joueurs.append(Joueur(j+1))
        return joueurs

    @staticmethod
    def peut_construire_colonie(j,intersection):
        ''' Un joueur peut construire une colonie si il n'est aps en ruine, si il ne la construit pas a un emplacement voisin d'une autre colonie, si il la construit sur un emplacement voisin d'une de ses routes, si cet emplacement est sur terre et si il peut payer la construiction.'''
        col = intersection.hasColonie()
        if not j.enRuine and not col and not intersection.isMaritime() and j.peut_payer(intersection.getTerre(), Tarifs.COLONIE):
    
            for i in intersection.neigh:
                if i.hasColonie():
                    return False
            for i in intersection.neigh:
                a = i.lien(intersection)
                jrout = a.getRouteJoueur()
                if jrout == j.num:
                    return True
        return False

    @staticmethod
    @protection
    def construire_colonie(j, intersection):
        ''' Pose une nouvelle colonie du joueur j sur l'intersection si il en a la possibilité, et effectue le paiement.'''
        c = Colonie(j.num, intersection)
        terre = intersection.getTerre()
        j.payer(terre, Tarifs.COLONIE)
        j.addStaticPoints(terre,1)

        c.save()
        print "yahoo"
        for jj in Jeu.get_all_joueurs():
            print "--->", jj.num, str(jj.get_route_la_plus_longue(terre))
            jj.recalcul_route_la_plus_longue(terre)
            print jj.get_route_la_plus_longue(terre), "<---"


    @staticmethod
    def peut_construire_route(j, arrete, construction_route = False):
        ''' Un joueur j peut construire une route sur l'arrete si il n'est pas en ruine, si il n'existe pas déjà de route non en ruine sur cet emplacement, si cette arrete est terrestre, si il peut payer ou s'il a jouer une carte développement de construction de route, et s'il existe une colonie ou une route voiine à cette arrete.'''
        rout = arrete.hasRoute()
        if not j.enRuine and not rout and not arrete.isMaritime() and (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.ROUTE)):
            jcol1 = arrete.int1.getColonieJoueur()
            jcol2 = arrete.int2.getColonieJoueur()
            if (jcol1 == j.num) or (jcol2 == j.num):
                return True
            for a in arrete.neighb():
                jrout = a.getRouteJoueur()
                if (jrout == j.num):
                    return True
        return False

    @staticmethod
    def construire_route(j,arrete, construction_route = False):
        ''' Pose, si c'est possible, une route du joueur j sur l'arrete et effectue le paiement.'''
        if construction_route or Jeu.peut_construire_route(j,arrete):
            r = Route(j.num,arrete)
            terre = arrete.getTerre()
            if not construction_route:
                j.payer(terre,Tarifs.ROUTE)
            r.save()
            j.recalcul_route_la_plus_longue(terre)
            return True
        else:
            return False

    @staticmethod
    def peut_evoluer_colonie(j, intersection):
        ''' Un joueur j peut faire evoluer une colonie si il n'est pas en ruine, si elle est a lui et si il peyt payer le cout de l'évolution'''
        colonie = Colonie.getColonie(intersection)
        if colonie == 0:
            return False
        return not j.enRuine and not colonie.isVille and colonie.joueur == j.num and j.peut_payer(intersection.getTerre(), Tarifs.VILLE)

    @staticmethod
    @protection
    def evoluer_colonie(j,intersection):
        ''' Evolue si c'est possible la colonie, via le joueur j et effectue le paiement'''
        colonie = Colonie.getColonie(intersection)
        colonie.evolue()
        terre = intersection.getTerre()
        j.payer(terre,Tarifs.VILLE)
        j.addStaticPoints(terre,1)

        colonie.save()
    
    @staticmethod
    def peut_recolter_ressources(des):
        ''' On peut lancer la récolte des réssources si les dés sont entre 2 et 12'''
        if des < 2 or des == 7 or des > 12:
            return False
        else:
            return True

    @staticmethod
    @protection
    def recolter_ressources(des):
        ''' Effectue pour tous les joueurs sur toutes les terres la récolte des ressources sauf s'ils sont en ruine'''
        for j in Jeu.get_all_joueurs():
            if not j.enRuine: 
                j.recolter_ressources(des)
    
    @staticmethod
    def peut_acheter_ressource(j,terre,carte):
        ''' Un joueur j sur cette terre peut acheter contre un lingot d'or une carte de type carte, si il n'est pas en ruien, si il possède au moins un lingot et si carte est une carte de ressource'''
        return not j.enRuine and j.aColoniseTerre(terre) and j.getOr(terre) > 0 and carte.est_ressource() and carte.size() == 1 and carte.est_physiquement_possible()

    @staticmethod
    @protection
    def acheter_ressource(j,terre, carte):
        ''' Effectue via le joueur j sur cette terre l'achat de cette carte si il est possible'''
        j.payerOr(terre)
        j.recevoir(terre,carte)

# On suppose que chaque ile est separee d'au moins 2 arrete. Ca evite des ambiguites au niveau de la terre de construction.
    @staticmethod
    def peut_construire_bateau(j,arrete,construction_route = False):
        ''' Le joueur j peut poser un bateau sur l'arrete si il n'est pas en ruine, et s'il l'arrete est maritime et s'il peyt payer ou s'il a joué une carte de développement construction de route, et si il existe une colonie cotiere voisine de l'arrete.'''
        terre = arrete.getTerre()
        # Si l'arrete n'a pas de terre, elle n'est surement pas reliée à la terre
        if terre == 0:
            return False
        if not j.enRuine and arrete.isMaritimeOuCotier() and (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.BATEAU_TRANSPORT)):
            col1 = Colonie.getColonie(arrete.int1)
            col2 = Colonie.getColonie(arrete.int2)
            if (col1 != 0 and col1.joueur == j.num) or (col2 != 0 and col2.joueur == j.num):
                return True
        return False
    
    @staticmethod
    def construire_bateau(j,arrete, construction_route = False):
        ''' Pose, si c'est possible un bateau du joueur j sur l'arrete et effectue le paiement.'''
        if construction_route or Jeu.peut_construire_bateau(j,arrete):
            i = REDIS.get('lastBateauId')
            if i == None:
                i = 1
                REDIS.set('lastBateauId',1)
            b = Bateau(i,j.num,arrete,Cartes.RIEN,Bateau.BateauType.TRANSPORT,False)
            if not construction_route:
                j.payer(arrete.getTerre(),Tarifs.BATEAU_TRANSPORT)

            b.save()
            REDIS.incr('lastBateauId')
            return True
        else:
            return False
    

    @staticmethod
    def peut_deplacer_bateau(j,bateau,arrete):
        ''' Le joueur j peut déplacer un bateau sur une arrete, si il n'est pas en ruine, si le bateau appartient à ce joueur, si le bateau n'est pas abordé par un bateau pirate, si il souhaite se déplacer sur une arrete maritime, si cette arrete est voisine de la position actuelle du bateau ou a 2 déplacements pour un voillier, et si ce bateau n'a pas déjà bougé'''
        if bateau == 0:
            return False
        return not j.enRuine and bateau.joueur == j.num and not bateau.position.est_pirate() and arrete.isMaritimeOuCotier() and (arrete in bateau.position.neighb() or (bateau.etat == Bateau.BateauType.VOILIER and arrete in bateau.position.doubleNeighb() )) and not bateau.aBouge
    
    @staticmethod
    @protection
    def deplacer_bateau(j,bateau,arrete):
        ''' Déplace si c'est possible le bateau via le joueur j sur l'arrete'''
        bateau.deplacer(arrete)
        bateau.aBouge = True
        bateau.save()

    @staticmethod
    def peut_echanger_bateau(j,bateau,ct,cb):
        ''' Le joueur j peut échanger avec ce bateau ct cartes de la terre où se trouve le bataeu vers le bateau et cb cartes du bateau vers la terre si il n'est pas en ruine, si le bateau appartient au joueur, si le bateau est sur une zone d'échange (colonie cotiere ou port), si il a assez de ressource sur la terre et dans le bateau et si les échanges sont des nombres entiers naturels.'''
        return not j.enRuine and j.num == bateau.joueur and bateau.en_position_echange() and j.peut_payer(bateau.position.getTerre(), ct) and bateau.peut_recevoir_et_payer(ct,cb) and ct.est_physiquement_possible() and cb.est_physiquement_possible()

    @staticmethod
    @protection
    def echanger_bateau(j,bateau,ct,cb):
        ''' Echange si c'est possible des cartes entre la cargaison du bateau et la main de j sur la terre où se trouve le bateau, ct cartes depuis la terre vers le bateau et cb depuis le bateau'''
        terre = bateau.position.getTerre()
        j.payer(terre,ct)
        j.recevoir(terre,cb)
        bateau.remove(cb)
        bateau.append(ct)
        bateau.save()
    
    @staticmethod
    def peut_evoluer_bateau(j,bateau):
        ''' Le joueur j peut faire evoluer le bateau si il n'est pas en ruine, si le bateau est a lui, si le bateau est en zone d'échange, si le bateau n'est pas un voilier et si il peut payer l'évolution.'''
        return not j.enRuine and j.num == bateau.joueur and bateau.en_position_echange() and ((bateau.etat == Bateau.BateauType.TRANSPORT and j.peut_payer(bateau.position.getTerre(), Tarifs.CARGO)) or (bateau.etat == Bateau.BateauType.CARGO and j.peut_payer(bateau.position.getTerre(), Tarifs.VOILIER)))

    
    @staticmethod
    @protection
    def evoluer_bateau(j,bateau):
        ''' Evolue, si c'est possible le bateau via le joueur j et effectue le paiement'''
        terre = bateau.position.getTerre()
        if(bateau.etat == Bateau.BateauType.TRANSPORT):
            bateau.evolue()
            j.payer(terre,Tarifs.CARGO)
            bateau.save()
        elif bateau.etat == Bateau.BateauType.CARGO :
            bateau.evolue()
            j.payer(terre,Tarifs.VOILIER)
            bateau.save()
        else:
            return False

    @staticmethod
    def peut_acheter_carte_developpement(j,terre):
        ''' Un joueur j peut acheter une carte de développement sur la terre si il peut la payer'''
        return not j.enRuine and j.aColoniseTerre(terre) and j.peut_payer(terre,Tarifs.DEVELOPPEMENT)
   
    @staticmethod
    @protection 
    def acheter_carte_developpement(j,terre):
        ''' Pioche pour le joueur j sur cette terre, une carte de développement si c'est possible, et effectue le paiement.'''
        j.payer(terre,Tarifs.DEVELOPPEMENT)
        return j.piocher_developpement(terre)

    @staticmethod
    def peut_coloniser(j,bateau,position,transfert):
        if not j.enRuine and j.num == bateau.joueur and transfert.est_physiquement_possible() and transfert <= (bateau.cargaison-Tarifs.COLONIE) and Tarifs.COLONIE <= bateau.cargaison and position.isTerrestreOuCotier() and not j.aColoniseTerre(position.getTerre()):
            col = Colonie.getColonie(position)
            if col != 0:
                return False
            for i in position.neighb():
                col = Colonie.getColonie(i)
                if col != 0:
                    return False
            return position in bateau.positions_colonisables()
        else:
            return False


    @staticmethod
    @protection
    def coloniser(j,bateau,position,transfert):
            Colonie(j.num,position).save()
            terre = position.getTerre()
            j.addTerre(terre)
            j.setCartes(terre,Cartes.RIEN)
            j.setOr(terre,0)
            j.set_chevalliers(terre,0)
            j.set_route_la_plus_longue(terre,0)
            j.setStaticPoints(terre,1)
            j.set_deplacement_voleur(terre,False)
            j.recevoir(terre,transfert)
            bateau.remove(Tarifs.COLONIE + transfert)

    @staticmethod
    def peut_echanger(j1,j2,terre,c1,c2):
        ''' Le joueur j1 peut echanger avec le joueur j2 sur la terre, des cartes c1 du joueur j1 vers j2 et c2 du joueur j2 vers j1 si aucun joueur n'est en ruine, si sur cette terre ils peuvent payer cette somme, si c1 et c2 sont des entiers naturels, et uniquement des ressources (pas carte de développement), '''
        return not j1.enRuine and not j2.enRuine and j1.aColoniseTerre(terre) and j2.aColoniseTerre(terre) and j1.peut_payer(terre,c1) and j2.peut_payer(terre,c2) and c1.est_ressource() and c2.est_ressource() and c1.est_physiquement_possible() and c2.est_physiquement_possible()

    @staticmethod
    @protection
    def echanger(j1,j2,terre,c1,c2):
        ''' Effectue si il est possible un échange de cartes entre j1 et j2 sur cette terre, avec j1 donnant c1 cartes et j2 donnant c2 cartes.'''
        j1.payer(terre,c1)
        j1.recevoir(terre,c2)
        j2.payer(terre,c2)
        j2.recevoir(terre,c1)
    
    @staticmethod
    def peut_echanger_classique(j,terre,t1,t2):
        ''' Un joueur j peut effectuer un echange classique (4 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a colonisé la terre et si il peut payer 4 cartes de t1'''
        return not j.enRuine and t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.aColoniseTerre(terre) and j.peut_payer(terre,t1*4)

    @staticmethod
    @protection
    def echanger_classique(j,terre,t1,t2):
        ''' Effectue s'il est possible un échange classique de cartes (4 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*4)
        j.recevoir(terre,t2)
    
    @staticmethod
    def peut_echanger_commerce_tous(j,terre,t1,t2):
        ''' Un joueur j peut effectuer un echange de commerce '?' (3 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce de type '?' et si il peut payer 3 cartes de t1'''

        return not j.enRuine and t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and j.aColoniseTerre(terre) and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.peut_payer(terre,t1*3) and j.contient_commerce_utilisable(terre,CommerceType.TOUS)
    
    @staticmethod
    @protection
    def echanger_commerce_tous(j,terre,t1,t2):
        ''' Effectue s'il est possible un échange commerce '?' de cartes (3 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*3)
        j.recevoir(terre,t2)
    
    @staticmethod
    def peut_echanger_commerce(j,terre,t1,t2):
        ''' Un joueur j peut effectuer un echange de commerce spécialisé (2 cartes de t1 contre une carte de t2) sur cette terre si il n'est pas en ruine, si t1 et t2 sont des  cartes de ressources, si il a un commerce spécialisé en le type t1 et si il peut payer 2 cartes de t1'''
        if not j.enRuine and t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and j.aColoniseTerre(terre) and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.peut_payer(terre,t1*2):
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
            
            return j.contient_commerce_utilisable(terre,comType)
        return False
    
    @staticmethod
    @protection
    def echanger_commerce(j,terre,t1,t2):
        ''' Effectue s'il est possible un échange de commerce spécialisé de cartes (2 cartes de t1 contre 1carte de t2) sur cette terre, via le joueur j'''
        j.payer(terre,t1*2)
        j.recevoir(terre,t2)





if __name__ == '__main__':
    j = Joueur("1")
