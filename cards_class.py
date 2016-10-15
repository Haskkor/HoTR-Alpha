import constants
import pygame

__author__ = "Jérémy Farnault"


class Cards:
    """
    OBJETS CARTES
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.font_small = None
        self.font_medium = None
        self.font_large = None
        self.name = None
        self.cost = None
        self.effect = None
        self.description = None
        self.faction = None
        self.linked_to = None
        self.possessed = None
        self.available = None
        self.limited_to = None
        self.miniature_text = None
        self.miniature = None
        self.miniature_rect = None
        self.zoom_text = None
        self.zoom = None
        self.zoom_rect = None
        self.name_text = None
        self.name_text_rect = None
        self.name_text_inspected = None
        self.name_text_inspected_rect = None
        self.available_text = None
        self.available_text_rect = None
        self.surface_list = None
        self.surface_list_rect = None
        self.process_kwargs(kwargs)
        self.process_fonts()
        self.update_text_available()
        self.update_images()

    def process_kwargs(self, kwargs):
        defaults = {}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def process_fonts(self):
        """
        Prépare les polices
        """
        self.name_text = self.font_small.render(self.name, 1, constants.Colors.WHITE)
        self.name_text_inspected = self.font_large.render(self.name, 1, constants.Colors.WHITE)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_inspected_rect = self.name_text_inspected.get_rect()

    def update_images(self):
        """
        Met à jour les images
        """
        self.miniature = pygame.image.load(self.miniature_text)
        self.miniature_rect = self.miniature.get_rect()
        self.zoom = pygame.image.load(self.zoom_text)
        self.zoom_rect = self.zoom.get_rect()

    def update_text_available(self):
        """
        Crée et met à jour le texte à afficher concernant le nombre de cartes à disposition
        """
        if self.limited_to < 10:
            self.available_text = self.font_small.render("x{} ({})".format(self.available, self.limited_to), 1,
                                                         constants.Colors.WHITE)
        else:
            self.available_text = self.font_small.render("x{}".format(self.available), 1, constants.Colors.WHITE)
        self.available_text_rect = self.available_text.get_rect()

    def get_list_inspected(self, font):
        """
        Renvoie le texte à afficher pour les attributs simples
        """
        for attr in ["Ressource Cost : {}".format(self.cost),
                     "Description : {}".format(self.description),
                     "Faction : {}".format(self.faction),
                     "Possessed : {}".format(self.possessed),
                     "Limited to : {}".format(self.limited_to)]:
            yield font.render(attr, 1, constants.Colors.WHITE)

    def get_effect_inspected(self, font):
        """
        Renvoie le texte à afficher pour les effets de la carte
        """
        effect = self.effect
        while len(effect) > constants.TeamSelection.SIZE_TEXT_MULTILINES:
            for i in range(constants.TeamSelection.SIZE_TEXT_MULTILINES, 0, -1):
                if effect[i] == " ":
                    yield font.render(effect[:i], 1, constants.Colors.WHITE)
                    effect = effect[i + 1:]
                    break
        yield font.render(effect, 1, constants.Colors.WHITE)

    def get_linked_inspected(self, font, list_in_team):
        """
        Renvoie le texte à afficher pour les cartes liées à la carte
        """
        heroes_name = [hero.name for hero in list_in_team]
        if len(self.linked_to) == 0:
            yield font.render("None", 1, constants.Colors.WHITE)
        else:
            for link in self.linked_to:
                if link in heroes_name:
                    yield font.render(link, 1, constants.Colors.WHITE)
                else:
                    yield font.render(link, 1, constants.Colors.RED)

    def search_card_in_list(self, list_cards):
        """
        Recherche la carte dans une liste et renvoie un booléen
        """
        truth_table = [self.name == elem.name for elem in list_cards]
        return any(truth_table)

    def count_card_in_list(self, list_cards):
        """
        Compte le nombre d'occurrences de la carte dans une liste
        """
        return len([elem for elem in list_cards if elem.name == self.name])

    def return_card_from_list(self, list_cards):
        """
        Renvoie la carte depuis une liste
        """
        return [elem for elem in list_cards if elem.name == self.name][0]

    def update_list_in_deck_render(self):
        """
        Crée et met à jour la surface à afficher pour la liste des cartes sélectionnées dans le deck
        """
        self.surface_list = pygame.Surface((constants.Card.SURFACE_LIST_WIDTH, constants.Card.SURFACE_LIST_HEIGHT),
                                           pygame.SRCALPHA, 32)
        self.surface_list = self.surface_list.convert_alpha()
        self.surface_list_rect = self.surface_list.get_rect()
        # Affiche une partie de la miniature de la carte dans la liste
        self.surface_list.blit(self.miniature, (constants.Card.SURFACE_LIST_WIDTH // 2 +
                                                constants.Card.MINIATURE_IN_LIST_MARGIN, 0),
                               (constants.Card.START_X_MINIATURE_PART, constants.Card.START_Y_MINIATURE_PART,
                                constants.Card.WIDTH_MINIATURE_PART, constants.Card.SURFACE_LIST_HEIGHT))
        # Rectangle autour de la carte de la liste
        pygame.draw.rect(self.surface_list, constants.Colors.DARK_SLATE_GRAY, (0, 0, constants.Card.SURFACE_LIST_WIDTH,
                                                                               constants.Card.SURFACE_LIST_HEIGHT), 4)
        # Coût de la carte
        cost_text = self.font_small.render(str(self.cost), 1, constants.Colors.ELECTRIC_BLUE)
        cost_text_rect = cost_text.get_rect()
        cost_text_rect.left = constants.Card.COST_SURFACE_LIST_MARGIN
        cost_text_rect.centery = constants.Card.SURFACE_LIST_HEIGHT // 2
        self.surface_list.blit(cost_text, cost_text_rect)
        # Nom de la carte
        name_text = self.font_medium.render(self.name, 1, constants.Colors.WHITE)
        name_text_rect = name_text.get_rect()
        name_text_rect.left = constants.Card.NAME_SURFACE_LIST_MARGIN
        name_text_rect.centery = constants.Card.SURFACE_LIST_HEIGHT // 2
        self.surface_list.blit(name_text, name_text_rect)
        # Nombre d'occurrence de la carte dans le deck
        in_deck_text = self.font_medium.render("x{}".format(self.possessed - self.available), 1,
                                               constants.Colors.SADDLE_BROW)
        in_deck_text_rect = in_deck_text.get_rect()
        in_deck_text_rect.right = constants.Card.SURFACE_LIST_WIDTH - constants.Card.IN_DECK_SURFACE_LIST_MARGIN
        in_deck_text_rect.centery = constants.Card.SURFACE_LIST_HEIGHT // 2
        self.surface_list.blit(in_deck_text, in_deck_text_rect)
