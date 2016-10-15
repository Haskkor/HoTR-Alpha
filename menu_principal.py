import pygame
import sys

import constants
import name_selection_multi_local
import overlay_exit
from button_text_class import ButtonText

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class MenuWindow:
    """
    FENETRE DE MENU
    """

    def __init__(self, *args):
        self.screen = args[0][0]
        self.clock = args[0][1]
        self.font = pygame.font.SysFont(constants.Fonts.ARIAL, 24)
        # Fond d'écran
        self.background = pygame.image.load(constants.ImagesPath.MENU_SCREEN).convert()
        # Initialisation des boutons
        self.list_buttons = list()
        top = (self.screen.get_rect().height - self.font.get_height() * (constants.Menu.NBR_BUTTONS_MENU * 2)) / 2
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_TUTO,
                                            on_clic=self.start_overlay,
                                            pos_centerx=self.screen.get_rect().centerx, pos_top=top))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_STORY,
                                            on_clic=self.start_overlay,
                                            pos_centerx=self.screen.get_rect().centerx,
                                            pos_top=top + self.font.get_height() * 2))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_SKIRMISH,
                                            on_clic=self.start_overlay,
                                            pos_centerx=self.screen.get_rect().centerx,
                                            pos_top=top + 2 * self.font.get_height() * 2))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_LOCALMP,
                                            on_clic=name_selection_multi_local.NameSelectionMultiLocal,
                                            parameters=(self.screen, self.clock),
                                            pos_centerx=self.screen.get_rect().centerx,
                                            pos_top=top + 3 * self.font.get_height() * 2))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_ONLINEMP,
                                            on_clic=self.start_overlay,
                                            pos_centerx=self.screen.get_rect().centerx,
                                            pos_top=top + 4 * self.font.get_height() * 2))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_OPTIONS,
                                            on_clic=self.start_overlay,
                                            pos_centerx=self.screen.get_rect().centerx,
                                            pos_top=top + 5 * self.font.get_height() * 2))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.MENU_EXIT,
                                            on_clic=self.start_overlay,
                                            pos_centerx=self.screen.get_rect().centerx,
                                            pos_top=top + 6 * self.font.get_height() * 2))
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.list_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.parameters is not None:
                            button.on_clic(button.parameters)
                        else:
                            button.on_clic()

    def draw(self, mouse_pos):
        self.screen.blit(self.background, (0, 0))
        for button in self.list_buttons:
            if button.rect.collidepoint(mouse_pos):
                self.screen.blit(button.render_hover, button.rect)
            else:
                self.screen.blit(button.render_base, button.rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def start_overlay(self):
        """
        Démarre la page de l'overlay de sortie du jeu
        """
        capture = self.screen.copy()
        overlay_exit.OverlayExit(self.screen, capture, self.clock)

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            self.draw(mouse_pos)
