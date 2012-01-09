import operator

# Test
class CartesGeneral:
    attributs = ['argile', 'ble', 'bois', 'caillou', 'mouton', 'chevalliers',
                 'monopoles', 'pointsVictoire', 'decouverte',
                 'constructionDeRoute']

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

    def _comparison(self, other, operation):
        return all(operation(getattr(self, att), getattr(other, att))
            for att in CartesGeneral.attributs)

    def __eq__(self,other):
        return self._comparison(other, operator.eq)

    def __add__(self,other):
        args = [getattr(self, att) + getattr(other, att)
                for att in CartesGeneral.attributs]
        return CartesGeneral(*args)

    def __mul__(self,other):
        args = [getattr(self, att) * other
                for att in CartesGeneral.attributs]
        return CartesGeneral(*args)

    def __sub__(self,other):
        return self + other*(-1)

    def size(self):
        return sum(getattr(self, att) for att in CartesGeneral.attributs)

    def ressources_size(self):
        return self.argile + self.ble + self.bois + self.caillou + self.mouton

    def __lt__(self,other):
        return self._comparison(other, operator.lt)

    def __gt__(self,other):
        return self._comparison(other, operator.gt)

    def __le__(self,other):
        return self._comparison(other, operator.le)

    def __ge__(self,other):
        return self._comparison(other, operator.ge)

    def __str__(self):
        return '(' +  ', '.join(str(getattr(self, att)) for att in CartesGeneral.attributs) + ')'

    def est_ressource(self):
        return (self.chevalliers == 0 and self.pointsVictoire == 0
                and self.decouverte == 0 and self.constructionDeRoute == 0
                and self.monopoles == 0)

    def est_entier(self):
        return all(isinstance(getattr(self, att), int)
            for att in CartesGeneral.attributs)

    def est_physiquement_possible(self):
        return self >= Cartes.RIEN and self.est_entier()

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




class CartesRessources(CartesGeneral):
    def __init__(self,argile,ble,bois,caillou,mouton):
	CartesGeneral.__init__(self,argile,ble,bois,caillou,mouton,0,0,0,0,0)

    def __str__(self):
        return '(' + str(self.argile) +','+ str(self.ble) + ',' + str(self.bois) + ',' + str(self.caillou) + ',' + str(self.mouton) + ')'


class CartesDeveloppement(CartesGeneral):
    def __init__(self,chevalliers, monopoles, pointsVictoire, decouverte, constructionDeRoute):
        CartesGeneral.__init__(self,0,0,0,0,0,chevalliers, monopoles, pointsVictoire, decouverte, constructionDeRoute)

    def __str__(self):
        return '(' + str(self.chevalliers) +','+ str(self.monopoles) + ',' + str(self.pointsVictoire) + ',' + str(self.decouverte) + ',' + str(self.constructionDeRoute) + ')'

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
