# *-* coding: utf8 *-*
import redis
from plateau import *
from pions import *
from errors import *
from bdd_interface import *
import Jeu
import functools
from ActionNight import *
REDIS = redis.StrictRedis()

def predefausse(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        import joueurs
        j = joueurs.JoueurPossible(args[0].num)
        if not j.doit_defausser_general():
            f(*args,**kwargs)
            return True
        else:
            raise ActionNightError(ActionNightError.DOIT_DEFAUSSER)

    return helper


def preruine(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        import joueurs
        j = joueurs.JoueurPossible(args[0].num)
        if not j.getEnRuine():
            f(*args,**kwargs)
            return True
        else:
            raise ActionNightError(ActionNightError.JOUEUR_EN_RUINE)

    return helper


def protection(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        peut_f = getattr(Joueur,'peut_' + f.__name__)
        if peut_f(*args,**kwargs):
            f(*args,**kwargs)
            return True
        else:
            return False

    return helper

class Joueur:
    ''' Classe qui représente juste l'interface entre le joueur et les noeuds'''

    def __init__(self,num):
        self.num = num
    
    
    def __eq__(self,other):
        if other is None:
            return False
        return self.num == other.num
    
    def __ne__(self,other):
        if other is None:
            return False
        return self.num != other.num
    
    def __str__(self):
        return str(self.num)


# Gestion de l'arbre d'action

    
    def setRoot(self,node):
        REDIS.set('J'+str(self.num)+':racine',node.num)

    def getRoot(self):
        return Node(int(REDIS.get('J'+str(self.num)+':racine')))

    def hasRoot(self):
        return REDIS.exists('J'+str(self.num)+':racine')

    def setNewRoot(self):

        node = Node.getNextNewNode()
        self.setRoot(node)
       
        node.setPlayer(self)
        node.setRoot(node)
        node.setFirstChild(NodeCst.NULL)
        node.setLastChildNode(NodeCst.NULL)
        node.setSiblingNode(NodeCst.NULL)
        node.setPSiblingNode(NodeCst.NULL)
        node.setFatherNode(NodeCst.NULL)
    
        Node.incrNodeId()

        return node


# Execution de l'arbre d'action
    
    def executer(self):
        ''' Execute l'ensemble de l'arbre d'action et construit une base de données à partir de toutes les actions. '''
        node = self.getRoot()
        ibdd = REDIS
        b = True
        while True:
            if b:
                node = node.getNextNode()
                if node != NodeCst.NULL:
                    ibdd = BDD(ibdd)
                else:
                    return ibdd
            else:
                node = node.getSiblingNode()
                if node == NodeCst.NULL:
                    return ibdd
            try:
                self.executerNode(node, ibdd)
                b = True
            except NodeError:
                b = False
    
    def executerPartiel(self, node, action):
        ''' Renvoie la base de données telle qu'elle serait si on exécutait l'arbre d'action jusqu'au noeud node, jusqu'à l'action action.'''

        listNodes = self.getRoot().getPath(node)
        if listNodes is None :
            return

        ibdd = BDD(REDIS)

        c = self.executerListNodes(listNodes,ibdd)
        ibdd = BDD(c)
        if action != 0:
            if not self.executerNodePartiel(node, action, ibdd):
                return
        return ibdd
        
                   
 
    def executerListNodes(self,listNodes, ibdd):
        ''' Execute linéairement l'ensemble des noeuds de la liste l. Si c'est impossible, renvoie un tuple (False,0), sinon renvoie (True, bdd) où bdd est l'interface de la base de donnée résultante de l'application des noeuds sur ibdd. ibdd n'est pas modifiée'''
        bdd = BDD(ibdd)
        for node in listNodes:
            self.executerNode(node,bdd)
            bdd = BDD(bdd)
        return bdd
            


    def executerNode(self,node, ibdd):
        ''' Execute l'ensemble des actions du noeud dans la base ibdd jusqu' à la dernière ou jusqu'a ce qu'une des action renvoie faux. Dans le premire cas, elle renvoie vrai et dans l'autre, vide la  base de données ibdd et renvoie faux. ibdd est modifiée'''
        actionsNum = node.getActionsNum()
        for actnum in actionsNum:
            action = Action.getAction(int(actnum))
            try:    
                b = self.executerAction(action, ibdd)
            except ActionError as err:
                ibdd.flushSurface()
                raise NodeError(node,action, err)
        return True

    def executerNodePartiel(self, node, action, ibdd):
        '''  Execute les actions du noeud jusqu'à l'exécution de action (incluse), ou jusqu'à ce qu'une action renvoie Faux. ibdd est modifiée'''
        actionsNum = node.getActionsNum()
        if not str(action.num) in actionsNum:
            return False
        
        for actnum in actionsNum:
            act = Action.getAction(int(actnum))
            b = self.executerAction(act, ibdd)
            if not b:
                return False
            if int(actnum) == action.num:
                return True

    def executerAction(self, action, ibdd):
        ''' Execute l'action, avec la base de donnée ibdd. ibdd est modifiée. '''
        import joueurs
        j = joueurs.JoueurPossible(self.num, ibdd)
        try:
            func = getattr(Jeu, action.func)
            translation_args = getattr(Jeu, 'translate_'+action.func)(j, *action.params)
            func.peut_etre_appelee
        except (AttributeError, TypeError):
            raise ActionError(ActionError.MAUVAIS_PARAMETRES)
        return func(j,*translation_args)
                

# Vérifications en cas d'insertion et de suppression d'une action
    
    def insererNouvelleAction(self, node, index, func, *params):
        ''' Crée une nouvelle action avec les parametres func et params et l'ajoute a node en position index'''
        num = Action.getNextActionId()
        Action.incrActionId()
        a = Action(num, func, *params)
        a.save()
        return self.insererAction(a,node,index)

    def insererAction(self,action, node, index):
        ''' Renvoie vrai si en ajoutant l'action n au noeud node en position index, toutes les exécutions de foret d'action qui suivent peuvent etre exécutées. Sinon n'ajoute pas l'action et renvoie faux'''
        if node.getPlayer() is None or node.getPlayer() != self:
            return False
        node.insertActionByIndex(index, action)
        try:
            self.testListNode(node)
            return True
        except NodeError as err:
            node.removeAction(action)
            raise err
    
    def retirerAction(self,action, node):
        ''' Renvoie vrai si en retirant l'action n au noeud node en position index, toutes les exécutions de foret d'action qui suivent peuvent etre exécutées. Sinon ne retire pas l'action et renvoie faux'''
        index = node.getActionIndex(action)
        if node.getPlayer() is None or node.getPlayer() != self:
            return False
        if index != -1:
            node.removeAction(action)
            try:
                self.testListNode(node)
                Action.delAction(action.num)
                return True
            except NodeError as err:
                node.insertActionByIndex(index, action)
                raise err
        return False

    def testListNode(self, node):
        ''' Renvoie vrai si le sous arbre de l'arbre de d'action contenant le plus court chemin de r à node et le sous arbre enraciné en node est cohérent. Ie, il est possible de le parcourir du début à la fin, quelque soit la feuille choisie. '''
        pathLists = node.getPathList()

        if pathLists is None:
            return False

        s = len(pathLists[1])

        ibdd = BDD(REDIS)
        # On teste le chemin de root jusque node.
        ibdd = self.executerListNodes(pathLists[0], ibdd)
        for i in xrange(s):
            # On teste le chemin de node jusque sa ie feuille, en repartant de la base de données fournie par le chemin de la racine jusque node.
            self.executerListNodes(pathLists[1][i], ibdd)
        
        return True


# Echanges

    def isGivingCompatible(self,terre,c):
        ''' Vérifie que pour tout noeud, toute action, le joueur possède toujours au moins c cartes '''
        import joueurs
        j = joueurs.JoueurPossible(self.num)
        if not j.peut_payer(terre, c):
            return False
        j.payer(terre,c)
        
        try:
            self.testListNode(self.getRoot())
            j.recevoir(terre,c)
            return True
        except NodeError as err:
            j.recevoir(terre,c)
            raise err


    @preruine
    @predefausse
    def peut_proposer_echange(joueur,j2num,terre,c1,c2):
        ''' j1 peut proposer un echange à j2 si aucun des deux n'est en ruine que les deux ont colonisé la terre, que c1 et c2 sont des flux possibles et que quelque soit le noeud de son arbre d'action il est en mesure de payer c1'''
        import joueurs
        j1 = joueurs.JoueurPossible(joueur.num)
        if j2num > joueurs.JoueurPossible.getNbJoueurs() or j2num < 1:
            raise EchangeError(EchangeError.PARTENAIRE_INEXISTANT)
        j2 = joueurs.JoueurPossible(j2num)
        if j2.getEnRuine():
            raise EchangeError(EchangeError.PARTENAIRE_EN_RUINE)
        if not j1.aColoniseTerre(terre):
            raise EchangeError(EchangeError.TERRE_NON_COLONISEE)
        if not j2.aColoniseTerre(terre): 
            raise EchangeError(EchangeError.TERRE_PARTENAIRE_NON_COLONISEE)
        if not(c1.est_ressource() and c1.est_physiquement_possible()):
            raise EchangeError(EchangeError.FLUX_IMPOSSIBLE)
        if not(c2.est_ressource() and c2.est_physiquement_possible()):
            raise EchangeError(EchangeError.FLUX_IMPOSSIBLE)
        if not joueur.isGivingCompatible(terre,c1):
            raise EchangeError(EchangeError.DON_INCOMPATIBLE)
            # Renvoei un node error si le joueur ne peut effectuer son echange à cause d'une action de l'arbre d'action.
        return True

    @protection
    def proposer_echange(joueur,j2num,terre,c1,c2):
        import joueurs
        j1 = joueurs.JoueurPossible(joueur.num)
        j1.payer(terre,c1)
        Echange(0,j1, Joueur(j2num), terre,c1,c2).save()

    @preruine
    @predefausse
    def peut_accepter_echange(joueur,echange):
        ''' j1 peut accepter un echange s'il est le deuxième joueur de cet échange et si quelque soit les noeuds de son arbre d'action il est en mesure de payer la somme demandée'''
        if echange.accepted:
            raise EchangeError(EchangeError.DEJA_ACCEPTE)
        if joueur != echange.j2:
            raise EchangeError(EchangeError.NON_PARTENAIRE)
        if not joueur.isGivingCompatible(echange.terre,echange.recu):
            raise EchangeError(EchangeError.DON_INCOMPATIBLE)
        return True

    @protection
    def accepter_echange(joueur,echange):
        import joueurs
        echange.isAccepted()
        j1 = joueurs.JoueurPossible(joueur.num)
        j1.payer(echange.terre,echange.recu)
        echange.save() 

    @preruine
    @predefausse
    def peut_annuler_echange(joueur,echange):
        if joueur != echange.j2 and joueur != echange.j1:
            raise EchangeError(EchangeError.NON_PARTENAIRE)
        return True
            

    @protection
    def annuler_echange(joueur,echange):
        import joueurs
        j1 = joueurs.JoueurPossible(echange.j1.num)
        j2 = joueurs.JoueurPossible(echange.j2.num)
        j1.recevoir(echange.terre, echange.don)
        if echange.accepted:
            j2.recevoir(echange.terre,echange.recu)
        echange.delete()
        
# Voleur

    @preruine
    @predefausse
    def peut_deplacer_voleur(j,terre,voleurType,hex,jvol):
        bdd = REDIS
        import joueurs
        joueur = joueurs.JoueurPossible(j.num)
        if not joueur.aColoniseTerre(terre):
            raise VoleurError(VoleurError.TERRE_NON_COLONISEE)
        if not joueur.get_deplacement_voleur(terre):
            raise VoleurError(VoleurError.DEPLACEMENT_INTERDIT) 
        if not (hex == 0 or hex.terre == terre):
            raise VoleurError(VoleurError.EMPLACEMENT_INTERDIT)
        if jvol > joueurs.JoueurPossible.getNbJoueurs() or jvol < 0: # jvol == 0 est toléré là où les voleurs nes sont pas déplaceables
            raise VoleurError(VoleurError.JOUEUR_VOLE_INEXISTANT)

        if voleurType == Voleur.VoleurType.BRIGAND:
            voleur = Voleur.getBrigand(terre,bdd)
        else:
            voleur = Voleur.getPirate(terre,bdd)
        if jvol == 0:
            t = (hex, 0)
        else:
            t = (hex, jvol)
        if not t in joueur.positions_possibles_voleur(terre,voleur):
            raise VoleurError(VoleurError.EMPLACEMENT_INTERDIT)

        return True

    @protection
    def deplacer_voleur(joueur,terre,voleurType,hex,jvol):
        DeplacementVoleur(0,joueur,terre,voleurType,hex,jvol, False).save(REDIS)
        joueur.set_deplacement_voleur(terre,False)
        

    @staticmethod
    def get_all_joueurs():
        import joueurs
        i = joueurs.JoueurPossible.getNbJoueurs()
        js = []
        for j in xrange(i):
            js.append(joueurs.JoueurPossible(j+1))
        return js
   
    @preruine
    def peut_defausser(j,terre,cartes):
        import joueurs
        joueur = joueurs.JoueurPossible(j.num)
        if not joueur.aColoniseTerre(terre):
            raise DefausseError(DefausseError.TERRE_NON_COLONISEE)
        if not joueur.doit_defausser(terre):
            raise DefausseError(DefausseError.DEFAUSSE_INTERDITE)
            
        c = joueur.getCartes(terre)
        rs = c.ressources_size()


        bs = []
        for bn in joueur.getBateaux():
            b = Bateau.getBateau(int(bn),REDIS)
            if b.est_proche(terre):
                bs.append(b.num)
                rs += b.cargaison.ressources_size()
        if rs <= 7:
            raise DefausseError(DefausseError.DEFAUSSE_INTERDITE)
        
        res = cartes[0]
        cargs = cartes[1]

        ds = rs/2 + rs%2 # ressource arrondi au superieur
        rs2 = rs - ds

        while rs2 > 7:
            ds += rs2/2 + rs2%2 # ressource arrondi au superieur
            rs2 = rs - ds

        if not (res.est_ressource() and res.est_physiquement_possible()):
            raise DefausseError(DefausseError.FLUX_IMPOSSIBLE)
        if not res <= c:
            raise DefausseError(DefausseError.FLUX_TROP_ELEVE)
        ss = res.ressources_size()
        for cb in cargs:
            if not cb[0].num in bs:
                raise DefausseError(DefausseError.BATEAU_NON_DEFAUSSABLE)
            if not (cb[1].est_physiquement_possible() and cb[1].est_ressource()):
                raise DefausseError(DefausseError.FLUX_IMPOSSIBLE)
            if not cb[1] <= cb[0].cargaison:
                raise DefausseError(DefausseError.FLUX_TROP_ELEVE)
            ss += cb[1].ressources_size()
        if ss > ds:
            raise DefausseError(DefausseError.DEFAUSSE_TROP_ELEVEE)
        elif ss < ds:
            raise DefausseError(DefausseError.DEFAUSSE_TROP_FAIBLE)
        return True


    @protection
    def defausser(j,terre,cartes):
        import joueurs
        joueur = joueurs.JoueurPossible(j.num)
        joueur.payer(terre,cartes[0])
        bdd = joueur.bdd
        for cb in cartes[1]:
            cb[0].remove(cb[1])
            cb[0].save(bdd)
        joueur.set_defausser(terre,0)


   
def protectTypeAttributeError(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except (TypeError, AttributeError):
            return
    return helper

class Node:
    ''' Classe représentant le noeud d'un arbre, avec un lien vers le pere, frere gauche et droit, premier et dernier fils. '''

    def __init__(self,num):
        self.num = num
    
    def __eq__(self,other):
        if other is None:
            return False
        return self.num == other.num
    
    def __ne__(self,other):
        if other is None:
            return False
        return self.num != other.num
    
    def __str__(self):
        return str(self.num)

# Interface avec la base de données

    @protectTypeAttributeError 
    def setPlayer(node, j):
        REDIS.set('N'+str(node.num)+':joueur',j.num)

    @protectTypeAttributeError 
    def getPlayer(node):
        return Joueur(int(REDIS.get('N'+str(node.num)+':joueur')))

    @protectTypeAttributeError 
    def setFirstChild(fatherNode,childNode):
        REDIS.set('N'+str(fatherNode.num)+':firstChild',childNode.num)

    @protectTypeAttributeError 
    def getFirstChild(fatherNode):
        return Node(int(REDIS.get('N'+str(fatherNode.num)+':firstChild')))

    @protectTypeAttributeError 
    def hasChild(fatherNode):
        return REDIS.get('N'+str(fatherNode.num)+':lastChild') != '-1'

    @protectTypeAttributeError 
    def setFatherNode(childNode,fatherNode):
        REDIS.set('N'+str(childNode.num)+':father',fatherNode.num)

    @protectTypeAttributeError 
    def getFatherNode(childNode):
        return Node(int(REDIS.get('N'+str(childNode.num)+':father')))

    @protectTypeAttributeError 
    def setSiblingNode(node,siblingNode):
        REDIS.set('N'+str(node.num)+':sibling',siblingNode.num)

    @protectTypeAttributeError 
    def getSiblingNode(node):
        return Node(int(REDIS.get('N'+str(node.num)+':sibling')))

    @protectTypeAttributeError 
    def hasSiblingNode(node):
        return REDIS.get('N'+str(node.num)+':sibling') != '-1'

    @protectTypeAttributeError 
    def setPSiblingNode(node,pSiblingNode):
        REDIS.set('N'+str(node.num)+':psibling',pSiblingNode.num)

    @protectTypeAttributeError 
    def getPSiblingNode(node):
        return Node(int(REDIS.get('N'+str(node.num)+':psibling')))
    
    @protectTypeAttributeError 
    def setLastChildNode(fatherNode,lastChildNode):
        REDIS.set('N'+str(fatherNode.num)+':lastChild',lastChildNode.num)
 
    @protectTypeAttributeError 
    def getLastChildNode(fatherNode):
        return Node(int(REDIS.get('N'+str(fatherNode.num)+':lastChild')))

    # Interface pour les racines 
    
    @protectTypeAttributeError 
    def setRoot(node, rootNode):
        REDIS.set('N'+str(node.num)+':root',rootNode.num)

    @protectTypeAttributeError 
    def getRoot(node):
        return Node(int(REDIS.get('N'+str(node.num)+':root')))

    def deleteNode(node):
        key = 'N'+str(node.num)
        REDIS.delete(key+':firstChild')
        REDIS.delete(key+':sibling')
        REDIS.delete(key+':psibling')
        REDIS.delete(key+':father')
        REDIS.delete(key+':lastChild')
        REDIS.delete(key+':joueur')
        REDIS.delete(key+':root')
        REDIS.delete(key+':racineSuivante')
        REDIS.delete(key+':racinePrecedente')


# Méthode calculant des noeuds particuliers

    def getNextNode(node):
        ''' Renvoie le noeud suivant au sens de l'éxécution classique d'un arbre d'action, à savoir le premier fils, ou s'il n'en a pas le premier fils de la racine de l'arbre d'action suivant. NULL sinon.'''
        return node.getFirstChild()

    def getPreviousNode(node):
        ''' Renvoie l'ensemble des noeuds précédents au sens de l'éxécution classique d'un arbre d'action, ie l'ensemble des noeuds dont getNextNode renvoie node'''
        return node.getFatherNode()

    def getPath(origin,dest):
        ''' Renvoie la liste des noeuds compris dans le chemin partant de origin jusque dest, destination non comprise'''
        path = []
        node = dest
        while(node != origin):
            node = node.getFatherNode()
            if node is None:
                return
            if node == NodeCst.NULL:
                return []
            path.append(node)
        path.reverse()
        return path     

    def getPathList(node):
        ''' Renvoie une liste contenant deux éléments : le chemin entre la racine et node, et la liste des chemins entre node et toutes ses feuilles. '''
        
        root = node.getRoot()
        if root is None:
            return 


        l = []
        l.append(root.getPath(node))
        l[0].append(node)
        l1 = []
        for leaf in node.getLeavesOf():
            path = node.getPath(leaf)
            path.append(leaf)
            l1.append(path[1:])
        l.append(l1)
        return l

# Interface avec la base de donnée concernant l'ajout d'un nouveau noeud    

    @staticmethod
    def getFirstChildId():
        lastNode = REDIS.get('LastNode')
        if lastNode == None:
            lastNode = 1
            REDIS.set('LastNode',lastNode)
        else:
            lastNode = int(lastNode)
        return lastNode

    @staticmethod
    def getNextNewNode():
        return Node(Node.getFirstChildId())

    @staticmethod
    def incrNodeId():
        REDIS.incr('LastNode')

# Methode de travail avec des racines

    def getDescendants(node):
        l = []

        if(not node.hasChild()):
            return l

        node = node.getFirstChild()
        while(node != NodeCst.NULL):
            l.append(node)
            l.extend(node.getDescendants())
            node = node.getSiblingNode()
        return l


    def getLeavesOf(node):

        if not Node.hasChild(node):
            return [node]

        l = []
        node = node.getFirstChild()
        while(node != NodeCst.NULL):
            l.extend(node.getLeavesOf())
            node = node.getSiblingNode()

        return l


# Methode de travail avec des noeuds non racines        

    def addChild(fatherNode):
        ''' Ajoute un fils à la fin de la liste des fils de fatherNode '''
        lastNode = Node.getNextNewNode()

        if fatherNode.hasChild():
            lastChild = fatherNode.getLastChildNode()
            lastChild.setSiblingNode(lastNode)
            lastNode.setPSiblingNode(lastChild)
        else:
            fatherNode.setFirstChild(lastNode)
            lastNode.setPSiblingNode(NodeCst.NULL)
        fatherNode.setLastChildNode(lastNode)

        lastNode.setFatherNode(fatherNode)
        lastNode.setLastChildNode(NodeCst.NULL)
        lastNode.setSiblingNode(NodeCst.NULL)
        lastNode.setFirstChild(NodeCst.NULL)

        Node.incrNodeId()

        root = fatherNode.getRoot()
        lastNode.setRoot(root)
        lastNode.setPlayer(fatherNode.getPlayer())
        

        return lastNode

    def addFirstChild(fatherNode):
        ''' Ajoute un fils au début de la liste des fils de fatherNode '''
        lastNode = Node.getNextNewNode()

        if fatherNode.hasChild():
            firstChild = fatherNode.getFirstChild()
            firstChild.setPSiblingNode(lastNode)
            lastNode.setSiblingNode(firstChild)
        else:
            fatherNode.setLastChildNode(lastNode)
            lastNode.setSiblingNode(NodeCst.NULL)
        fatherNode.setFirstChild(lastNode)
        lastNode.setFatherNode(fatherNode)
        lastNode.setFirstChild(NodeCst.NULL)
        lastNode.setLastChildNode(NodeCst.NULL)
        lastNode.setPSiblingNode(NodeCst.NULL)
        Node.incrNodeId()
        root = fatherNode.getRoot()
        lastNode.setRoot(root)
        lastNode.setPlayer(fatherNode.getPlayer())
        
        return lastNode
        

    def addSibling(node):
        ''' Ajoute un frere à node, le place après node dans la liste des fils du pere de node'''
        lastNode = Node.getNextNewNode()
        
        fatherNode = node.getFatherNode()
        siblingNode = node.getSiblingNode()

        lastNode.setFatherNode(fatherNode)
        lastNode.setSiblingNode(siblingNode)
        if siblingNode != NodeCst.NULL:
            siblingNode.setPSiblingNode(lastNode)
        lastNode.setPSiblingNode(node)
        node.setSiblingNode(lastNode)
        lastNode.setFirstChild(NodeCst.NULL)
        lastNode.setLastChildNode(NodeCst.NULL)

        if siblingNode == NodeCst.NULL:
            fatherNode.setLastChildNode(lastNode)
        
        Node.incrNodeId()
        root = fatherNode.getRoot()
        lastNode.setRoot(root)
        lastNode.setPlayer(node.getPlayer())
        
        return lastNode
    
    def removeNode(node):
        ''' Retire node de son arbre '''
        
        fatherNode = node.getFatherNode()
        siblingNode = node.getSiblingNode()
        pSiblingNode = node.getPSiblingNode()
        childs = []
        child = node.getFirstChild()
        while(child != NodeCst.NULL):
            childs.append(child)
            child = child.getSiblingNode()

        for child in childs:
            child.setFatherNode(fatherNode)
        if(len(childs) != 0):
            if pSiblingNode != NodeCst.NULL:
                pSiblingNode.setSiblingNode(childs[0])
            if siblingNode != NodeCst.NULL:
                siblingNode.setPSiblingNode(childs[len(childs)-1])
            childs[len(childs)-1].setSiblingNode(siblingNode)
            childs[0].setPSiblingNode(pSiblingNode)
        else:
            if pSiblingNode != NodeCst.NULL:
                pSiblingNode.setSiblingNode(siblingNode)
            if siblingNode != NodeCst.NULL:
                siblingNode.setPSiblingNode(pSiblingNode)

        lastChild = fatherNode.getLastChildNode()
        if lastChild == node:
            if(len(childs) != 0):
                fatherNode.setLastChildNode(childs[len(childs)-1])
            else:
                fatherNode.setLastChildNode(pSiblingNode)

        child = fatherNode.getFirstChild()
        if(child == node):
            if(len(childs) != 0):
                fatherNode.setFirstChild(childs[0])
            else:
                fatherNode.setFirstChild(siblingNode)

        node.deleteNode()



# Travail avec les actions

    def getActionsNum(node):
        ''' Ajoute une action au noeud node, en fin de liste des actions '''
        return REDIS.lrange('N'+str(node.num)+':actions',0,-1)

    def addAction(node,action):
        ''' Ajoute une action au noeud node, en fin de liste des actions '''
        REDIS.rpush('N'+str(node.num)+':actions',action.num)

    def lPushAction(node,action):
        ''' Ajoute une action au noeud node, au début de liste des actions '''
        REDIS.lpush('N'+str(node.num)+':actions',action.num)
    
    def insertAction(node,beforeAction,action):
        ''' Ajoute une action au noeud node juste après l'action beforeAction '''
        key = 'N' + str(node.num) + ':actions'
        REDIS.linsert(key,'after',beforeAction, action.num)
    
    def insertActionByIndex(node,index,action):
        ''' Ajoute une action au noeud node juste après l'action située à l'indice index '''
        key = 'N' + str(node.num) + ':actions'
        if index == 0:
            return node.lPushAction(action)
        else:
            beforeAction = REDIS.lindex(key,index-1)
            node.insertAction(beforeAction,action)

    def getActionIndex(node,action):
        ''' Renvoie l'indice de l'action dans le noeud'''
        key = 'N' + str(node.num) + ':actions'
        actions = REDIS.lrange(key,0,-1)
        try:
            return actions.index(str(action.num))
        except ValueError:
            return -1
        

    def removeAction(node,action):
        ''' Retire l'action du noeud node '''
        REDIS.lrem('N'+str(node.num)+':actions',0,action.num)

        

class Action:

    def __init__(self, num, func, *params):
        self.num = num
        self.func = func
        self.params = list(params)

    def __eq__(self,other):
        return self.num == other.num

    def save(self):
        key = 'Act'+str(self.num)
        REDIS.set(key+':fonction',self.func)
        if len(self.params) != 0:
            REDIS.rpush(key+':params',*self.params)

    @staticmethod
    def getAction(num):
        key = 'Act'+str(num)
        func = REDIS.get(key+':fonction')
        params = REDIS.lrange(key+':params',0,-1)
        return Action(num,func,*params)

    @staticmethod
    def getNextActionId():
        lastAction = REDIS.get('LastAction')
        if lastAction == None:
            REDIS.set('LastAction',1)
            lastAction = 1
        return lastAction

    @staticmethod
    def incrActionId():
        REDIS.incr('LastAction')

    @staticmethod
    def delAction(num):
        key = 'Act'+str(num)
        func = REDIS.delete(key+':fonction')
        params = REDIS.delete(key+':params')

class NodeCst:
    NULL = Node(-1)


if __name__ == '__main__':
    
    REDIS.flushdb() 
