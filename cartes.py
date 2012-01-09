# Test
class CartesGeneral:    

    def __init__(self,argile,ble,bois,caillou,mouton,chevalliers,monopoles,pointsVictoire,decouverte,constructionDeRoute):
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
    
    def __eq__(self,other):
        return self.argile == other.argile and self.ble == other.ble and self.bois == other.bois and self.caillou == other.caillou and self.mouton == other.mouton and self.chevalliers == other.chevalliers and self.monopoles == other.monopoles and self.pointsVictoire == other.pointsVictoire and self.decouverte == other.decouverte and self.constructionDeRoute == other.constructionDeRoute

    def __add__(self,other):
        return CartesGeneral(self.argile + other.argile, self.ble + other.ble, self.bois + other.bois, self.caillou + other.caillou, self.mouton + other.mouton,self.chevalliers + other.chevalliers, self.monopoles + other.monopoles, self.pointsVictoire + other.pointsVictoire, self.decouverte + other.decouverte, self.constructionDeRoute + other.constructionDeRoute)

    def __mul__(self,other):
        return CartesGeneral(self.argile * other, self.ble * other, self.bois * other, self.caillou * other,  self.mouton * other,self.chevalliers * other, self.monopoles * other, self.pointsVictoire * other, self.decouverte * other,  self.constructionDeRoute * other)

    def __sub__(self,other):
        return self + other*(-1)

    def size(self):
        return self.argile + self.ble + self.bois + self.caillou + self.mouton + self.chevalliers + self.monopoles + self.pointsVictoire + self.decouverte + self.constructionDeRoute

    def ressources_size(self):
        return self.argile + self.ble + self.bois + self.caillou + self.mouton
    
    def __lt__(self,other):
        return self.argile < other.argile and self.ble < other.ble and self.bois < other.bois and self.caillou < other.caillou and self.mouton < other.mouton and self.chevalliers < other.chevalliers and self.monopoles < other.monopoles and self.pointsVictoire < other.pointsVictoire and self.decouverte < other.decouverte and self.constructionDeRoute < other.constructionDeRoute

    def __gt__(self,other):
        return self.argile > other.argile and self.ble > other.ble and self.bois > other.bois and self.caillou > other.caillou and self.mouton > other.mouton and self.chevalliers > other.chevalliers and self.monopoles > other.monopoles and self.pointsVictoire > other.pointsVictoire and self.decouverte > other.decouverte and self.constructionDeRoute > other.constructionDeRoute
    
    def __le__(self,other):
        return self.argile <= other.argile and self.ble <= other.ble and self.bois <= other.bois and self.caillou <= other.caillou and self.mouton <= other.mouton and self.chevalliers <= other.chevalliers and self.monopoles <= other.monopoles and self.pointsVictoire <= other.pointsVictoire and self.decouverte <= other.decouverte and self.constructionDeRoute <= other.constructionDeRoute

    def __ge__(self,other):
        return self.argile >= other.argile and self.ble >= other.ble and self.bois >= other.bois and self.caillou >= other.caillou and self.mouton >= other.mouton and self.chevalliers >= other.chevalliers and self.monopoles >= other.monopoles and self.pointsVictoire >= other.pointsVictoire and self.decouverte >= other.decouverte and self.constructionDeRoute >= other.constructionDeRoute

    def __str__(self):
        return '(' + str(self.argile) +','+ str(self.ble) + ',' + str(self.bois) + ',' + str(self.caillou) + ',' + str(self.mouton) + ',' + str(self.chevalliers) +','+ str(self.monopoles) + ',' + str(self.pointsVictoire) + ',' + str(self.decouverte) + ',' + str(self.constructionDeRoute) + ')'

    def est_ressource(self):
        return self.chevalliers == 0 and self.pointsVictoire == 0 and self.decouverte == 0 and self.constructionDeRoute == 0 and self.monopoles == 0

    def est_entier(self):
        return type(self.argile) == int and type(self.bois) == int and type(self.ble) == int and type(self.caillou) == int and type(self.mouton) == int and type(self.chevalliers) == int and type(self.monopoles) == int and type(self.pointsVictoire) == int and type(self.decouverte) == int and type(self.constructionDeRoute) == int

    def est_physiquement_possible(self):
        return self >= Cartes.RIEN and self.est_entier()

    def carte(self,nb):
        if nb <= 0 and nb > self.ressources_size():
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
