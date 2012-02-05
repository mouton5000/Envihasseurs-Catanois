# *-* coding: iso-8859-1 *-*


class ForetAction:
    ''' Classe représentant une forêt dont les arbres sont placés les uns à la suite.
    Chaque noeud contient un ensemble d'étiquettes qu'il enregistre. Puis un curseur
    peut se ballader de pere en fils ou de frere en frere. Si le curseur est au bout
    d'un arbre est qu'on souhaite voir le fils, le curseur passe à l'arbre suivant.'''


    def __init__(self):
        na = NoeudAction()
        self.roots = [na]
        self.noeud_courrant = na
        self.nbOfNodes = 1;

    def size(self):
        ''' Renvoie le nombre de noeuds total de la foret'''
        return self.nbOfNodes

    def addChild(self):
        ''' Ajoute un fils à la fin de la liste des fils du noeud courrant'''
        self.nbOfNodes += 1
        na = NoeudAction()
        nc = self.noeud_courrant
        nc.addChild(na)
    
    def addChildAt(self,index):
        ''' Ajoute un fils à la liste des fils du noeud courrant en position index'''
        self.nbOfNodes += 1
        na = NoeudAction()
        nc = self.noeud_courrant
        nc.addChildAt(na,index)

    def addRoot(self):
        ''' Ajoute un arbre à la forêt dans la position immédiatement après l'arbre
        du noeud courrant'''
        self.nbOfNodes += 1
        r = self.noeud_courrant.getRoot()
        i = self.roots.index(r)
        na = NoeudAction()
        self.roots.insert(i+1,na)

    def moveCursor(self,index):
        ''' Déplace le curseur sur le noeud de position index de la forêt'''
        nc = self.roots[0]
        i = 0
        s = nc.size()
        while(s <= index):
            index -= s
            i += 1
            if i >= len(self.roots):
                self.noeud_courrant = 0
            nc = self.roots[i]
            s = nc.size()
        self.noeud_courrant = nc.getNoeud(index)

    def moveChild(self):
        ''' Déplace le curseur sur le premier fils sur noeud courrant, s'il n'existe pas
            le déplace sur la racine de l'arbre d'action suivant.'''
        na = self.noeud_courrant.firstChild()
        if (na == 0):
            r = self.noeud_courrant.getRoot()
            i = self.roots.index(r)
            if (i == len(self.roots)-1):
                return
            else:
                self.noeud_courrant = self.roots[i+1]
        else:
            self.noeud_courrant = na


    def moveSibling(self):
        ''' Déplace le curseur sur le frere du noeud courrant s'il existe. Sinon ne
            se déplace pas'''
        na = self.noeud_courrant.sibling()
        if na != 0:
            self.noeud_courrant = na
    
    def remove(self):
        ''' Supprime le noeud courrant. Déplace tous ses fils sur sa position et les
        suivantes puis place le curseur sur son premier fils, ou frère s'il n'en a pas
        ou la racine de l'arbre suivant s'il n'en a pas.'''
        nc = self.noeud_courrant
        b = True
        if len(nc.fils)!=0:
            self.moveChild()
        else: 
            self.moveSibling()
            if self.noeud_courrant == nc:
                self.moveChild()
                if self.noeud_courrant == nc:
                    b = False

        if nc != 0:
            self.nbOfNodes -= 1
        else:
            return
        if nc in self.roots:
            i = self.roots.index(nc)
            self.roots.remove(nc)
            for f in nc.fils:
                self.roots.insert(i,f)
                i+=1
        nc.remove()
        if not b:
            self.moveCursor(self.size()-1)
     
    def appendLabel(self,label):
        ''' Ajoute l'étiquette label en fin de liste des étiquettes du noeud courrant'''
        self.noeud_courrant.appendLabel(label)

    def insertLabel(self,index,label):
        ''' Ajoute l'étiquette label en position index des étiquettes du noeud courrant'''
        self.noeud_courrant.insertLabel(index,label)

    def removeLabel(self,index):
        ''' Supprime l'étiquette en position index des étiquettes du noeud courrant'''
        self.noeud_courrant.removeLabel(index)

    def getLabels(self):
        ''' Renvoie les étiquettees du noeud courrant'''
        return self.noeud_courrant.getLabels()
    
    def sizeArbre(self, index):
        ''' Renvoie la taille de l'arbre numéro index de la foret'''
        return self.roots[index].size()
 

    def sizeArbres(self):
        ''' Renvoie le nombre d'arbres de la forêt'''
        return len(self.roots)
 
    def __str__(self):
        s = ''
        for r in self.roots:
            s+=str(r)+' '
        return s

class NoeudAction:
    ''' Noeud d'un arbre d'action pouvant contenir des étiquettes'''

    def __init__(self):
        self.pere = 0
        self.fils = []
        self.labels = []


    def __str__(self):
        s = str(self.labels)
        for na in self.fils:
            s += str(na)
        s += '$'
        return s


    def addChild(self,na):
        ''' Ajoute na en temps que dernier fils'''
        self.fils.append(na)
        na.pere = self

    def addChildAt(self,na,index):
        ''' Ajoute na en fils en position index'''
        self.fils.insert(index,na)
        na.pere = self

    def nbChilds(self):
        ''' Renvoie le nombre de fils'''
        return len(self.fils)

    def remove(self):
        ''' Supprime tous les liens de ce noeud avec son pere et ses fils
        puis relie le pere et les fils. Supprime également toutes les étiquettes'''
        p = self.pere

        if p!=0:
            i = p.fils.index(self)
            p.fils.remove(self)
        else:
            i = -1

        for na in self.fils:
            na.pere = p
            if p != 0:
                p.fils.insert(i,na)
                i+=1
            

        self.pere = 0
        self.fils = []
        self.labels = []


    def size(self):
        ''' Renvoie la taille du sous arbre enraciné en ce noeud'''
        s = 1
        for nc in self.fils:
            s += nc.size()
        return s

    def getNoeud(self,index):
        if(index == 0):
            return self
        elif len(self.fils) == 0:
            return 0
        else:
            index -= 1
            nc = self.fils[0]
            i = 0
            s = nc.size()
            while(s <= index):
                index -= s
                i += 1
                if (i>= len(self.fils)):
                    return 0
                nc = self.fils[i]
                s = nc.size()
            return nc.getNoeud(index)

    def appendLabel(self,label):
        ''' Ajoute label à la fin des étiquettes de ce noeud'''
        self.labels.append(label)
    
    def insertLabel(self,index,label):
        ''' Ajoute l'étiquette label en position index des étiquettes de ce noeud'''
        self.labels.insert(index,label)

    def removeLabel(self,index):
        ''' Supprime l'étiquette en position index des étiquettes de ce noeud'''
        self.labels.pop(index)

    def getLabels(self):
        ''' Renvoie tous les étiquettes du noeud'''
        return self.labels

    def getRoot(self):
        ''' Renvoie la racine de l'arbre contenant ce noeud'''
        nc = self
        while nc.pere != 0:
            nc = nc.pere
        return nc

    def firstChild(self):
        ''' Renvoie s'il existe le premier fils de ce noeud, ou 0 sinon'''
        if len(self.fils) > 0:
            return self.fils[0]
        else:
            return 0

    def sibling(self):
        ''' Renvoie s'il existe le frere droit de ce noeud, ou 0 sinon.'''
        p = self.pere
        if(p != 0):
            i = p.fils.index(self)
            if i != len(p.fils)-1:
                return p.fils[i+1]
        return 0
