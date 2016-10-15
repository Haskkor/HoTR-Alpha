import pygame

import constants
import heroes_creation
import cards_creation
import intro

__author__ = "Jérémy Farnault"


def main():
    """
    FONCTION PRINCIPALE
    """

    pygame.init()
    pygame.key.set_repeat(500, 30)
    pygame.font.init()

    # Initialisation de l'écran
    size = [constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(constants.Window.WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Création du fichier contenant les champions
    heroes_creation.main()

    # Création du fichier contenant les cartes
    cards_creation.main()

    # Appel de la fenêtre d'intro
    intro.IntroWindows(screen, clock)

    pygame.quit()

if __name__ == "__main__":
    # LANCEMENT DU PROGRAMME

    main()
