# *-* coding: utf8 *-*

class ActionError(Exception):
    def __init__(self,value):
        self.error_code = value

class ColonieError(ActionError):
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
        ActionError.__init__(self,value)

class RouteError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec une route'''
    JOUEUR_EN_RUINE = 0
    ARRETE_OCCUPEE = 1
    ARRETE_MARITIME = 2
    RESSOURCES_INSUFFISANTES = 3
    ARRETE_NON_RELIEE = 4

    def __init__(self,value):
        ActionError.__init__(self,value)

class BateauError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec une route'''

    JOUEUR_EN_RUINE = 0
    ARRETE_NON_CONSTRUCTIBLE = 1 # Survient si on essaie de construire un bateau sur la terre ou trop loin de la cote
    RESSOURCES_INSUFFISANTES = 2
    ARRETE_NON_RELIEE = 3 # Survient si on essaie de construire un bateau la où aucune colonie n'est presente

    BATEAU_INEXISTANT = 4 # Survient si on essaie d'evoluer, construire ou echanger avec un bateau nul
    NON_PROPRIETAIRE = 5 # Survient si on essaie d'effectuer une action avec un bateau dont on est pas proprietaire
    BATEAU_PIRATE = 6
    ARRETE_TERRESTRE = 7 # Survient si on essaie de déplacer un bateau sur la terre
    ARRETE_INATTEIGNABLE = 8
    BATEAU_DEJA_DEPLACE = 9

    PAS_EMPLACEMENT_ECHANGE = 10
    DEJA_EVOLUE = 11

    FLUX_TROP_ELEVE = 12 # Survient si on essaie d'echanger avec un bateau des sommes non compatibles avec les ressources du joueurs ou du bateau, ou avec la place disponible dans le bateau
    FLUX_IMPOSSIBLE = 13 # Survient si on essaie d'echanger des sommes non entieres ou négatives

    TERRE_DEJA_COLONISEE = 14
    EMPLACEMENT_INATTEIGNABLE = 15 # Survient si on essaie de coloniser une terre sur un emplacement a plus de trois hexagones du bateau.
    def __init__(self,value):
        ActionError.__init__(self,value)
