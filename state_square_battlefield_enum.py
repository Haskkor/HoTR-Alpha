from enum import Enum

__author__ = "Jérémy Farnault"


class StateSquareBattlefield(Enum):
    """
    ENUM DES DIFFERENTS ETATS POSSIBLES POUR LES CASES DU CHAMP DE BATAILLE
    """

    current = "CURRENT"
    hero = "HERO"
    hero_selected = "HERO_SELECTED"
    hero_hovered = "HERO_HOVERED"
    available = "AVAILABLE"
    available_hovered = "AVAILABLE_HOVERED"
    selected_hovered = "SELECTED_HOVERED"
    hero_attack = "HERO_ATTACK"
    hero_magic = "HERO_MAGIC"
    foe = "FOE"
    foe_hovered = "FOE_HOVERED"
    foe_selected = "FOE_SELECTED"
    none = "NONE"
