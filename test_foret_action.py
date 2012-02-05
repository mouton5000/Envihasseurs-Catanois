# *-* coding: iso-8859-1 *-*
import unittest
from foret_action import *

class TestForetAction(unittest.TestCase):
    def setUp(self):
        # On crée un arbre avec une racine vide, sans fils. Le curseur est placé sur
        # la racine
        self.a = ForetAction()

    def test_ajouter_noeuds(self):
        a = self.a
        self.assertEqual(a.size(),1)
        # On ajoute un fils au noeuds courrant, en dernière position.
        a.addChild()
        self.assertEqual(a.size(),2)
        a.moveCursor(1)
        a.appendLabel('1') # On écrit 1 sur le fils
        a.moveCursor(0)
        a.addChild() # On ajoute un fils en tant que frère droit du fils précédent
        self.assertEqual(a.size(),3)
        a.moveCursor(1)
        self.assertEqual(a.getLabels(),['1'])
        a.moveCursor(2)
        self.assertEqual(a.getLabels(),[])
        a.moveCursor(0)
        a.addChildAt(0) # On ajoute un fils en tant que frère gauche du premier fils.
        self.assertEqual(a.size(),4)
        a.moveCursor(1)
        self.assertEqual(a.getLabels(),[])
        a.moveCursor(2)
        self.assertEqual(a.getLabels(),['1'])

        # On ajoute une racine. Située après l' arbre dans lequel se trouve le
        # curseur
        a.addRoot()
        a.moveCursor(4)
        
        a.appendLabel('R2')
        self.assertEqual(a.sizeArbres(),2)
        self.assertEqual(a.sizeArbre(0),4)
        self.assertEqual(a.sizeArbre(1),1)

        a.moveCursor(2)
        a.addChild()
        self.assertEqual(a.size(),6)
        self.assertEqual(a.sizeArbre(0),5)
        self.assertEqual(a.sizeArbre(1),1)
        a.moveCursor(5)
        self.assertEqual(a.getLabels(),['R2'])
        
        a.moveCursor(2)
        a.addRoot()
        self.assertEqual(a.size(),7)
        self.assertEqual(a.sizeArbres(),3)
        self.assertEqual(a.sizeArbre(0),5)
        self.assertEqual(a.sizeArbre(1),1)
        self.assertEqual(a.sizeArbre(2),1)
        a.moveCursor(5)
        self.assertEqual(a.getLabels(),[])
        a.moveCursor(6)
        self.assertEqual(a.getLabels(),['R2'])
        
    
    def test_deplacer_curseur(self):

        a = self.a

        a.addChild()
        a.addChild()
        a.addChild()

        a.moveCursor(1)
        a.addChild()
        a.addChild()
        
        a.addRoot()

        a.moveCursor(0)
        a.appendLabel("R1")
        a.moveCursor(1)
        a.appendLabel("F1")
        a.moveCursor(2)
        a.appendLabel("PF1")
        a.moveCursor(3)
        a.appendLabel("PF2")
        a.moveCursor(4)
        a.appendLabel("F2")
        a.moveCursor(5)
        a.appendLabel("F3")
        a.moveCursor(6)
        a.appendLabel("R2")

        a.moveCursor(0)
        self.assertEqual(a.getLabels(),["R1"])
        a.moveChild()
        self.assertEqual(a.getLabels(),["F1"])
        a.moveSibling()
        self.assertEqual(a.getLabels(),["F2"])
        a.moveSibling()
        self.assertEqual(a.getLabels(),["F3"])
        a.moveSibling()
        self.assertEqual(a.getLabels(),["F3"])
        a.moveChild()
        self.assertEqual(a.getLabels(),["R2"])
        
        a.moveCursor(0)
        a.moveChild()
        a.moveSibling()
        a.moveChild()
        self.assertEqual(a.getLabels(),["R2"])
       
        a.moveCursor(0)
        a.moveChild()
        a.moveChild()
        self.assertEqual(a.getLabels(),["PF1"])
        a.moveChild()
        self.assertEqual(a.getLabels(),["R2"])

        a.moveCursor(0)
        a.moveChild()
        a.moveChild()
        a.moveSibling()
        self.assertEqual(a.getLabels(),["PF2"])
        a.moveChild()
        self.assertEqual(a.getLabels(),["R2"])


    def test_remove(self):
        a = self.a

        a.addChild()
        a.addChild()
        a.addChild()

        a.moveCursor(1)
        a.addChild()
        a.addChild()
        
        a.addRoot()

        a.moveCursor(0)
        a.appendLabel("R1")
        a.moveCursor(1)
        a.appendLabel("F1")
        a.moveCursor(2)
        a.appendLabel("PF1")
        a.moveCursor(3)
        a.appendLabel("PF2")
        a.moveCursor(4)
        a.appendLabel("F2")
        a.moveCursor(5)
        a.appendLabel("F3")
        a.moveCursor(6)
        a.appendLabel("R2")

        # On supprime le noeud courrant, il passe automatiquement au noeud fils, ou si c'est impossible, au noeud frere ou si c'est impossible au dernier noeud de la foret.
        # Les fils remontent tous d'un cran dans l'arbre. Si il s'agissait de la racine, alors tous les fils deviennent racine.
        a.moveCursor(4)
        a.remove()
        self.assertEqual(a.size(),6)
        self.assertEqual(a.sizeArbres(),2)
        self.assertEqual(a.sizeArbre(0),5)
        self.assertEqual(a.sizeArbre(1),1)
        self.assertEqual(a.getLabels(),['F3'])

        a.remove()
        self.assertEqual(a.getLabels(),['R2'])
        
        a.remove()
        self.assertEqual(a.getLabels(),['PF2'])
        
        a.moveCursor(0)
        a.addChild()
        a.addChild()

        a.moveCursor(4)
        a.appendLabel("F2")
        a.moveCursor(5)
        a.appendLabel("F3")

        a.addRoot()
        a.moveCursor(6)
        a.appendLabel("R2")

        a.moveCursor(1)
        a.remove()
        self.assertEqual(a.getLabels(),['PF1'])
        a.moveCursor(2)
        self.assertEqual(a.getLabels(),['PF2'])

        a.moveCursor(0)
        a.moveChild()
        self.assertEqual(a.getLabels(),['PF1'])
        a.moveSibling()
        a.moveSibling()
        self.assertEqual(a.getLabels(),['F2'])
        
        a.remove()
        a.remove()
        
        a.moveCursor(1)
        a.addChild()
        a.addChild()

        a.moveCursor(0)
        a.remove()
        self.assertEqual(a.size(),5)
        self.assertEqual(a.sizeArbres(),3)
        self.assertEqual(a.sizeArbre(0),3)
        self.assertEqual(a.sizeArbre(1),1)
        self.assertEqual(a.sizeArbre(2),1)


    def test_labels(self):
        a = self.a
        a.appendLabel("r1")
        a.appendLabel(["wha",1,2])

        self.assertEqual(a.getLabels(),["r1",["wha",1,2]])

        a.insertLabel(1,0)
        self.assertEqual(a.getLabels(),["r1",0,["wha",1,2]])
 
        a.removeLabel(2)
        self.assertEqual(a.getLabels(),["r1",0])

if __name__ == '__main__':
    unittest.main()
