import pygame
import sys

import battle_size_selection
import constants
import menu_principal
from button_text_class import ButtonText
from textbox_class import TextBox

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class NameSelectionMultiLocal:
    """
    FENETRE DE MENU
    """

    def __init__(self, *args):
        self.screen = args[0][0]
        self.clock = args[0][1]
        self.font = pygame.font.SysFont(constants.Fonts.ARIAL, 26)
        self.font.set_bold(True)
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_back.set_bold(True)
        # Fond d'écran
        self.background = pygame.image.load(constants.ImagesPath.BACK_NAME_SELECT).convert()
        # Textes pour les deux joueurs
        self.render_text_fp = self.font.render(constants.Texts.FIRST_PLAYER_NAME, 1, constants.Colors.WHITE)
        self.render_text_fp_rect = self.render_text_fp.get_rect()
        self.render_text_fp_rect.centerx = self.screen.get_rect().centerx
        self.render_text_fp_rect.bottom = self.screen.get_rect().centery - constants.NameSelectionMultiLocal.ELEM_FAR
        self.render_text_sp = self.font.render(constants.Texts.SECOND_PLAYER_NAME, 1, constants.Colors.WHITE)
        self.render_text_sp_rect = self.render_text_sp.get_rect()
        self.render_text_sp_rect.centerx = self.screen.get_rect().centerx
        self.render_text_sp_rect.top = self.screen.get_rect().centery + constants.NameSelectionMultiLocal.ELEM_NEAR
        # Déclaration des 2 textboxes
        self.text_box_fp = \
            TextBox((self.screen.get_rect().centerx - constants.Textbox.TEXTBOX_WIDTH // 2,
                     self.screen.get_rect().centery - constants.NameSelectionMultiLocal.ELEM_NEAR -
                     constants.Textbox.TEXTBOX_HEIGHT, constants.Textbox.TEXTBOX_WIDTH,
                     constants.Textbox.TEXTBOX_HEIGHT), clear_on_enter=True, inactive_on_enter=False, active=False,
                    font=self.font)
        self.text_box_sp = \
            TextBox((self.screen.get_rect().centerx - constants.Textbox.TEXTBOX_WIDTH // 2,
                     self.screen.get_rect().centery + constants.NameSelectionMultiLocal.ELEM_FAR,
                     constants.Textbox.TEXTBOX_WIDTH, constants.Textbox.TEXTBOX_HEIGHT), clear_on_enter=True,
                    inactive_on_enter=False, active=False, font=self.font)
        # Bouton de lancement de l'écran suivant et bouton retour
        self.button_next = \
            ButtonText(font=self.font, pos_right=self.screen.get_rect().width -
                       constants.NameSelectionMultiLocal.MARGIN_NEXT, text=constants.Texts.NEXT,
                       on_clic=battle_size_selection.BattleSizeSelection,
                       pos_bottom=self.screen.get_rect().height - constants.NameSelectionMultiLocal.MARGIN_NEXT)
        self.button_back = \
            ButtonText(font=self.font_back, text=constants.Texts.BACK, pos_centerx=self.screen.get_rect().centerx,
                       pos_bottom=self.screen.get_rect().height, on_clic=menu_principal.MenuWindow,
                       parameters=(self.screen, self.clock))
        self.run()

    def change_state_button_next(self):
        """
        N'active le bouton next que lorque les deux champs de saisie comportent au moins 3 lettres et qu'ils sont
        différents
        """
        if self.text_box_fp.final is not None and self.text_box_sp.final is not None:
            if len(self.text_box_fp.final) < constants.NameSelectionMultiLocal.MIN_LEN_NAME or \
                            len(self.text_box_sp.final) < constants.NameSelectionMultiLocal.MIN_LEN_NAME or \
                            self.text_box_sp.final == self.text_box_fp.final:
                self.button_next.active = False
            else:
                self.button_next.active = True

    def get_event(self, events, mouse_pos):
        for event in events:
            self.text_box_fp.get_event(event)
            self.text_box_sp.get_event(event)
            if event.type == pygame.QUIT:
                leave()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_next.rect.collidepoint(mouse_pos):
                    self.button_next.on_clic((self.screen, self.clock, self.text_box_fp.final, self.text_box_sp.final))
                elif self.button_back.rect.collidepoint(mouse_pos):
                    self.button_back.on_clic(self.button_back.parameters)
            elif event.type == pygame.KEYDOWN:
                # Déplacement entre les textbox avec la touche tab
                if event.key == pygame.K_TAB:
                    if not self.text_box_fp.active and not self.text_box_sp.active:
                        self.text_box_fp.active = True
                    elif self.text_box_fp.active:
                        self.text_box_fp.active = False
                        self.text_box_sp.active = True
                    elif self.text_box_sp.active:
                        self.text_box_sp.active = False

    def draw(self, mouse_pos):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.render_text_fp, self.render_text_fp_rect)
        self.screen.blit(self.render_text_sp, self.render_text_sp_rect)
        self.text_box_fp.draw(self.screen)
        self.text_box_sp.draw(self.screen)
        self.text_box_fp.update()
        self.text_box_sp.update()
        if self.button_next.rect.collidepoint(mouse_pos) and self.button_next.active:
            self.screen.blit(self.button_next.render_hover, self.button_next.rect)
        elif self.button_next.active:
            self.screen.blit(self.button_next.render_base, self.button_next.rect)
        else:
            self.screen.blit(self.button_next.render_inactive, self.button_next.rect)
        if self.button_back.rect.collidepoint(mouse_pos):
            self.screen.blit(self.button_back.render_hover, self.button_back.rect)
        else:
            self.screen.blit(self.button_back.render_base, self.button_back.rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.change_state_button_next()
            self.get_event(pygame.event.get(), mouse_pos)
            self.draw(mouse_pos)
