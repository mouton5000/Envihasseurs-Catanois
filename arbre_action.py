# *-* coding: utf8 *-*
import redis
from plateau import *
REDIS = redis.StrictRedis()


class Joueur:
    ''' Classe qui représente juste l'interface entre le joueur et les noeuds'''

    def __init__(self,num):
        self.num = num
    
    
    def __eq__(self,other):
        return self.num == other.num
    
    def __ne__(self,other):
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
        node.setNextRoot(NodeCst.NULL)
        
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
        node = self.getFirstRoot()
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
            b = self.executerNode(node, ibdd)
    
    def executerPartiel(self, node, action):
        ''' Renvoie la base de données telle qu'elle serait si on exécutait l'arbre d'action jusqu'au noeud node, jusqu'à l'action action.'''

        listNodes = self.getRoot().getPath(node)
        ibdd = BDD(REDIS)

        c = self.executerListNodes(listNodes,ibdd)
        if not c[0]:
            return
    
        ibdd = BDD(c[1])
        b = self.executerNodePartiel(node, action, ibdd)
        if not b:
            return
        return ibdd
        
                   
 
    def executerListNodes(self,listNodes, ibdd):
        ''' Execute linéairement l'ensemble des noeuds de la liste l. Si c'est impossible, renvoie un tuple (False,0), sinon renvoie (True, bdd) où bdd est l'interface de la base de donnée résultante de l'application des noeuds sur ibdd. ibdd n'est pas modifiée'''
        bdd = BDD(ibdd)
        for node in listNodes:
            if not self.executerNode(node,bdd):
                return (False,0)
            bdd = BDD(bdd)
        return (True,bdd)
            


    def executerNode(self,node, ibdd):
        ''' Execute l'ensemble des actions du noeud dans la base ibdd jusqu' à la dernière ou jusqu'a ce qu'une des action renvoie faux. Dans le premire cas, elle renvoie vrai et dans l'autre, vide la  base de données ibdd et renvoie faux. ibdd est modifiée'''
        actionsNum = node.getActionsNum()
        for actnum in actionsNum:
            action = Action.getAction(int(actnum))
            b = self.executerAction(action, ibdd)
            if not b:
                ibdd.flushSurface()
                return False
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
        j = JoueurPossible(self.num, ibdd)
        func = getattr(Jeu, action.func)
        if func.peut_etre_appelee:
            return Jeu.func(j,*action.params)
        return False

# Vérifications en cas d'insertion et de suppression d'une action

    def insererAction(self,action, node, index):
        ''' Renvoie vrai si en ajoutant l'action n au noeud node en position index, toutes les exécutions de foret d'action qui suivent peuvent etre exécutées. Sinon n'ajoute pas l'action et renvoie faux'''
        node.insertActionByIndex(index, action)
        
        if self.testListNode(node):
            return True
        else:
            node.removeAction(action)
            return False
    
    def retirerAction(self,action, node):
        ''' Renvoie vrai si en retirant l'action n au noeud node en position index, toutes les exécutions de foret d'action qui suivent peuvent etre exécutées. Sinon n'ajoute pas l'action et renvoie faux'''
        index = node.getActionIndex(action)
        node.removeAction(action)
        
        if self.testListNode(node):
            return True
        else:
            node.insertActionByIndex(index, action)
            return False

    def testListNode(self, node):
        ''' Renvoie vrai si le sous arbre de l'arbre de d'action contenant le plus court chemin de r à node et le sous arbre enraciné en node est cohérent. Ie, il est possible de le parcourir du début à la fin, quelque soit la feuille choisie. '''
        pathLists = node.getPathLists()

        s = len(pathLists[1])

        ibdd = BDD(REDIS)
        # On teste le chemin de root jusque node.
        c = self.executerListNodes(pathLists[0][0], ibdd)
        if not c[0]:
            return False
        for i in xrange(s):
            # On teste le chemin de node jusque sa ie feuille.
            c = self.executerListeNodes(pathLists[i][indexes[i]], ibdd)
            if not c[0]:
                return False
        
        return True


# Echanges

    def isGivingCompatible(self,c):
        ''' Vérifie que pour tout noeud, toute action, le joueur possède toujours au moins c cartes '''
        pathLists = self.getRoot().getPathLists()

        s = len(pathLists[1])

        ibdd = BDD(REDIS)
        j = Joueur(self.num, ibdd)
        j.payer(c)
        for i in xrange(s):
            # On teste le chemin de node jusque sa ie feuille. Si un des chemin n'est pas bon, alors l'échange n'est pas compatible.
            c = self.executerListeNodes(pathLists[i][indexes[i]], ibdd)
            if not c[0]:
                return False

        return True


    def peut_proposer_echange(j1,j2num,terre,c1,c2):
        ''' j1 peut proposer un echange à j2 si aucun des deux n'est en ruine que les deux ont colonisé la terre, que c1 et c2 sont des flux possibles et que quelque soit le noeud de son arbre d'action il est en mesure de payer c1'''
        j2 = Joueur(j2num)
        if j1.getEnRuine():
            raise EchangeError(EchangeError.JOUEUR_EN_RUINE)
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
        if not j1.isGivingCompatible(c1):
            raise EchangeError(EchangeError.DON_INCOMPATIBLE)
        return True

    def proposer_echange(j1,j2num,terre,c1,c2):    
        Echange(j1, Joueur(j2num), terre,c1,c2).save()

    def peut_accepter_echange(j1,echange):
        ''' j1 peut accepter un echange s'il est le deuxième joueur de cet échange et si quelque soit les noeuds de son arbre d'action il est en mesure de payer la somme demandée'''
        if j1 != echange.j2:
            raise EchangeError(EchangeError.NON_PARTENAIRE) 
        if not j1.isGivingCompatible(echange.c2):
            raise EchangeError(EchangeError.DON_INCOMPATIBLE)
        return True

    def accepter_echange(j1,echange):
        echange.isAccepted()
        echange.save() 

    
