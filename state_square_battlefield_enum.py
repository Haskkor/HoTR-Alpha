from enum import Enum

__author__ = "Jérémy Farnault"


class StateSquareBattlefield(Enum):
    """
    ENUM DES DIFFERENTS ETATS POSSIBLES POUR LES CASES DU CHAMP DE BATAILLE
    """

    current = "CURRENT"
    current_hovered = "CURRENT_HOVERED"
    current_selected = "CURRENT_SELECTED"
    hero = "HERO"
    hero_selected = "HERO_SELECTED"
    hero_hovered = "HERO_HOVERED"
    available = "AVAILABLE"
    available_hovered = "AVAILABLE_HOVERED"
    selected_hovered = "SELECTED_HOVERED"
    hero_attack = "HERO_ATTACK"
    hero_attack_armor = "HERO_ATTACK_ARMOR"
    hero_attack_armor_with_foe = "HERO_ATTACK_ARMOR_WITH_FOE"
    hero_attack_armor_with_foe_hovered = "HERO_ATTACK_ARMOR_WITH_FOE_HOVERED"
    hero_attack_with_foe = "HERO_ATTACK_WITH_FOE"
    hero_attack_with_foe_hovered = "HERO_ATTACK_WITH_FOE_HOVERED"
    hero_defense = "HERO_DEFENSE"
    hero_defense_hovered = "HERO_DEFENSE_HOVERED"
    hero_magic = "HERO_MAGIC"
    hero_magic_with_foe = "HERO_MAGIC_WITH_FOE"
    hero_magic_with_foe_hovered = "HERO_MAGIC_WITH_FOE_HOVERED"
    hero_ranged_attack = "HERO_RANGED_ATTACK"
    hero_ranged_attack_with_foe = "HERO_RANGED_ATTACK_WITH_FOE"
    hero_ranged_attack_with_foe_hovered = "HERO_RANGED_ATTACK_WITH_FOE_HOVERED"
    foe = "FOE"
    foe_hovered = "FOE_HOVERED"
    foe_selected = "FOE_SELECTED"
    grave = "GRAVE"
    none = "NONE"
