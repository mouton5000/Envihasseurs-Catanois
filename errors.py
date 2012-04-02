# *-* coding: utf8 *-*

class ColonieError(Exception):
    ''' Ensemble des erreurs associées aux actions en rapport avec une colonie ou une ville'''

    JOUEUR_EN_RUINE = 0
    EMPLACEMENT_OCCUPE = 1
    EMPLACEMENT_MARITIME = 2
    RESSOURCES_INSUFFISANTES = 3
    EMPLACEMENTS_VOISINS_OCCUPES = 4
    EMPLACEMENT_NON_RELIE = 5    
 
    def __init__(self,value):
        self.error_code = value
