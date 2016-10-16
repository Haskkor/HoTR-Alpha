import pygame
import sys
import constants
import deck_visualization_class
import hero_details_zone
import initiative_bar_class
import square_battlefield_class
import timer_class
from button_text_class import ButtonText
from heroes_class import Heroes

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class MultiLocalBattle:
    """
    FENETRE DE BATAILLE DEUX JOUEURS EN LOCAL
    """

    # TEST GIT AVEC PYCHARM

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
        # Le premier jour commence
        self.current_player = fplayer_name
        self.background = pygame.image.load(constants.ImagesPath.BATTLEFIELD_DARK).convert()
        # Initialisation des polices
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_back.set_bold(True)
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_small_bold = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_small_bold.set_bold(True)
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_medium.set_bold(True)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 28)
        self.font_large.set_bold(True)
        # Création du champ de bataille
        self.battlefield = [[square_battlefield_class.SquareBattlefield(j * constants.LocalTwoBattle.SIZE_SQUARE_BF,
                                                                        i * constants.LocalTwoBattle.SIZE_SQUARE_BF)
                             for j in range(constants.LocalTwoBattle.COLUMNS_BF)]
                            for i in range(constants.LocalTwoBattle.LINES_BF)]
        # Ajout des héros sur le champ de bataille
        for hero in self.fplayer_team:
            self.battlefield[hero.pos_bf_i][hero.pos_bf_j].hero = hero
        for hero in self.splayer_team:
            self.battlefield[hero.pos_bf_i][hero.pos_bf_j].hero = hero
        # Timer
        self.timer = timer_class.Timer(timer_min=constants.LocalTwoBattle.MIN_TIMER,
                                       timer_sec=constants.LocalTwoBattle.SEC_TIMER, font=self.font_medium,
                                       pos_centerx=self.screen.get_rect().centerx,
                                       pos_top=constants.LocalTwoBattle.TOP_TEXT_POINTS, color=constants.Colors.WHITE,
                                       color_end=constants.Colors.RED, to_do=print, parameters="GOGOGO")
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
        # Zone des détails du héro
        self.hero_details_zone = hero_details_zone.HeroDetailsZone()
        # Image du deck
        self.deck_open = False
        self.deck_image = pygame.image.load(constants.ImagesPath.DECK)
        self.deck_image_rect = self.deck_image.get_rect()
        self.deck_image_rect.right = \
            constants.Window.SCREEN_WIDTH - constants.LocalTwoBattle.DECK_IMAGE_RECT_MARGIN_RIGHT
        self.deck_image_rect.bottom = \
            constants.Window.SCREEN_HEIGHT - constants.LocalTwoBattle.DECK_IMAGE_RECT_MARGIN_BOT
        self.text_deck = \
            ButtonText(font=self.font_medium, pos_centerx=self.deck_image_rect.centerx, text=constants.Texts.HAND,
                       active=True,
                       pos_centery=constants.Window.SCREEN_HEIGHT - constants.LocalTwoBattle.DECK_TXT_MARGIN)
        # Bouton pour tirer une carte
        self.button_draw = ButtonText(font=self.font_medium, text=constants.Texts.DRAW, active=True,
                                      pos_centerx=self.deck_image_rect.centerx,
                                      pos_bottom=self.deck_image_rect.top - constants.LocalTwoBattle.MARGIN_DRAW)
        # Visualisation du deck
        self.fplayer_deck_visualization = deck_visualization_class.DeckVisualization(self.fplayer_deck, False)
        self.splayer_deck_visualization = deck_visualization_class.DeckVisualization(self.splayer_deck, False)
        # Héros sélectionné
        self.selected_hero = None
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic gauche
                if event.button == 1:
                    # Permet de désectionner un héro au clic sur une partie non utilisée de l'écran
                    remove_selected_hero = True
                    # Si la visualisation du deck n'est pas ouverte, controle les events de la barre d'initiative
                    if not self.deck_open:
                        temp_return_init = self.init_bar.get_event(event, mouse_pos)
                        if isinstance(temp_return_init, Heroes):
                            remove_selected_hero = False
                            self.selected_hero = temp_return_init
                        elif isinstance(temp_return_init, bool):
                            remove_selected_hero = False
                            self.current_hero = self.init_bar.heroes_sorted[0]
                        # Traite les évènements si la visualisation du deck n'est pas ouverte
                        if self.deck_image_rect.collidepoint(mouse_pos):
                            remove_selected_hero = False
                            self.deck_open = True
                            self.deck_visualization.calculate_hand_size()
                        # Permet de tirer une nouvelle carte
                        elif self.button_draw.rect.collidepoint(mouse_pos) and self.button_draw.active:
                            self.deck_visualization.draw_new_card()
                    # Traite les évènements de la visualisation du deck
                    else:
                        temp_selected_card = self.deck_visualization.get_event(event, mouse_pos)
                        if temp_selected_card is not None:
                            remove_selected_hero = False
                            self.deck_open = False
                    # Clic sur un héro ou sur une case vide
                    for i in range(constants.HeroesDeployment.LINES_BF):
                        for j in range(constants.HeroesDeployment.COLUMNS_BF):
                            if self.battlefield[i][j].rect.collidepoint(mouse_pos):
                                remove_selected_hero = False
                                if self.battlefield[i][j].hero is not None:
                                    self.selected_hero = self.battlefield[i][j].hero
                                break
                    if remove_selected_hero:
                        self.selected_hero = None
            if event.type == pygame.QUIT:
                leave()

    def draw(self, mouse_pos):
        # Affiche le fond d'écran
        self.screen.blit(self.background, (-1, 0))
        # Affiche le champ de bataille
        for elem in self.battlefield:
            for square in elem:
                self.screen.blit(square.render, square.rect)
                if square.hero is not None:
                    self.screen.blit(square.hero.battlefield, square.hero.battlefield_rect)
        # Afficher le timer
        self.screen.blit(self.timer.render, self.timer.rect)
        # Affiche les éléments si le deck est fermé
        if not self.deck_open:
            # Affiche le texte du nombre de points des deux camps
            self.screen.blit(self.points_team_render, self.points_team_rect)
            self.screen.blit(self.points_opp_team_render, self.points_opp_team_rect)
            # Affiche les détails du héros sélectionné
            if self.selected_hero is not None:
                self.hero_details_zone.draw(self.screen, self.selected_hero)
            # Affiche la barre d'initiative
            self.init_bar.draw(self.screen, mouse_pos, constants.Texts.PLAYER_1)
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
        # Affiche la visualisation des cartes du deck
        else:
            self.deck_visualization.draw(self.screen, mouse_pos)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

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

    def update_battlefield(self, mouse_pos):
        """
        Met à jour les cases du champ de bataille
        """
        for i in range(constants.HeroesDeployment.LINES_BF):
            for j in range(constants.HeroesDeployment.COLUMNS_BF):
                if self.selected_hero is not None and self.battlefield[i][j].hero == self.selected_hero:
                    self.selected_hero.pos_bf_i = i
                    self.selected_hero.pos_bf_j = j
                    if self.battlefield[i][j].hero.player_name == self.player:
                        self.battlefield[i][j].render_hero_selected()
                    else:
                        self.battlefield[i][j].render_foe_selected()
                elif self.battlefield[i][j].rect.collidepoint(mouse_pos) and self.battlefield[i][j].hero is not None:
                    if self.battlefield[i][j].hero.player_name == self.player:
                        self.battlefield[i][j].render_hero_hovered()
                    else:
                        self.battlefield[i][j].render_foe_hovered()
                elif self.battlefield[i][j].hero is not None:
                    if self.battlefield[i][j].hero.player_name == self.player:
                        self.battlefield[i][j].render_hero()
                    else:
                        self.battlefield[i][j].render_foe()
                elif self.selected_hero == self.current_hero and constants.LocalTwoBattle.LINES_BF > i >= 0 \
                        and self.current_hero.pos_bf_i + self.current_hero.speed > i > self.current_hero.pos_bf_i - self.current_hero.speed \
                        and constants.LocalTwoBattle.COLUMNS_BF > j >= 0 \
                        and self.current_hero.pos_bf_j + self.current_hero.speed > j > self.current_hero.pos_bf_j - self.current_hero.speed:
                    self.battlefield[i][j].render_available()
                else:
                    self.battlefield[i][j].render_none()

    def update_button_draw(self):
        """
        Met à jour l'état du bouton pour tirer une carte
        """
        if len(self.deck_visualization.deck) < 1:
            self.button_draw.active = False

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.timer.update_timer()
            self.get_event(pygame.event.get(), mouse_pos)
            self.update_battlefield(mouse_pos)
            self.update_button_draw()
            self.draw(mouse_pos)
