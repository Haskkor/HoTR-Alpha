import constants
import pygame
import sys

import menu_principal

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class IntroWindows:
    """
    FENETRE D'INTRODUCTION
    """

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        # Fond d'écran et texte d'indication
        self.background = pygame.image.load(constants.ImagesPath.INTRO_SCREEN).convert()
        self.text = pygame.image.load(constants.ImagesPath.PRESS_TO_CONTINUE)
        # Position du texte
        self.textpos = self.text.get_rect()
        self.textpos.centerx = self.screen.get_rect().centerx
        self.textpos.centery = self.screen.get_rect().centery + constants.Intro.POS_TEXT_Y
        self.run()

    def get_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                leave()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                menu_principal.MenuWindow((self.screen, self.clock))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.text, self.textpos)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            self.get_event(pygame.event.get())
            self.draw()
