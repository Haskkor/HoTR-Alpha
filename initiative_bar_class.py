import pygame
import constants
from random import shuffle

from button_text_class import ButtonText

__author__ = "Jérémy Farnault"


class InitiativeBar:
    """
    OBJETS BARRE D'INITIATIVE
    """

    def __init__(self, **kwargs):
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_small_bold = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_small_bold.set_bold(True)
        self.player_team = None
        self.adv_team = None
        self.heroes_sorted = []
        self.surface = pygame.Surface((constants.InitiativeBar.WIDTH, constants.InitiativeBar.HEIGHT), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.right = constants.Window.SCREEN_WIDTH // 2 - constants.InitiativeBar.WIDTH // 2
        self.surface_rect.top = constants.Window.SCREEN_HEIGHT - constants.InitiativeBar.POS_Y
        # Bouton pour afficher le reste des héros
        right = constants.InitiativeBar.START_X_RECT - constants.InitiativeBar.BUTTON_MARGIN
        centery = constants.InitiativeBar.START_Y_LINE
        self.button_more = ButtonText(font=self.font_small_bold, pos_right=right, text=constants.Texts.MORE,
                                      active=False, pos_centery=centery)
        self.fake_rect_but = pygame.Rect(self.button_more.rect)
        self.fake_rect_but.centerx += self.surface_rect.left
        self.fake_rect_but.centery += self.surface_rect.top
        # Bouton pour finir le tour
        left = constants.InitiativeBar.END_LAST_LINE + constants.InitiativeBar.BUTTON_MARGIN
        self.button_end_turn = ButtonText(font=self.font_small_bold, pos_left=left, text=constants.Texts.END_TURN,
                                          active=True, pos_centery=centery)
        self.fake_rect_but_end = pygame.Rect(self.button_end_turn.rect)
        self.fake_rect_but_end.centerx += self.surface_rect.left
        self.fake_rect_but_end.centery += self.surface_rect.top
        self.process_kwargs(kwargs)
        self.first_up = True
        self.sort_heroes()

    def process_kwargs(self, kwargs):
        defaults = {}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def sort_heroes(self):
        """
        Trie les héros par initiative, par speed et si il y a encore des égalités, trie aléatoirement
        """
        if self.adv_team is not None:
            heros_temp = self.player_team + self.adv_team
        else:
            heros_temp = self.player_team
        heros_temp.sort(key=lambda hero: (hero.initiative, hero.speed), reverse=True)
        to_sort = []
        for i in range(len(heros_temp)):
            if i < len(heros_temp) - 1:
                if heros_temp[i].initiative == heros_temp[i+1].initiative and \
                                heros_temp[i].speed == heros_temp[i+1].speed:
                    to_sort.append(heros_temp[i])
                else:
                    if len(to_sort) > 0:
                        to_sort.append(heros_temp[i])
                        shuffle(to_sort)
                        self.heroes_sorted += to_sort
                        to_sort = []
                    else:
                        self.heroes_sorted.append(heros_temp[i])
            else:
                if len(to_sort) > 0 and heros_temp[i].initiative == heros_temp[i - 1].initiative and \
                                heros_temp[i].speed == heros_temp[i - 1].speed:
                    to_sort.append(heros_temp[i])
                    shuffle(to_sort)
                    self.heroes_sorted += to_sort
                    to_sort = []
                else:
                    self.heroes_sorted.append(heros_temp[i])

    def print_heroes_left(self, player_name):
        """
        Affiche la liste des héros qui ne sont pas présents dans la barre d'initiative
        """
        height = self.font_small.render(self.heroes_sorted[0].name, 1,
                                        constants.Colors.WHITE).get_height() * (len(self.heroes_sorted) -
                                                                                constants.InitiativeBar.MAX_HERO_LEN)
        width = max([self.font_small.render(hero.name, 1, constants.Colors.WHITE).get_width()
                     for hero in self.heroes_sorted]) + constants.InitiativeBar.MAX_HERO_LEN
        pygame.draw.rect(self.surface, constants.Colors.BLACK_200_ALPHA,
                         (self.button_more.rect.right - width, self.button_more.rect.top - height, width, height))
        pygame.draw.rect(self.surface, constants.Colors.SADDLE_BROW,
                         (self.button_more.rect.right - width, self.button_more.rect.top - height, width, height), 2)
        for i in range(constants.InitiativeBar.MAX_HERO_LEN, len(self.heroes_sorted)):
            if self.heroes_sorted[i].player_name == player_name:
                color = constants.Colors.GOLD
            else:
                color = constants.Colors.RED
            self.heroes_sorted[i].name_text = self.font_small.render(self.heroes_sorted[i].name, 1, color)
            self.heroes_sorted[i].name_text_rect.left = \
                self.button_more.rect.right - width + constants.InitiativeBar.BUTTON_MARGIN
            self.heroes_sorted[i].name_text_rect.top = \
                self.button_more.rect.top - height + \
                self.heroes_sorted[i].name_text.get_height() * (i - constants.InitiativeBar.MAX_HERO_LEN)
            self.surface.blit(self.heroes_sorted[i].name_text, self.heroes_sorted[i].name_text_rect)

    def end_turn(self):
        """
        Met fin au tour en cours
        """
        self.heroes_sorted.append(self.heroes_sorted[0])
        del self.heroes_sorted[0]
        self.first_up = not self.first_up

    def get_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.fake_rect_but_end.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.end_turn()
                return True
            else:
                end = min(10, len(self.heroes_sorted))
                for i in range(end):
                    # Crée un faux rect pour rendre la collision avec la souris possible
                    fake_rect = pygame.Rect(self.heroes_sorted[i].token_init_rect)
                    fake_rect.centerx += self.surface_rect.left
                    fake_rect.centery += self.surface_rect.top
                    # Affecte les différentes couleurs
                    if fake_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        return self.heroes_sorted[i]
            return None

    def draw(self, screen, mouse_pos, player_name):
        # Dessine la barre
        self.surface.fill(constants.Colors.BLACK_FULL_ALPHA)
        pygame.draw.rect(self.surface, constants.Colors.WHITE, (constants.InitiativeBar.START_X_RECT,
                                                                constants.InitiativeBar.START_Y_RECT,
                                                                constants.InitiativeBar.SIZE_X_RECT,
                                                                constants.InitiativeBar.SIZE_Y_RECT))
        pygame.draw.line(self.surface, constants.Colors.ELECTRIC_BLUE,
                         (constants.InitiativeBar.START_FIRST_LINE, constants.InitiativeBar.START_Y_LINE),
                         (constants.InitiativeBar.END_FIRST_LINE, constants.InitiativeBar.START_Y_LINE),
                         constants.InitiativeBar.WIDTH_BAR)
        pygame.draw.line(self.surface, constants.Colors.WHITE,
                         (constants.InitiativeBar.END_FIRST_LINE, constants.InitiativeBar.START_Y_LINE),
                         (constants.InitiativeBar.END_SEC_LINE, constants.InitiativeBar.START_Y_LINE),
                         constants.InitiativeBar.WIDTH_BAR)
        pygame.draw.line(self.surface, constants.Colors.ORANGE_RED,
                         (constants.InitiativeBar.END_SEC_LINE, constants.InitiativeBar.START_Y_LINE),
                         (constants.InitiativeBar.END_LAST_LINE, constants.InitiativeBar.START_Y_LINE),
                         constants.InitiativeBar.WIDTH_BAR)
        # Dessine le portrait des héros
        end = min(constants.InitiativeBar.MAX_HERO_LEN, len(self.heroes_sorted))
        up = self.first_up
        for i in range(end):
            # Affecte les positions en fonction de l'emplacement du héros sur la barre (haut, bas)
            if up:
                pos_y = constants.InitiativeBar.START_Y_RECT_TOP
                pos_y_end = constants.InitiativeBar.START_Y_RECT_TOP - constants.InitiativeBar.SIZE_LINE_TOKEN
                pos_y_circle = constants.InitiativeBar.START_Y_RECT_TOP - constants.InitiativeBar.TOKEN_SPACING
            else:
                pos_y = constants.InitiativeBar.START_Y_RECT_BOT
                pos_y_end = constants.InitiativeBar.START_Y_RECT_BOT + constants.InitiativeBar.SIZE_LINE_TOKEN
                pos_y_circle = constants.InitiativeBar.START_Y_RECT_BOT + constants.InitiativeBar.TOKEN_SPACING
            self.heroes_sorted[i].token_init_rect.centerx = \
                constants.InitiativeBar.FIRST_HERO + 1 - constants.InitiativeBar.TOKEN_MARGIN * i
            self.heroes_sorted[i].token_init_rect.centery = pos_y_circle
            # Crée un faux rect pour rendre la collision avec la souris possible
            fake_rect = pygame.Rect(self.heroes_sorted[i].token_init_rect)
            fake_rect.centerx += self.surface_rect.left
            fake_rect.centery += self.surface_rect.top
            # Affecte les différentes couleurs
            if fake_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                # Affiche le nom du héros au survol
                color = constants.Colors.ELECTRIC_BLUE
                self.heroes_sorted[i].name_text = \
                    self.font_small.render(self.heroes_sorted[i].name, 1, constants.Colors.WHITE)
                if up:
                    self.heroes_sorted[i].name_text_rect.centerx = self.heroes_sorted[i].token_init_rect.centerx
                    self.heroes_sorted[i].name_text_rect.bottom = self.heroes_sorted[i].token_init_rect.top
                else:
                    self.heroes_sorted[i].name_text_rect.centerx = self.heroes_sorted[i].token_init_rect.centerx
                    self.heroes_sorted[i].name_text_rect.top = self.heroes_sorted[i].token_init_rect.bottom
                self.surface.blit(self.heroes_sorted[i].name_text, self.heroes_sorted[i].name_text_rect)
            else:
                if self.heroes_sorted[i].player_name == player_name:
                    color = constants.Colors.GOLD
                else:
                    color = constants.Colors.RED
            # Dessine les éléments
            pygame.draw.line(self.surface, color,
                             (constants.InitiativeBar.FIRST_HERO - constants.InitiativeBar.TOKEN_MARGIN * i, pos_y),
                             (constants.InitiativeBar.FIRST_HERO - constants.InitiativeBar.TOKEN_MARGIN * i, pos_y_end),
                             constants.InitiativeBar.LINE_THICK)
            self.surface.blit(self.heroes_sorted[i].token_init, self.heroes_sorted[i].token_init_rect)
            pygame.draw.circle(self.surface, color,
                               (constants.InitiativeBar.FIRST_HERO + 1 - constants.InitiativeBar.TOKEN_MARGIN * i,
                                pos_y_circle), constants.InitiativeBar.TOKEN_MARGIN // 2,
                               constants.InitiativeBar.LINE_THICK)
            up = not up
        # Affiche le bouton permettant de visulaliser le reste des héros
        if len(self.heroes_sorted) <= constants.InitiativeBar.MAX_HERO_LEN:
            self.surface.blit(self.button_more.render_inactive, self.button_more.rect)
        elif self.fake_rect_but.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.surface.blit(self.button_more.render_hover, self.button_more.rect)
            self.print_heroes_left(player_name)
        else:
            self.surface.blit(self.button_more.render_base, self.button_more.rect)
        # Affiche le bouton permettant de finir le tour en cours
        if self.adv_team is None:
            self.surface.blit(self.button_end_turn.render_inactive, self.button_end_turn.rect)
        elif self.fake_rect_but_end.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.surface.blit(self.button_end_turn.render_hover, self.button_end_turn.rect)
        else:
            self.surface.blit(self.button_end_turn.render_base, self.button_end_turn.rect)
        screen.blit(self.surface, self.surface_rect)
