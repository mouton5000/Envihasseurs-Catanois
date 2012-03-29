# *-* coding: utf8 *-*
import redis
from plateau import *
from joueurs import *
REDIS = redis.StrictRedis()


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
    
    def setPlayer(node, jnum):
        REDIS.set('N'+str(node.num)+':joueur',jnum)

    def getPlayer(node):
        return int(REDIS.get('N'+str(node.num)+':joueur'))

    def setNextNode(fatherNode,childNode):
        REDIS.set('N'+str(fatherNode.num)+':next',childNode.num)

    def getNextNode(fatherNode):
        return Node(int(REDIS.get('N'+str(fatherNode.num)+':next')))

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
   
    @staticmethod
    def setFirstRoot(node,jnum):
        REDIS.set('J'+str(jnum)+':racine',node.num)

    @staticmethod
    def getFirstRoot(jnum):
        return Node(int(REDIS.get('J'+str(jnum)+':racine')))

    @staticmethod
    def hasRoot(jnum):
        return REDIS.exists('J'+str(jnum)+':racine')

    @staticmethod
    def setLastRoot(node,jnum):
        REDIS.set('J'+str(jnum)+':derniereRacine',node.num)

    @staticmethod
    def getLastRoot(jnum):
        return Node(int(REDIS.get('J'+str(jnum)+':derniereRacine')))
    
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
        REDIS.delete(key+':next')
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
    def getNextNodeId():
        lastNode = REDIS.get('LastNode')
        if lastNode == None:
            lastNode = 1
            REDIS.set('LastNode',lastNode)
        else:
            lastNode = int(lastNode)
        return lastNode

    @staticmethod
    def getNextNewNode():
        return Node(Node.getNextNodeId())

    @staticmethod
    def incrNodeId():
        REDIS.incr('LastNode')

# Methode de travail avec des racines

    @staticmethod
    def setNewRoot(jnum):

        node = Node.getNextNewNode()
        hasRoot = Node.hasRoot(jnum)
        if hasRoot:
            lastRoot = Node.getLastRoot(jnum)
            lastRoot.setNextRoot(node)
            node.setPreviousRoot(lastRoot)
        else:
            Node.setFirstRoot(node,jnum)
            node.setPreviousRoot(NodeCst.NULL)
        Node.setLastRoot(node,jnum)
        node.setNextRoot(NodeCst.NULL)
        
        node.setPlayer(jnum)
        node.setRoot(node)
        node.setNextNode(NodeCst.NULL)
        node.setLastChildNode(NodeCst.NULL)
        node.setSiblingNode(NodeCst.NULL)
        node.setPSiblingNode(NodeCst.NULL)
        node.setFatherNode(NodeCst.NULL)
    
        Node.incrNodeId()

        if hasRoot: 
            ls = lastRoot.getLeavesOf()
            for n in ls:
                n.setNextNode(n,node)
        return node

    @staticmethod
    def setNewFirstRoot(j):

        node = Node.getNextNewNode()
        if Node.hasRoot(j):
            firstRoot = Node.getFirstRoot(j)
            node.setNextRoot(firstRoot)
            firstRoot.setPreviousRoot(node)
        else:
            Node.setLastRoot(node,j)
            node.setNextRoot(NodeCst.NULL)
        node.setFirstRoot(j)
        node.setPreviousRoot(NodeCst.NULL)

        Node.setPlayer(node,j)
        node.setRoot(node)
        node.setNextNode(NodeCst.NULL)
        node.setLastChildNode(NodeCst.NULL)
        node.setSiblingNode(NodeCst.NULL)
        node.setPSiblingNode(NodeCst.NULL)
        node.setFatherNode(NodeCst.NULL)
        Node.incrNodeId()
        
        return node
    
    @staticmethod
    def setNewNextRoot(root, j):

        node = Node.getNextNewNode()
        lastRoot = Node.getLastRoot(j)
        if lastRoot == root:
            Node.setLastRoot(node,j)
            node.setNextRoot(NodeCst.NULL)
        nroot = root.getNextRoot()
        node.setNextRoot(nroot)
        if nroot != NodeCst.NULL:
            nroot.setPreviousRoot(node)
        root.setNextRoot(node)
        node.setPreviousRoot(root)

        Node.setPlayer(node,j)
        node.setRoot(node)
        node.setNextNode(NodeCst.NULL)
        node.setLastChildNode(NodeCst.NULL)
        node.setSiblingNode(NodeCst.NULL)
        node.setPSiblingNode(NodeCst.NULL)
        node.setFatherNode(NodeCst.NULL)
        Node.incrNodeId()


        ls = Node.getLeavesOf(root)
        for n in ls:
            n.setNextNode(node)
        return node
   
    @staticmethod
    def removeRoot(root):
        j = root.getPlayer()
        froot = Node.getFirstRoot(j)
        lroot = Node.getLastRoot(j)
        nroot = root.getNextRoot()
        proot = root.getPreviousRoot()

        if proot != NodeCst.NULL:
            proot.setNextRoot(nroot) 
            ls = proot.getLeavesOf()
            for n in ls:
                n.setNextNode(nroot)
        if nroot != NodeCst.NULL:
            nroot.setPreviousRoot(proot)
        if root == froot:
            Node.setFirstRoot(nroot,j)
        if root == lroot:
            Node.setLastRoot(proot,j)
 

        l = Node.selectNodesFromRoot(root)
        for n in l:
            n.deleteNode()
        
        root.deleteNode()


    def selectNodesFromRoot(root):
        l = []

        if(not root.hasChild()):
            return l

        node = root.getNextNode()
        while(node != NodeCst.NULL):
            l.append(node)
            l.extend(node.selectNodesFromRoot())
            node = node.getSiblingNode()
        return l


    def getLeavesOf(root):

        if not Node.hasChild(root):
            return [root]

        l = []
        node = root.getNextNode()
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
            fatherNode.setNextNode(lastNode)
            lastNode.setPSiblingNode(NodeCst.NULL)
        fatherNode.setLastChildNode(lastNode)

        lastNode.setFatherNode(fatherNode)
        lastNode.setLastChildNode(NodeCst.NULL)
        lastNode.setSiblingNode(NodeCst.NULL)

        Node.incrNodeId()

        root = fatherNode.getRoot()
        lastNode.setRoot(root)
        lastNode.setPlayer(fatherNode.getPlayer())
        
        nextRoot = root.getNextRoot()
        lastNode.setNextNode(nextRoot)

        return lastNode

    def addFirstChild(fatherNode):
        ''' Ajoute un fils au début de la liste des fils de fatherNode '''
        lastNode = Node.getNextNewNode()

        if fatherNode.hasChild():
            firstChild = fatherNode.getNextNode()
            firstChild.setPSiblingNode(lastNode)
            lastNode.setSiblingNode(firstChild)
        else:
            fatherNode.setLastChildNode(lastNode)
            lastNode.setSiblingNode(NodeCst.NULL)
        fatherNode.setNextNode(lastNode)
        lastNode.setFatherNode(fatherNode)
        lastNode.setNextNode(NodeCst.NULL)
        lastNode.setLastChildNode(NodeCst.NULL)
        lastNode.setPSiblingNode(NodeCst.NULL)
        Node.incrNodeId()
        root = fatherNode.getRoot()
        lastNode.setRoot(root)
        lastNode.setPlayer(fatherNode.getPlayer())
        
        nextRoot = root.getNextRoot()
        lastNode.setNextNode(nextRoot)
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
        lastNode.setNextNode(NodeCst.NULL)
        lastNode.setLastChildNode(NodeCst.NULL)

        if siblingNode == NodeCst.NULL:
            fatherNode.setLastChildNode(lastNode)
        
        Node.incrNodeId()
        root = fatherNode.getRoot()
        lastNode.setRoot(root)
        lastNode.setPlayer(node.getPlayer())
        
        nextRoot = root.getNextRoot()
        lastNode.setNextNode(nextRoot)
        return lastNode
    
    def removeNode(node):
        ''' Retire node de son arbre '''
        
        fatherNode = node.getFatherNode()
        siblingNode = node.getSiblingNode()
        pSiblingNode = node.getPSiblingNode()
        childs = []
        child = node.getNextNode()
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

        child = fatherNode.getNextNode()
        if(child == node):
            if(len(childs) != 0):
                fatherNode.setNextNode(childs[0])
            else:
                if siblingNode != NodeCst.NULL:
                    fatherNode.setNextNode(siblingNode)
                else:
                    nRoot = fatherNode.getRoot().getNextRoot()
                    fatherNode.setNextNode(nRoot)

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
    


