import pygame
import constants
from action_type_enum import ActionType

__author__ = "Jérémy Farnault"


class Action:
    """
    OBJETS ACTION
    """

    def __init__(self, path, pos_y, pos_x, active, action_type):
        font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.top = pos_y
        self.rect.right = pos_x
        self.active = active
        self.action_type = action_type
        self.hovered = False
        self.selected = False
        self.tooltip = font_small.render(self.action_type.value, 1, constants.Colors.GOLD)
        self.tooltip_rect = self.tooltip.get_rect()
        self.tooltip_rect.right = self.rect.left - constants.ActionsSelectionZone.MARGIN_TOOLTIP
        self.tooltip_rect.centery = self.rect.centery


class ActionsSelectionZone:
    """
    OBJETS ZONE DE SELECTION DES DIFFERENTES ACTIONS
    """

    def __init__(self, movement_active=False, attack_active=False, ranged_attack_active=False, defense_active=False,
                 attack_armor_active=False, magic_active=False):
        self.surface = pygame.Surface((constants.ActionsSelectionZone.WIDTH, constants.ActionsSelectionZone.HEIGHT),
                                      pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.right = constants.Window.SCREEN_WIDTH
        self.surface_rect.top = constants.ActionsSelectionZone.ZONE_POS_Y
        self.magic_action = Action(constants.ImagesPath.MAGIC_ACTION, constants.ActionsSelectionZone.ACTION_1_MARGIN_Y,
                                   self.surface_rect.width - constants.ActionsSelectionZone.MARGIN_ACTION_X,
                                   magic_active, ActionType.MAGIC)
        self.attack_armor_action = Action(constants.ImagesPath.ATTACK_ARMOR_ACTION,
                                          constants.ActionsSelectionZone.ACTION_2_MARGIN_Y,
                                          self.surface_rect.width - constants.ActionsSelectionZone.MARGIN_ACTION_X,
                                          attack_armor_active, ActionType.ATTACK_ARMOR)
        self.defense_action = Action(constants.ImagesPath.DEFENSE_ACTION,
                                     constants.ActionsSelectionZone.ACTION_3_MARGIN_Y,
                                     self.surface_rect.width - constants.ActionsSelectionZone.MARGIN_ACTION_X,
                                     defense_active, ActionType.DEFENSE)
        self.ranged_attack_action = Action(constants.ImagesPath.RANGED_ATTACK_ACTION,
                                           constants.ActionsSelectionZone.ACTION_4_MARGIN_Y,
                                           self.surface_rect.width - constants.ActionsSelectionZone.MARGIN_ACTION_X,
                                           ranged_attack_active, ActionType.RANGED_ATTACK)
        self.attack_action = Action(constants.ImagesPath.ATTACK_ACTION,
                                    constants.ActionsSelectionZone.ACTION_5_MARGIN_Y,
                                    self.surface_rect.width - constants.ActionsSelectionZone.MARGIN_ACTION_X,
                                    attack_active, ActionType.ATTACK)
        self.movement_action = Action(constants.ImagesPath.MOVEMENT_ACTION,
                                      constants.ActionsSelectionZone.ACTION_6_MARGIN_Y,
                                      self.surface_rect.width - constants.ActionsSelectionZone.MARGIN_ACTION_X,
                                      movement_active, ActionType.MOVEMENT)
        self.actions_list = [self.magic_action, self.attack_armor_action, self.defense_action,
                             self.ranged_attack_action, self.attack_action, self.movement_action]

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action in self.actions_list:
                if action.hovered and action.selected:
                    action.selected = False
                    return ActionType.NONE
                elif action.hovered and action.active:
                    for elem in self.actions_list:
                        elem.selected = False
                    action.selected = True
                    return action.action_type
            return None

    def update_actions(self, current_action_points, current_hero):
        """
        Met à jour les différentes actions disponibles
        """
        if current_action_points < 1:
            for action in self.actions_list:
                action.active = False
        elif current_action_points < 2:
            self.magic_action.active = False
        if current_hero.is_defending:
            self.defense_action.active = False

    def draw_action(self, action):
        """
        Dessine les différentes actions sur la surface
        """
        # Détermine la couleur de l'action en fonction de ses différents états
        if action.selected and action.hovered and action.active:
            color_alpha = constants.Colors.ORANGE_RED_150_ALPHA
            color = constants.Colors.ORANGE_RED
        elif action.selected and action.active:
            color_alpha = constants.Colors.GOLD_150_ALPHA
            color = constants.Colors.GOLD
        elif action.active and action.hovered:
            color_alpha = constants.Colors.ROYAL_BLUE_150_ALPHA
            color = constants.Colors.ROYAL_BLUE
        elif action.active:
            color_alpha = constants.Colors.ELECTRIC_BLUE_150_ALPHA
            color = constants.Colors.ELECTRIC_BLUE
        else:
            color_alpha = constants.Colors.DARK_SLATE_GRAY_150_ALPHA
            color = constants.Colors.DARK_SLATE_GRAY
        pygame.draw.circle(self.surface, color_alpha, (action.rect.centerx, action.rect.centery),
                           constants.ActionsSelectionZone.CIRCLE_RADIUS, 0)
        pygame.draw.circle(self.surface, color, (action.rect.centerx, action.rect.centery),
                           constants.ActionsSelectionZone.CIRCLE_RADIUS, 2)
        # Dessine la tooltip indiquant le type de l'action
        if action.hovered or (action.selected and action.active):
            self.surface.blit(action.tooltip, action.tooltip_rect)
        self.surface.blit(action.image, action.rect)

    def draw(self, screen, mouse_pos):
        self.surface.fill(constants.Colors.BLACK_FULL_ALPHA)
        for action in self.actions_list:
            # Crée un faux rect pour rendre la collision avec la souris possible
            fake_rect = pygame.Rect(action.rect)
            fake_rect.centerx += self.surface_rect.left
            fake_rect.centery += self.surface_rect.top
            # Contrôle si une des actions est survolée
            action.hovered = True if fake_rect.collidepoint(mouse_pos[0], mouse_pos[1]) else False
            self.draw_action(action)
        screen.blit(self.surface, self.surface_rect)
