import operator

# Cette classe représente les cartes que les joueurs ont en main. 
# Aussi bien les cartes de ressources que les cartes de développement. 
# Elles sont représentées ensembles de la même façon pour la simple
# raison qu'elles sont manipulées de la même façon.
# Il s'agit d'un upplet d'entiers, chaque coordonnée correspond à
# un type de carte.
class CartesGeneral:
    attributs = ['argile', 'ble', 'bois', 'caillou', 'mouton', 'chevalliers',
                 'monopoles', 'pointsVictoire', 'decouverte',
                 'constructionDeRoute']

	# Construit l'upplet de carte manuellement.
    def __init__(self, argile, ble, bois, caillou, mouton, chevalliers,
                 monopoles, pointsVictoire, decouverte, constructionDeRoute):
        self.argile = argile
        self.ble = ble
        self.bois = bois
        self.caillou = caillou
        self.mouton = mouton
        self.chevalliers = chevalliers
        self.monopoles = monopoles
        self.pointsVictoire = pointsVictoire
        self.decouverte = decouverte
        self.constructionDeRoute = constructionDeRoute

	# Renvoie vrai si l'opération appliquée à tout attribut de self et other renvoie vrai.
    def _comparison(self, other, operation):
        return all(operation(getattr(self, att), getattr(other, att))
            for att in CartesGeneral.attributs)

	# Renvoie vrai si les deux mains sont identiques
    def __eq__(self,other):
        return self._comparison(other, operator.eq)

	# Renvoie la fusion des deux mains
    def __add__(self,other):
        args = [getattr(self, att) + getattr(other, att)
                for att in CartesGeneral.attributs]
        return CartesGeneral(*args)

	# Multiplie chaque carte de la main par un nombre other
    def __mul__(self,other):
        args = [getattr(self, att) * other
                for att in CartesGeneral.attributs]
        return CartesGeneral(*args)

	# Renvoie la différence de la première main par la deuxième main
    def __sub__(self,other):
        return self + other*(-1)

	# Renvoie le nombre de cartes en main
    def size(self):
        return sum(getattr(self, att) for att in CartesGeneral.attributs)

	# Renvoie le nombre de ressources en main
    def ressources_size(self):
        return self.argile + self.ble + self.bois + self.caillou + self.mouton

	# Renvoie vrai si la main de other a strictement plus de carte de chaque type que self
    def __lt__(self,other):
        return self._comparison(other, operator.lt)

	# Renvoie vrai si la main de other a strictement moins de carte de chaque type que self. Ce n'est donc pas l'opération inverse de le
    def __gt__(self,other):
        return self._comparison(other, operator.gt)

	# Renvoie vrai si la main de other a plus de carte de chaque type que self
    def __le__(self,other):
        return self._comparison(other, operator.le)

	# Renvoie vrai si la main de other a moins de carte de chaque type que self. Ce n'est donc pas l'opération inverse de lt
    def __ge__(self,other):
        return self._comparison(other, operator.ge)

    def __str__(self):
        return '(' +  ', '.join(str(getattr(self, att)) for att in CartesGeneral.attributs) + ')'

	# Renvoie vrai si la main ne contient que des ressources
    def est_ressource(self):
        return (self.chevalliers == 0 and self.pointsVictoire == 0
                and self.decouverte == 0 and self.constructionDeRoute == 0
                and self.monopoles == 0)

	# Renvoie vrai si la main ne contient que des nombres entiers
    def est_entier(self):
        return all(isinstance(getattr(self, att), int)
            for att in CartesGeneral.attributs)

	# Renvoie vrai si la main ne contient que des entiers positifs
    def est_physiquement_possible(self):
        return self >= Cartes.RIEN and self.est_entier()

	# Renvoie la cartes numéro nb de la main, si elles sont classées dans l'ordre des attributs.
    def carte(self,nb):
        if 0 >= nb > self.ressources_size():
            return 0

        if nb <= self.argile:
            return Cartes.ARGILE
        else:
            nb -= self.argile

        if nb <= self.ble:
            return Cartes.BLE
        else:
            nb -= self.ble

        if nb <= self.bois:
            return Cartes.BOIS
        else:
            nb -= self.bois

        if nb <= self.caillou:
            return Cartes.CAILLOU
        else:
            nb -= self.caillou

        if nb <= self.mouton:
            return Cartes.MOUTON
        else:
            nb -= self.mouton
        return 0

		
	# Renvoie le nombre de carte en main du type désigné.
    def get_cartes_de_type(self,carte):
        if carte == Cartes.ARGILE:
            i = self.argile
        elif carte == Cartes.BLE:
            i = self.ble
        elif carte == Cartes.BOIS:
            i = self.bois
        elif carte == Cartes.CAILLOU:
            i = self.caillou
        elif carte == Cartes.MOUTON:
            i = self.mouton
        elif carte == Cartes.CHEVALLIER:
            i = self.chevalliers
        elif carte == Cartes.MONOPOLE:
            i = self.monopoles
        elif carte == Cartes.DECOUVERTE:
            i = self.decouverte
        elif carte == Cartes.CONSTRUCTION_ROUTES:
            i = self.constructionDeRoute
        elif carte == Cartes.POINT_VICTOIRE:
            i = self.pointsVictoire
        else:
            return 0
        return i



# Permet une petite facilité quand on ne travaille qu'avec des ressources
class CartesRessources(CartesGeneral):
    def __init__(self,argile,ble,bois,caillou,mouton):
	CartesGeneral.__init__(self,argile,ble,bois,caillou,mouton,0,0,0,0,0)

    def __str__(self):
        return '(' + str(self.argile) +','+ str(self.ble) + ',' + str(self.bois) + ',' + str(self.caillou) + ',' + str(self.mouton) + ')'

# Permet une petite facilité quand on ne travaille qu'avec des certes de développement
class CartesDeveloppement(CartesGeneral):
    def __init__(self,chevalliers, monopoles, pointsVictoire, decouverte, constructionDeRoute):
        CartesGeneral.__init__(self,0,0,0,0,0,chevalliers, monopoles, pointsVictoire, decouverte, constructionDeRoute)

    def __str__(self):
        return '(' + str(self.chevalliers) +','+ str(self.monopoles) + ',' + str(self.pointsVictoire) + ',' + str(self.decouverte) + ',' + str(self.constructionDeRoute) + ')'

# Vecteurs unitaires
class Cartes:
    RIEN = CartesGeneral(0,0,0,0,0,0,0,0,0,0)
    ARGILE = CartesRessources(1,0,0,0,0)
    BLE = CartesRessources(0,1,0,0,0)
    BOIS = CartesRessources(0,0,1,0,0)
    CAILLOU = CartesRessources(0,0,0,1,0)
    MOUTON = CartesRessources(0,0,0,0,1)
    CHEVALLIER = CartesDeveloppement(1,0,0,0,0)
    MONOPOLE = CartesDeveloppement(0,1,0,0,0)
    POINT_VICTOIRE = CartesDeveloppement(0,0,1,0,0)
    DECOUVERTE = CartesDeveloppement(0,0,0,1,0)
    CONSTRUCTION_ROUTES = CartesDeveloppement(0,0,0,0,1)
