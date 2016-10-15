import pygame
import sys
import constants
import hero_details_zone
import initiative_bar_class
import deck_visualization_class
import muti_local_battle
import square_battlefield_class
import timer_class
from button_text_class import ButtonText
from cards_class import Cards
from heroes_class import Heroes

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class HeroesDeployment:
    """
    FENETRE DE DEPLOIEMENT DES HEROS SUR LE CHAMPS DE BATAILLE
    """

    def __init__(self, screen, clock, fplayer_name, splayer_name, fplayer_team, splayer_team, fplayer_deck,
                 splayer_deck, is_fplayer_deployed):
        self.screen = screen
        self.clock = clock
        self.fplayer_name = fplayer_name
        self.splayer_name = splayer_name
        self.fplayer_team = fplayer_team
        self.splayer_team = splayer_team
        self.fplayer_deck = fplayer_deck
        self.splayer_deck = splayer_deck
        self.is_fplayer_deployed = is_fplayer_deployed
        # Initialisation du fond d'écran
        self.background = pygame.image.load(constants.ImagesPath.BATTLEFIELD_DARK).convert()
        # Initialisation des polices
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_back.set_bold(True)
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_medium.set_bold(True)
        self.font_name = pygame.font.SysFont(constants.Fonts.ARIAL, 22)
        self.font_name.set_bold(True)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 28)
        self.font_large.set_bold(True)
        if not is_fplayer_deployed:
            self.team = self.treat_heroes_double(fplayer_team)
            self.deck = self.treat_cards_double(fplayer_deck)
            self.opposing_team = self.treat_heroes_double(splayer_team)
        else:
            self.team = self.treat_heroes_double(splayer_team)
            self.deck = self.treat_cards_double(splayer_deck)
            self.opposing_team = self.treat_heroes_double(fplayer_team)
        # Création du champ de bataille
        self.battlefield = \
            [[square_battlefield_class.SquareBattlefield(j * constants.HeroesDeployment.SIZE_SQUARE_BF,
                                                         i * constants.HeroesDeployment.SIZE_SQUARE_BF)
              for j in range(constants.HeroesDeployment.COLUMNS_BF)]
             for i in range(constants.HeroesDeployment.LINES_BF)]
        # Position d'origine des héros
        if not self.is_fplayer_deployed:
            i, j = 0, 0
            for hero in self.team:
                hero.pos_bf_i = i
                hero.pos_bf_j = j
                self.battlefield[i][j].hero = hero
                i += 1
                if i == constants.HeroesDeployment.LINES_BF:
                    i = 0
                    j += 1
        else:
            i, j = 0, constants.HeroesDeployment.COLUMNS_BF - 1
            for hero in self.team:
                hero.pos_bf_i = i
                hero.pos_bf_j = j
                self.battlefield[i][j].hero = hero
                i += 1
                if i == constants.HeroesDeployment.LINES_BF:
                    i = 0
                    j -= 1
        # Background du texte de démarrage
        self.back_text = pygame.image.load(constants.ImagesPath.BACK_START_DEPLOYMENT)
        self.back_text_rect = self.back_text.get_rect()
        self.back_text_rect.centerx = self.screen.get_rect().centerx
        self.back_text_rect.top = constants.HeroesDeployment.POS_Y_BACK_START
        # Boutons texte
        self.list_buttons_text = list()
        self.list_buttons_text.append(ButtonText(font=self.font_large, pos_centerx=self.screen.get_rect().centerx,
                                                 pos_centery=constants.HeroesDeployment.POS_Y_BACK_START +
                                                 self.back_text_rect.height // 2, on_clic=self.launch_next_page,
                                                 text=constants.Texts.START, active=True))
        # Timer
        self.timer = timer_class.Timer(timer_min=constants.HeroesDeployment.MIN_TIMER,
                                       timer_sec=constants.HeroesDeployment.SEC_TIMER, font=self.font_medium,
                                       pos_centerx=self.screen.get_rect().centerx,
                                       pos_top=self.back_text_rect.bottom, color=constants.Colors.WHITE,
                                       color_end=constants.Colors.RED, to_do=self.launch_next_page)
        # Nombre de points des deux équipes
        points_team = sum([hero.cost for hero in self.team])
        points_opp_team = sum([hero.cost for hero in self.opposing_team])
        self.points_team_render = self.font_medium.render("{}".format(points_team), 1, constants.Colors.GOLD)
        self.points_opp_team_render = self.font_medium.render("{}".format(points_opp_team), 1, constants.Colors.RED)
        self.points_team_rect = self.points_team_render.get_rect()
        self.points_opp_team_rect = self.points_opp_team_render.get_rect()
        self.points_team_rect.right = self.screen.get_rect().centerx - constants.HeroesDeployment.MARGIN_POINTS
        self.points_opp_team_rect.left = self.screen.get_rect().centerx + constants.HeroesDeployment.MARGIN_POINTS
        self.points_team_rect.top = constants.HeroesDeployment.TOP_TEXT_POINTS
        self.points_opp_team_rect.top = constants.HeroesDeployment.TOP_TEXT_POINTS
        # Barre d'initiative
        self.init_bar = initiative_bar_class.InitiativeBar(player_team=self.team)
        # Zone des détails du héro
        self.hero_details_zone = hero_details_zone.HeroDetailsZone()
        # Image du deck
        self.deck_open = False
        self.deck_image = pygame.image.load(constants.ImagesPath.DECK)
        self.deck_image_rect = self.deck_image.get_rect()
        self.deck_image_rect.right = \
            constants.Window.SCREEN_WIDTH - constants.HeroesDeployment.DECK_IMAGE_RECT_MARGIN_RIGHT
        self.deck_image_rect.bottom = \
            constants.Window.SCREEN_HEIGHT - constants.HeroesDeployment.DECK_IMAGE_RECT_MARGIN_BOT
        self.text_deck = \
            ButtonText(font=self.font_medium, pos_centerx=self.deck_image_rect.centerx, text=constants.Texts.DECK,
                       active=True,
                       pos_centery=constants.Window.SCREEN_HEIGHT - constants.HeroesDeployment.DECK_TXT_MARGIN)
        # Visualisation du deck
        self.deck_visualization = deck_visualization_class.DeckVisualization(self.deck, True)
        # Héros sélectionné
        self.selected_hero = None
        # Affiche le nom du joueur courant
        if self.is_fplayer_deployed:
            self.render_text_name = self.font_name.render(self.splayer_name, 1, constants.Colors.WHITE)
        else:
            self.render_text_name = self.font_name.render(self.fplayer_name, 1, constants.Colors.WHITE)
        self.render_text_name_rect = self.render_text_name.get_rect()
        self.render_text_name_rect.right = self.deck_image_rect.left - 20
        self.render_text_name_rect.bottom = self.deck_image_rect.bottom
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
                        temp_selected_hero = self.init_bar.get_event(event, mouse_pos)
                        if temp_selected_hero is not None:
                            remove_selected_hero = False
                            self.selected_hero = temp_selected_hero
                        # Traite les évènements si la visualisation du deck n'est pas ouverte
                        if self.deck_image_rect.collidepoint(mouse_pos):
                            remove_selected_hero = False
                            self.deck_open = True
                            self.deck_visualization.calculate_hand_size()
                    # Traite les évènements de la visualisation du deck
                    else:
                        temp_selected_card = self.deck_visualization.get_event(event, mouse_pos)
                        if temp_selected_card is not None:
                            remove_selected_hero = False
                            self.deck_open = False
                    # Clic sur un bouton
                    for button in self.list_buttons_text:
                        if button.rect.collidepoint(mouse_pos):
                            button.on_clic()
                    # Clic sur un héro ou sur une case vide
                    for i in range(constants.HeroesDeployment.LINES_BF):
                        for j in range(constants.HeroesDeployment.COLUMNS_BF):
                            if self.battlefield[i][j].rect.collidepoint(mouse_pos):
                                remove_selected_hero = False
                                if self.battlefield[i][j].hero is not None:
                                    self.selected_hero = self.battlefield[i][j].hero
                                elif (not self.is_fplayer_deployed and j <= constants.HeroesDeployment.LIMIT_FPLAYER) \
                                        or (self.is_fplayer_deployed and j >= constants.HeroesDeployment.LIMIT_SPLAYER):
                                    self.battlefield[i][j].hero = self.selected_hero
                                    self.battlefield[self.selected_hero.pos_bf_i][self.selected_hero.pos_bf_j].hero = \
                                        None
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
        # Affiche l'image du texte de démarrage
        self.screen.blit(self.back_text, self.back_text_rect)
        # Afficher le timer
        self.screen.blit(self.timer.render, self.timer.rect)
        # Affiche les éléments si le deck est fermé
        if not self.deck_open:
            # Affiche le nom du joueur courant
            self.screen.blit(self.render_text_name, self.render_text_name_rect)
            # Affiche le texte du nombre de points des deux camps
            self.screen.blit(self.points_team_render, self.points_team_rect)
            self.screen.blit(self.points_opp_team_render, self.points_opp_team_rect)
            # Affiche les détails du héros sélectionné
            if self.selected_hero is not None:
                self.hero_details_zone.draw(self.screen, self.selected_hero)
            # Affiche la barre d'initiative
            self.init_bar.draw(self.screen, mouse_pos, self.fplayer_name)
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
        # Affiche la visualisation des cartes du deck
        else:
            self.deck_visualization.draw(self.screen, mouse_pos)
        # Affiche les boutons texte
        for button in self.list_buttons_text:
            if not button.active:
                self.screen.blit(button.render_inactive, button.rect)
            elif button.rect.collidepoint(mouse_pos):
                self.screen.blit(button.render_hover, button.rect)
            else:
                self.screen.blit(button.render_base, button.rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def treat_heroes_double(self, team):
        """
        Créations de nouvelles de héros pour les éléments sélectionnées en plusieurs exemplaires
        """
        team_to_return = list()
        for hero in team:
            if hero.count_hero_in_list(team) > 1 and not hero.search_hero_in_list(team_to_return):
                for i in range(hero.count_hero_in_list(team)):
                    team_to_return.append(Heroes(name=hero.name, speed=hero.speed, initiative=hero.initiative,
                                                 life_points=hero.life_points, life_points_current=hero.life_points,
                                                 magic_points=hero.magic_points, magic=hero.magic,
                                                 magic_points_current=hero.magic_points, armor=hero.armor,
                                                 armor_current=hero.armor, scope=hero.scope, size=hero.size,
                                                 agility=hero.agility, stamina=hero.stamina, cost=hero.cost,
                                                 strength=hero.strength, mental=hero.mental, attack=hero.attack,
                                                 unique=hero.unique, skills=hero.skills, font_small=self.font_small,
                                                 description=hero.description, token_text=hero.token_text,
                                                 miniature_text=hero.miniature_text, font_large=self.font_large,
                                                 token_init_text=hero.token_init_text, player_name=hero.player_name,
                                                 battlefield_text=hero.battlefield_text))
            elif not hero.search_hero_in_list(team_to_return):
                team_to_return.append(hero)
        team_to_return.sort(key=lambda data: data.name)
        return team_to_return

    def treat_cards_double(self, deck):
        """
        Créations de nouvelles de cartes pour les éléments sélectionnées en plusieurs exemplaires
        """
        deck_to_return = list()
        for card in deck:
            if card.possessed - card.available > 1:
                for i in range(card.possessed - card.available):
                    deck_to_return.append(Cards(name=card.name, cost=card.cost, effect=card.effect,
                                                description=card.description, faction=card.faction,
                                                linked_to=card.linked_to, available=0, possessed=0,
                                                limited_to=card.limited_to, zoom_text=card.zoom_text,
                                                miniature_text=card.miniature_text, font_small=self.font_small,
                                                font_medium=self.font_medium, font_large=self.font_large))
            else:
                deck_to_return.append(card)
        deck_to_return.sort(key=lambda data: data.name)
        return deck_to_return

    def launch_next_page(self):
        """
        Lance la prochaine page
        """
        if not self.is_fplayer_deployed:
            self.__init__(self.screen, self.clock, self.fplayer_name, self.splayer_name, self.fplayer_team,
                          self.splayer_team, self.fplayer_deck, self.splayer_deck, True)
        else:
            muti_local_battle.MultiLocalBattle(self.screen, self.clock, self.fplayer_name, self.splayer_name,
                                               self.fplayer_team, self.splayer_team, self.fplayer_deck,
                                               self.splayer_deck)

    def update_battlefield(self, mouse_pos):
        """
        Met à jour les cases du champ de bataille
        """
        for i in range(constants.HeroesDeployment.LINES_BF):
            for j in range(constants.HeroesDeployment.COLUMNS_BF):
                if (not self.is_fplayer_deployed and j > constants.HeroesDeployment.LIMIT_FPLAYER) or \
                        (self.is_fplayer_deployed and j < constants.HeroesDeployment.LIMIT_SPLAYER):
                    self.battlefield[i][j].render_none()
                elif self.selected_hero is not None and self.battlefield[i][j].hero == self.selected_hero:
                    if self.battlefield[i][j].hero.player_name == self.fplayer_name:
                        self.battlefield[i][j].render_hero_selected()
                    else:
                        self.battlefield[i][j].render_foe_selected()
                    self.selected_hero.pos_bf_i = i
                    self.selected_hero.pos_bf_j = j
                elif self.battlefield[i][j].rect.collidepoint(mouse_pos) and self.battlefield[i][j].hero is not None:
                    if self.battlefield[i][j].hero.player_name == self.fplayer_name:
                        self.battlefield[i][j].render_hero_hovered()
                    else:
                        self.battlefield[i][j].render_foe_hovered()
                elif self.battlefield[i][j].hero is not None:
                    if self.battlefield[i][j].hero.player_name == self.fplayer_name:
                        self.battlefield[i][j].render_hero()
                    else:
                        self.battlefield[i][j].render_foe()
                else:
                    self.battlefield[i][j].render_available()

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.timer.update_timer()
            self.get_event(pygame.event.get(), mouse_pos)
            self.update_battlefield(mouse_pos)
            self.draw(mouse_pos)
