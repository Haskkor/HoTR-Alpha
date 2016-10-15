import constants
import pygame

__author__ = "Jérémy Farnault"


class Heroes:
    """
    OBJETS HEROS
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.player_name = None
        self.name = None
        self.speed = None
        self.initiative = None
        self.life_points = None
        self.life_points_current = None
        self.magic_points = None
        self.magic_points_current = None
        self.armor = None
        self.armor_current = None
        self.scope = None
        self.size = None
        self.agility = None
        self.stamina = None
        self.strength = None
        self.magic = None
        self.mental = None
        self.attack = None
        self.cost = None
        self.unique = None
        self.skills = None
        self.description = None
        self.is_inspected = False
        self.token_text = None
        self.token = None
        self.token_rect = None
        self.miniature_text = None
        self.miniature = None
        self.miniature_rect = None
        self.token_init_text = None
        self.token_init = None
        self.token_init_rect = None
        self.battlefield_text = None
        self.battlefield = None
        self.battlefield_rect = None
        self.font_small = None
        self.font_large = None
        self.name_text = None
        self.name_text_in_team = None
        self.name_text_inspected = None
        self.name_text_rect = None
        self.name_text_inspected_rect = None
        self.pos_bf_i = None
        self.pos_bf_j = None
        self.process_kwargs(kwargs)
        self.process_fonts()
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
        self.name_text_in_team = self.font_small.render(self.name, 1, constants.Colors.GOLD)
        self.name_text_inspected = self.font_large.render(self.name, 1, constants.Colors.WHITE)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_inspected_rect = self.name_text_inspected.get_rect()

    def update_images(self):
        """
        Met à jour les images
        """
        self.token = pygame.image.load(self.token_init_text)
        self.token_rect = self.token.get_rect()
        self.miniature = pygame.image.load(self.miniature_text)
        self.miniature_rect = self.miniature.get_rect()
        self.token_init = pygame.image.load(self.token_init_text)
        self.token_init_rect = self.token_init.get_rect()
        self.battlefield = pygame.image.load(self.battlefield_text)
        self.battlefield_rect = self.battlefield.get_rect()

    def get_list_inspected(self, font):
        """
        Renvoie les attributs simples du héros choisi pour l'affichage des détails du héros sélectionné
        """
        for attr in ["Points Cost : {}".format(self.cost),
                     "Unique : {}".format(self.unique),
                     "Size : {}".format(self.size),
                     "Life Points : {}".format(self.life_points),
                     "Magic Points : {}".format(self.magic_points),
                     "Armor : {}".format(self.armor),
                     "Initiative : {}".format(self.initiative),
                     "Speed : {}".format(self.speed),
                     "Attack Points : {}".format(self.attack),
                     "Range : {}".format(self.scope),
                     "Strength : {}".format(self.strength),
                     "Stamina : {}".format(self.stamina),
                     "Agility : {}".format(self.agility),
                     "Magic : {}".format(self.magic),
                     "Mental : {}".format(self.mental)]:
            yield font.render(attr, 1, constants.Colors.WHITE)

    def get_basic_inspected_battle(self, font):
        """
        Renvoie les attributs basiques du héros choisi pour l'affichage sur l'écran du déploiement ou de la bataille
        """
        for attr in ["Initiative : {}".format(self.initiative),
                     "Speed : {}".format(self.speed),
                     "Attack Points : {}".format(self.attack),
                     "Range : {}".format(self.scope),
                     "Strength : {}".format(self.strength),
                     "Stamina : {}".format(self.stamina),
                     "Agility : {}".format(self.agility),
                     "Magic : {}".format(self.magic),
                     "Mental : {}".format(self.mental)]:
            yield font.render(attr, 1, constants.Colors.WHITE)

    def get_points_inspected_battle(self, font):
        """
        Renvoie les attributs à points du héros choisi pour l'affichage sur l'écran du déploiement ou de la bataille
        """
        for attr in ["Life Points : {} / {}".format(self.life_points, self.life_points_current),
                     "Magic Points : {} / {}".format(self.magic_points, self.magic_points_current),
                     "Armor : {} / {}".format(self.armor, self.armor_current)]:
            yield font.render(attr, 1, constants.Colors.WHITE)

    def get_skills_inspected(self, font):
        """
        Renvoie les compétences du héros choisi pour l'affichage des détails du héros sélectionné
        """
        for skill in self.skills:
            temp_skill = skill
            while len(temp_skill) >= constants.TeamSelection.SIZE_TEXT_MULTILINES+1:
                for i in range(constants.TeamSelection.SIZE_TEXT_MULTILINES+1, 0, -1):
                    if temp_skill[i] == " ":
                        yield font.render(temp_skill[:i], 1, constants.Colors.WHITE)
                        temp_skill = temp_skill[i+1:]
                        break
            yield font.render(temp_skill, 1, constants.Colors.WHITE)

    def get_description_inspected(self, font):
        """
        Renvoie la description du héros choisi pour l'affichage des détails du héros sélectionné
        """
        descr = self.description
        while len(descr) > constants.TeamSelection.SIZE_TEXT_MULTILINES:
            for i in range(constants.TeamSelection.SIZE_TEXT_MULTILINES, 0, -1):
                if descr[i] == " ":
                    yield font.render(descr[:i], 1, constants.Colors.WHITE)
                    descr = descr[i+1:]
                    break
        yield font.render(descr, 1, constants.Colors.WHITE)

    def search_hero_in_list(self, list_heroes):
        """
        Cherche le héros dans une liste et renvoie un booléen
        """
        truth_table = [self.name == elem.name for elem in list_heroes]
        return any(truth_table)

    def count_hero_in_list(self, list_heroes):
        """
        Compte le nombre d'occurrences du héros dans une liste
        """
        return len([elem for elem in list_heroes if elem.name == self.name])

    def return_hero_from_list(self, list_heroes):
        """
        Renvoie le héros depuis une liste
        """
        return [elem for elem in list_heroes if elem.name == self.name][0]
