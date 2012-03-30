# *-* coding: utf8 *-*
import redis
from plateau import *
from joueurs import *
REDIS = redis.StrictRedis()


class JoueurNodeInterface:
    ''' Classe qui représente juste l'interface entre le joueur et les noeuds'''

    def __init__(self,num):
        self.num = num
    
    
    def __eq__(self,other):
        return self.num == other.num
    
    def __ne__(self,other):
        return self.num != other.num
    
    def __str__(self):
        return str(self.num)

    
    def setFirstRoot(self,node):
        REDIS.set('J'+str(self.num)+':racine',node.num)

    def getFirstRoot(self):
        return Node(int(REDIS.get('J'+str(self.num)+':racine')))

    def hasRoot(self):
        return REDIS.exists('J'+str(self.num)+':racine')

    def setLastRoot(self,node):
        REDIS.set('J'+str(self.num)+':derniereRacine',node.num)

    def getLastRoot(self):
        return Node(int(REDIS.get('J'+str(self.num)+':derniereRacine')))
    
    def setNewRoot(self):

        node = Node.getNextNewNode()
        hasRoot = self.hasRoot()
        if hasRoot:
            lastRoot = self.getLastRoot()
            lastRoot.setNextRoot(node)
            node.setPreviousRoot(lastRoot)
        else:
            self.setFirstRoot(node)
            node.setPreviousRoot(NodeCst.NULL)
        self.setLastRoot(node)
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

    def setNewFirstRoot(self):

        node = Node.getNextNewNode()
        if self.hasRoot():
            firstRoot = self.getFirstRoot()
            node.setNextRoot(firstRoot)
            firstRoot.setPreviousRoot(node)
        else:
            self.setLastRoot(node)
            node.setNextRoot(NodeCst.NULL)
        self.setFirstRoot(node)
        node.setPreviousRoot(NodeCst.NULL)

        node.setPlayer(self)
        node.setRoot(node)
        node.setFirstChild(NodeCst.NULL)
        node.setLastChildNode(NodeCst.NULL)
        node.setSiblingNode(NodeCst.NULL)
        node.setPSiblingNode(NodeCst.NULL)
        node.setFatherNode(NodeCst.NULL)
        Node.incrNodeId()
        
        return node

# Execution
    
    def executer(self):
        ''' Execute l'ensemble de la foret d'action et construit une base de données à partir de toutes les actions. '''
        node = self.getFirstRoot()
        ibdd = REDIS
        b = True
        while True:
            if b:
                if node.hasChild(node):
                    node = node.getFirstChild(node)
                    ibdd = BDD(ibdd)
                else:
                    root = node.getRoot()
                    if root.hasNextRoot():
                        node = ForetAction.getNextRoot(root)
                        continue
                    else:
                        return ibdd
            else:
                if node.hasSibling():
                    node = node.getSiblingNode()
                else:
                    return ibdd
            b = self.executerNode(node, ibdd)
    
    def executerNode(self,node, ibdd):
        ''' Execute l'ensemble des actions du noeud dans la base ibdd jusqu' à la dernière ou jusqu'a ce qu'une des action renvoie faux. Dans le premire cas, elle renvoie vrai et dans l'autre, vide la  base de données ibdd et renvoie faux.'''
        actionsNum = ForetAction.getActions(node)
        for actnum in actionsNum:
            action = Action.getAction(int(actnum))
            b = self.executerAction(action, ibdd)
            if not b:
                ibdd.flushSurface()
                return False
        return True

    def executerAction(self, action, ibdd):
        ''' Execute l'action, avec la base de donnée ibdd '''
        j = Joueur(self.num, ibdd)
        func = getattr(Jeu, action.func)
        if func.peut_etre_appelee:
            return Jeu.func(j,*action.params)
        return False


    def peutExecuterAction(self, action, ibdd):
        ''' Vérifie si on peut executer l'action, avec la base de donnée ibdd '''
        j = Joueur(self.num, ibdd)
        func = getattr(Jeu, 'peut_'+action.func)
        if func.peut_etre_appelee:
            return Jeu.func(j,*action.paramsi)
        return False

        

