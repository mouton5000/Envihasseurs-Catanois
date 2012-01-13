# *-* coding: iso-8859-1 *-*
from constructions import *
from plateau import *
from cartes import *
import random
import functools
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

    def __init__(self,num):
        self.num = num
        self.mains = []
        self.terres = []
        self.colonies = []
        self.villes = []
        self.routes = []
        self.bateaux_transport = []
        self.cargo = []
        self.voilier = []
        self.aur = []
        self.deplacement_voleur = []
        self.chevalliers = []
        self.routes_les_plus_longues = []
        self.points = []

    def getTerreIndex(self,terre):
        if terre in self.terres:
            return self.terres.index(terre)
        else:
             return -1

    def setCartes(self,terre,cartes):
        self.mains[self.getTerreIndex(terre)] = cartes

    def getCartes(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.mains[i]
        else:
            return Cartes.RIEN
    def addTerre(self,terre):
        self.terres.append(terre)
        self.mains.append(Cartes.RIEN)
        self.aur.append(0)

    def payer(self,terre, cartes):
        self.setCartes(terre,self.getCartes(terre) - cartes)

    def recevoir(self,terre,cartes):
        self.payer(terre,cartes*(-1))

    def peut_payer(self,terre,cartes):
        return cartes <= self.getCartes(terre)

    def piocher_developpement(self):
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
            carte = Cartes.CONSTRUCTION_ROUTE
        self.setCartes(terre,self.getCartes(terre) + carte)
        return carte

    def contient_commerce_utilisable(self,terre,comType):
        for c in self.getBatiments():
            m = c.position.marcheNonBrigande()
            p = c.position.portNonPirate()
            if (m != 0 and m.commerceType == comType):
                return True
            if (p != 0 and p.commerceType == comType):
                return True
        return False

    def getOr(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.aur[i]
        else:
            return 0

    def addOr(self,terre,nb):
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.aur[i] += nb
        
    def payerOr(self,terre):
        self.addOr(terre,-1)

    def recolter_ressources(self,des):
        for c in self.getBatiments():
            terre = c.position.getTerre()
            res = c.ressources_from_past(des)
            if (res != 0):
                self.addOr(terre,res[1])
                self.recevoir(terre,res[0]) 

    def getBateaux(self):
        return self.bateaux_transport + self.cargo + self.voilier

    def getBatiments(self):
        return self.colonies + self.villes
                
    def add_chevallier(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.chevalliers[i] += 1 
    
    def get_chevalliers(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.chevalliers[i]
        else:
            return -1
    
    def get_carte_armee_la_plus_grande(self,terre):
        u = Jeu.get_armee_la_plus_grande(terre)
        return u!=0 and u[0] == self
 
    def get_deplacement_voleur(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.deplacement_voleur[i]
        else:
            return 0

    def set_deplacement_voleur(self,terre,dep):
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.deplacement_voleur[i] = dep


    def get_route_la_plus_longue(self,terre):
        i = self.getTerreIndex(terre)
        if i!=-1:
            return self.routes_les_plus_longues[i]
        
    def set_route_la_plus_longue(self,terre, l):
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.routes_les_plus_longues[i] = l

    def route_la_plus_longue(self,terre, recalculer=False):
        if terre in self.terres:
            if recalculer:
                i = 0
                for r in self.routes:
                    if r.position.getTerre() == terre and r.est_extremite():
                        i = max(i, r.rlplfr())
                self.set_route_la_plus_longue(terre,i)
                return i
            else:
                return self.get_route_la_plus_longue(terre)
        else:
            return 0
                       
    def get_carte_route_la_plus_longue(self,terre):
        u = Jeu.get_route_la_plus_longue(terre)
        return u!=0 and u[0]== self

    def addStaticPoint(self,terre,nb):
        i = self.getTerreIndex(terre)
        if i!=-1:
            self.points[i] += nb

    def getPoints(self,terre):
        i = self.getTerreIndex(terre)
        p = 0
        if (self.get_carte_route_la_plus_longue(terre)):
            p += 2
        if (self.get_carte_armee_la_plus_grande(terre)):
            p += 2
        if i!=-1:
            return self.points[i] + self.getCartes(terre).get_cartes_de_type(Cartes.POINT_VICTOIRE) + p


class Jeu:

    JOUEURS = [Joueur(1), Joueur(2), Joueur(3), Joueur(4)]

    des = []
    joueurs_origine = []
    terres = []

    routes_les_plus_longues = []
    armees_les_plus_grandes = []
    


    @staticmethod
    def get_joueur(num):
        return Jeu.JOUEURS[num-1]

    @staticmethod
    def get_all_joueurs():
        return Jeu.JOUEURS

    @staticmethod
    def get_terre_index(terre):
        if terre in Jeu.terres:
            return Jeu.terres.index(terre)
        else:
            return -1

    @staticmethod
    def get_joueurs_origine(terre):
        n = Jeu.get_terre_index(terre)
        if n != -1 and len(Jeu.joueurs_origine)-1 >= n:
            return Jeu.joueurs_origine[n]
        else:
            return 0

    @staticmethod
    def designer_deplaceur_de_voleur():
        b = False
        for i in range(0,3):
            if Jeu.des[i] == 7:
                for terre in Jeu.terres:
                    Jeu.JOUEURS[(i + Jeu.get_joueurs_origine(terre))%len(Jeu.JOUEURS)].deplacement_voleur.set_deplacement_voleur(terre,True)

    # Renvoie le joueur qui possède la route la plus longue sur la terre terre et sa longueur.
    @staticmethod
    def get_route_la_plus_longue(terre):
        n = Jeu.get_terre_index(terre)
        if n != -1:
            return Jeu.routes_les_plus_longues[n]

    # Vérifie si j a une route plus longue que la route la plus longue sur la terre terre. Si la route actuelle est nulle, alors vérifie si j a une route de plus de 5 troncons. Si c'est le cas, j prend la plus du joueur actuellement en position
    @staticmethod
    def challenge_route_la_plus_longue(j,terre):
        i = Jeu.get_terre_index(terre)
        if i != -1:
            n = j.get_route_la_plus_longue(terre)
            if n>=5:
                u = Jeu.routes_les_plus_longues[i]
                if u == 0 or  n > u[1]:
                    Jeu.routes_les_plus_longues[i] = (j,n)
                    
    
        

    # Renvoie le joueur qui possède l'armee la plus grande sur la terre terre et sa longueur.
    @staticmethod
    def get_armee_la_plus_grande(terre):
        n = Jeu.get_terre_index(terre)
        if n != -1:
            return Jeu.armees_les_plus_grandes[n]

                
    # Vérifie si j a une armee plus grande que la armee la plus grande sur la terre terre. Si l'armee actuelle est nulle, alors vérifie si j a une armee de plus de 3 chevalliers. Si c'est le cas, j prend la plus du joueur actuellement en position
    @staticmethod
    def challenge_armee_la_plus_grande(j,terre):
        i = Jeu.get_terre_index(terre)
        if i != -1:
            n = j.get_chevalliers(terre)
            if n>=3:
                u = Jeu.armees_les_plus_grandes[i]
                if u == 0 or  n > u[1]:
                    Jeu.armees_les_plus_grandes[i] = (j,n)
    

# -----------------------------------------------------
#    Actions dans la journee
# -----------------------------------------------------

    @staticmethod
    def peut_construire_colonie(j,intersection):
        if intersection.colonie == 0 and not (intersection.isMaritime()) and j.peut_payer(intersection.getTerre(), Tarifs.COLONIE)  :
            
            for int in intersection.neigh:
                if int.colonie != 0:
                    return False
                a = int.lien(intersection)
                if a.route != 0 and a.route.joueur == j:
                    return True
        return False


    @staticmethod
    @protection
    def construire_colonie(j, intersection):
        Colonie(j, intersection)
        terre = intersection.getTerre()
        j.payer(terre, Tarifs.COLONIE)
        j.addStaticPoint(terre,1)




    @staticmethod
    def peut_construire_route(j, arrete, construction_route = False):
        if arrete.route == 0 and not(arrete.isMaritime()) and (construction_route or j.peut_payer(arrete.getTerre(), Tarifs.ROUTE)):
            if (arrete.int1.colonie != 0 and arrete.int1.colonie.joueur == j) or (arrete.int2.colonie != 0 and arrete.int2.colonie.joueur == j):
                return True
            for a in arrete.neighb():
                if (a.route != 0 and a.route.joueur == j):
                    return True
        return False

    @staticmethod
    def construire_route(j,arrete, construction_route = False):
        if construction_route or Jeu.peut_construire_route(j,arrete):
            Route(j,arrete)
            terre = arrete.getTerre()
            if not construction_route:
                j.payer(terre,Tarifs.ROUTE)
            j.route_la_plus_longue(terre, True)
            Jeu.challenge_route_la_plus_longue(j,terre)
            return True
        else:
            return False

# On suppose que chaque ile est separee d'au moins 2 arrete. Ca evite des ambiguites au niveau de la terre de construction.
    @staticmethod
    def peut_construire_bateau(j,arrete):
        if arrete.bateau == 0 and arrete.isMaritime() and j.peut_payer(arrete.getTerre(), Tarifs.BATEAU_TRANSPORT):
            if (arrete.int1.colonie != 0 and arrete.int1.colonie.joueur == j) or (arrete.int2.colonie != 0 and arrete.int2.colonie.joueur == j):
                return True
        return False
    
    @staticmethod
    @protection
    def construire_bateau(j,arrete):
        Bateau(j,arrete)
        j.payer(arrete.getTerre(),Tarifs.BATEAU_TRANSPORT)


    @staticmethod
    def peut_evoluer_colonie(j, colonie):
        return colonie.joueur == j and j.peut_payer(colonie.position.getTerre(), Tarifs.VILLE)

    @staticmethod
    @protection
    def evoluer_colonie(j,colonie):
        colonie.evolue()
        terre = colonie.position.getTerre()
        j.payer(terre,Tarifs.VILLE)
        j.addStaticPoint(terre,1)

    @staticmethod
    def peut_acheter_carte_developpement(j,terre):
        return j.peut_payer(terre,Tarifs.DEVELOPPEMENT)
    
    def acheter_carte_developpement(j,terre):
            j.payer(terre,Tarifs.DEVELOPPEMENT)
            return j.piocher_developpement()

    @staticmethod
    def peut_deplacer_bateau(j,bateau,arrete):
        return bateau.joueur == j and not bateau.position.est_pirate() and arrete.isMaritimeOuCotier() and (arrete in bateau.position.neighb() or (bateau.etat == Bateau.BateauType.VOILIER and arrete in bateau.position.double_neighb() )) and (arrete.bateau == 0 or arrete.bateau.joueur != j) and not bateau.aBouge
    
    @staticmethod
    @protection
    def deplacer_bateau(j,bateau,arrete):
            bateau.deplacer(arrete)
            bateau.aBouge = True


    @staticmethod
    def peut_echanger_bateau(j,bateau,ct,cb):
        return j == bateau.joueur and bateau.en_position_echange() and j.peut_payer(bateau.position.getTerre(), ct) and bateau.peut_recevoir_et_payer(ct,cb) and ct.est_physiquement_possible() and cb.est_physiquement_possible()

    @staticmethod
    @protection
    def echanger_bateau(j,bateau,ct,cb):
            terre = bateau.position.getTerre()
            j.payer(terre,ct)
            j.recevoir(terre,cb)
            bateau.remove(cb)
            bateau.append(ct)
    
    @staticmethod
    def peut_evoluer_bateau(j,bateau):
        return bateau.en_position_echange() and ((bateau.etat == Bateau.BateauType.TRANSPORT and j.peut_payer(bateau.position.getTerre(), Tarifs.CARGO)) or (bateau.etat == Bateau.BateauType.CARGO and j.peut_payer(bateau.position.getTerre(), Tarifs.VOILIER)))

    
    @staticmethod
    @protection
    def evoluer_bateau(j,bateau):
            terre = bateau.position.getTerre()
            if(bateau.etat == Bateau.BateauType.TRANSPORT):
                bateau.evolue()
                j.payer(terre,Tarifs.CARGO)
            elif bateau.etat == Bateau.BateauType.CARGO :
                bateau.evolue()
                j.payer(terre,Tarifs.VOILIER)
            else:
                return False
    
    @staticmethod
    def peut_echanger(j1,j2,terre,c1,c2):
        return j1.peut_payer(terre,c1) and j2.peut_payer(terre,c2) and c1.est_ressource() and c2.est_ressource() and c1.est_physiquement_possible() and c2.est_physiquement_possible()

    @staticmethod
    @protection
    def echanger(j1,j2,terre,c1,c2):
            j1.payer(terre,c1)
            j1.recevoir(terre,c2)
            j2.payer(terre,c2)
            j2.recevoir(terre,c1)
    
    @staticmethod
    def peut_echanger_classique(j,terre,t1,t2):
        return t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and t1.est_physiquement_possible() and t2.est_physiquement_possible() and terre in j.terres and j.peut_payer(terre,t1*4)

    @staticmethod
    @protection
    def echanger_classique(j,terre,t1,t2):
            j.payer(terre,t1*4)
            j.recevoir(terre,t2)
    
    @staticmethod
    def peut_echanger_commerce_tous(j,terre,t1,t2):
        return t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and terre in j.terres and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.peut_payer(terre,t1*3) and j.contient_commerce_utilisable(terre,CommerceType.TOUS)
    
    @staticmethod
    @protection
    def echanger_commerce_tous(j,terre,t1,t2):
            j.payer(terre,t1*3)
            j.recevoir(terre,t2)
    
    @staticmethod
    def peut_echanger_commerce(j,terre,t1,t2):
        if t1.est_ressource() and t2.est_ressource() and t1.size() == 1 and t2.size() == 1 and terre in j.terres and t1.est_physiquement_possible() and t2.est_physiquement_possible() and j.peut_payer(terre,t1*2):
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
            j.payer(terre,t1*2)
            j.recevoir(terre,t2)
        
    @staticmethod
    def peut_recolter_ressources(des):
        if des < 2 or des == 7 or des > 12:
            return False
        else:
            return True

    @staticmethod
    @protection
    def recolter_ressources(des):
            for j in Jeu.get_all_joueurs():
                j.recolter_ressources(des)


    @staticmethod
    def peut_acheter_ressource(j,terre,carte):
        return j.getOr(terre) > 0 and carte.est_ressource() and carte.size() == 1 and carte.est_physiquement_possible()

    @staticmethod
    @protection
    def acheter_ressource(j,terre, carte):
            j.payerOr(terre)
            j.recevoir(terre,carte)

    @staticmethod
    def peut_coloniser(j,bateau,position,transfert):
        if j == bateau.joueur and transfert.est_physiquement_possible() and transfert <= (bateau.cargaison-Tarifs.COLONIE) and Tarifs.COLONIE <= bateau.cargaison and j.getTerreIndex(position.getTerre()) == -1 and position.colonie == 0:
            for i in position.neighb():
                if i.colonie != 0:
                    return False
            return position in bateau.positions_colonisables()
        else:
            return False


    @staticmethod
    @protection
    def coloniser(j,bateau,position,transfert):
            Colonie(j,position)
            terre = position.getTerre()
            j.terres.append(terre)
            j.mains.append(Cartes.RIEN)
            j.aur.append(0)
            j.chevalliers.append(0)
            j.routes_les_plus_longues.append(0)
            j.points.append(1)
            j.deplacement_voleur.append(False)
            j.recevoir(terre,transfert)
            bateau.remove(Tarifs.COLONIE + transfert)
    
    @staticmethod
    def positions_possibles_voleur(joueur,terre,voleurType):
        b = voleurType == Voleur.VoleurType.PIRATE
        if not (b or voleurType == Voleur.VoleurType.BRIGAND):
            return []
        if not b:
            voleur = terre.brigand
            hexs = terre.hexagones[:]
        else:
            voleur = terre.pirate
            hexs = terre.espaceMarin[:]
        hexs.remove(voleur.position)
        possibilite = []
        if b:
            for h in hexs:
                if h.commerceType!= 0:
                    for i in h.ints:
                        if (i.colonie != 0) and (i.colonie.joueur != joueur):
                            possibilite.append((h,i.colonie.joueur))
                for a in h.liens:
                        if (a.bateau != 0) and (a.bateau.joueur != joueur):
                            possibilite.append((h,a.bateau.joueur))
            if possibilite == []:
                return [(0,0)]
        else:
            for h in hexs:
                for i in h.ints:
                    if (i.colonie != 0) and (i.colonie.joueur != joueur):
                            possibilite.append((h,i.colonie.joueur))
            if possibilite == []:
                for h in voleur.position.terre.hexagones:
                    if h.etat == HexaType.DESERT and h.commerceType == 0:
                        possibilite.append((h,0))
        return possibilite 



    @staticmethod
    def peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,chevallier = False):
        if joueur.deplacement_voleur or chevallier:
            if voleurType == Voleur.VoleurType.BRIGAND:
                voleur = terre.brigand
            else:
                voleur = terre.pirate
            return terre in joueur.terres and (hex,jvol) in Jeu.positions_possibles_voleur(joueur,terre,voleurType)
        return False

    @staticmethod
    def voler(j1,terre,j2):
        ressources_terrestres = j2.getCartes(terre)
        nc = ressources_terrestres.ressources_size()
        ressources_bateaux = []
        s = nc
        for b in j2.getBateaux():
            if b.en_position_echange() and b.position.getTerre() == terre:
                n = b.cargaison.size()
                ressources_bateaux.append((n,b))
                s+=n
        if s == 0:
            return
        u = random.randint(1,s)
        if u <= nc:
            c = ressources_terrestres.carte(u)
            j2.payer(terre,c)
            j1.recevoir(terre,c)
        else:
            u-=nc
            for rb in ressources_bateaux:
                if u <= rb[0]:
                    c = rb[1].cargaison.carte(u)
                    rb[1].remove(c)
                    j1.recevoir(terre,c)
                else:
                    u -= rb[0]

    @staticmethod
    def deplacer_voleur(joueur,terre,voleurType,hex,jvol, chevallier = False):
        if chevallier or Jeu.peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol):
            terre.deplacer_voleur(voleurType,hex)
            Jeu.voler(joueur,terre,jvol)
            if not chevallier:
                joueur.deplacement_voleur = False
            return True
        else:
            return False


    @staticmethod
    def peut_defausser(joueur,terre,cartes):
        if 7 in Jeu.des and terre in joueur.terres:
            c = joueur.getCartes(terre)
            res = cartes[0]
            cargs = cartes[1]
            rs = c.ressources_size()

            bs = []
            for b in joueur.getBateaux():
                if b.est_proche(terre):
                    bs.append(b)
                    rs += b.cargaison.ressources_size()
            if rs <= 7:
                return cartes == (Cartes.RIEN,[])

            ds = rs/2 + rs%2 # ressource arrondi au superieur
            rs2 = rs - ds

            while rs2 > 7:
                ds += rs2/2 + rs2%2 # ressource arrondi au superieur
                rs2 = rs - ds
            if res <= c and res.est_ressource() and res.est_physiquement_possible():
                ss = res.ressources_size()
                for cb in cargs:
                    if cb[0] in bs and cb[1] <= cb[0].cargaison and cb[1].est_physiquement_possible() and cb[1].est_ressource():
                        ss += cb[1].ressources_size()
                    else:
                        return False
                return ss == ds
        return False

    @staticmethod
    @protection
    def defausser(joueur,terre,cartes):
            joueur.payer(terre,cartes[0])
            for cb in cartes[1]:
                cb[0].remove(cb[1])

    @staticmethod
    def peut_jouer_chevallier(joueur,terre,voleurType, hex,jvol):
        return Cartes.CHEVALLIER <= joueur.getCartes(terre) and terre in joueur.terres and Jeu.peut_deplacer_voleur(joueur,terre,voleurType,hex,jvol,True)

    @staticmethod
    @protection
    def jouer_chevallier(joueur,terre,voleurType, hex,jvol):
            joueur.add_chevallier(terre)
            joueur.payer(terre,Cartes.CHEVALLIER)
            Jeu.challenge_armee_la_plus_grande(joueur,terre)
            Jeu.deplacer_voleur(joueur,terre,voleurType,hex,jvol,True)



    @staticmethod
    def peut_jouer_decouverte(joueur,terre,cartes):
        return Cartes.DECOUVERTE <= joueur.getCartes(terre) and terre in joueur.terres and cartes.size() == 2 and cartes.est_ressource() and cartes.est_physiquement_possible()

    @staticmethod
    @protection
    def jouer_decouverte(joueur,terre,cartes):
            joueur.recevoir(terre,cartes)
            joueur.payer(terre,Cartes.DECOUVERTE)
    

    @staticmethod
    def peut_jouer_construction_routes(joueur,terre,a1,a2):
        return a1 != a2 and Cartes.CONSTRUCTION_ROUTES <= joueur.getCartes(terre) and terre in joueur.terres and a1.getTerre() == terre and a2.getTerre() == terre and Jeu.peut_construire_route(joueur,a1,True) and Jeu.peut_construire_route(joueur,a2,True)

    @staticmethod
    @protection
    def jouer_construction_routes(joueur,terre,a1,a2):
            joueur.payer(terre,Cartes.CONSTRUCTION_ROUTES)
            Jeu.construire_route(joueur,a1,True)
            Jeu.construire_route(joueur,a2,True)

    @staticmethod
    def peut_jouer_monopole(joueur,terre,t1, jvols):
        b = Cartes.MONOPOLE <= joueur.getCartes(terre) and terre in joueur.terres and t1.est_ressource() and t1.size() == 1 and t1.est_physiquement_possible() and len(jvols) <= 3 and not joueur in jvols

        for j in jvols:
            b = b and terre in j.terres

        return b

    @staticmethod
    @protection
    def jouer_monopole(joueur,terre,t1,jvols):
        i = 0
        for j in jvols:
            r =  j.getCartes(terre).get_cartes_de_type(t1)
            i += r
            j.payer(terre,t1*r)
        joueur.recevoir(terre,t1*i)

