# -*- coding: utf8 -*-

__all__ = ['Des', 'Monopole', 'DeplacementVoleur', 'Echange', 'recolter_ressources', 'peut_recolter_ressources'] 
import redis
from cartes import *
from joueurs import *
from plateau import *
from errors import *
from pions import *
REDIS = redis.StrictRedis()


class Des:
    NB_LANCES = 4

    @staticmethod
    def roll():
        ''' Enregistre une liste de 4 lancés de dés dans la bdd '''
        dices = []
        for i in xrange(Des.NB_LANCES):
            dices.append(random.randint(2, 12))
        Des.save(dices)


    @staticmethod
    def getOrigin():
        ''' Renvoie le nombre de lancés de dés, correspond donc en jeu de plateau au nombres de joueurs qui ont lancé les dés et donc au numéro du joueur, modulo le nombre de joueurs, qui a effectué le premiers des 4 derniers lancés. '''
        return int(REDIS.get('dices:joueur_origine'))
    
    @staticmethod
    def setOrigin(num):
        ''' Enregistre le nombre de lancés de dés depuis le début de la partie '''
        REDIS.set('dices:joueur_origine',num)
    
    @staticmethod
    def incrOrigin():
        ''' Incrémente le nombre de lancé de dés '''
        REDIS.incr('dices:joueur_origine',Des.NB_LANCES)

    @staticmethod
    def save(dices):
        ''' Sauvegarde un lancé de 4 dés '''
        REDIS.delete('dices')
        REDIS.rpush('dices',*dices)
        Des.incrOrigin()

    @staticmethod
    def getDices():
        ''' Renvoie les 4 derniers lancés de dés '''
        a =  REDIS.lrange('dices',0,-1)
        dices = [int(i) for i in a]
        return dices

class Monopole:
    def __init__(self,num,j,jvols,terre,carte):
        if num == 0:
            self.num = REDIS.incr("LastMonopole")
        else:
            self.num = num
        self.j = j
        self.jvols = jvols
        self.terre = terre
        self.carte = carte

    def save(self, bdd):
        key = "M"+str(self.num)
        bdd.set(key + ':joueur', self.j.num)
        for j in self.jvols:
            bdd.sadd(key + ':joueurVoles', j)
        bdd.set(key + ':terre', self.terre.num)
        self.carte.setTo(key + ':carte')

    @staticmethod
    def getMonopole(num):
        key = "M"+str(num)
        j1N = int(REDIS.get(key + ':joueur'))
        jvols = []
        for j in REDIS.smembers(key + ':joueurVoles'):
            jvols.append(int(j))
        terreN = int(REDIS.get(key + ':terre'))
        accepted = REDIS.get(key + ':accepte') == 'True'

        carte = CartesGeneral.get(key+':carte')

        j1 = JoueurPossible(j1N)
        terre = Plateau.getPlateau().ter(terreN)

        return Monopole(num,j1,jvols,terre,carte)

# Execution Monopole

    def executer(self):
        i = 0
        for j in self.jvols:
            j = JoueurPossible(j)
            r =  j.getCartes(self.terre).get_cartes_de_type(self.carte)
            i += r
            j.payer(self.terre,self.carte*r)
        self.j.recevoir(self.terre,self.carte*i)


