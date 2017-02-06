from enum import Enum

__author__ = "Jérémy Farnault"


class ActionType(Enum):
    """
    ENUM DES DIFFERENTS ETATS POSSIBLES POUR LES CASES DU CHAMP DE BATAILLE
    """

    ATTACK = "Attack"
    DEFENSE = "Defense"
    MAGIC = "Magic"
    MOVEMENT = "Movement"
    NONE = "None"
    RANGED_ATTACK = "Ranged attack"
    SPECIAL_ATTACK = "Special attack"
