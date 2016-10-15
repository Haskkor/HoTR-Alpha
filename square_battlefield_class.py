import constants
import pygame

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
        self.update_rect()

    def render_available(self):
        """
        Case disponible, carré jaune légèrement transparent, bords solides, 50*50
        """
        self.pos_x = self.orig_pos_x
        self.pos_y = self.orig_pos_y
        self.render = pygame.Surface((constants.SquareBattlefield.SQUARE, constants.SquareBattlefield.SQUARE),
                                     pygame.SRCALPHA)
        self.render.fill(constants.Colors.ELECTRIC_BLUE_150_ALPHA)
        pygame.draw.rect(self.render, constants.Colors.ELECTRIC_BLUE, (0, 0, constants.SquareBattlefield.SQUARE - 1,
                                                                       constants.SquareBattlefield.SQUARE - 1),
                         constants.SquareBattlefield.THICK_SMALL)
        self.update_rect()

    def render_hero_attack(self):
        """
        Case disponible pour attaque, carré orange, vide, bords solides, 25*25
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
        self.update_rect()

    def render_hero_magic(self):
        """
        Case disponible pour magie, carré violet, intérieur gris très transparent, bords solides, 25*25
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
        self.update_rect()

    def update_rect(self):
        self.rect = self.render.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        if self.hero is not None:
            self.hero.battlefield_rect.centerx = self.rect.centerx
            self.hero.battlefield_rect.bottom = self.rect.centery + constants.SquareBattlefield.HEROES_MARGIN_BOT
