from enum import Enum

__author__ = "Jérémy Farnault"


class ActionType(Enum):
    """
    ENUM DES DIFFERENTS ACTIONS POSSIBLES POUR LES HEROS
    """

    ATTACK = "Attack"
    ATTACK_ARMOR = "Attack armor"
    DEFENSE = "Defense"
    MAGIC = "Magic"
    MOVEMENT = "Movement"
    NONE = "None"
    RANGED_ATTACK = "Ranged attack"
