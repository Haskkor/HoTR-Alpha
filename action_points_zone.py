import pygame
from django.contrib.gis.db.backends.postgis import const

import constants

__author__ = "Jérémy Farnault"


class ActionPointsZone:
    """
    OBJETS ZONE DES POINTS D'ACTION
    """

    def __init__(self):
        self.surface = pygame.Surface((constants.ActionPointsZone.WIDTH, constants.ActionPointsZone.HEIGHT),
                                      pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.left = constants.ActionPointsZone.ZONE_POS_X
        self.surface_rect.top = constants.ActionPointsZone.ZONE_POS_Y
        self.ap_unused_top = pygame.image.load(constants.ImagesPath.ACTION_POINT_UNUSED)
        self.ap_unused_top_rect = self.ap_unused_top.get_rect()
        self.ap_unused_mid = pygame.image.load(constants.ImagesPath.ACTION_POINT_UNUSED)
        self.ap_unused_mid_rect = self.ap_unused_mid.get_rect()
        self.ap_unused_bot = pygame.image.load(constants.ImagesPath.ACTION_POINT_UNUSED)
        self.ap_unused_bot_rect = self.ap_unused_bot.get_rect()
        self.ap_used_top = pygame.image.load(constants.ImagesPath.ACTION_POINT_USED)
        self.ap_used_top_rect = self.ap_used_top.get_rect()
        self.ap_used_mid = pygame.image.load(constants.ImagesPath.ACTION_POINT_USED)
        self.ap_used_mid_rect = self.ap_used_mid.get_rect()
        self.ap_used_bot = pygame.image.load(constants.ImagesPath.ACTION_POINT_USED)
        self.ap_used_bot_rect = self.ap_used_bot.get_rect()

    def number_0(self):
        self.ap_used_top_rect.top = constants.ActionPointsZone.IMAGE_1_Y
        self.ap_used_top_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_used_top, self.ap_used_top_rect)
        self.ap_used_mid_rect.top = constants.ActionPointsZone.IMAGE_2_Y
        self.ap_used_mid_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_used_mid, self.ap_used_mid_rect)
        self.ap_used_bot_rect.top = constants.ActionPointsZone.IMAGE_3_Y
        self.ap_used_bot_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_used_bot, self.ap_used_bot_rect)

    def number_1(self):
        self.ap_unused_top_rect.top = constants.ActionPointsZone.IMAGE_1_Y
        self.ap_unused_top_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_unused_top, self.ap_unused_top_rect)
        self.ap_used_mid_rect.top = constants.ActionPointsZone.IMAGE_2_Y
        self.ap_used_mid_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_used_mid, self.ap_used_mid_rect)
        self.ap_used_bot_rect.top = constants.ActionPointsZone.IMAGE_3_Y
        self.ap_used_bot_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_used_bot, self.ap_used_bot_rect)

    def number_2(self):
        self.ap_unused_top_rect.top = constants.ActionPointsZone.IMAGE_1_Y
        self.ap_unused_top_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_unused_top, self.ap_unused_top_rect)
        self.ap_unused_mid_rect.top = constants.ActionPointsZone.IMAGE_2_Y
        self.ap_unused_mid_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_unused_mid, self.ap_unused_mid_rect)
        self.ap_used_bot_rect.top = constants.ActionPointsZone.IMAGE_3_Y
        self.ap_used_bot_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_used_bot, self.ap_used_bot_rect)

    def number_3(self):
        self.ap_unused_top_rect.top = constants.ActionPointsZone.IMAGE_1_Y
        self.ap_unused_top_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_unused_top, self.ap_unused_top_rect)
        self.ap_unused_mid_rect.top = constants.ActionPointsZone.IMAGE_2_Y
        self.ap_unused_mid_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_unused_mid, self.ap_unused_mid_rect)
        self.ap_unused_bot_rect.top = constants.ActionPointsZone.IMAGE_3_Y
        self.ap_unused_bot_rect.left = constants.ActionPointsZone.IMAGES_X
        self.surface.blit(self.ap_unused_bot, self.ap_unused_bot_rect)

    def draw(self, screen, current_action_points):
        self.surface.fill(constants.Colors.BLACK_FULL_ALPHA)
        method_name = 'number_' + str(current_action_points)
        method = getattr(self, method_name, lambda: "nothing")
        method()
        screen.blit(self.surface, self.surface_rect)