class DeplacementVoleur:
    
    def __init__(self,num,joueur,terre, voleurType, hex, jvol, chevallier):
        if num == 0:
            self.num = REDIS.incr("LastDeplacementVoleur")
        else:
            self.num = num
        self.j = joueur.num
        self.terre = terre
        self.voleurType = voleurType
        self.hex = hex
        self.jvol = jvol
        self.chevallier = chevallier

    def save(self,bdd):
        key = "DV"+str(self.num)
        bdd.set(key + ':joueur', self.j)
        bdd.set(key + ':terre', self.terre.num)
        bdd.set(key + ':voleurType', self.voleurType)
        bdd.set(key + ':emplacement', self.hex.num)
        bdd.set(key + ';jvol', self.jvol)
        bdd.set(key + ':chevallier', self.chevallier)

        joueur = JoueurPossible(self.j,bdd)
        if self.chevallier:
            j = Des.NB_LANCES+1
            for i in joueur.get_lance_des_deplacements_voleur(self.terre):
                j = min(j, int(i))
            if j !=  Des.NB_LANCES+1:
                joueur.add_deplacement_voleur(self.terre,j,self.num)
        else:
            joueur.add_deplacement_voleur_chevallier(self.terre, self.num)

    @staticmethod
    def getDeplacementVoleur(num):
        key = "DV"+str(num)
        
        j = JoueurPossible(int(REDIS.get(key + ':joueur')))
        terre = Plateau.getPlateau().ter(int(REDIS.get(key + ':terre')))
        voleurType = REDIS.get(key + ':voleurType')
        hex = Plateau.getPlateau().hexa(int(REDIS.get(key + ':emplacement')))
        jvol = int(REDIS.get(key + ';jvol'))
        chevallier = REDIS.get(key + ':chevallier') == 'True'

        return DeplacementVoleur(num,j,terre,voleurType,hex,jvol,chevallier)

    def executer(self):
        j = JoueurPossible(self.j)
        if self.voleurType == Voleur.VoleurType.BRIGAND:
            voleur = Voleur.getBrigand(self.terre,REDIS)
        else:
            voleur = Voleur.getPirate(self.terre,REDIS)
        voleur.deplacer(self.hex)
        voleur.save(REDIS)
        j.voler(self.terre,self.jvol)

    @staticmethod 
    def designer_deplaceur_de_voleur():
        p = Plateau.getPlateau()
        for terre in p.terres:
            js = terre.getJoueurs(REDIS)
            for jn in js:
                j = JoueurPossible(int(jn))
                j.set_deplacement_voleur(terre,False)
                j.clear_lance_des_deplacement_voleur(terre)
                j.clear_deplacement_voleur_chevallier(terre)
                for i in xrange(Des.NB_LANCES):
                    j.clear_deplacement_voleur(terre,i+1)
    
        des = Des.getDices()
        defausse = 7 in des 
        origin = Des.getOrigin()
        for terre in p.terres:            
            js = []
            for jns in terre.getJoueurs(REDIS):
                j = JoueurPossible(int(jns))
                if(not j.getEnRuine()):
                    js.append(j)
            for j in js:
                
                # Gestion de la défausse
                if defausse:
                    c = j.getCartes(terre)
                    rs = c.ressources_size()
                    bs = []
                    for bn in j.getBateaux():
                        b = Bateau.getBateau(int(bn),REDIS)
                        if b.est_proche(terre):
                            bs.append(b.num)
                            rs += b.cargaison.ressources_size()
                    if rs <= 7:
                        j.set_defausser(terre, 0)
                    else:
                        ds = rs/2 + rs%2 # ressource arrondi au superieur
                        rs2 = rs - ds

                        while rs2 > 7:
                            ds += rs2/2 + rs2%2 # ressource arrondi au superieur
                            rs2 = rs - ds
                        j.set_defausser(terre,ds)
                else:
                    j.set_defausser(terre, 0)
                # Gestion du déplacemnt de voleur
                for i in range(0,Des.NB_LANCES):
                    if des[i] == 7:
                        j = js[(i+origin)%len(js)]
                        j.set_deplacement_voleur(terre,True)
                        j.add_lance_des_deplacement_voleur(terre,i+1)

