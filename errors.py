# *-* coding: utf8 *-*

class ColonieError(Exception):
    ''' Ensemble des erreurs associées aux actions en rapport avec une colonie ou une ville'''

    JOUEUR_EN_RUINE = 0
    EMPLACEMENT_OCCUPE = 1
    EMPLACEMENT_MARITIME = 2
    RESSOURCES_INSUFFISANTES = 3
    EMPLACEMENTS_VOISINS_OCCUPES = 4
    EMPLACEMENT_NON_RELIE = 5

    COLONIE_INEXISTANTE = 6
    COLONIE_DEJA_EVOLUEE = 7
    NON_PROPRIETAIRE = 8
 
    def __init__(self,value):
        self.error_code = value

class RouteError(Exception):
    ''' Ensemble des erreurs associées aux actions en rapport avec une route'''
    JOUEUR_EN_RUINE = 0
    ARRETE_OCCUPEE = 1
    ARRETE_MARITIME = 2
    RESSOURCES_INSUFFISANTES = 3
    ARRETE_NON_RELIEE = 4

    def __init__(self,value):
        self.error_code = value
