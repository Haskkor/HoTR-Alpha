import pygame
import sys

import constants
import deck_selection
import team_selection
from button_text_class import ButtonText

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class OverlayPointsLeftTeamSelection:
    """
    OVERLAY POUR LE PASSAGE AU CHOIX DU DECK SI IL RESTE DES POINTS
    """

    def __init__(self, screen, capture, timer, total_points, fplayer_name, splayer_name, fplayer_team, splayer_team):
        self.screen = screen
        self.capture = capture
        self.clock = timer
        self.to_return = None
        self.fplayer_name = fplayer_name
        self.splayer_name = splayer_name
        self.fplayer_team = fplayer_team
        self.splayer_team = splayer_team
        self.total_points = total_points
        # Police
        self.font = pygame.font.SysFont(constants.Fonts.ARIAL, 36)
        self.font.set_bold(True)
        # Création de l'overlay
        self.overlay = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT))
        self.overlay.fill(constants.Colors.BLACK)
        self.overlay.set_alpha(constants.Colors.OVERLAY_ALPHA)
        # Image de la modal et position
        self.modal = pygame.image.load(constants.ImagesPath.MODAL_POINTS_LEFT)
        self.modalpos = self.modal.get_rect()
        self.modalpos.centerx = self.screen.get_rect().centerx
        self.modalpos.centery = self.screen.get_rect().centery
        # Création des boutons de la modal et du texte
        if self.splayer_team is not None:
            self.sum_points = sum([hero.cost for hero in self.splayer_team])
        else:
            self.sum_points = sum([hero.cost for hero in self.fplayer_team])
        self.list_buttons = list()
        centerx = self.screen.get_rect().centerx
        centery = self.screen.get_rect().centery + self.font.get_height() * 3
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.YES, pos_centery=centery,
                                            pos_centerx=centerx + -1 * constants.Modals.POS_TEXT_YES_NO))
        self.list_buttons.append(ButtonText(font=self.font, text=constants.Texts.NO, pos_centery=centery,
                                            pos_centerx=centerx + constants.Modals.POS_TEXT_YES_NO))
        self.text_1 = self.font.render(constants.Texts.MODAL_POINTS_LEFT_1.format(str(self.total_points -
                                                                                      self.sum_points)),
                                       1, constants.Colors.WHITE)
        self.text_2 = self.font.render(constants.Texts.MODAL_POINTS_LEFT_2, 1, constants.Colors.WHITE)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.list_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == constants.Texts.NO:
                            self.to_return = True
                        else:
                            if self.splayer_team is None:
                                team_selection.TeamSelection((self.screen, self.clock, self.total_points,
                                                              self.fplayer_name, self.splayer_name, self.fplayer_team,
                                                              None, list()))
                            else:
                                deck_selection.DeckSelection((self.screen, self.clock, self.total_points,
                                                              self.fplayer_name, self.splayer_name, self.fplayer_team,
                                                              self.splayer_team, None, None, list()))

    def draw(self, mouse_pos):
        # Affiche la page de la sélection de l'équipe
        self.screen.blit(self.capture, (0, 0))
        # Affiche l'overlay, les boutons et le texte
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.modal, self.modalpos)
        for button in self.list_buttons:
            button.draw(self.screen, mouse_pos)
        self.screen.blit(self.text_1, self.text_1_rect)
        self.screen.blit(self.text_2, self.text_2_rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            if self.to_return is not None:
                return
            self.draw(mouse_pos)
