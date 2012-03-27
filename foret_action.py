# *-* coding: iso-8859-1 *-*
import redis
from plateau import *
from joueurs import *
REDIS = redis.StrictRedis()

class ForetAction:
    ''' Classe représentant une forêt dont les arbres sont placés les uns à la suite.
    Chaque noeud contient un ensemble d'étiquettes qu'il enregistre. Puis un curseur
    peut se ballader de pere en fils ou de frere en frere. Si le curseur est au bout
    d'un arbre est qu'on souhaite voir le fils, le curseur passe à l'arbre suivant.'''



    @staticmethod
    def setNextNode(fatherNode,childNode):
        REDIS.set('N'+str(fatherNode)+':next',childNode)

    @staticmethod
    def getNextNode(fatherNode):
        return int(REDIS.get('N'+str(fatherNode)+':next'))

    @staticmethod
    def hasChild(fatherNode):
        return REDIS.get('N'+str(fatherNode)+':lastChild') != '-1'

    @staticmethod
    def setFatherNode(childNode,fatherNode):
        REDIS.set('N'+str(childNode)+':father',fatherNode)

    @staticmethod
    def getFatherNode(childNode):
        return int(REDIS.get('N'+str(childNode)+':father'))

    @staticmethod
    def setSiblingNode(node,siblingNode):
        REDIS.set('N'+str(node)+':sibling',siblingNode)

    @staticmethod
    def getSiblingNode(node):
        return int(REDIS.get('N'+str(node)+':sibling'))

    @staticmethod
    def hasSiblingNode(node):
        return REDIS.get('N'+str(node)+':sibling') != '-1'

    @staticmethod
    def setPSiblingNode(node,pSiblingNode):
        REDIS.set('N'+str(node)+':psibling',pSiblingNode)

    @staticmethod
    def getPSiblingNode(node):
        return int(REDIS.get('N'+str(node)+':psibling'))
    

    @staticmethod
    def setLastChildNode(fatherNode,lastChildNode):
        REDIS.set('N'+str(fatherNode)+':lastChild',lastChildNode)
 
    @staticmethod
    def getLastChildNode(fatherNode):
        return int(REDIS.get('N'+str(fatherNode)+':lastChild'))
   
    @staticmethod
    def setFirstRoot(node,j):
        REDIS.set('J'+str(j.num)+':racine',node)

    @staticmethod
    def getFirstRoot(j):
        return int(REDIS.get('J'+str(j.num)+':racine'))

    @staticmethod
    def hasRoot(j):
        return REDIS.exists('J'+str(j.num)+':racine')

    @staticmethod
    def setLastRoot(node,j):
        REDIS.set('J'+str(j.num)+':derniereRacine',node)

    @staticmethod
    def getLastRoot(j):
        return int(REDIS.get('J'+str(j.num)+':derniereRacine'))
    
    @staticmethod
    def setNextRoot(root,node):
        REDIS.set('N'+str(root)+':racineSuivante',node)

    @staticmethod
    def getNextRoot(root):
        return int(REDIS.get('N'+str(root)+':racineSuivante'))
    
    @staticmethod
    def hasNextRoot(root):
        return REDIS.get('N'+str(root)+':racineSuivante') != '-1'
    
    @staticmethod
    def setPreviousRoot(root,node):
        REDIS.set('N'+str(root)+':racinePrecedente',node)

    @staticmethod
    def getPreviousRoot(root):
        return int(REDIS.get('N'+str(root)+':racinePrecedente'))

    @staticmethod
    def setNewRoot(j):

        node = ForetAction.getNextNodeId()
        hasRoot = ForetAction.hasRoot(j)
        if hasRoot:
            lastRoot = ForetAction.getLastRoot(j)
            ForetAction.setNextRoot(lastRoot,node)
            ForetAction.setPreviousRoot(node,lastRoot)
        else:
            ForetAction.setFirstRoot(node,j)
            ForetAction.setPreviousRoot(node,-1)
        ForetAction.setLastRoot(node,j)
        ForetAction.setNextRoot(node,-1)
        
        ForetAction.setPlayer(node,j)
        ForetAction.setRoot(node,node)
        ForetAction.setNextNode(node,-1)
        ForetAction.setLastChildNode(node,-1)
        ForetAction.setSiblingNode(node,-1)
        ForetAction.setPSiblingNode(node,-1)
        ForetAction.setFatherNode(node,-1)
    
        ForetAction.incrNodeId()


        if hasRoot: 
            ls = ForetAction.getLeavesOf(lastRoot)
            for n in ls:
                ForetAction.setNextNode(n,node)
        return node

    @staticmethod
    def setNewFirstRoot(j):

        node = ForetAction.getNextNodeId()
        if ForetAction.hasRoot(j):
            firstRoot = ForetAction.getFirstRoot(j)
            ForetAction.setNextRoot(node,firstRoot)
            ForetAction.setPreviousRoot(firstRoot,node)
        else:
            ForetAction.setLastRoot(node,j)
            ForetAction.setNextRoot(node,-1)
        ForetAction.setFirstRoot(node,j)
        ForetAction.setPreviousRoot(node,-1)

        ForetAction.setPlayer(node,j)
        ForetAction.setRoot(node,node)
        ForetAction.setNextNode(node,-1)
        ForetAction.setLastChildNode(node,-1)
        ForetAction.setSiblingNode(node,-1)
        ForetAction.setPSiblingNode(node,-1)
        ForetAction.setFatherNode(node,-1)
        ForetAction.incrNodeId()
        
        return node
    
    @staticmethod
    def setNewNextRoot(root, j):

        node = ForetAction.getNextNodeId()
        lastRoot = ForetAction.getLastRoot(j)
        if lastRoot == root:
            ForetAction.setLastRoot(node,j)
            yyForetAction.setNextRoot(node,-1)
        nroot = ForetAction.getNextRoot(root)
        ForetAction.setNextRoot(node, nroot)
        if nroot != -1:
            ForetAction.setPreviousRoot(nroot,node)
        ForetAction.setNextRoot(root,node)
        ForetAction.setPreviousRoot(node,root)

        ForetAction.setPlayer(node,j)
        ForetAction.setRoot(node,node)
        ForetAction.setNextNode(node,-1)
        ForetAction.setLastChildNode(node,-1)
        ForetAction.setSiblingNode(node,-1)
        ForetAction.setPSiblingNode(node,-1)
        ForetAction.setFatherNode(node,-1)
        ForetAction.incrNodeId()


        ls = ForetAction.getLeavesOf(root)
        for n in ls:
            ForetAction.setNextNode(n,node)
        return node
   
    @staticmethod
    def removeRoot(root):
        j = ForetAction.getPlayer(root)
        froot = ForetAction.getFirstRoot(j)
        lroot = ForetAction.getLastRoot(j)
        nroot = ForetAction.getNextRoot(root)
        proot = ForetAction.getPreviousRoot(root)

        if proot != -1:
            ForetAction.setNextRoot(proot,nroot) 
            ls = ForetAction.getLeavesOf(proot)
            for n in ls:
                ForetAction.setNextNode(n,nroot)
        if nroot != -1:
            ForetAction.setPreviousRoot(nroot,proot)
        if root == froot:
            ForetAction.setFirstRoot(nroot,j)
        if root == lroot:
            ForetAction.setLastRoot(proot,j)
 

        l = ForetAction.selectNodesFromRoot(root)
        for n in l:
            ForetAction.deleteNode(n)
        
        key = 'N'+str(root)
        REDIS.delete(key+':racineSuivante')
        REDIS.delete(key+':racinePrecedente')
        ForetAction.deleteNode(root)

    @staticmethod
    def selectNodesFromRoot(root):
        l = []

        if(not ForetAction.hasChild(root)):
            return l

        node = ForetAction.getNextNode(root)
        while(node != -1):
            l.append(node)
            l.extend(ForetAction.selectNodesFromRoot(node))
            node = ForetAction.getSiblingNode(node)

        return l

    @staticmethod
    def getLeavesOf(root):

        if not ForetAction.hasChild(root):
            return [root]

        l = []
        node = ForetAction.getNextNode(root)
        while(node != -1):
            l.extend(ForetAction.getLeavesOf(node))
            node = ForetAction.getSiblingNode(node)

        return l
    
    @staticmethod
    def setPlayer(node, j):
        REDIS.set('N'+str(node)+':joueur',j.num)

    @staticmethod
    def getPlayer(node):
        jnum = int(REDIS.get('N'+str(node)+':joueur'))
        return Plateau.getPlateau().j(jnum)
 
    @staticmethod
    def setRoot(node, rootNode):
        REDIS.set('N'+str(node)+':root',rootNode)

    @staticmethod
    def getRoot(node):
        return int(REDIS.get('N'+str(node)+':root'))

    @staticmethod
    def deleteNode(node):
        key = 'N'+str(node)
        REDIS.delete(key+':next')
        REDIS.delete(key+':sibling')
        REDIS.delete(key+':psibling')
        REDIS.delete(key+':father')
        REDIS.delete(key+':lastChild')
        REDIS.delete(key+':joueur')
        REDIS.delete(key+':root')

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
    def incrNodeId():
        REDIS.incr('LastNode')
        

    @staticmethod
    def addChild(fatherNode):
        ''' Ajoute un fils à la fin de la liste des fils de fatherNode '''
        lastNode = ForetAction.getNextNodeId()

        if ForetAction.hasChild(fatherNode):
            lastChild = ForetAction.getLastChildNode(fatherNode)
            ForetAction.setSiblingNode(lastChild,lastNode)
            ForetAction.setPSiblingNode(lastNode,lastChild)
        else:
            ForetAction.setNextNode(fatherNode,lastNode)
            ForetAction.setPSiblingNode(lastNode,-1)
        ForetAction.setLastChildNode(fatherNode,lastNode)
        ForetAction.setFatherNode(lastNode,fatherNode)
        ForetAction.setLastChildNode(lastNode,-1)
        ForetAction.setSiblingNode(lastNode,-1)
        ForetAction.incrNodeId()
        root = ForetAction.getRoot(fatherNode)
        ForetAction.setRoot(lastNode, root)
        ForetAction.setPlayer(lastNode, ForetAction.getPlayer(fatherNode))
        
        nextRoot = ForetAction.getNextRoot(root)
        ForetAction.setNextNode(lastNode,nextRoot)

        return lastNode

    @staticmethod
    def addFirstChild(fatherNode):
        ''' Ajoute un fils au début de la liste des fils de fatherNode '''
        lastNode = ForetAction.getNextNodeId()

        if ForetAction.hasChild(fatherNode):
            firstChild = ForetAction.getNextNode(fatherNode)
            ForetAction.setPSiblingNode(firstChild,lastNode)
            ForetAction.setSiblingNode(lastNode,firstChild)
        else:
            ForetAction.setLastChildNode(fatherNode,lastNode)
            ForetAction.setSiblingNode(lastNode,-1)
        ForetAction.setNextNode(fatherNode,lastNode)
        ForetAction.setFatherNode(lastNode,fatherNode)
        ForetAction.setNextNode(lastNode,-1)
        ForetAction.setLastChildNode(lastNode,-1)
        ForetAction.setPSiblingNode(lastNode,-1)
        ForetAction.incrNodeId()
        root = ForetAction.getRoot(fatherNode)
        ForetAction.setRoot(lastNode, root)
        ForetAction.setPlayer(lastNode, ForetAction.getPlayer(fatherNode))
        
        nextRoot = ForetAction.getNextRoot(root)
        ForetAction.setNextNode(lastNode,nextRoot)
        return lastNode
        

    @staticmethod
    def addSibling(node):
        ''' Ajoute un frere à node, le place après node dans la liste des fils du pere de node'''
        lastNode = ForetAction.getNextNodeId()
        
        fatherNode = ForetAction.getFatherNode(node)
        siblingNode = ForetAction.getSiblingNode(node)

        ForetAction.setFatherNode(lastNode,fatherNode)
        ForetAction.setSiblingNode(lastNode,siblingNode)
        if siblingNode != -1:
            ForetAction.setPSiblingNode(siblingNode,lastNode)
        ForetAction.setPSiblingNode(lastNode,node)
        ForetAction.setSiblingNode(node,lastNode)
        ForetAction.setNextNode(lastNode,-1)
        ForetAction.setLastChildNode(lastNode,-1)

        if siblingNode == -1:
            ForetAction.setLastChildNode(fatherNode,lastNode)
        
        ForetAction.incrNodeId()
        root = ForetAction.getRoot(fatherNode)
        ForetAction.setRoot(lastNode, root)
        ForetAction.setPlayer(lastNode, ForetAction.getPlayer(node))
        
        nextRoot = ForetAction.getNextRoot(root)
        ForetAction.setNextNode(lastNode,nextRoot)
        return lastNode
    
    @staticmethod
    def removeNode(node):
        ''' Retire node de son arbre '''
        
        fatherNode = ForetAction.getFatherNode(node)
        siblingNode = ForetAction.getSiblingNode(node)
        pSiblingNode = ForetAction.getPSiblingNode(node)
        childs = []
        child = ForetAction.getNextNode(node)
        while(child != -1):
            childs.append(child)
            child = ForetAction.getSiblingNode(child)

        for child in childs:
            ForetAction.setFatherNode(child,fatherNode)
        if(len(childs) != 0):
            if pSiblingNode != -1:
                ForetAction.setSiblingNode(pSiblingNode,childs[0])
            if siblingNode != -1:
                ForetAction.setPSiblingNode(siblingNode,childs[len(childs)-1])
            ForetAction.setSiblingNode(childs[len(childs)-1],siblingNode)
            ForetAction.setPSiblingNode(childs[0],pSiblingNode)
        else:
            if pSiblingNode != -1:
                ForetAction.setSiblingNode(pSiblingNode,siblingNode)
            if siblingNode != -1:
                ForetAction.setPSiblingNode(siblingNode,pSiblingNode)

        lastChild = ForetAction.getLastChildNode(fatherNode)
        if lastChild == node:
            if(len(childs) != 0):
                ForetAction.setLastChildNode(fatherNode,childs[len(childs)-1])
            else:
                ForetAction.setLastChildNode(fatherNode,pSiblingNode)

        child = ForetAction.getNextNode(fatherNode)
        if(child == node):
            if(len(childs) != 0):
                ForetAction.setNextNode(fatherNode,childs[0])
            else:
                if siblingNode != -1:
                    ForetAction.setNextNode(fatherNode,siblingNode)
                else:
                    nRoot = ForetAction.getNextRoot(ForetAction.getRoot(fatherNode))
                    ForestAction.setNextNode(fatherNode, nRoot)

        ForetAction.deleteNode(node)

    @staticmethod
    def getActions(node):
        ''' Ajoute une action au noeud node, en fin de liste des actions '''
        return REDIS.lrange('N'+str(node)+':actions',0,-1)

    @staticmethod
    def addAction(node,action):
        ''' Ajoute une action au noeud node, en fin de liste des actions '''
        REDIS.rpush('N'+str(node)+':actions',action.num)

    @staticmethod
    def lPushAction(node,action):
        ''' Ajoute une action au noeud node, au début de liste des actions '''
        REDIS.lpush('N'+str(node)+':actions',action.num)
    
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
        ForetAction.insertAction(node,beforeAction,action)

    @staticmethod
    def removeAction(node,action):
        ''' Retire l'action du noeud node '''
        REDIS.lrem('N'+str(node)+':actions',0,action.num)
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

if __name__ == '__main__':
    
    REDIS.flushdb()
    j = Joueur(1)
    Plateau.getPlateau().joueurs = [j]

    j.addRoot()
    ForetAction.addChild(1)

    

    a = Action(1,'hello',1,2,3)
    b = Action(24,'youhou',3,"haa")
    c = Action(12,'test',9,1,3,4,2)
    a.save()
    b.save()
    c.save()

    ForetAction.addAction(2,a)
    ForetAction.addAction(2,b)
    ForetAction.insertAction(2,1,c)
   
    ForetAction.removeAction(2,c) 

 
    ks =  REDIS.keys()
    ks.sort()
    for k in ks:
        print k, REDIS.type(k)
    
    print REDIS.lrange('N2:actions',0,-1)