#    def addRoot(self):
#        ''' Ajoute un arbre d'action à la foret de ce joueur, en fin de liste '''
#        return ForetAction.setNewRoot(self) 
    
#    def addFirstRoot(self):
#        ''' Ajoute un arbre d'action à la foret de ce joueur, en début de liste '''
#        return ForetAction.setNewFirstRoot(self) 
    
#    def getFirstRoot(self):
#        ''' Ajoute un arbre d'action à la foret de ce joueur, en début de liste '''
#        return ForetAction.getFirstRoot(self) 

#    def addNextRoot(self,root):
#        ''' Ajoute un arbre d'action à la foret de ce joueur, juste après l'arbre de racine root '''
#        return ForetAction.setNewNextRoot(root,self) 
    
#    def peutExecuterAction(self, action):
#        ''' Vérifie si on peut executer l'action, avec la base de donnée bdd '''
#        func = getattr(Jeu, 'peut_'+action.func)
#        if func.peut_etre_appelee:
#            return Jeu.func(self,*action.paramsi)
#        return False

#    def executerAction(self, action):
#        ''' Execute l'action, avec la base de donnée bdd '''
#        func = getattr(Jeu, action.func)
#        if func.peut_etre_appelee:
#            return Jeu.func(self,*action.params)
#        return False

#    def executerNode(self, node):
#        ''' Execute l'ensemble des actions du noeud jusqu' à la dernière ou jusqu'a ce qu'une des action renvoie faux. Dans le premire cas, elle renvoie vrai et dans l'autre, vide la  base de données et renvoie faux.'''
#        actions = ForetAction.getActions(node)
#        for actnum in actions:
#            action = Action.getAction(int(actnum))
#            b = self.executerAction(action)
#            if not b:
#                self.bdd.flushSurface()
#                return False
#        return True
        
#    def executerForetAction(self):
#        ''' Execute l'ensemble de la foret d'action et renvoie la dernière base de données avant que l'execution ne s'arrete. '''
#        node = self.getFirstRoot()
#        bdd = REDIS
#        b = True
#        while True:
#            if b:
#                if ForetAction.hasChild(node):
#                    node = ForetAction.getNextNode(node)
#                    self.bdd = BDD(bdd)
#                else:
#                    root = ForetAction.getRoot(node)
#                    if ForetAction.hasNextRoot(root):
#                        node = ForetAction.getNextRoot(root)
#                        continue
#                    else:
#                        return self.bdd
#            else:
#                if ForetAction.hasSibling(node):
#                    node = ForetAction.getSiblingNode(node)
#                else:
#                    return self.bdd
#            b = self.executerNode(node, self.bdd)
