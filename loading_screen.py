import pygame

import constants

__author__ = "Jérémy Farnault"


def show_loading_screen(screen):
    overlay = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT))
    overlay.fill(constants.Colors.BLACK)
    overlay.set_alpha(constants.Colors.OVERLAY_ALPHA)
    screen.blit(overlay, (0, 0))
    loading_img = pygame.image.load(constants.ImagesPath.LOADING)
    loading_img_rect = loading_img.get_rect()
    loading_img_rect.centerx = screen.get_rect().centerx
    loading_img_rect.centery = screen.get_rect().centery
    screen.blit(loading_img, loading_img_rect)
    pygame.display.flip()
