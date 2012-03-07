# *-* coding: iso-8859-1 *-*
import unittest
from foret_action import *

class TestForetAction(unittest.TestCase):
    def setUp(self):
        # On crée un arbre avec une racine vide, sans fils. Le curseur est placé sur
        # la racine
        self.a = ForetAction()


if __name__ == '__main__':
    unittest.main()
