import constants
import menu_principal
import pygame
import sys

from button_text_class import ButtonText

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class OverlayExit:
    """
    OVERLAY POUR LA CONFIRMATION DU EXIT
    """

    def __init__(self, screen, capture, clock):
        self.screen = screen
        self.background = capture
        self.clock = clock
        self.font = pygame.font.SysFont(constants.Fonts.ARIAL, 36)
        self.font.set_bold(True)
        # Création de l'overlay
        self.overlay = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT))
        self.overlay.fill(constants.Colors.BLACK)
        self.overlay.set_alpha(constants.Colors.OVERLAY_ALPHA)
        # Image de la modal et position
        self.modal = pygame.image.load(constants.ImagesPath.MODAL_EXIT)
        self.modalpos = self.modal.get_rect()
        self.modalpos.centerx = self.screen.get_rect().centerx
        self.modalpos.centery = self.screen.get_rect().centery
        # Création des boutons de la modal et du texte
        self.list_buttons = list()
        centerx = self.screen.get_rect().centerx
        centery = self.screen.get_rect().centery + self.font.get_height() * 3
        self.list_buttons.append(ButtonText(font=self.font, pos_centery=centery, on_clic=leave,
                                            pos_centerx=centerx + -1 * constants.Modals.POS_TEXT_YES_NO,
                                            text=constants.Texts.YES))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.NO, on_clic=menu_principal.MenuWindow,
                                            parameters=(self.screen, self.clock), pos_centery=centery,
                                            pos_centerx=centerx + constants.Modals.POS_TEXT_YES_NO))
        self.text_1 = self.font.render(constants.Texts.MODAL_EXIT_1, 1, constants.Colors.WHITE)
        self.text_2 = self.font.render(constants.Texts.MODAL_EXIT_2, 1, constants.Colors.WHITE)
        self.text_1_rect = self.text_1.get_rect()
        self.text_2_rect = self.text_2.get_rect()
        self.text_1_rect.centerx = self.screen.get_rect().centerx
        self.text_2_rect.centerx = self.screen.get_rect().centerx
        self.text_1_rect.centery = self.screen.get_rect().centery - constants.Modals.POS_TEXT_EXIT_1
        self.text_2_rect.centery = self.screen.get_rect().centery - constants.Modals.POS_TEXT_EXIT_2
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
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.modal, self.modalpos)
        for button in self.list_buttons:
            button.draw()
        self.screen.blit(self.text_1, self.text_1_rect)
        self.screen.blit(self.text_2, self.text_2_rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            self.draw(mouse_pos)
