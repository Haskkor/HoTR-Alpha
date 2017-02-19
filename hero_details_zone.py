import pygame
import constants

__author__ = "Jérémy Farnault"


class HeroDetailsZone:
    """
    OBJETS ZONE DE DETAILS DU HERO SELECTIONNE
    """

    def __init__(self):
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 11)
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.surface = pygame.Surface((constants.HeroDetailsZone.WIDTH, constants.HeroDetailsZone.HEIGHT),
                                      pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.left = 0
        self.surface_rect.top = constants.Window.SCREEN_HEIGHT - constants.HeroDetailsZone.HEIGHT

    def draw(self, screen, selected_hero):
        self.surface.fill(constants.Colors.BLACK_FULL_ALPHA)
        selected_hero.miniature_rect.left = 0
        selected_hero.miniature_rect.bottom = constants.HeroDetailsZone.HEIGHT
        selected_hero.token_rect.centerx = selected_hero.miniature_rect.centerx
        selected_hero.token_rect.bottom = selected_hero.miniature_rect.top
        self.surface.blit(selected_hero.miniature, selected_hero.miniature_rect)
        self.surface.blit(selected_hero.token, selected_hero.token_rect)
        # Affiche les caractéristiques basiques
        pos_details_y = selected_hero.token_rect.top
        for detail in selected_hero.get_basic_inspected_battle(self.font_small):
            detail_rect = detail.get_rect()
            detail_rect.left = selected_hero.miniature_rect.right + constants.HeroDetailsZone.BASE_MARGIN
            detail_rect.top = pos_details_y
            pos_details_y += detail_rect.height
            self.surface.blit(detail, detail_rect)
        # Affiche les caractéristiques à points
        pos_details_y = selected_hero.token_rect.top
        for detail in selected_hero.get_points_inspected_battle(self.font_medium):
            detail_rect = detail.get_rect()
            detail_rect.left = selected_hero.miniature_rect.right + constants.HeroDetailsZone.POINTS_MARGIN
            detail_rect.top = pos_details_y
            pos_details_y += detail_rect.height
            self.surface.blit(detail, detail_rect)
        # Affiche les compétences
        pos_details_y = 100
        for detail in selected_hero.get_skills_inspected(self.font_medium):
            detail_rect = detail.get_rect()
            detail_rect.left = selected_hero.miniature_rect.right + constants.HeroDetailsZone.SKILLS_MARGIN
            detail_rect.top = pos_details_y
            pos_details_y += detail_rect.height
            self.surface.blit(detail, detail_rect)
        screen.blit(self.surface, self.surface_rect)
