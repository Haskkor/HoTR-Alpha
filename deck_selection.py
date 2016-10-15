import pygame
import sys
import constants
import heroes_deployment
import overlay_load
import overlay_save
import overlay_zoom_card
import team_selection
from button_image_class import ButtonImage
from button_text_class import ButtonText
from cards_class import Cards
from load_class import Load
from textbox_class import TextBox

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class DeckSelection:
    """
    FENETRE DE SELECTION DU DECK DE CARTES
    """

    def __init__(self, *args):
        # Récupération de l'écran, du timer, du total de points disponibles, du nom des joueurs, des équipes choisies
        # et des decks choisis
        self.screen = args[0][0]
        self.clock = args[0][1]
        self.total_points = args[0][2]
        self.fplayer_name = args[0][3]
        self.splayer_name = args[0][4]
        self.fplayer_team = args[0][5]
        self.splayer_team = args[0][6]
        self.fplayer_deck = args[0][7]
        self.splayer_deck = args[0][8]
        self.cards_in_deck = args[0][9]
        self.render_cards_in_deck = []
        if self.fplayer_deck is None:
            self.list_in_team = self.fplayer_team
        else:
            self.list_in_team = self.splayer_team
        # Variables (mode_list : 0=all, 1=evil, 2=good; mode_sort : 0: name, 1: cost, 2: available)
        self.current_page = 1
        self.mode_list = 0
        self.mode_sort = 0
        # Initialisation des polices, du fond d'écran et de la zone des détails
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_back.set_bold(True)
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 22)
        self.font_large.set_bold(True)
        self.font_medium.set_bold(True)
        self.background = pygame.image.load(constants.ImagesPath.T_S_SCREEN).convert()
        self.frame = pygame.image.load(constants.ImagesPath.FRAME_DETAILS)
        self.frame_rect = self.frame.get_rect()
        self.frame_rect.left, self.frame_rect.top = constants.TeamSelection.DETAILS_ZONE, 0
        # Récupère les héros dans le fichier binaire
        load = Load(constants.Files.CARDS_FILE)
        self.cards = load.load
        # Crée une liste de cartes pour chaque mode de visualisation des cartes (all, good or evil) et les trie par nom
        self.all_cards = []
        for name, attr in self.cards.items():
            self.all_cards.append(
                Cards(name=name, cost=attr["cost"], effect=attr["effect"], description=attr["description"],
                      faction=attr["faction"], linked_to=attr["linked_to"], available=attr["available"],
                      possessed=attr["available"], limited_to=attr["limited_to"], zoom_text=attr["big_path"],
                      miniature_text=attr["small_path"], font_small=self.font_small, font_medium=self.font_medium,
                      font_large=self.font_large))
        self.current_cards = self.all_cards
        self.sort_by_name()
        # Initialise la carte sélectionnée et les variables propres à la liste de cartes
        self.current_card = self.current_cards[0]
        self.start_list_card = constants.DeckSelection.CARDS_PER_PAGE * (self.current_page - 1)
        self.end_list_card = constants.DeckSelection.CARDS_PER_PAGE * self.current_page
        # Initialisation des boutons image
        self.list_buttons_image = list()
        pos_top = constants.Window.SCREEN_HEIGHT - constants.DeckSelection.TOP_BUTTONS_ARROWS
        self.list_buttons_image.append(ButtonImage(image_base=constants.ImagesPath.BUTTON_ARROW_LEFT_BASE,
                                                   image_hovered=constants.ImagesPath.BUTTON_ARROW_LEFT_HOVERED,
                                                   image_disabled=constants.ImagesPath.BUTTON_ARROW_LEFT_DISABLED,
                                                   on_clic=self.list_left, pos_centery=pos_top, position=1,
                                                   pos_left=constants.DeckSelection.BUTTON_ARROW_LEFT_MARGIN))
        self.list_buttons_image.append(ButtonImage(image_base=constants.ImagesPath.BUTTON_ARROW_RIGHT_BASE,
                                                   image_hovered=constants.ImagesPath.BUTTON_ARROW_RIGHT_HOVERED,
                                                   image_disabled=constants.ImagesPath.BUTTON_ARROW_RIGHT_DISABLED,
                                                   on_clic=self.list_right, pos_centery=pos_top, position=2,
                                                   pos_left=constants.DeckSelection.BUTTON_ARROW_RIGHT_MARGIN))
        # Initialisation des boutons texte dédiés aux listes de cartes
        self.list_buttons_text_lists_cards = list()
        self.list_buttons_text_lists_cards.append(ButtonText(font=self.font_large, text=constants.Texts.CARDS_ALL,
                                                             on_clic=self.list_all_cards, active=False,
                                                             pos_left=constants.DeckSelection.START_MINIATURE_X,
                                                             pos_top=constants.DeckSelection.START_BUTTON_LISTS_Y))
        self.list_buttons_text_lists_cards.append(ButtonText(font=self.font_large, text=constants.Texts.CARDS_GOOD,
                                                             on_clic=self.list_good_cards,
                                                             pos_left=constants.DeckSelection.START_MINIATURE_X +
                                                             constants.DeckSelection.BUTTON_LISTS_PADDING,
                                                             pos_top=constants.DeckSelection.START_BUTTON_LISTS_Y))
        self.list_buttons_text_lists_cards.append(ButtonText(font=self.font_large, text=constants.Texts.CARDS_EVIL,
                                                             on_clic=self.list_evil_cards,
                                                             pos_left=constants.DeckSelection.START_MINIATURE_X +
                                                             constants.DeckSelection.BUTTON_LISTS_PADDING * 2.5,
                                                             pos_top=constants.DeckSelection.START_BUTTON_LISTS_Y))
        # Initialisation des boutons texte liés aux tris
        self.list_buttons_text_sort = list()
        self.list_buttons_text_sort.append(ButtonText(font=self.font_medium, text=constants.Texts.SORT_NAME,
                                                      on_clic=self.sort_by_name, active=False,
                                                      pos_centerx=constants.DeckSelection.BUTTON_SORT_MARGIN,
                                                      pos_centery=pos_top -
                                                      constants.DeckSelection.BUTTON_SORT_PADDING))
        self.list_buttons_text_sort.append(ButtonText(font=self.font_medium, text=constants.Texts.SORT_COST,
                                                      on_clic=self.sort_by_cost,
                                                      pos_centerx=constants.DeckSelection.BUTTON_SORT_MARGIN,
                                                      pos_centery=pos_top))
        self.list_buttons_text_sort.append(ButtonText(font=self.font_medium, text=constants.Texts.SORT_AVAIL,
                                                      on_clic=self.sort_by_available,
                                                      pos_centerx=constants.DeckSelection.BUTTON_SORT_MARGIN,
                                                      pos_centery=pos_top +
                                                      constants.DeckSelection.BUTTON_SORT_PADDING))
        # Initialise la liste des boutons texte divers
        centerx_back = self.screen.get_rect().centerx
        bottom_back = self.screen.get_rect().height
        bottom_ts = self.screen.get_rect().height - constants.TeamSelection.BOT_BUTTONS_TEXT
        left_ts = constants.TeamSelection.DETAIL_INSPECTED_X
        left_load_save = constants.TeamSelection.BUTTONS_LOADSAVE_MARGIN
        bottom_load_save = self.screen.get_rect().height - constants.TeamSelection.BOT_BUTTONS_TEXT
        self.list_buttons = list()
        self.list_buttons.append(ButtonText(font=self.font_back, text=constants.Texts.BACK, pos_bottom=bottom_back,
                                            pos_centerx=centerx_back))
        self.list_buttons.append(ButtonText(font=self.font_large, pos_bottom=bottom_ts, text=constants.Texts.ADD,
                                            on_clic=self.add_card_in_deck, pos_left=left_ts))
        self.list_buttons.append(ButtonText(font=self.font_large, pos_bottom=bottom_ts, text=constants.Texts.REMOVE,
                                            on_clic=self.del_card_in_deck, active=False,
                                            pos_right=self.screen.get_rect().width -
                                            constants.TeamSelection.BUTTON_REMOVE_MARGIN))
        self.list_buttons.append(ButtonText(font=self.font_large, pos_bottom=bottom_ts, text=constants.Texts.START,
                                            active=False, pos_right=constants.DeckSelection.BUTTON_START_MARGIN))
        self.list_buttons.append(ButtonText(font=self.font_large, text=constants.Texts.SAVE_DECK,
                                            pos_left=left_load_save, on_clic=self.start_overlay_save,
                                            pos_bottom=bottom_load_save))
        self.list_buttons.append(ButtonText(font=self.font_large, text=constants.Texts.LOAD_DECK,
                                            pos_left=left_load_save, on_clic=self.start_overlay_load,
                                            pos_bottom=bottom_load_save + self.font_large.get_height()))
        # Affiche le nom du joueur courant
        if self.fplayer_deck is None:
            self.render_text_name = self.font_large.render(self.fplayer_name, 1, constants.Colors.WHITE)
        else:
            self.render_text_name = self.font_large.render(self.splayer_name, 1, constants.Colors.WHITE)
        self.render_text_name_rect = self.render_text_name.get_rect()
        self.render_text_name_rect.centerx = centerx_back
        self.render_text_name_rect.bottom = bottom_back - constants.DeckSelection.NAME_MARGIN
        # Initialisation du bouton zoom
        self.button_image_zoom = ButtonImage(image_base=constants.ImagesPath.ZOOM, position=3,
                                             image_hovered=constants.ImagesPath.ZOOM_HOVERED,
                                             image_disabled=constants.ImagesPath.ZOOM_DISABLED,
                                             pos_centerx=self.current_card.miniature_rect.centerx,
                                             pos_top=self.current_card.miniature_rect.centery)
        # Déclaration de la textbox de recherche
        self.text_box = TextBox((self.screen.get_rect().centerx - constants.DeckSelection.POS_SEARCH_FIELD_X,
                                 pos_top + constants.DeckSelection.POS_SEARCH_FIELD_Y,
                                 constants.Textbox.TEXTBOX_WIDTH, constants.Textbox.TEXTBOX_HEIGHT),
                                clear_on_enter=True, inactive_on_enter=False, active=False, font=self.font_medium)
        self.text_box_final_old = self.text_box.final
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            # Events de la textbox de recherche
            self.text_box.get_event(event)
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic gauche
                if event.button == 1:
                    # Zoom de la carte
                    if self.button_image_zoom.rect.collidepoint(mouse_pos):
                        screen_capture = self.screen.copy()
                        overlay_zoom_card.OverlayZoomCard(self.screen, screen_capture, self.clock, self.current_card)
                    else:
                        # Sélectionne la carte
                        for card in self.current_cards[self.start_list_card:self.end_list_card]:
                            if card.miniature_rect.collidepoint(mouse_pos):
                                if card == self.current_card and self.current_card.available > 0:
                                    if self.current_card.possessed - self.current_card.available < \
                                            self.current_card.limited_to:
                                        if sum(card.possessed - card.available for card in self.cards_in_deck) < \
                                                constants.DeckSelection.TOTAL_CARDS:
                                            self.add_card_in_deck()
                                self.current_card = card
                    # Clic sur les boutons images
                    for button in self.list_buttons_image:
                        if button.rect.collidepoint(mouse_pos):
                            # Si le bouton est actif, lance la fonction liée
                            if button.active:
                                button.on_clic()
                    # Clic sur les boutons texte liés aux listes de cartes
                    for button in self.list_buttons_text_lists_cards:
                        if button.rect.collidepoint(mouse_pos):
                            if button.active:
                                button.on_clic()
                    # Clic sur les boutons texte liés aux tris
                    for button in self.list_buttons_text_sort:
                        if button.rect.collidepoint(mouse_pos):
                            if button.active:
                                button.on_clic()
                    # Clic sur les boutons texte divers
                    for button in self.list_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if button.active:
                                if button.text == constants.Texts.REMOVE:
                                    button.on_clic(self.current_card)
                                elif button.text == constants.Texts.START:
                                    if self.fplayer_deck is None:
                                        self.fplayer_deck = self.cards_in_deck
                                        self.__init__((self.screen, self.clock, self.total_points, self.fplayer_name,
                                                       self.splayer_name, self.fplayer_team, self.splayer_team,
                                                       self.fplayer_deck, self.splayer_deck, list()))
                                    else:
                                        self.splayer_deck = self.cards_in_deck
                                        heroes_deployment.HeroesDeployment(self.screen, self.clock, self.fplayer_name,
                                                                           self.splayer_name, self.fplayer_team,
                                                                           self.splayer_team, self.fplayer_deck,
                                                                           self.splayer_deck, False)
                                elif button.text == constants.Texts.BACK:
                                    if self.fplayer_deck is not None:
                                        self.__init__((self.screen, self.clock, self.total_points, self.fplayer_name,
                                                       self.splayer_name, self.fplayer_team, self.splayer_team,
                                                       None, self.splayer_deck, self.fplayer_deck))
                                    else:
                                        team_selection.TeamSelection((self.screen, self.clock, self.total_points,
                                                                      self.fplayer_name, self.splayer_name,
                                                                      self.fplayer_team, None, self.splayer_team))
                                else:
                                    if button.parameters is not None:
                                        button.on_clic(button.parameters)
                                    else:
                                        button.on_clic()
                    # Supprime une carte de la liste des cartes sélectionnées
                    for i in range(len(self.cards_in_deck)):
                        temp_rect = self.cards_in_deck[i].surface_list_rect.inflate(-2, -2)
                        if temp_rect.collidepoint(mouse_pos):
                            self.del_card_in_deck(self.cards_in_deck[i])
                            break
                # Clic droit
                if event.button == 3:
                    # Supprime le héros si il est dans la liste des héros sélectionnés
                    for card in self.current_cards:
                        if card.miniature_rect.collidepoint(mouse_pos):
                            if card == self.current_card and card.search_card_in_list(self.cards_in_deck):
                                self.del_card_in_deck(self.current_card)
                # Scroll up
                elif event.button == 4:
                    if self.current_page * constants.DeckSelection.CARDS_PER_PAGE < len(self.current_cards):
                        self.list_right()
                # Scroll down
                elif event.button == 5:
                    if self.current_page > 1:
                        self.list_left()
            if event.type == pygame.KEYDOWN:
                # Fléche de droite
                if event.key == pygame.K_RIGHT:
                    if (self.current_cards.index(self.current_card) + 1) % 5 != 0:
                        self.current_card = self.current_cards[self.current_cards.index(self.current_card) + 1]
                    elif self.current_page * constants.DeckSelection.CARDS_PER_PAGE < len(self.current_cards):
                        self.list_right()
                        if self.current_cards.index(self.current_card) + 11 < len(self.current_cards):
                            self.current_card = self.current_cards[self.current_cards.index(self.current_card) + 11]
                        else:
                            self.current_card = self.current_cards[self.start_list_card]
                # Flèche de gauche
                if event.key == pygame.K_LEFT:
                    if self.current_cards.index(self.current_card) % 5 != 0:
                        self.current_card = self.current_cards[self.current_cards.index(self.current_card) - 1]
                    elif self.current_page > 1:
                        self.list_left()
                        self.current_card = self.current_cards[self.current_cards.index(self.current_card) - 11]
                # Flèche du haut
                if event.key == pygame.K_UP:
                    if self.current_cards.index(self.current_card) - 5 > self.start_list_card:
                        self.current_card = self.current_cards[self.current_cards.index(self.current_card) - 5]
                # Flèche du bas
                if event.key == pygame.K_DOWN:
                    if self.current_cards.index(self.current_card) + 5 < self.end_list_card:
                        self.current_card = self.current_cards[self.current_cards.index(self.current_card) + 5]
                # Page suivante
                if event.key == pygame.K_PAGEUP:
                    if self.current_page * constants.DeckSelection.CARDS_PER_PAGE < len(self.current_cards):
                        self.list_right()
                # Page précédente
                if event.key == pygame.K_PAGEDOWN:
                    if self.current_page > 1:
                        self.list_left()
                # Touche entrée
                if event.key == pygame.K_RETURN:
                    if self.current_card.available > 0 and self.current_card.possessed - self.current_card.available < \
                            self.current_card.limited_to and sum(card.possessed - card.available
                                                                 for card in self.cards_in_deck) < \
                            constants.DeckSelection.TOTAL_CARDS:
                        self.add_card_in_deck()
                    elif self.current_card.search_card_in_list(self.cards_in_deck):
                        self.del_card_in_deck(self.current_card)
                # Touche supprimer
                if event.key == pygame.K_DELETE:
                    if self.current_card.search_card_in_list(self.cards_in_deck):
                        self.del_card_in_deck(self.current_card)
        # Met à jour la position de l'image du zoom en fonction de la carte sélectionnée
        self.button_image_zoom.rect.centerx = self.current_card.miniature_rect.centerx
        self.button_image_zoom.rect.centery = self.current_card.miniature_rect.centery

    def draw(self, mouse_pos):
        # Affiche le fond d'écran et la zone des détails
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.frame, self.frame_rect)
        # Affiche le nom du joueur
        self.screen.blit(self.render_text_name, self.render_text_name_rect)
        # Affiche les boutons image
        for button in self.list_buttons_image:
            button.draw(self.screen, mouse_pos)
        # Affiche les boutons texte dédiés aux listes de cartes
        for button in self.list_buttons_text_lists_cards:
            button.draw(self.screen, mouse_pos)
        # Affiche les boutons texte liés aux tris
        for button in self.list_buttons_text_sort:
            button.draw(self.screen, mouse_pos)
        # Affiche les boutons texte divers
        for button in self.list_buttons:
            button.draw(self.screen, mouse_pos)
        miniature_x, miniature_y = constants.DeckSelection.START_MINIATURE_X, constants.DeckSelection.START_MINIATURE_Y
        for ind in range(self.start_list_card, self.end_list_card):
            # Affiche les miniatures
            self.current_cards[ind].miniature_rect.left = miniature_x
            self.current_cards[ind].miniature_rect.top = miniature_y
            self.screen.blit(self.current_cards[ind].miniature, self.current_cards[ind].miniature_rect)
            miniature_x += constants.DeckSelection.MARGIN_X
            if miniature_x >= constants.TeamSelection.LIMIT_RIGHT:
                miniature_x = constants.DeckSelection.START_MINIATURE_X
                miniature_y += constants.DeckSelection.MARGIN_Y
            # Affiche le nom des cartes et le nombre de cartes disponibles
            self.current_cards[ind].name_text_rect.centerx = self.current_cards[ind].miniature_rect.centerx
            self.current_cards[ind].name_text_rect.top = \
                self.current_cards[ind].miniature_rect.top + constants.DeckSelection.DIFF_MINIATURE_TEXT
            self.screen.blit(self.current_cards[ind].name_text, self.current_cards[ind].name_text_rect)
            self.current_cards[ind].available_text_rect.centerx = self.current_cards[ind].miniature_rect.centerx
            self.current_cards[ind].available_text_rect.top = \
                self.current_cards[ind].miniature_rect.top + constants.DeckSelection.DIFF_AVAILABLE_TEXT
            self.screen.blit(self.current_cards[ind].available_text, self.current_cards[ind].available_text_rect)
            # Affiche un carré blanc autour de la miniature survolée
            if self.current_cards[ind].miniature_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, constants.Colors.WHITE, (self.current_cards[ind].miniature_rect.x -
                                                                       constants.DeckSelection.SQUARE_HOVERED_DIFF,
                                                                       self.current_cards[ind].miniature_rect.y -
                                                                       constants.DeckSelection.SQUARE_HOVERED_DIFF,
                                                                       self.current_cards[ind].miniature_rect.width +
                                                                       constants.DeckSelection.SQUARE_HOVERED_DIFF * 2,
                                                                       self.current_cards[ind].miniature_rect.height +
                                                                       constants.DeckSelection.SQUARE_HOVERED_DIFF * 2),
                                 2)
        # Affiche un carré or autour de la carte sélectionnée
        if self.end_list_card >= self.current_cards.index(self.current_card) >= self.start_list_card:
            pygame.draw.rect(self.screen, constants.Colors.GOLD, (self.current_card.miniature_rect.x -
                                                                  constants.DeckSelection.SQUARE_HOVERED_DIFF,
                                                                  self.current_card.miniature_rect.y -
                                                                  constants.DeckSelection.SQUARE_HOVERED_DIFF,
                                                                  self.current_card.miniature_rect.width +
                                                                  constants.DeckSelection.SQUARE_HOVERED_DIFF * 2,
                                                                  self.current_card.miniature_rect.height +
                                                                  constants.DeckSelection.SQUARE_HOVERED_DIFF * 2), 2)
        # Affiche le nombre de cartes dans le deck
        number_cards_text = self.font_large.render("{} / {}".format(sum(card.possessed - card.available
                                                                        for card in self.cards_in_deck),
                                                                    constants.DeckSelection.TOTAL_CARDS), 1,
                                                   constants.Colors.WHITE)
        number_cards_text_rect = number_cards_text.get_rect()
        number_cards_text_rect.centerx = [button.rect.centerx for button in self.list_buttons if button.text ==
                                          constants.Texts.START][0]
        number_cards_text_rect.y = self.screen.get_rect().height - constants.DeckSelection.BOT_BUTTONS_TEXT
        self.screen.blit(number_cards_text, number_cards_text_rect)
        # Affiche le texte "SEARCH : " au dessus du champs de recherche
        search_text = self.font_medium.render(constants.Texts.SEARCH, 1, constants.Colors.WHITE)
        search_text_rect = search_text.get_rect()
        search_text_rect.left = self.text_box.rect.left
        search_text_rect.bottom = self.text_box.rect.top - constants.DeckSelection.SEARCH_TEXT_PADDING
        self.screen.blit(search_text, search_text_rect)
        # Affiche le texte "SORT BY :" au dessus des différents tris
        render_text_sort = self.font_medium.render(constants.Texts.SORT_BY, 1, constants.Colors.WHITE)
        render_text_sort_rect = render_text_sort.get_rect()
        render_text_sort_rect.centerx = constants.DeckSelection.BUTTON_SORT_MARGIN
        render_text_sort_rect.centery = \
            constants.Window.SCREEN_HEIGHT - constants.DeckSelection.TOP_BUTTONS_ARROWS - \
            constants.DeckSelection.BUTTON_SORT_PADDING * 2
        self.screen.blit(render_text_sort, render_text_sort_rect)
        # Affiche le bouton du zoom sur la carte sélectionnée
        if self.end_list_card >= self.current_cards.index(self.current_card) >= self.start_list_card:
            if self.button_image_zoom.rect.collidepoint(mouse_pos):
                self.screen.blit(self.button_image_zoom.image_hovered, self.button_image_zoom.rect)
            else:
                self.screen.blit(self.button_image_zoom.image_base, self.button_image_zoom.rect)
        # Affichage de la textbox de recherche
        self.text_box.draw(self.screen)
        self.text_box.update()
        # Affiche les informations de la carte inspectée
        # Affiche le nom
        self.current_card.name_text_inspected_rect.centerx = self.frame_rect.centerx
        self.current_card.name_text_inspected_rect.top = \
            self.frame_rect.centery - constants.DeckSelection.NAME_MARGIN_DETAILS
        self.screen.blit(self.current_card.name_text_inspected, self.current_card.name_text_inspected_rect)
        # Affiche les caractéristiques
        pos_details_y = self.frame_rect.centery + constants.DeckSelection.DETAILS_MARGIN_TOP
        for detail in self.current_card.get_list_inspected(self.font_medium):
            detail_rect = detail.get_rect()
            detail_rect.left = constants.TeamSelection.DETAIL_INSPECTED_X
            detail_rect.top = pos_details_y
            pos_details_y += detail_rect.height
            self.screen.blit(detail, detail_rect)
        # Affiche la description
        effect_text = self.font_medium.render(constants.Texts.EFFECTS, 1, constants.Colors.WHITE)
        pos_details_y += effect_text.get_rect().height
        self.screen.blit(effect_text, (constants.TeamSelection.DETAIL_INSPECTED_X, pos_details_y))
        pos_details_y += effect_text.get_rect().height
        for text in self.current_card.get_effect_inspected(self.font_small):
            text_rect = text.get_rect()
            text_rect.left = constants.TeamSelection.DETAIL_INSPECTED_X
            text_rect.top = pos_details_y
            pos_details_y += text_rect.height
            self.screen.blit(text, text_rect)
        # Affiche les cartes liées
        linked_text = self.font_medium.render(constants.Texts.LINKED_TO, 1, constants.Colors.WHITE)
        pos_details_y += linked_text.get_rect().height
        self.screen.blit(linked_text, (constants.TeamSelection.DETAIL_INSPECTED_X, pos_details_y))
        pos_details_y += effect_text.get_rect().height
        for text in self.current_card.get_linked_inspected(self.font_small, self.list_in_team):
            text_rect = text.get_rect()
            text_rect.left = constants.TeamSelection.DETAIL_INSPECTED_X
            text_rect.top = pos_details_y
            pos_details_y += text_rect.height
            self.screen.blit(text, text_rect)
        # Affiche la liste des cartes sélectionnées
        for i in range(len(self.cards_in_deck)):
            left = constants.TeamSelection.DETAILS_ZONE + constants.DeckSelection.LIST_IN_DETAIL_ZONE_X
            top = (constants.Card.SURFACE_LIST_HEIGHT - 2) * i + constants.DeckSelection.LIST_IN_DETAIL_ZONE_Y
            self.cards_in_deck[i].surface_list_rect.left = left
            self.cards_in_deck[i].surface_list_rect.top = top
            self.screen.blit(self.cards_in_deck[i].surface_list, self.cards_in_deck[i].surface_list_rect)
            # Affiche la carte zoomée au survol d'une carte dans la liste
            temp_rect = self.cards_in_deck[i].surface_list_rect.inflate(-2, -2)
            if temp_rect.collidepoint(mouse_pos):
                self.cards_in_deck[i].zoom_rect.right = left
                self.cards_in_deck[i].zoom_rect.top = top
                self.screen.blit(self.cards_in_deck[i].zoom, self.cards_in_deck[i].zoom_rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def sort_by_name(self):
        """
        Trie les cartes par leur nom
        """
        self.mode_sort = 0
        self.current_cards.sort(key=lambda card: (card.name, card.cost))

    def sort_by_cost(self):
        """
        Trie les cartes par leur coût
        """
        self.mode_sort = 1
        self.current_cards.sort(key=lambda card: (card.cost, card.name))

    def sort_by_available(self):
        """
        Trie les cartes par le nombre de cartes possédées
        """
        self.mode_sort = 2
        self.current_cards.sort(key=lambda card: (card.available, card.name))

    def list_all_cards(self):
        """
        Renvoie une liste contenant toutes les cartes
        """
        self.current_cards = self.all_cards
        self.mode_list = 0
        self.sorting_and_initializing_list()

    def list_evil_cards(self):
        """
        Renvoie une liste contenant les cartes Evil
        """
        self.current_cards = [card for card in self.all_cards if card.faction == "Evil"]
        self.mode_list = 1
        self.sorting_and_initializing_list()

    def list_good_cards(self):
        """
        Renvoie une liste contenant les cartes Good
        """
        self.current_cards = [card for card in self.all_cards if card.faction == "Good"]
        self.mode_list = 2
        self.sorting_and_initializing_list()

    def list_left(self):
        """
        Change la page de la liste de carte vers la gauche
        """
        self.current_page -= 1
        self.update_start_end_list()

    def list_right(self):
        """
        Change la page de la liste de carte vers la droite
        """
        self.current_page += 1
        self.update_start_end_list()

    def add_card_in_deck(self):
        """
        Ajoute une carte dans le deck
        """
        if not self.current_card.search_card_in_list(self.cards_in_deck):
            self.cards_in_deck.append(self.current_card)
            self.cards_in_deck.sort(key=lambda card: (card.name, card.cost))
        self.current_card.available -= 1
        self.current_card.update_text_available()
        self.current_card.update_list_in_deck_render()

    def del_card_in_deck(self, card_clicked):
        """
        Supprime une carte du deck
        """
        card = card_clicked.return_card_from_list(self.cards_in_deck)
        card.available += 1
        if card.possessed - card.available == 0:
            self.cards_in_deck.remove(card)
        card.update_text_available()
        card.update_list_in_deck_render()

    def change_state_image_buttons(self):
        """
        Modifie létat des boutons images en fonction de la position du scroll
        """
        for button in self.list_buttons_image:
            if button.position == 1 and self.current_page > 1:
                button.active = True
            elif button.position == 1:
                button.active = False
            if button.position == 2 and (self.current_page * constants.DeckSelection.CARDS_PER_PAGE) \
                    < len(self.current_cards):
                button.active = True
            elif button.position == 2:
                button.active = False

    def change_state_text_buttons_lists(self):
        """
        Modifie l'état des boutons texte dédiés au changement de liste en fonction de l'état des autres
        """
        for button in self.list_buttons_text_lists_cards:
            if self.mode_list == 0:
                if button.text == constants.Texts.CARDS_ALL:
                    button.active = False
                else:
                    button.active = True
            elif self.mode_list == 1:
                if button.text == constants.Texts.CARDS_EVIL:
                    button.active = False
                else:
                    button.active = True
            else:
                if button.text == constants.Texts.CARDS_GOOD:
                    button.active = False
                else:
                    button.active = True

    def change_state_text_buttons_sort(self):
        """
        Modifie l'état des boutons texte liés aux tris en fonction de l'état des autres
        """
        for button in self.list_buttons_text_sort:
            if self.mode_sort == 0:
                if button.text == constants.Texts.SORT_NAME:
                    button.active = False
                else:
                    button.active = True
            elif self.mode_sort == 1:
                if button.text == constants.Texts.SORT_COST:
                    button.active = False
                else:
                    button.active = True
            else:
                if button.text == constants.Texts.SORT_AVAIL:
                    button.active = False
                else:
                    button.active = True

    def change_state_text_buttons(self):
        """
        Modifie l'état des boutons texte divers
        """
        for button in self.list_buttons:
            if button.text == constants.Texts.ADD:
                if self.current_card.available == 0 or self.current_card.possessed - self.current_card.available >= \
                        self.current_card.limited_to or sum(card.possessed - card.available
                                                            for card in self.cards_in_deck) == \
                        constants.DeckSelection.TOTAL_CARDS:
                    button.active = False
                else:
                    button.active = True
            elif button.text == constants.Texts.REMOVE:
                if self.current_card.search_card_in_list(self.cards_in_deck):
                    button.active = True
                else:
                    button.active = False
            elif button.text == constants.Texts.START:
                if sum(card.possessed - card.available for card in self.cards_in_deck) == \
                        constants.DeckSelection.TOTAL_CARDS:
                    button.active = True
                else:
                    button.active = False

    def use_search_field(self):
        """
        Modifie la liste des cartes affichées en fonction du champs de recherche
        """
        self.text_box_final_old = self.text_box.final
        if self.mode_list == 0:
            self.list_all_cards()
        elif self.mode_list == 1:
            self.list_evil_cards()
        else:
            self.list_good_cards()
        temp_cards = [card for card in self.current_cards if self.text_box.final.lower() in card.name.lower()]
        if len(temp_cards) > 0:
            self.current_cards = temp_cards
        self.sorting_and_initializing_list()

    def update_start_end_list(self):
        """
        Met à jour le point de départ et de de fin de la liste à afficher
        """
        self.start_list_card = constants.DeckSelection.CARDS_PER_PAGE * (self.current_page - 1)
        if (len(self.current_cards) - (self.current_page - 1) * constants.DeckSelection.CARDS_PER_PAGE) < \
                constants.DeckSelection.CARDS_PER_PAGE:
            self.end_list_card = len(self.current_cards)

        else:
            self.end_list_card = constants.DeckSelection.CARDS_PER_PAGE * self.current_page

    def sorting_and_initializing_list(self):
        """
        Trie la liste nouvellement créée en respectant le tri choisi, initialise la carte sélectionnée et
        remet les paramètres de la page à leur valeurs initiales
        """
        if self.mode_sort == 0:
            self.sort_by_name()
        elif self.mode_sort == 1:
            self.sort_by_cost()
        else:
            self.sort_by_available()
        self.current_card = self.current_cards[0]
        self.current_page = 1
        self.update_start_end_list()

    def start_overlay_save(self):
        """
        Démarre la page de l'overlay de sauvegarde d'un deck
        """
        capture = self.screen.copy()
        to_save = {}
        for card in self.cards_in_deck:
            to_save[card.name] = card.possessed - card.available
        overlay_save.OverlaySave(self.screen, capture, self.clock, to_save, constants.Files.DECKS_SAVE)

    def start_overlay_load(self):
        """
        Démarre la page de l'overlay de chargement d'un deck
        """
        capture = self.screen.copy()
        class_button = \
            overlay_load.OverlayLoad(self.screen, capture, self.clock, self.cards_in_deck, constants.Files.DECKS_SAVE)
        to_load = class_button.run()
        if to_load is not None:
            self.cards_in_deck = []
            for key, value in to_load.items():
                for card in self.all_cards:
                    if card.name == key:
                        card.available -= value
                        self.cards_in_deck.append(card)
            for card in self.cards_in_deck:
                card.update_images()
                card.update_text_available()
                card.update_list_in_deck_render()

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            self.change_state_image_buttons()
            self.change_state_text_buttons_lists()
            self.change_state_text_buttons_sort()
            self.change_state_text_buttons()
            if self.text_box_final_old != self.text_box.final:
                self.use_search_field()
            self.draw(mouse_pos)
