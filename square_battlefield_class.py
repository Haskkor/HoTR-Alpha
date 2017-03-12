import pygame

import constants
from state_square_battlefield_enum import StateSquareBattlefield

__author__ = "Jérémy Farnault"


class SquareBattlefield:
    """
    OBJETS CARRES DU CHAMP DE BATAILLE
    """

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.orig_pos_x = pos_x + constants.SquareBattlefield.START_X
        self.orig_pos_y = pos_y + constants.SquareBattlefield.START_Y
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.LITTLE_SQUARE,
                                      constants.SquareBattlefield.LITTLE_SQUARE), pygame.SRCALPHA)
        self.rect = None
        self.hero = None
        self.state = None
        self.has_grave = False
        self.ap_movement_1 = pygame.image.load(constants.ImagesPath.ACTION_POINT_MOUSE_PATH)
        self.ap_movement_1_rect = self.ap_movement_1.get_rect()
        self.ap_movement_2 = pygame.image.load(constants.ImagesPath.ACTION_POINT_MOUSE_PATH)
        self.ap_movement_2_rect = self.ap_movement_2.get_rect()
        self.grave_icon = pygame.image.load(constants.ImagesPath.GRAVE)
        self.grave_icon_rect = self.grave_icon.get_rect()
        self.movement_cost = 0
        self.update_rect()

    def render_current(self):
        """
        Héro courant, carré bleu électrique vide, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.HEROES // 2
        self.pos_y = self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.HEROES // 2
        self.render = pygame.Surface((constants.SquareBattlefield.HEROES, constants.SquareBattlefield.HEROES),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.ELECTRIC_BLUE, (0, 0, constants.SquareBattlefield.HEROES - 1,
                                                                       constants.SquareBattlefield.HEROES - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.current
        self.update_rect()

    def render_current_hovered(self):
        """
        Héro courant survolé, rond bleu électrique, vide, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)

        pygame.draw.circle(self.render, constants.Colors.ELECTRIC_BLUE, (constants.SquareBattlefield.SQUARE // 2,
                                                                         constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.current_hovered
        self.update_rect()

    def render_current_selected(self):
        """
        Héro courant sélectionné, rond bleu électrique légèrement transparent, bords solides, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.ELECTRIC_BLUE_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.ELECTRIC_BLUE, (constants.SquareBattlefield.SQUARE // 2,
                                                                         constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.current_selected
        self.update_rect()

    def render_hero(self):
        """
        Héro inactif : carré gris vide, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.HEROES // 2
        self.pos_y = self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.HEROES // 2
        self.render = pygame.Surface((constants.SquareBattlefield.HEROES, constants.SquareBattlefield.HEROES),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.DARK_SLATE_GRAY, (0, 0, constants.SquareBattlefield.HEROES - 1,
                                                                         constants.SquareBattlefield.HEROES - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero
        self.update_rect()

    def render_hero_selected(self):
        """
        Héro sélectionné, rond jaune légèrement transparent, bords solides, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.GOLD_150_ALPHA, (constants.SquareBattlefield.SQUARE // 2,
                                                                          constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.GOLD, (constants.SquareBattlefield.SQUARE // 2,
                                                                constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_selected
        self.update_rect()

    def render_hero_hovered(self):
        """
        Héro survolé, rond jaune, vide, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)

        pygame.draw.circle(self.render, constants.Colors.GOLD, (constants.SquareBattlefield.SQUARE // 2,
                                                                constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_hovered
        self.update_rect()

    def render_foe(self):
        """
        Ennemi inactif, carré rouge vide, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.HEROES // 2
        self.pos_y = self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.HEROES // 2
        self.render = pygame.Surface((constants.SquareBattlefield.HEROES, constants.SquareBattlefield.HEROES),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.DARK_RED, (0, 0, constants.SquareBattlefield.HEROES - 1,
                                                                  constants.SquareBattlefield.HEROES - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.foe
        self.update_rect()

    def render_foe_hovered(self):
        """
        Ennemi survolé, rond rouge, vide, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.RED, (constants.SquareBattlefield.SQUARE // 2,
                                                               constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.foe_hovered
        self.update_rect()

    def render_foe_selected(self):
        """
        Ennemi sélectionné, rond rouge légèrement transparent, bords solides, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.RED_150_ALPHA, (constants.SquareBattlefield.SQUARE // 2,
                                                                         constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.RED, (constants.SquareBattlefield.SQUARE // 2,
                                                               constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.foe_selected
        self.update_rect()

    def render_available(self):
        """
        Case disponible, carré bleu électrique légèrement transparent, bords solides, 50*50
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.ELECTRIC_BLUE_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.ELECTRIC_BLUE, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                       constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.available
        self.update_rect()

    def render_available_hovered(self, in_battle=False, semi_movement=False):
        """
        Case disponible survolé, carré bleu royal légèrement transparent, bords solides, 50*50, images représentant
        les points d'action
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.ROYAL_BLUE_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.ELECTRIC_BLUE, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                       constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        # Affiche les points d'action nécessaires pour effectuer le mouvement
        self.movement_cost = 0
        if in_battle:
            self.manage_action_points(semi_movement)
        self.state = StateSquareBattlefield.available_hovered
        self.update_rect()

    def render_selected_hovered(self, semi_movement=False):
        """
        Case sélectionnée pour le mouvement et survolée, rond bleu royal légèrement transparent, bords solides,
        diamètre 44, images représentant les points d'action
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.ROYAL_BLUE_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.ELECTRIC_BLUE, (constants.SquareBattlefield.SQUARE // 2,
                                                                         constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.manage_action_points(semi_movement)
        self.state = StateSquareBattlefield.selected_hovered
        self.update_rect()

    def render_hero_attack(self):
        """
        Case disponible pour l'attaque, carré orange, vide, bords solides, 25*25
        """
        self.pos_x = \
            self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.pos_y = \
            self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.render = pygame.Surface((constants.SquareBattlefield.LITTLE_SQUARE,
                                      constants.SquareBattlefield.LITTLE_SQUARE), pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.ORANGE_RED, (0, 0, constants.SquareBattlefield.LITTLE_SQUARE - 1,
                                                                    constants.SquareBattlefield.LITTLE_SQUARE - 1),
                         constants.SquareBattlefield.THICK_BIG)
        self.state = StateSquareBattlefield.hero_attack
        self.update_rect()

    def render_hero_attack_with_foe(self):
        """
        Case disponible pour l'attaque avec ennemi, carré orange légèrement transparent, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.ORANGE_RED_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.ORANGE_RED, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                    constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_attack_with_foe
        self.update_rect()

    def render_hero_attack_with_foe_hovered(self):
        """
        Case disponible pour l'attaque avec ennemi survolée, rond orange légèrement transparent, bords solides,
        diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.ORANGE_RED_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.ORANGE_RED, (constants.SquareBattlefield.SQUARE // 2,
                                                                      constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_attack_with_foe_hovered
        self.update_rect()

    def render_hero_magic(self):
        """
        Case disponible pour la magie, carré violet, intérieur gris très transparent, bords solides, 25*25
        """
        self.pos_x = \
            self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.pos_y = \
            self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.render = pygame.Surface((constants.SquareBattlefield.LITTLE_SQUARE,
                                      constants.SquareBattlefield.LITTLE_SQUARE), pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.PURPLE, (0, 0, constants.SquareBattlefield.LITTLE_SQUARE - 1,
                                                                constants.SquareBattlefield.LITTLE_SQUARE - 1),
                         constants.SquareBattlefield.THICK_BIG)
        self.state = StateSquareBattlefield.hero_magic
        self.update_rect()

    def render_hero_magic_with_foe(self):
        """
        Case disponible pour la magie avec ennemi, carré violet légèrement transparent, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.PURPLE_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.PURPLE, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_magic_with_foe
        self.update_rect()

    def render_hero_magic_with_foe_hovered(self):
        """
        Case disponible pour la magie avec ennemi survolée, rond violet légèrement transparent, bords solides,
        diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.PURPLE_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.PURPLE, (constants.SquareBattlefield.SQUARE // 2,
                                                                  constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_magic_with_foe_hovered
        self.update_rect()

    def render_hero_ranged_attack(self):
        """
        Case disponible pour l'attaque à distance, carré violet, intérieur gris très transparent, bords solides, 25*25
        """
        self.pos_x = \
            self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.pos_y = \
            self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.render = pygame.Surface((constants.SquareBattlefield.LITTLE_SQUARE,
                                      constants.SquareBattlefield.LITTLE_SQUARE), pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.GREEN, (0, 0, constants.SquareBattlefield.LITTLE_SQUARE - 1,
                                                               constants.SquareBattlefield.LITTLE_SQUARE - 1),
                         constants.SquareBattlefield.THICK_BIG)
        self.state = StateSquareBattlefield.hero_ranged_attack
        self.update_rect()

    def render_hero_ranged_attack_with_foe(self):
        """
        Case disponible pour l'attaque à distance avec ennemi, carré violet légèrement transparent, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.GREEN_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.GREEN, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                               constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_ranged_attack_with_foe
        self.update_rect()

    def render_hero_ranged_attack_with_foe_hovered(self):
        """
        Case disponible pour l'attaque à distance avec ennemi survolée, rond violet légèrement transparent,
        bords solides, diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.GREEN_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.GREEN, (constants.SquareBattlefield.SQUARE // 2,
                                                                 constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_ranged_attack_with_foe_hovered
        self.update_rect()

    def render_hero_attack_armor(self):
        """
        Case disponible pour l'attaque contre l'armure, carré bronze, vide, bords solides, 25*25
        """
        self.pos_x = \
            self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.pos_y = \
            self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.render = pygame.Surface((constants.SquareBattlefield.LITTLE_SQUARE,
                                      constants.SquareBattlefield.LITTLE_SQUARE), pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.BRONZE, (0, 0, constants.SquareBattlefield.LITTLE_SQUARE - 1,
                                                                constants.SquareBattlefield.LITTLE_SQUARE - 1),
                         constants.SquareBattlefield.THICK_BIG)
        self.state = StateSquareBattlefield.hero_attack_armor
        self.update_rect()

    def render_hero_attack_armor_with_foe(self):
        """
        Case disponible pour l'attaque avec ennemi, carré bronze légèrement transparent, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BRONZE_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.BRONZE, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_attack_armor_with_foe
        self.update_rect()

    def render_hero_attack_armor_with_foe_hovered(self):
        """
        Case disponible pour l'attaque avec ennemi survolée, rond bronze légèrement transparent, bords solides,
        diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.BRONZE_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.BRONZE, (constants.SquareBattlefield.SQUARE // 2,
                                                                  constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_attack_armor_with_foe_hovered
        self.update_rect()

    def render_hero_defense(self):
        """
        Case disponible pour la défense pour le héro, carré gris foncé légèrement transparent, bords solides, 44*44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.LIGHT_GRAY_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.LIGHT_GRAY, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                    constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_defense
        self.update_rect()

    def render_hero_defense_hovered(self):
        """
        Case disponible pour la défense pour le héro survolée, rond gris foncé légèrement transparent, bords solides,
        diamètre 44
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.circle(self.render, constants.Colors.LIGHT_GRAY_150_ALPHA,
                           (constants.SquareBattlefield.SQUARE // 2, constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, 0)
        pygame.draw.circle(self.render, constants.Colors.LIGHT_GRAY, (constants.SquareBattlefield.SQUARE // 2,
                                                                      constants.SquareBattlefield.SQUARE // 2),
                           constants.SquareBattlefield.CIRCLE_HEROES, constants.SquareBattlefield.THICK_SMALL)
        self.state = StateSquareBattlefield.hero_defense_hovered
        self.update_rect()

    def render_grave(self):
        """
        Affiche une tombe à l'emplacement d'un héro mort
        """
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.BLACK_FULL_ALPHA)
        self.grave_icon_rect.centerx = self.render.get_rect().centerx
        self.grave_icon_rect.centery = self.render.get_rect().centery
        self.render.blit(self.grave_icon, self.grave_icon_rect)
        self.state = StateSquareBattlefield.grave
        self.update_rect()

    def render_none(self):
        """
        Case vide, carré gris légèrement transparent, pas de bords, 25*25
        """
        self.pos_x = \
            self.orig_pos_x + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.pos_y = \
            self.orig_pos_y + constants.SquareBattlefield.SQUARE // 2 - constants.SquareBattlefield.LITTLE_SQUARE // 2
        self.render = pygame.Surface((constants.SquareBattlefield.LITTLE_SQUARE,
                                      constants.SquareBattlefield.LITTLE_SQUARE), pygame.SRCALPHA)
        self.render.fill(constants.Colors.DARK_SLATE_GRAY_100_ALPHA)
        self.state = None
        self.update_rect()

    def manage_action_points(self, semi_movement):
        """
        Affiche et calcule le nombre de points d'action en fonction de la position de la case
        """
        if semi_movement:
            self.ap_movement_1_rect.centerx = self.render.get_rect().centerx
            self.ap_movement_1_rect.centery = self.render.get_rect().centery
            self.render.blit(self.ap_movement_1, self.ap_movement_1_rect)
            self.movement_cost = 1
        else:
            self.ap_movement_1_rect.centerx = \
                self.render.get_rect().centerx - constants.SquareBattlefield.MOVEMENT_ACTION_POINTS_PADDING
            self.ap_movement_1_rect.centery = self.render.get_rect().centery
            self.render.blit(self.ap_movement_1, self.ap_movement_1_rect)
            self.ap_movement_2_rect.centerx = \
                self.render.get_rect().centerx + constants.SquareBattlefield.MOVEMENT_ACTION_POINTS_PADDING
            self.ap_movement_2_rect.centery = self.render.get_rect().centery
            self.render.blit(self.ap_movement_2, self.ap_movement_2_rect)
            self.movement_cost = 2

    def update_rect(self):
        self.rect = self.render.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        if self.hero is not None:
            self.hero.battlefield_rect.centerx = self.rect.centerx
            self.hero.battlefield_rect.bottom = self.rect.centery + constants.SquareBattlefield.HEROES_MARGIN_BOT
