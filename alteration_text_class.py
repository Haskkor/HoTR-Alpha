import pygame
import constants
from enum import Enum

__author__ = "Jérémy Farnault"


class AlterationType(Enum):
    """
    ENUM DES DIFFERENTES ALTERATIONS POSSIBLES POUR LES HEROS
    """

    ACTION_POINTS = "AP"
    LIFE_POINTS = "LP"
    ARMOR_POINTS = "ArP"
    MAGIC_POINTS = "MP"


def switch_colors(action_type):
    """
    Select the right color for the text
    """
    if action_type == AlterationType.ACTION_POINTS:
        return constants.Colors.GREEN
    elif action_type == AlterationType.LIFE_POINTS:
        return constants.Colors.RED
    elif action_type == AlterationType.ARMOR_POINTS:
        return constants.Colors.GOLD
    elif action_type == AlterationType.MAGIC_POINTS:
        return constants.Colors.PURPLE


def switch_signs(bonus):
    """
    Select the sign for the text
    """
    if bonus:
        return "+"
    return "-"


class AlterationText:
    """
    OBJETS VISUELS DES ALTERATIONS
    """

    def __init__(self, bonus, number, action_type, pos_x, pos_y):
        self.font = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font.set_bold(True)
        self.timer = pygame.time.get_ticks()
        self.bonus = bonus
        self.number = number
        self.type = action_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = switch_colors(action_type)
        self.sign = switch_signs(bonus)
        self.text = self.font.render(self.sign + "{} ".format(number) + self.type, 1, self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.pos_x
        self.text_rect.centery = self.pos_y

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.timer < constants.AlterationText.TIMER:
            screen.blit(self.text, self.text_rect)
        else:
            self.timer = 0
        self.text_rect.centery -= 1
