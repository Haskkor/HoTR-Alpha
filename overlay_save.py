import pygame
import sys

import constants
from button_text_class import ButtonText
from load_class import Load
from save_class import Save
from textbox_class import TextBox

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class OverlaySave:
    """
    OVERLAY POUR LA SAUVEGARDE
    """

    def __init__(self, screen, capture, timer, list_to_save, filename):
        self.screen = screen
        self.capture = capture
        self.clock = timer
        self.to_return = None
        self.list_to_save = list_to_save
        self.filename = filename
        # Polices
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_medium.set_bold(True)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 28)
        self.font_large.set_bold(True)
        # Récupération de la liste de sauvegardes
        load_object = Load(self.filename)
        self.list_saves = load_object.load
        # Création de l'overlay
        self.overlay = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT))
        self.overlay.fill(constants.Colors.BLACK)
        self.overlay.set_alpha(constants.Colors.OVERLAY_ALPHA)
        # Création des boutons et du texte
        self.list_buttons = list()
        centerx = self.screen.get_rect().centerx
        centery = self.screen.get_rect().centery + constants.Modals.POS_ELEM_SAVE
        self.list_buttons.append(ButtonText(font=self.font_large, pos_centery=centery, text=constants.Texts.SAVE,
                                            active=False, pos_centerx=centerx + -1 * constants.Modals.POS_TEXT_YES_NO))
        self.list_buttons.append(ButtonText(font=self.font_large, pos_centery=centery,
                                            text=constants.Texts.CANCEL, active=True,
                                            pos_centerx=centerx + constants.Modals.POS_TEXT_YES_NO))
        self.text = self.font_large.render(constants.Texts.MODAL_SAVE, 1, constants.Colors.WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.screen.get_rect().centerx
        self.text_rect.centery = self.screen.get_rect().centery - constants.Modals.POS_ELEM_SAVE
        # Création de la textbox
        self.text_box = TextBox((self.screen.get_rect().centerx - constants.Textbox.TEXTBOX_WIDTH / 2,
                                 self.screen.get_rect().centery - constants.Textbox.TEXTBOX_HEIGHT / 2,
                                 constants.Textbox.TEXTBOX_WIDTH, constants.Textbox.TEXTBOX_HEIGHT),
                                clear_on_enter=True, inactive_on_enter=False, active=False, font=self.font_medium)
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            self.text_box.get_event(event)
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.list_buttons:
                    if button.active:
                        if button.rect.collidepoint(mouse_pos):
                            if button.text == constants.Texts.CANCEL:
                                self.to_return = True
                            else:
                                save = Save(self.filename)
                                save.save_new_object(self.text_box.final, self.list_to_save)
                                self.to_return = True

    def draw(self, mouse_pos):
        # Affiche la page précédente
        self.screen.blit(self.capture, (0, 0))
        # Affiche l'overlay, les boutons et le texte
        self.screen.blit(self.overlay, (0, 0))
        for button in self.list_buttons:
            button.draw(self.screen, mouse_pos)
        self.screen.blit(self.text, self.text_rect)
        self.text_box.draw(self.screen)
        self.text_box.update()
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def change_state_text_buttons(self):
        """
        Modifie l'état des boutons textes en fonctions des différents paramètres
        """
        for button in self.list_buttons:
            if button.text == constants.Texts.SAVE and self.text_box.final is not None and self.text_box.final != "":
                if self.text_box.final in self.list_saves:
                    self.text_box.error = True
                    button.active = False
                else:
                    self.text_box.error = False
                    button.active = True
            elif button.text == constants.Texts.SAVE:
                button.active = False

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            if self.to_return is not None:
                return
            self.change_state_text_buttons()
            self.draw(mouse_pos)
