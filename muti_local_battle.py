import copy
import sys

import pygame

import action_points_zone
import actions_selection_zone
import constants
import deck_visualization_class
import hero_details_zone
import initiative_bar_class
import square_battlefield_class
import timer_class
import available_squares
from button_text_class import ButtonText
from heroes_class import Heroes
from loading_screen import show_loading_screen
from state_square_battlefield_enum import StateSquareBattlefield
from action_type_enum import ActionType
from alteration_text_class import AlterationText
from alteration_text_class import AlterationType

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class MultiLocalBattle:
    """
    FENETRE DE BATAILLE DEUX JOUEURS EN LOCAL
    """

    def __init__(self, screen, clock, fplayer_name, splayer_name, fplayer_team, splayer_team, fplayer_deck,
                 splayer_deck):
        self.screen = screen
        self.clock = clock
        self.fplayer_name = fplayer_name
        self.splayer_name = splayer_name
        self.fplayer_team = fplayer_team
        self.splayer_team = splayer_team
        self.fplayer_deck = fplayer_deck
        self.splayer_deck = splayer_deck
        # Pas de carte tirée
        self.card_drawn = False
        self.background = pygame.image.load(constants.ImagesPath.BATTLEFIELD_DARK).convert()
        # Initialisation des polices
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_back.set_bold(True)
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_small_bold = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_small_bold.set_bold(True)
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_medium.set_bold(True)
        self.font_name = pygame.font.SysFont(constants.Fonts.ARIAL, 22)
        self.font_name.set_bold(True)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 28)
        self.font_large.set_bold(True)
        # Création du champ de bataille
        self.battlefield = [[square_battlefield_class.SquareBattlefield(j * constants.Battle.SIZE_SQUARE_BF,
                                                                        i * constants.Battle.SIZE_SQUARE_BF)
                             for j in range(constants.Battle.COLUMNS_BF)]
                            for i in range(constants.Battle.LINES_BF)]
        # Ajout des héros sur le champ de bataille
        for hero in self.fplayer_team:
            self.battlefield[hero.pos_bf_i][hero.pos_bf_j].hero = hero
        for hero in self.splayer_team:
            self.battlefield[hero.pos_bf_i][hero.pos_bf_j].hero = hero
        # Timer
        self.timer = timer_class.Timer(timer_min=constants.Battle.MIN_TIMER,
                                       timer_sec=constants.Battle.SEC_TIMER, font=self.font_medium,
                                       pos_centerx=self.screen.get_rect().centerx,
                                       pos_top=constants.Battle.TOP_TEXT_POINTS, color=constants.Colors.WHITE,
                                       color_end=constants.Colors.RED, to_do=self.end_turn, parameters=True)
        # Nombre de points des deux équipes
        self.points_team_render = None
        self.points_opp_team_render = None
        self.points_team_rect = None
        self.points_opp_team_rect = None
        self.update_teams_points()
        # Barre d'initiative
        self.init_bar = initiative_bar_class.InitiativeBar(player_team=self.fplayer_team, adv_team=self.splayer_team)
        # Héro courant
        self.current_hero = self.init_bar.heroes_sorted[0]
        # Le premier joueur commence
        self.current_player = self.current_hero.player_name
        self.current_player_action_points = constants.Battle.ACTION_POINTS
        # Points d'action
        self.action_points_zone = action_points_zone.ActionPointsZone()
        # Sélection des actions
        self.actions_selection_zone = actions_selection_zone.ActionsSelectionZone(
            ActionType.MOVEMENT in self.current_hero.actions_list, ActionType.ATTACK in self.current_hero.actions_list,
            ActionType.RANGED_ATTACK in self.current_hero.actions_list,
            ActionType.DEFENSE in self.current_hero.actions_list,
            ActionType.ATTACK_ARMOR in self.current_hero.actions_list,
            ActionType.MAGIC in self.current_hero.actions_list)
        self.current_action = None
        # Zone des détails du héro
        self.hero_details_zone = hero_details_zone.HeroDetailsZone()
        # Image du deck
        self.deck_open = False
        self.deck_image = pygame.image.load(constants.ImagesPath.DECK)
        self.deck_image_rect = self.deck_image.get_rect()
        self.deck_image_rect.right = \
            constants.Window.SCREEN_WIDTH - constants.Battle.DECK_IMAGE_RECT_MARGIN_RIGHT
        self.deck_image_rect.bottom = \
            constants.Window.SCREEN_HEIGHT - constants.Battle.DECK_IMAGE_RECT_MARGIN_BOT
        self.text_deck = \
            ButtonText(font=self.font_medium, pos_centerx=self.deck_image_rect.centerx, text=constants.Texts.HAND,
                       active=True,
                       pos_centery=constants.Window.SCREEN_HEIGHT - constants.Battle.DECK_TXT_MARGIN)
        # Bouton pour tirer une carte
        self.button_draw = ButtonText(font=self.font_medium, text=constants.Texts.DRAW, active=True,
                                      pos_centerx=self.deck_image_rect.centerx,
                                      pos_bottom=self.deck_image_rect.top - constants.Battle.MARGIN_DRAW)
        # Visualisation du deck
        self.fplayer_deck_visualization = deck_visualization_class.DeckVisualization(self.fplayer_deck, False)
        self.splayer_deck_visualization = deck_visualization_class.DeckVisualization(self.splayer_deck, False)
        # Héros sélectionné
        self.selected_hero = None
        self.available_movement_squares = None
        self.available_attack_squares = None
        self.available_magic_squares = None
        self.available_ranged_squares = None
        # Case sélectionnée pour le mouvement
        self.selected_movement_tile = None
        # Affiche le nom du joueur courant
        self.render_text_name = self.font_name.render(self.current_player, 1, constants.Colors.WHITE)
        self.render_text_name_rect = self.render_text_name.get_rect()
        self.render_text_name_rect.right = self.deck_image_rect.left - constants.Battle.PLAYER_NAME_MARGIN
        self.render_text_name_rect.bottom = self.deck_image_rect.bottom
        self.calculate_actions_squares()
        # Affiche les modifications infligés au héro ciblé
        self.alteration_text = None
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic gauche
                if event.button == 1:
                    # Permet de désectionner un héro au clic sur une partie non utilisée de l'écran
                    remove_selected = True
                    # Si la visualisation du deck n'est pas ouverte
                    if not self.deck_open:
                        # Contrôle les events de la barre d'initiative
                        temp_return_init = self.init_bar.get_event(event, mouse_pos)
                        if isinstance(temp_return_init, Heroes):
                            remove_selected = False
                            self.selected_hero = temp_return_init
                        # Clic sur le bouton de fin de tour
                        elif isinstance(temp_return_init, bool):
                            remove_selected = False
                            self.end_turn(False)
                        # Clic sur une action dans la zone de sélection
                        if self.actions_selection_zone.surface_rect.collidepoint(mouse_pos):
                            self.current_action = self.actions_selection_zone.get_event(event)
                            if self.current_action != None:
                                remove_selected = False
                        # Ouvre le deck au clic sur l'image
                        if self.deck_image_rect.collidepoint(mouse_pos):
                            remove_selected = False
                            self.deck_open = True
                            if self.current_player == self.fplayer_name:
                                self.fplayer_deck_visualization.calculate_hand_size()
                            else:
                                self.splayer_deck_visualization.calculate_hand_size()
                        # Permet de tirer une nouvelle carte
                        elif self.button_draw.rect.collidepoint(mouse_pos) and self.button_draw.active:
                            if self.current_player == self.fplayer_name:
                                self.fplayer_deck_visualization.draw_new_card()
                            else:
                                self.splayer_deck_visualization.draw_new_card()
                            self.current_player_action_points -= constants.Battle.ACTION_POINTS
                            self.card_drawn = True
                    # Traite les évènements de la visualisation du deck
                    else:
                        if self.current_player == self.fplayer_name:
                            temp_selected_card = self.fplayer_deck_visualization.get_event(event, mouse_pos)
                        else:
                            temp_selected_card = self.splayer_deck_visualization.get_event(event, mouse_pos)
                        if temp_selected_card is not None:
                            remove_selected = False
                            self.deck_open = False
                            if (self.current_player == self.fplayer_name and
                                    self.fplayer_deck_visualization.card_drawn) or \
                                    (self.current_player == self.fplayer_name and
                                         self.fplayer_deck_visualization.card_drawn):
                                self.card_drawn = True
                    # Clic sur un élément du champ de bataille
                    for i in range(constants.HeroesDeployment.LINES_BF):
                        for j in range(constants.HeroesDeployment.COLUMNS_BF):
                            if self.battlefield[i][j].rect.collidepoint(mouse_pos) and self.battlefield[i][j].state is not None:
                                remove_selected = False
                                # Clic sur un héro
                                if self.battlefield[i][j].hero is not None:
                                    # Si l'action choisie est la défense
                                    if self.battlefield[i][j].state == StateSquareBattlefield.hero_defense_hovered:
                                        self.current_hero.is_defending = True
                                        self.current_player_action_points -= 1
                                    # Si l'action choisie est l'attaque contre l'armure
                                    elif self.battlefield[i][j].state == StateSquareBattlefield.hero_attack_armor_with_foe_hovered:
                                        if self.battlefield[i][j].hero.is_defending:
                                            damages = self.current_hero.attack_armor // 2
                                        else:
                                            damages = self.current_hero.attack_armor
                                        self.battlefield[i][j].hero.armor_current -= damages
                                        self.alteration_text = AlterationText(False, damages, AlterationType.ARMOR_POINTS, self.battlefield[i][j].hero.battlefield_rect.centerx, self.battlefield[i][j].hero.battlefield_rect.bottom)
                                        self.current_player_action_points -= 1
                                        if self.battlefield[i][j].hero.armor_current < 0:
                                            self.battlefield[i][j].hero.armor_current = 0
                                    # Si l'action choisie est l'attaque
                                    elif self.battlefield[i][j].state == StateSquareBattlefield.hero_attack_with_foe_hovered:
                                        if self.battlefield[i][j].hero.is_defending:
                                            damages = max(0, (self.current_hero.attack - self.battlefield[i][j].hero.armor_current) // 2)
                                        else:
                                            damages = max(1, self.current_hero.attack - self.battlefield[i][j].hero.armor_current)
                                        self.battlefield[i][j].hero.life_points_current -= damages
                                        self.alteration_text = AlterationText(False, damages, AlterationType.LIFE_POINTS, self.battlefield[i][j].hero.battlefield_rect.centerx, self.battlefield[i][j].hero.battlefield_rect.bottom)
                                        self.current_player_action_points -= 1
                                        if self.battlefield[i][j].hero.life_points_current < 0:
                                            self.battlefield[i][j].hero.life_points_current = 0
                                    # Sélectionne le héro si il n'est pas déjà sélectionné
                                    elif self.selected_hero != self.battlefield[i][j].hero:
                                        self.selected_hero = self.battlefield[i][j].hero
                                # Clic sur une case disponible pour le mouvement
                                elif self.battlefield[i][j].state == StateSquareBattlefield.available_hovered or \
                                                self.battlefield[i][j].state == StateSquareBattlefield.available:
                                    self.selected_movement_tile = copy.copy(self.battlefield[i][j])
                                # Second clic sur une case sélectionnée pour le mouvement
                                elif self.selected_movement_tile is not None and self.selected_movement_tile.pos_x == \
                                        self.battlefield[i][j].pos_x and self.selected_movement_tile.pos_y == \
                                        self.battlefield[i][j].pos_y:
                                    self.current_player_action_points -= self.selected_movement_tile.movement_cost
                                    self.selected_movement_tile = None
                                    self.battlefield[i][j].hero = self.selected_hero
                                    self.battlefield[self.selected_hero.pos_bf_i][
                                        self.selected_hero.pos_bf_j].hero = None
                                    self.current_hero.pos_bf_i, self.current_hero.pos_bf_j = i, j
                                    self.calculate_actions_squares()
                                # Mise à jour de l'état de la zone de la sélection des actions et de l'action sélectionnée
                                self.actions_selection_zone.update_actions(self.current_player_action_points,
                                                                           self.current_hero)
                                self.unselect_inactive_action()
                                break
                    # Déselection du héro courant ou de la case choisie pour le mouvement
                    if remove_selected and self.selected_movement_tile is None:
                        self.selected_hero = None
                    elif remove_selected:
                        self.selected_movement_tile = None
            if event.type == pygame.QUIT:
                leave()

    def draw(self, mouse_pos):
        # Affiche le fond d'écran
        self.screen.blit(self.background, (-1, 0))
        # Affiche le champ de bataille
        for elem in self.battlefield:
            for square in elem:
                self.screen.blit(square.render, square.rect)
                # Affiche les héros
                if square.hero is not None:
                    self.screen.blit(square.hero.battlefield, square.hero.battlefield_rect)
                    if square.hero.is_defending:
                        square.hero.draw_defending_visual(self.screen)
        # Afficher le timer
        self.screen.blit(self.timer.render, self.timer.rect)
        # Affiche les éléments si le deck est fermé
        if not self.deck_open:
            # Affiche le nom du joueur courant
            self.screen.blit(self.render_text_name, self.render_text_name_rect)
            # Affiche le texte du nombre de points des deux camps
            self.screen.blit(self.points_team_render, self.points_team_rect)
            self.screen.blit(self.points_opp_team_render, self.points_opp_team_rect)
            # Affiche le visuel des points d'action
            self.action_points_zone.draw(self.screen, self.current_player_action_points)
            # Affiche le visuel des actions sélectionnables
            self.actions_selection_zone.draw(self.screen, mouse_pos)
            # Affiche la barre d'initiative
            if self.current_player == self.fplayer_name:
                self.init_bar.draw(self.screen, mouse_pos, self.fplayer_name)
            else:
                self.init_bar.draw(self.screen, mouse_pos, self.splayer_name)
            # Affiche les détails du héros sélectionné
            if self.selected_hero is not None:
                self.hero_details_zone.draw(self.screen, self.selected_hero)
            # Affiche la carte du deck et son texte
            self.screen.blit(self.deck_image, self.deck_image_rect)
            if self.deck_image_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, constants.Colors.GOLD,
                                 (self.deck_image_rect.x - constants.HeroesDeployment.DECK_IMAGE_RECT_MARGIN,
                                  self.deck_image_rect.y - constants.HeroesDeployment.DECK_IMAGE_RECT_MARGIN,
                                  self.deck_image_rect.width + constants.HeroesDeployment.DECK_IMAGE_RECT_MARGIN,
                                  self.deck_image_rect.height + 3), 2)
                self.screen.blit(self.text_deck.render_hover, self.text_deck.rect)
            else:
                self.screen.blit(self.text_deck.render_base, self.text_deck.rect)
            # Affiche le bouton pour tirer une carte
            if self.button_draw.rect.collidepoint(mouse_pos) and self.button_draw.active:
                self.screen.blit(self.button_draw.render_hover, self.button_draw.rect)
            elif self.button_draw.active:
                self.screen.blit(self.button_draw.render_base, self.button_draw.rect)
            else:
                self.screen.blit(self.button_draw.render_inactive, self.button_draw.rect)
            # Affiche le texte indiquant les modifications sur le héro ciblé
            if self.alteration_text is not None:
                self.alteration_text.draw(self.screen)
                if self.alteration_text.timer == 0:
                    self.alteration_text = None
        # Affiche la visualisation des cartes du deck
        else:
            if self.current_player == self.fplayer_name:
                self.fplayer_deck_visualization.draw(self.screen, mouse_pos)
            else:
                self.splayer_deck_visualization.draw(self.screen, mouse_pos)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def unselect_inactive_action(self):
        """
        Déselectionne l'action courante si elle est inactive
        """
        for action in self.actions_selection_zone.actions_list:
            if action.action_type == self.current_action and not action.active:
                self.current_action = None

    def update_teams_points(self):
        """
        Met à jour le nombre de points total des deux équipes à afficher
        """
        points_team = sum([hero.cost for hero in self.fplayer_team])
        points_opp_team = sum([hero.cost for hero in self.splayer_team])
        self.points_team_render = self.font_medium.render("{}".format(points_team), 1, constants.Colors.GOLD)
        self.points_opp_team_render = self.font_medium.render("{}".format(points_opp_team), 1, constants.Colors.RED)
        self.points_team_rect = self.points_team_render.get_rect()
        self.points_opp_team_rect = self.points_opp_team_render.get_rect()
        self.points_team_rect.right = self.screen.get_rect().centerx - constants.HeroesDeployment.MARGIN_POINTS
        self.points_opp_team_rect.left = self.screen.get_rect().centerx + constants.HeroesDeployment.MARGIN_POINTS
        self.points_team_rect.top = constants.HeroesDeployment.TOP_TEXT_POINTS
        self.points_opp_team_rect.top = constants.HeroesDeployment.TOP_TEXT_POINTS

    def calculate_available_movement_squares(self):
        """
        Calcule les cases disponibles pour le mouvement du héro
        """
        if self.current_player_action_points > 1:
            avail_squares = available_squares.AvailableSquares(self.battlefield,
                                                               (self.current_hero.pos_bf_i, self.current_hero.pos_bf_j),
                                                               self.current_hero.speed)
        else:
            avail_squares = available_squares.AvailableSquares(self.battlefield,
                                                               (self.current_hero.pos_bf_i, self.current_hero.pos_bf_j),
                                                               self.current_hero.speed // 2)
        self.available_movement_squares = avail_squares.available_squares

    def calculate_available_attack_squares(self):
        """
        Calcule les cases disponibles pour l'attaque du héro
        """
        for i in range(self.current_hero.pos_bf_i - 1, self.current_hero.pos_bf_i + 2):
            for j in range(self.current_hero.pos_bf_j - 1, self.current_hero.pos_bf_j + 2):
                if 0 <= i < constants.Battle.LINES_BF and 0 <= j < constants.Battle.COLUMNS_BF and (
                        self.battlefield[i][j].hero is None or (
                        self.battlefield[i][j].hero is not None and self.battlefield[i][j].hero.player_name != self.current_hero.player_name)):
                    self.available_attack_squares.append((i, j))

    def calculate_available_magic_squares(self):
        """
        Calcule les cases disponibles pour l'attaque magique du héro
        """
        avail_squares = available_squares.AvailableSquares(self.battlefield,
                                                           (self.current_hero.pos_bf_i, self.current_hero.pos_bf_j),
                                                           self.current_hero.magic, self.current_player, True)
        self.available_magic_squares = avail_squares.available_squares

    def calculate_available_ranged_squares(self):
        """
        Calcule les cases disponibles pour l'attaque à distance du héro
        """
        avail_squares = available_squares.AvailableSquares(self.battlefield,
                                                           (self.current_hero.pos_bf_i, self.current_hero.pos_bf_j),
                                                           self.current_hero.scope, self.current_player, True)
        self.available_ranged_squares = avail_squares.available_squares

    def calculate_actions_squares(self):
        """
        Calcule les cases disponibles en fonction des différentes actions
        """
        show_loading_screen(self.screen)
        self.available_movement_squares = {}
        self.available_attack_squares = []
        self.available_magic_squares = {}
        if self.current_player_action_points > 0:
            self.calculate_available_movement_squares()
            self.calculate_available_attack_squares()
            if self.current_hero.magic > 0:
                self.calculate_available_magic_squares()
            if self.current_hero.scope > 0:
                self.calculate_available_ranged_squares()

    def update_battlefield(self, mouse_pos):
        """
        Met à jour les cases du champ de bataille
        """
        for i in range(constants.HeroesDeployment.LINES_BF):
            for j in range(constants.HeroesDeployment.COLUMNS_BF):
                # Cases disponibles pour le déplacement
                if self.selected_hero == self.current_hero and self.current_action == ActionType.MOVEMENT and (i, j) in self.available_movement_squares.keys():
                    temp_rect = pygame.Rect(self.battlefield[i][j].rect.left + 1, self.battlefield[i][j].rect.top + 1,
                                            self.battlefield[i][j].rect.width - 1,
                                            self.battlefield[i][j].rect.height - 1)
                    if self.selected_movement_tile is None:
                        if temp_rect.collidepoint(mouse_pos):
                            self.battlefield[i][j].render_available_hovered(True, self.available_movement_squares[
                                (i, j)] <= self.current_hero.speed // 2)
                        else:
                            self.battlefield[i][j].render_available()
                    # Si une case a été sélectionnée pour le mouvement
                    else:
                        if self.battlefield[i][j].pos_x == self.selected_movement_tile.pos_x and self.battlefield[i][j].pos_y == self.selected_movement_tile.pos_y:
                            if temp_rect.collidepoint(mouse_pos):
                                self.battlefield[i][j].render_selected_hovered(
                                    self.selected_movement_tile.movement_cost < 2)
                            else:
                                self.battlefield[i][j].render_available_hovered(True, self.selected_movement_tile.movement_cost < 2)
                        else:
                            self.battlefield[i][j].render_none()
                # Cases disponibles pour l'attaque
                elif self.selected_hero == self.current_hero and self.current_action == ActionType.ATTACK and (
                i, j) in self.available_attack_squares:
                    temp_rect = pygame.Rect(self.battlefield[i][j].rect.left + 1, self.battlefield[i][j].rect.top + 1,
                                            self.battlefield[i][j].rect.width - 1,
                                            self.battlefield[i][j].rect.height - 1)
                    if self.battlefield[i][j].hero is not None:
                        if temp_rect.collidepoint(mouse_pos):
                            self.battlefield[i][j].render_hero_attack_with_foe_hovered()
                        else:
                            self.battlefield[i][j].render_hero_attack_with_foe()
                    else:
                        self.battlefield[i][j].render_hero_attack()
                # Cases disponibles pour la magie
                elif self.selected_hero == self.current_hero and self.current_action == ActionType.MAGIC and (
                i, j) in self.available_magic_squares.keys():
                    temp_rect = pygame.Rect(self.battlefield[i][j].rect.left + 1, self.battlefield[i][j].rect.top + 1,
                                            self.battlefield[i][j].rect.width - 1,
                                            self.battlefield[i][j].rect.height - 1)
                    if self.battlefield[i][j].hero is not None:
                        if temp_rect.collidepoint(mouse_pos):
                            self.battlefield[i][j].render_hero_magic_with_foe_hovered()
                        else:
                            self.battlefield[i][j].render_hero_magic_with_foe()
                    else:
                        self.battlefield[i][j].render_hero_magic()
                # Cases disponibles pour l'attaque à distance
                elif self.selected_hero == self.current_hero and self.current_action == ActionType.RANGED_ATTACK and (
                i, j) in self.available_ranged_squares.keys():
                    temp_rect = pygame.Rect(self.battlefield[i][j].rect.left + 1, self.battlefield[i][j].rect.top + 1,
                                            self.battlefield[i][j].rect.width - 1,
                                            self.battlefield[i][j].rect.height - 1)
                    if self.battlefield[i][j].hero is not None:
                        if temp_rect.collidepoint(mouse_pos):
                            self.battlefield[i][j].render_hero_ranged_attack_with_foe_hovered()
                        else:
                            self.battlefield[i][j].render_hero_ranged_attack_with_foe()
                    else:
                        self.battlefield[i][j].render_hero_ranged_attack()
                # Cases disponibles pour l'attaque
                elif self.selected_hero == self.current_hero and self.current_action == ActionType.ATTACK_ARMOR and (
                i, j) in self.available_attack_squares:
                    temp_rect = pygame.Rect(self.battlefield[i][j].rect.left + 1, self.battlefield[i][j].rect.top + 1,
                                            self.battlefield[i][j].rect.width - 1,
                                            self.battlefield[i][j].rect.height - 1)
                    if self.battlefield[i][j].hero is not None:
                        if temp_rect.collidepoint(mouse_pos):
                            self.battlefield[i][j].render_hero_attack_armor_with_foe_hovered()
                        else:
                            self.battlefield[i][j].render_hero_attack_armor_with_foe()
                    else:
                        self.battlefield[i][j].render_hero_attack_armor()
                # Héro courant et défense sélectionnée
                elif self.selected_hero == self.current_hero and self.current_action == ActionType.DEFENSE and \
                                self.battlefield[i][j].hero == self.current_hero:
                    temp_rect = pygame.Rect(self.battlefield[i][j].rect.left + 1, self.battlefield[i][j].rect.top + 1,
                                            self.battlefield[i][j].rect.width - 1,
                                            self.battlefield[i][j].rect.height - 1)
                    if temp_rect.collidepoint(mouse_pos):
                        self.battlefield[i][j].render_hero_defense_hovered()
                    else:
                        self.battlefield[i][j].render_hero_defense()
                # Héro sélectionné
                elif self.selected_hero is not None and self.battlefield[i][j].hero == self.selected_hero:
                    self.selected_hero.pos_bf_i = i
                    self.selected_hero.pos_bf_j = j
                    # Héro courant sélectionné
                    if self.selected_hero == self.current_hero:
                        self.battlefield[i][j].render_current_selected()
                    elif self.battlefield[i][j].hero.player_name == self.current_player:
                        self.battlefield[i][j].render_hero_selected()
                    else:
                        self.battlefield[i][j].render_foe_selected()
                # Héro courant
                elif self.battlefield[i][j].hero == self.current_hero:
                    if self.battlefield[i][j].rect.collidepoint(mouse_pos):
                        self.battlefield[i][j].render_current_hovered()
                    else:
                        self.battlefield[i][j].render_current()
                # Héro survolé
                elif self.battlefield[i][j].rect.collidepoint(mouse_pos) and self.battlefield[i][j].hero is not None:
                    if self.battlefield[i][j].hero.player_name == self.current_player:
                        self.battlefield[i][j].render_hero_hovered()
                    else:
                        self.battlefield[i][j].render_foe_hovered()
                # Héro idle
                elif self.battlefield[i][j].hero is not None:
                    if self.battlefield[i][j].hero.player_name == self.current_player:
                        self.battlefield[i][j].render_hero()
                    else:
                        self.battlefield[i][j].render_foe()
                else:
                    self.battlefield[i][j].render_none()

    def update_button_draw(self):
        """
        Met à jour l'état du bouton pour tirer une carte
        """
        if self.card_drawn or self.current_player_action_points < constants.Battle.ACTION_POINTS \
                or (self.current_player == self.fplayer_name and len(self.fplayer_deck_visualization.deck) < 1) or \
                (self.current_player == self.splayer_name and len(self.splayer_deck_visualization.deck) < 1):
            self.button_draw.active = False
        else:
            self.button_draw.active = True

    def end_turn(self, from_timer):
        """
        Met fin au tour en cours
        """
        if from_timer:
            self.init_bar.end_turn()
        self.current_hero = self.init_bar.heroes_sorted[0]
        self.current_hero.is_defending = False
        self.current_player_action_points = constants.Battle.ACTION_POINTS
        self.current_player = self.init_bar.heroes_sorted[0].player_name
        self.render_text_name = self.font_name.render(self.current_player, 1, constants.Colors.WHITE)
        self.calculate_actions_squares()
        self.card_drawn = False
        self.fplayer_deck_visualization.card_drawn = False
        self.splayer_deck_visualization.card_drawn = False
        self.actions_selection_zone = actions_selection_zone.ActionsSelectionZone(
            ActionType.MOVEMENT in self.current_hero.actions_list, ActionType.ATTACK in self.current_hero.actions_list,
            ActionType.RANGED_ATTACK in self.current_hero.actions_list,
            ActionType.DEFENSE in self.current_hero.actions_list,
            ActionType.ATTACK_ARMOR in self.current_hero.actions_list,
            ActionType.MAGIC in self.current_hero.actions_list)
        self.current_action = None
        self.timer = timer_class.Timer(timer_min=constants.Battle.MIN_TIMER,
                                       timer_sec=constants.Battle.SEC_TIMER, font=self.font_medium,
                                       pos_centerx=self.screen.get_rect().centerx,
                                       pos_top=constants.Battle.TOP_TEXT_POINTS, color=constants.Colors.WHITE,
                                       color_end=constants.Colors.RED, to_do=self.end_turn, parameters=True)

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.timer.update_timer()
            self.get_event(pygame.event.get(), mouse_pos)
            self.update_battlefield(mouse_pos)
            self.update_button_draw()
            self.update_teams_points()
            self.draw(mouse_pos)
