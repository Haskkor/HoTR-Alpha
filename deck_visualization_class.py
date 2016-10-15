import constants
import pygame
import random

from button_text_class import ButtonText

__author__ = "Jérémy Farnault"


class DeckVisualization:
    """
    OBJETS VISUALISATION DU DECK
    """

    def __init__(self, deck, deployment):
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_medium.set_bold(True)
        self.surface = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.left = 0
        self.surface_rect.top = 0
        self.hand_size = None
        self.surface_deck = None
        self.surface_deck_rect = None
        self.button_back = None
        self.deck = deck
        self.hand = []
        self.deployment = deployment
        # Construit la main de départ si l'objet n'est pas créé pendant l'écran de déploiement
        if not self.deployment:
            self.list_buttons_right = []
            for i in range(3):
                self.draw_new_card()
        else:
            self.hand = self.deck

    def calculate_hand_size(self):
        """
        Calcule la taille de la main
        """
        self.hand_size = (self.hand[0].miniature_rect.width // 2) * (len(self.hand) + 1)
        self.surface_deck = pygame.Surface((self.hand_size + constants.DeckVisualization.SURFACE_DECK_MARGIN,
                                            self.hand[0].miniature_rect.height +
                                            constants.DeckVisualization.SURFACE_DECK_MARGIN), pygame.SRCALPHA)
        self.surface_deck_rect = self.surface_deck.get_rect()
        self.surface_deck_rect.centerx = self.surface_rect.centerx
        self.surface_deck_rect.bottom = \
            constants.Window.SCREEN_HEIGHT - constants.DeckVisualization.SURFACE_DECK_MARGIN // 2
        # Crée le bouton retour
        self.button_back = \
            ButtonText(font=self.font_medium, text=constants.Texts.BACK,
                       pos_right=self.surface_deck_rect.left - constants.DeckVisualization.BUTTON_BACK_MARGIN,
                       pos_centery=self.surface_deck_rect.centery)
        if not self.deployment:
            self.list_buttons_right = []
            # Crée le bouton pour tirer une carte
            self.list_buttons_right.append(ButtonText(font=self.font_medium, text=constants.Texts.DRAW,
                                                      pos_left=self.surface_deck_rect.right +
                                                      constants.DeckVisualization.BUTTON_BACK_MARGIN,
                                                      pos_centery=self.surface_deck_rect.centery -
                                                      constants.DeckVisualization.BUTTONS_PADDING))
            self.list_buttons_right.append(ButtonText(font=self.font_medium, text=constants.Texts.SORT_BY_NAME,
                                                      pos_left=self.surface_deck_rect.right +
                                                      constants.DeckVisualization.BUTTON_BACK_MARGIN,
                                                      pos_centery=self.surface_deck_rect.centery))
            self.list_buttons_right.append(ButtonText(font=self.font_medium, text=constants.Texts.SORT_BY_COST,
                                                      pos_left=self.surface_deck_rect.right +
                                                      constants.DeckVisualization.BUTTON_BACK_MARGIN,
                                                      pos_centery=self.surface_deck_rect.centery +
                                                      constants.DeckVisualization.BUTTONS_PADDING))

    def draw_new_card(self):
        """
        Permet de tirer une nouvelle carte
        """
        card = random.choice(self.deck)
        self.hand.append(card)
        self.deck.remove(card)
        self.calculate_hand_size()

    def sort_by_cost(self):
        """
        Trie les cartes par coût
        """
        self.hand.sort(key=lambda card: (card.cost, card.name))

    def sort_by_name(self):
        """
        Trie les cartes par nom
        """
        self.hand.sort(key=lambda card: (card.name, card.cost))

    def change_state_buttons(self):
        """
        Change l'état du bouton pour tirer une carte
        """
        for button in self.list_buttons_right:
            if len(self.deck) < 1 and button.text == constants.Texts.DRAW:
                button.active = False

    def get_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_back.rect.collidepoint(mouse_pos):
                return False
            else:
                for card in reversed(self.hand):
                    fake_rect = pygame.Rect(card.miniature_rect)
                    fake_rect.x = card.miniature_rect.left + self.surface_deck_rect.left
                    fake_rect.y = card.miniature_rect.top + self.surface_deck_rect.top
                    if fake_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        return card
            if not self.deployment:
                for button in self.list_buttons_right:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == constants.Texts.DRAW and button.active:
                            self.draw_new_card()
                            self.change_state_buttons()
                        elif button.text == constants.Texts.SORT_BY_COST:
                            self.sort_by_cost()
                        elif button.text == constants.Texts.SORT_BY_NAME:
                            self.sort_by_name()

    def draw(self, screen, mouse_pos):
        self.surface.fill(constants.Colors.BLACK_FULL_ALPHA)
        self.surface_deck.fill(constants.Colors.BLACK_FULL_ALPHA)
        # Affiche les cartes
        for i in range(len(self.hand)):
            self.hand[i].miniature_rect.left = (self.hand[0].miniature_rect.width // 2) * i + \
                                               constants.DeckVisualization.SURFACE_DECK_MARGIN // 2
            self.hand[i].miniature_rect.top = constants.DeckVisualization.SURFACE_DECK_MARGIN // 2
            self.surface_deck.blit(self.hand[i].miniature, self.hand[i].miniature_rect)
        # Affiche le bouton retour
        if self.button_back.rect.collidepoint(mouse_pos):
            self.surface.blit(self.button_back.render_hover, self.button_back.rect)
        else:
            self.surface.blit(self.button_back.render_base, self.button_back.rect)
        # Affiche le bouton pour tirer une carte
        if not self.deployment:
            for button in self.list_buttons_right:
                if button.rect.collidepoint(mouse_pos) and button.active:
                    screen.blit(button.render_hover, button.rect)
                elif button.active:
                    screen.blit(button.render_base, button.rect)
                else:
                    screen.blit(button.render_inactive, button.rect)
        # Réaffiche la carte survolée par dessus les autres, affiche un carré jaune autour et affiche son zoom
        # au milieu de l'écran
        for card in reversed(self.hand):
            fake_rect = pygame.Rect(card.miniature_rect)
            fake_rect.x = card.miniature_rect.left + self.surface_deck_rect.left
            fake_rect.y = card.miniature_rect.top + self.surface_deck_rect.top
            if fake_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.surface_deck.blit(card.miniature, card.miniature_rect)
                pygame.draw.rect(self.surface_deck, constants.Colors.GOLD,
                                 (card.miniature_rect.left - constants.DeckVisualization.RECT_WIDTH,
                                  card.miniature_rect.top - constants.DeckVisualization.RECT_WIDTH,
                                  card.miniature_rect.width + constants.DeckVisualization.RECT_WIDTH,
                                  card.miniature_rect.height + constants.DeckVisualization.RECT_WIDTH),
                                 constants.DeckVisualization.RECT_WIDTH)
                card.zoom_rect.centerx = self.surface_rect.centerx
                card.zoom_rect.centery = self.surface_rect.centery
                self.surface.blit(card.zoom, card.zoom_rect)
                break
        self.surface.blit(self.surface_deck, self.surface_deck_rect)
        screen.blit(self.surface, self.surface_rect)