class Node:
    ''' Classe représentant une forêt dont les arbres sont placés les uns à la suite.
    Chaque noeud contient un ensemble d'étiquettes qu'il enregistre. Puis un curseur
    peut se ballader de pere en fils ou de frere en frere. Si le curseur est au bout
    d'un arbre est qu'on souhaite voir le fils, le curseur passe à l'arbre suivant.'''


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
        return JoueurNodeInterface(int(REDIS.get('N'+str(node.num)+':joueur')))

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
   
    
    def setNextRoot(root,node):
        REDIS.set('N'+str(root.num)+':racineSuivante',node.num)

    def getNextRoot(root):
        return Node(int(REDIS.get('N'+str(root.num)+':racineSuivante')))
    
    def hasNextRoot(root):
        return REDIS.get('N'+str(root.num)+':racineSuivante') != '-1'
    
    def setPreviousRoot(root,node):
        REDIS.set('N'+str(root.num)+':racinePrecedente',node.num)

    def getPreviousRoot(root):
        return Node(int(REDIS.get('N'+str(root.num)+':racinePrecedente')))
    
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

    def setNewNextRoot(root):

        node = Node.getNextNewNode()
        j = root.getPlayer()
        lastRoot = j.getLastRoot()
        if lastRoot == root:
            j.setLastRoot(node)
            node.setNextRoot(NodeCst.NULL)
        nroot = root.getNextRoot()
        node.setNextRoot(nroot)
        if nroot != NodeCst.NULL:
            nroot.setPreviousRoot(node)
        root.setNextRoot(node)
        node.setPreviousRoot(root)

        node.setPlayer(j)
        node.setRoot(node)
        node.setFirstChild(NodeCst.NULL)
        node.setLastChildNode(NodeCst.NULL)
        node.setSiblingNode(NodeCst.NULL)
        node.setPSiblingNode(NodeCst.NULL)
        node.setFatherNode(NodeCst.NULL)
        Node.incrNodeId()

        return node
   
    def removeRoot(root):
        j = root.getPlayer()
        froot = j.getFirstRoot()
        lroot = j.getLastRoot()
        nroot = root.getNextRoot()
        proot = root.getPreviousRoot()

        if proot != NodeCst.NULL:
            proot.setNextRoot(nroot) 
        if nroot != NodeCst.NULL:
            nroot.setPreviousRoot(proot)
        if root == froot:
            j.setFirstRoot(nroot)
        if root == lroot:
            j.setLastRoot(proot)
 

        l = Node.selectNodesFromRoot(root)
        for n in l:
            n.deleteNode()
        
        root.deleteNode()


    def selectNodesFromRoot(root):
        l = []

        if(not root.hasChild()):
            return l

        node = root.getFirstChild()
        while(node != NodeCst.NULL):
            l.append(node)
            l.extend(node.selectNodesFromRoot())
            node = node.getSiblingNode()
        return l


    def getLeavesOf(root):

        if not Node.hasChild(root):
            return [root]

        l = []
        node = root.getFirstChild()
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

    @staticmethod
    def getActions(node):
        ''' Ajoute une action au noeud node, en fin de liste des actions '''
        return REDIS.lrange('N'+str(node.num)+':actions',0,-1)

    @staticmethod
    def addAction(node,action):
        ''' Ajoute une action au noeud node, en fin de liste des actions '''
        REDIS.rpush('N'+str(node.num)+':actions',action.num)

    @staticmethod
    def lPushAction(node,action):
        ''' Ajoute une action au noeud node, au début de liste des actions '''
        REDIS.lpush('N'+str(node.num)+':actions',action.num)
    
    @staticmethod
    def insertAction(node,beforeAction,action):
        ''' Ajoute une action au noeud node juste après l'action beforeAction '''
        key = 'N' + str(node) + ':actions'
        REDIS.linsert(key,'after',beforeAction, action.num)
    
    @staticmethod
    def insertActionByIndex(node,index,action):
        ''' Ajoute une action au noeud node juste après l'action située à l'indice index '''
        key = 'N' + str(node) + ':actions'
        beforeAction = REDIS.lindex(key,index)
        Node.insertAction(node,beforeAction,action)

    @staticmethod
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

if __name__ == '__main__':
    
    REDIS.flushdb()
    print Node(-1) == NodeCst.NULL
    