# Ruine

    def setEnRuine(self,ruine):
        self.bdd.set('J'+str(self.num)+':ruine',ruine)
    
    def getEnRuine(self):
        return self.bdd.get('J'+str(self.num)+':ruine') == 'True'

    def ruiner(self):
        self.setEnRuine(True)
        for t in self.getTerres():
            self.setStaticPoints(t,0)
            Jeu.recalcul_route_la_plus_longue(t,self.bdd)
            Jeu.recalcul_armee_la_plus_grande(t,self.bdd)
    

class Node:
    ''' Classe représentant le noeud d'un arbre, avec un lien vers le pere, frere gauche et droit, premier et dernier fils. '''

    def __init__(self,num):
        self.num = num
    
    def __eq__(self,other):
        return self.num == other.num
    
    def __ne__(self,other):
        return self.num != other.num
    
    def __str__(self):
        return str(self.num)

# Interface avec la base de données
    
    def setPlayer(node, j):
        REDIS.set('N'+str(node.num)+':joueur',j.num)

    def getPlayer(node):
        return Joueur(int(REDIS.get('N'+str(node.num)+':joueur')))

    def setFirstChild(fatherNode,childNode):
        REDIS.set('N'+str(fatherNode.num)+':firstChild',childNode.num)

    def getFirstChild(fatherNode):
        return Node(int(REDIS.get('N'+str(fatherNode.num)+':firstChild')))

    def hasChild(fatherNode):
        return REDIS.get('N'+str(fatherNode.num)+':lastChild') != '-1'

    def setFatherNode(childNode,fatherNode):
        REDIS.set('N'+str(childNode.num)+':father',fatherNode.num)

    def getFatherNode(childNode):
        return Node(int(REDIS.get('N'+str(childNode.num)+':father')))

    def setSiblingNode(node,siblingNode):
        REDIS.set('N'+str(node.num)+':sibling',siblingNode.num)

    def getSiblingNode(node):
        return Node(int(REDIS.get('N'+str(node.num)+':sibling')))

    def hasSiblingNode(node):
        return REDIS.get('N'+str(node.num)+':sibling') != '-1'

    def setPSiblingNode(node,pSiblingNode):
        REDIS.set('N'+str(node.num)+':psibling',pSiblingNode.num)

    def getPSiblingNode(node):
        return Node(int(REDIS.get('N'+str(node.num)+':psibling')))
    
    def setLastChildNode(fatherNode,lastChildNode):
        REDIS.set('N'+str(fatherNode.num)+':lastChild',lastChildNode.num)
 
    def getLastChildNode(fatherNode):
        return Node(int(REDIS.get('N'+str(fatherNode.num)+':lastChild')))

    # Interface pour les racines
   
    
    def setRoot(node, rootNode):
        REDIS.set('N'+str(node.num)+':root',rootNode.num)

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
        while(node != origine):
            node = node.getFatherNode()
            if node == NodeCst.NULL:
                return []
            path.append(node)
        path.reverse()
        return path     

    def getPathList(node):
        ''' Renvoie une liste contenant deux éléments : le chemin entre la racine et node, et la liste des chemins entre node et toutes ses feuilles. '''
        root = node.getRoot()

        l = []
        l.append([root.getPath(node)])

        l1 = []
        for leaf in node.getLeaves():
            l1.append(node.getPath(leaf))

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
        beforeAction = REDIS.lindex(key,index)
        Node.insertAction(node,beforeAction,action)

    def getActionIndex(node,action):
        ''' Renvoie l'indice de l'action dans le noeud'''
        key = 'N' + str(node.num) + ':actions'
        actions = REDIS.lrange(key,0,-1)
        return actions.index(str(action.num))
        

    def removeAction(node,action):
        ''' Retire l'action du noeud node '''
        REDIS.lrem('N'+str(node.num)+':actions',0,action.num)
        Action.delAction(action.num)

        

class Action:

    def __init__(self, num, func, *params):
        self.num = num
        self.func = func
        self.params = list(params)

    def save(self):
        key = 'Act'+str(self.num)
        REDIS.set(key+':fonction',self.func)
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

def hasNext(indexes, sizes):
    return indexes != sizes

def next(indexes, sizes):
    for i in xrange(len(sizes)):
        if indexes[i] == sizes[i]:
            indexes[i] = 0
        else:
            indexes[i] += 1
            return


if __name__ == '__main__':
    
    REDIS.flushdb()
    indexes = [0,0,0]
    sizes = [0,3,2]

    print indexes
    while(hasNext(indexes,sizes)):
        next(indexes,sizes)
        print indexes
        
