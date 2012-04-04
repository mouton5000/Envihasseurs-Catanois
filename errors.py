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
    ''' Ensemble des erreurs associées aux actions en rapport avec un bateau'''

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

class CommerceError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec un échange avec un port ou un marche'''
    
    JOUEUR_EN_RUINE = 0
    RESSOURCES_INSUFFISANTES = 1
    FLUX_IMPOSSIBLE = 2
    TERRE_NON_COLONISEE = 3
    COMMERCE_NON_UTILISABLE = 4 # Survient si le joueur tente d'utiliser un commerce sur lequel il ne possède aucune colonie ou surlequel un voleur est actuellement placé

    def __init__(self,value):
        ActionError.__init__(self,value)

class OrError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec l'or'''
    
    JOUEUR_EN_RUINE = 0
    RESSOURCES_INSUFFISANTES = 1
    FLUX_IMPOSSIBLE = 2
    TERRE_NON_COLONISEE = 3

    def __init__(self,value):
        ActionError.__init__(self,value)

class EchangeError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec l'or'''
   
    JOUEUR_EN_RUINE = 0
    PARTENAIRE_EN_RUINE = 1
    TERRE_NON_COLONISEE = 2
    TERRE_PARTENAIRE_NON_COLONISEE = 3
    FLUX_IMPOSSIBLE = 4
    DON_INCOMPATIBLE = 5
 
    def __init__(self,value):
        ActionError.__init__(self,value)

class DeveloppementError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec une carte de développement'''

    JOUEUR_EN_RUINE = 0
    TERRE_NON_COLONISEE = 1
    CARTE_NON_POSSEDEE = 2
    RESSOURCES_INSUFFISANTES = 3

    # Découverte
    DECOUVERTE_FLUX_IMPOSSIBLE = 4 # Survient si on essaie de récupérer moins ou plus de 2 ressources ou un nombre négatif, ou un nombre non entier de ressource

    # Monopole
    MONOPOLE_FLUX_IMPOSSIBLE = 5 # Survient si le paramètre désignant la ressource est différent d'une seule carte de ressources
    MONOPOLE_NBJOUEURS_TROP_FAIBLE = 6 # Survient si le nb de joueurs choisis est nul
    MONOPOLE_NBJOUEURS_TROP_ELEVE = 7 # Survient si le nombre est supérieur à 4
    MONOPOLE_AUTO_ATTAQUE = 8 # Survient si un joueur se vise lui même avec une carte monopole
    MONOPOLE_JOUEUR_EN_RUINE = 9 # Survient si un des joueurs choisis est en ruine
    MONOPOLE_TERRE_NON_COLONISEE = 10 # Survient si un des joueurs choisis n'a pas colonise cette terre

    # Construction
    CONSTRUCTION_ROUTES_IDENTIQUES = 11
    CONSTRUCTION_EMPLACEMENT_INCORRECT = 12
    def __init__(self,value):
        ActionError.__init__(self,value)
    

class VoleurError(ActionError):
    ''' Ensemble des erreurs associées aux actions en rapport avec le voleur'''

    JOUEUR_EN_RUINE = 0
    TERRE_NON_COLONISEE = 1
    DEPLACEMENT_INTERDIT = 2 # Survient si le joueur n'a pas le droit de déplacer le voleur
    EMPLACEMENT_INTERDIT = 3 # Survient si le joueur tente de déplacer le voleur sur un hexagone non autorisé


    def __init__(self,value):
        ActionError.__init__(self,value)
