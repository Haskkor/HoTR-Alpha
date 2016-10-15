import pygame
import sys

import constants

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class OverlayZoomCard:
    """
    OVERLAY POUR L'AFFICHAGE DE LA CARTE ZOOMEE
    """

    def __init__(self, screen, capture, timer, card):
        self.screen = screen
        self.capture = capture
        self.clock = timer
        self.card = card
        self.to_return = False
        # Création de l'overlay
        self.overlay = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT))
        self.overlay.fill(constants.Colors.BLACK)
        self.overlay.set_alpha(constants.Colors.OVERLAY_ALPHA)
        self.run()

    def get_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.to_return = True

    def draw(self):
        # Affiche la page de création du deck
        self.screen.blit(self.capture, (0, 0))
        # Affiche l'overlay
        self.screen.blit(self.overlay, (0, 0))
        # Affiche la carte zoomée
        self.card.zoom_rect.centerx = self.screen.get_rect().centerx
        self.card.zoom_rect.centery = self.screen.get_rect().centery
        self.screen.blit(self.card.zoom, self.card.zoom_rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            self.get_event(pygame.event.get())
            if self.to_return:
                return
            self.draw()
