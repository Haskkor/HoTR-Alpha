import pygame
import sys

import constants
import name_selection_multi_local
import team_selection
from loading_screen import show_loading_screen
from button_text_class import ButtonText

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class BattleSizeSelection:
    """
    FENETRE DE SELECTION DE LA TAILLE DE LA BATAILLE
    """

    def __init__(self, *args):
        self.screen = args[0][0]
        self.clock = args[0][1]
        self.fplayer_name = args[0][2]
        self.splayer_name = args[0][3]
        # Initialisation des polices
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_big = pygame.font.SysFont(constants.Fonts.ARIAL, 36)
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 28)
        self.font_back.set_bold(True)
        self.font_big.set_bold(True)
        self.font_small.set_bold(True)
        # Fond d'écran et modal
        self.background = pygame.image.load(constants.ImagesPath.B_S_S_SCREEN).convert()
        self.background_pos = self.background.get_rect()
        self.background_pos.centerx = self.screen.get_rect().centerx
        self.background_pos.centery = self.screen.get_rect().centery
        self.modal = pygame.image.load(constants.ImagesPath.MODAL_BSS)
        self.modal_pos = self.modal.get_rect()
        self.modal_pos.centerx = self.screen.get_rect().centerx
        self.modal_pos.centery = self.screen.get_rect().centery
        # Initialisation des boutons
        self.list_buttons = list()
        centerx_bss = self.screen.get_rect().centerx
        centery_bss = self.screen.get_rect().centery
        centerx_back = self.screen.get_rect().centerx
        bottom_back = self.screen.get_rect().height
        # Paramètres None : prévisions de listes de héros pour la page suivante
        self.list_buttons.append(ButtonText(font=self.font_small, pos_centerx=centerx_bss,
                                            text=constants.Texts.BSS_SMALL_TEXT,
                                            on_clic=team_selection.TeamSelection, pos_centery=centery_bss,
                                            parameters=(self.screen, self.clock, constants.Modals.BSS_SMALL,
                                                        self.fplayer_name, self.splayer_name, None, None, list())))
        self.list_buttons.append(ButtonText(font=self.font_small,  pos_centerx=centerx_bss,
                                            text=constants.Texts.BSS_MEDIUM_TEXT,
                                            on_clic=team_selection.TeamSelection,
                                            pos_centery=centery_bss + self.font_small.get_height() * 2,
                                            parameters=(self.screen, self.clock, constants.Modals.BSS_MEDIUM,
                                                        self.fplayer_name, self.splayer_name, None, None, list())))
        self.list_buttons.append(ButtonText(font=self.font_small,  pos_centerx=centerx_bss,
                                            text=constants.Texts.BSS_LARGE_TEXT,
                                            on_clic=team_selection.TeamSelection,
                                            pos_centery=centery_bss + self.font_small.get_height() * 4,
                                            parameters=(self.screen, self.clock, constants.Modals.BSS_LARGE,
                                                        self.fplayer_name, self.splayer_name, None, None, list())))
        self.list_buttons.append(ButtonText(font=self.font_back, pos_centerx=centerx_back,
                                            text=constants.Texts.BACK, pos_bottom=bottom_back,
                                            on_clic=name_selection_multi_local.NameSelectionMultiLocal,
                                            parameters=(self.screen, self.clock)))
        # Initialisation des textes
        self.text_1 = self.font_big.render(constants.Texts.BSS_TEXT_1, 1, constants.Colors.WHITE)
        self.text_2 = self.font_big.render(constants.Texts.BSS_TEXT_2, 1, constants.Colors.WHITE)
        self.text_1_rect = self.text_1.get_rect()
        self.text_2_rect = self.text_2.get_rect()
        self.text_1_rect.centerx = self.screen.get_rect().centerx
        self.text_2_rect.centerx = self.screen.get_rect().centerx
        self.text_1_rect.centery = self.screen.get_rect().centery - constants.Modals.POS_TEXT_BSS_1
        self.text_2_rect.centery = self.screen.get_rect().centery - constants.Modals.POS_TEXT_BSS_2
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.list_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        show_loading_screen(self.screen)
                        button.on_clic(button.parameters)

    def draw(self, mouse_pos):
        self.screen.blit(self.background, self.background_pos)
        self.screen.blit(self.modal, self.modal_pos)
        self.screen.blit(self.text_1, self.text_1_rect)
        self.screen.blit(self.text_2, self.text_2_rect)
        for button in self.list_buttons:
            if button.rect.collidepoint(mouse_pos):
                self.screen.blit(button.render_hover, button.rect)
            else:
                self.screen.blit(button.render_base, button.rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            self.draw(mouse_pos)