class Echange:

    def __init__(self,num,j1,j2,terre,don,recu, accepted = False):
        if num == 0:
            self.num = REDIS.incr("LastEchange")
        else:
            self.num = num
        self.j1 = j1
        self.j2 = j2
        self.terre = terre
        self.don = don
        self.recu = recu
        self.accepted = accepted

    def isAccepted(self):
        self.accepted = True

    def save(self):
        key = "E"+str(self.num)
        REDIS.set(key + ':joueurProposant', self.j1.num)
        REDIS.set(key + ':joueurAcceptant', self.j2.num)
        REDIS.set(key + ':terre', self.terre.num)
        self.don.setTo(key + ':don')
        self.recu.setTo(key + ':recu')
        REDIS.set(key + ':accepte', self.accepted)

    @staticmethod
    def getEchange(num):
        key = "E"+str(num)
        if REDIS.get(key+':joueurProposant'):
            j1N = int(REDIS.get(key + ':joueurProposant'))
            j2N = int(REDIS.get(key + ':joueurAcceptant'))
            terreN = int(REDIS.get(key + ':terre'))
            accepted = REDIS.get(key + ':accepte') == 'True'

            don = CartesGeneral.get(key+':don')
            recu = CartesGeneral.get(key+':recu')

            j1 = JoueurPossible(j1N)
            j2 = JoueurPossible(j2N)
            terre = Plateau.getPlateau().ter(terreN)

            return Echange(num,j1,j2,terre,don,recu, accepted)
        else:
            return 0

    def delete(echange):
        key = "E"+str(echange.num)
        REDIS.delete(key + ':joueurProposant')
        REDIS.delete(key + ':joueurAcceptant')
        REDIS.delete(key + ':terre')
        REDIS.delete(key + ':accepte')

        CartesGeneral.delete(key+':don')
        CartesGeneral.delete(key+':recu')
        

    def executer(echange):
        ''' Effectue  de cartes entre les joueurs de echange sur cette terre, avec j1 donnant c1 cartes et j2 donnant c2 cartes.'''
        j1 = echange.j1
        terre = echange.terre
        if echange.accepted:
            j2 = echange.j2
            # Le paiement a déjà été fait lors de l'acceptation et la propsoition de l'échange
            j1.recevoir(terre,echange.recu)
            j2.recevoir(terre,echange.don)
        else:
            j1.recevoir(terre,echange.don)
        echange.delete()



def peut_recolter_ressources(des):
        ''' On peut lancer la récolte des réssources si les dés sont entre 2 et 12'''
        if des < 2 or des > 12:
            raise RecolteError(RecolteError.HORS_LIMITE)
        if des == 7:
            raise RecolteError(RecolteError.SEPT)
        return True


def recolter_ressources(des):
        ''' Effectue pour tous les joueurs sur toutes les terres la récolte des ressources sauf s'ils sont en ruine'''
        import arbre_action
        if peut_recolter_ressources(des):
            for j in arbre_action.Joueur.get_all_joueurs():
                if not j.getEnRuine(): 
                    j.recolter_ressources(des)
            return True
        return False


def getJoueursParPriorite():
        ''' Renvoie la liste des joueurs par ordre de priorité de la journée '''
        return REDIS.lrange('JoueursPriorite',0,-1)

def setNextJoueursParPriorite():
        ''' Remplace la liste de priorite des joueurs actuelle par la suivante '''
        pass

def action_nuit():
        ''' Execute l'ensemble des actions du jour '''
        import arbre_action

        # En premier on fait defausser les gens qui n'ont pas defaussé leurs cartes au hasard.
        # On exécute les arbres d'actions.
        # On effectue les echanges
        # On deplace les voleurs et on effectue les vols
        # On effectue les monopoles.
        # On relance les dés
        # On redonne la priorié des joueurs
        # On désigne les déplaceurs de voleur
        # On effectue les récoltes
        # On donne les cartes de développement achetée la veille
        
        for j in arbre_action.Joueur.get_all_joueurs():
            jp = JoueurPossible(j.num)
            for terre in jp.getTerres():
                if jp.doit_defausser(terre):
                    Defausse.defausse_aleatoire(jp, terre)
        pass
        
