import pygame
import sys

import battle_size_selection
import constants
import deck_selection
import overlay_load
import overlay_points_left_team_selection
import overlay_save
from button_image_class import ButtonImage
from button_text_class import ButtonText
from heroes_class import Heroes
from load_class import Load

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class TeamSelection:
    """
    FENETRE DE SELECTION DES HEROS
    """

    def __init__(self, *args):
        # Récupération de l'écran, du timer, du total de points disponibles, du nom des joueurs et des équipes choisies
        self.screen = args[0][0]
        self.clock = args[0][1]
        self.total_points = args[0][2]
        self.fplayer_name = args[0][3]
        self.splayer_name = args[0][4]
        self.fplayer_team = args[0][5]
        self.splayer_team = args[0][6]
        # Initialise la liste des héros sélectionnés, liste précédemment choisie dans le cas d'un retour arrière,
        # liste vide sinon
        self.list_in_team = args[0][7]
        # Initialisation des polices
        self.font_back = pygame.font.SysFont(constants.Fonts.ARIAL, 16)
        self.font_back.set_bold(True)
        self.font_small = pygame.font.SysFont(constants.Fonts.ARIAL, 14)
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 22)
        self.font_large.set_bold(True)
        self.font_medium.set_bold(True)
        # Variables
        self.start_list_heroes = 0
        self.end_list_heroes = \
            self.start_list_heroes + constants.TeamSelection.LINE_LENGTH * constants.TeamSelection.COLUMN_LENGTH
        # Récupère les héros dans le fichier binaire
        load = Load(constants.Files.HEROES_FILE)
        self.heroes = load.load
        # Initialisation du fond d'écran et de la zone des détails
        self.background = pygame.image.load(constants.ImagesPath.T_S_SCREEN).convert()
        self.frame = pygame.image.load(constants.ImagesPath.FRAME_DETAILS)
        self.frame_rect = self.frame.get_rect()
        self.frame_rect.left, self.frame_rect.top = constants.TeamSelection.DETAILS_ZONE, 0
        # Crée une liste d'objets héros
        self.list_heroes = []
        for name, stats in self.heroes.items():
            self.list_heroes.append(
                Heroes(name=name, speed=stats["speed"], initiative=stats["initiative"],
                       life_points=stats["life_points"], life_points_current=stats["life_points"],
                       magic_points=stats["magic_points"], magic_points_current=stats["magic_points"],
                       armor=stats["armor"], armor_current=stats["armor"], scope=stats["range"], size=stats["size"],
                       agility=stats["agility"], stamina=stats["stamina"], strength=stats["strength"],
                       magic=stats["magic"], mental=stats["mental"], attack=stats["attack"], cost=stats["cost"],
                       unique=stats["unique"], skills=stats["skills"], description=stats["description"],
                       token_text=stats["token_path"], miniature_text=stats["miniature_path"],
                       token_init_text=stats["token_init_path"], battlefield_text=stats["battlefield_path"],
                       font_small=self.font_small, font_large=self.font_large))
        # Trie la liste par ordre alphabétique, sélectionne le premier héros
        self.list_heroes = sorted(self.list_heroes, key=lambda hero: hero.name)
        self.list_heroes[0].is_inspected = True
        self.current_hero = self.list_heroes[0]
        # Initialisation des boutons texte
        self.list_buttons_text = list()
        centerx_back = self.screen.get_rect().centerx
        bottom_back = self.screen.get_rect().height
        left_load_save = constants.TeamSelection.BUTTONS_LOADSAVE_MARGIN
        bottom_load_save = self.screen.get_rect().height - constants.TeamSelection.BOT_BUTTONS_TEXT
        bottom_ts = self.screen.get_rect().height - constants.TeamSelection.BOT_BUTTONS_TEXT
        left_ts = constants.TeamSelection.DETAIL_INSPECTED_X
        self.list_buttons_text.append(ButtonText(font=self.font_large, pos_bottom=bottom_ts, text=constants.Texts.ADD,
                                                 on_clic=self.add_hero_in_team, active=True, pos_left=left_ts))
        self.list_buttons_text.append(ButtonText(font=self.font_large, pos_bottom=bottom_ts,
                                                 text=constants.Texts.REMOVE, on_clic=self.del_hero_in_team,
                                                 active=False, pos_right=self.screen.get_rect().width -
                                                 constants.TeamSelection.BUTTON_REMOVE_MARGIN))
        self.list_buttons_text.append(ButtonText(font=self.font_large, pos_bottom=bottom_ts, text=constants.Texts.NEXT,
                                                 active=False, pos_right=constants.TeamSelection.DETAIL_INSPECTED_X -
                                                 constants.TeamSelection.BUTTON_NEXT_MARGIN,
                                                 on_clic=self.start_overlay_points_left))
        self.list_buttons_text.append(ButtonText(font=self.font_back, text=constants.Texts.BACK,
                                                 pos_centerx=centerx_back, pos_bottom=bottom_back))
        self.list_buttons_text.append(ButtonText(font=self.font_large, text=constants.Texts.SAVE_TEAM,
                                                 pos_left=left_load_save, on_clic=self.start_overlay_save,
                                                 pos_bottom=bottom_load_save))
        self.list_buttons_text.append(ButtonText(font=self.font_large, text=constants.Texts.LOAD_TEAM,
                                                 pos_left=left_load_save, on_clic=self.start_overlay_load,
                                                 pos_bottom=bottom_load_save + self.font_large.get_height()))
        # Affiche le nom du joueur courant
        if self.fplayer_team is None:
            self.render_text_name = self.font_large.render(self.fplayer_name, 1, constants.Colors.WHITE)
        else:
            self.render_text_name = self.font_large.render(self.splayer_name, 1, constants.Colors.WHITE)
        self.render_text_name_rect = self.render_text_name.get_rect()
        self.render_text_name_rect.centerx = centerx_back
        self.render_text_name_rect.bottom = bottom_back - constants.TeamSelection.NAME_MARGIN
        # Initialisation des boutons image
        self.list_buttons_image = list()
        pos_left = constants.TeamSelection.DETAIL_INSPECTED_X - constants.TeamSelection.BUTTON_ARROWS_MARGIN
        pos_top = constants.Window.SCREEN_HEIGHT - constants.TeamSelection.TOP_BUTTONS_ARROWS
        self.list_buttons_image.append(ButtonImage(position=1, image_base=constants.ImagesPath.BUTTON_ARROW_DOWN_BASE,
                                                   image_hovered=constants.ImagesPath.BUTTON_ARROW_DOWN_HOVERED,
                                                   image_disabled=constants.ImagesPath.BUTTON_ARROW_DOWN_DISABLED,
                                                   on_clic=self.list_down, active=True, pos_left=pos_left,
                                                   pos_top=pos_top - constants.TeamSelection.BUTTON_ARROWS_PADDING * 1))
        self.list_buttons_image.append(ButtonImage(position=2, image_base=constants.ImagesPath.BUTTON_ARROW_UP_BASE,
                                                   image_hovered=constants.ImagesPath.BUTTON_ARROW_UP_HOVERED,
                                                   image_disabled=constants.ImagesPath.BUTTON_ARROW_UP_DISABLED,
                                                   on_clic=self.list_up, pos_left=pos_left,
                                                   pos_top=pos_top - constants.TeamSelection.BUTTON_ARROWS_PADDING * 2))
        self.run()

    def get_event(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.KEYDOWN:
                # Fléche de droite
                if event.key == pygame.K_RIGHT:
                    if self.list_heroes.index(self.current_hero) < self.end_list_heroes - 1 and \
                                            self.list_heroes.index(self.current_hero) % \
                                            constants.TeamSelection.LINE_LENGTH < \
                                            constants.TeamSelection.LINE_LENGTH - 1:
                        self.current_hero = self.list_heroes[self.list_heroes.index(self.current_hero) + 1]
                # Flèche de gauche
                if event.key == pygame.K_LEFT:
                    if self.list_heroes.index(self.current_hero) > self.start_list_heroes and \
                                            self.list_heroes.index(self.current_hero) % \
                                            constants.TeamSelection.LINE_LENGTH > 0:
                        self.current_hero = self.list_heroes[self.list_heroes.index(self.current_hero) - 1]
                # Flèche du haut
                if event.key == pygame.K_UP:
                    if self.start_list_heroes > 0 and self.list_heroes.index(self.current_hero) < \
                            (self.start_list_heroes + constants.TeamSelection.LINE_LENGTH):
                        self.list_up()
                    if self.list_heroes.index(self.current_hero) > self.start_list_heroes + \
                            constants.TeamSelection.LINE_LENGTH - 1:
                        self.current_hero = self.list_heroes[self.list_heroes.index(self.current_hero) -
                                                             constants.TeamSelection.LINE_LENGTH]
                # Flèche du bas
                if event.key == pygame.K_DOWN:
                    if self.list_heroes.index(self.current_hero) > \
                                            self.end_list_heroes - constants.TeamSelection.LINE_LENGTH - 1:
                        self.list_down()
                    if self.list_heroes.index(self.current_hero) < self.end_list_heroes - \
                            constants.TeamSelection.LINE_LENGTH:
                        self.current_hero = self.list_heroes[self.list_heroes.index(self.current_hero) +
                                                             constants.TeamSelection.LINE_LENGTH]
                # Page suivant
                if event.key == pygame.K_PAGEDOWN:
                    self.list_down()
                # Page précédente
                if event.key == pygame.K_PAGEUP:
                    if self.start_list_heroes > 0:
                        self.list_up()
                # Touche entrée
                if event.key == pygame.K_RETURN:
                    if self.current_hero.unique:
                        if self.current_hero.search_hero_in_list(self.list_in_team):
                            self.del_hero_in_team()
                        else:
                            self.add_hero_in_team()
                    else:
                        self.add_hero_in_team()
                # Touche supprimer
                if event.key == pygame.K_DELETE:
                    if self.current_hero.search_hero_in_list(self.list_in_team):
                        self.del_hero_in_team()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic gauche
                if event.button == 1:
                    # Passe le héros sélectionné à "is_inspected" et tous les autres à false
                    # Ajoute le héros dans la liste des sélectionnés dans le cas d'un deuxième clic
                    for hero in self.list_heroes[self.start_list_heroes:self.end_list_heroes]:
                        if hero.token_rect.collidepoint(mouse_pos):
                            if hero == self.current_hero and not hero.search_hero_in_list(self.list_in_team):
                                self.add_hero_in_team()
                            elif hero == self.current_hero and hero in self.list_in_team:
                                if hero.unique:
                                    self.del_hero_in_team()
                                else:
                                    self.add_hero_in_team()
                            for h in self.list_heroes:
                                h.is_inspected = False
                            hero.is_inspected = True
                            self.current_hero = hero
                    for button in self.list_buttons_text:
                        if button.rect.collidepoint(mouse_pos):
                            # Si le bouton est actif, lance la fonction liée
                            if button.active:
                                # Gestion des instances multiples de la page avec le bouton retour
                                if button.text == constants.Texts.BACK:
                                    if self.fplayer_team is None:
                                        battle_size_selection.BattleSizeSelection((self.screen, self.clock,
                                                                                   self.fplayer_name,
                                                                                   self.splayer_name))
                                    else:
                                        self.__init__((self.screen, self.clock, self.total_points, self.fplayer_name,
                                                       self.splayer_name, None, None, self.fplayer_team))
                                elif button.parameters is not None:
                                    button.on_clic(button.parameters)
                                else:
                                    button.on_clic()
                    for button in self.list_buttons_image:
                        if button.rect.collidepoint(mouse_pos):
                            # Si le bouton est actif, lance la fonction liée
                            if button.active:
                                button.on_clic()
                # Clic droit
                if event.button == 3:
                    # Supprime le héros si il est dans la liste des héros sélectionnés
                    for hero in self.list_heroes:
                        if hero.token_rect.collidepoint(mouse_pos):
                            if hero == self.current_hero and hero.search_hero_in_list(self.list_in_team):
                                self.del_hero_in_team()
                # Scroll up
                elif event.button == 4:
                    if self.start_list_heroes > 0:
                        self.start_list_heroes -= constants.TeamSelection.LINE_LENGTH
                        self.end_list_heroes = \
                            self.start_list_heroes + \
                            constants.TeamSelection.LINE_LENGTH * constants.TeamSelection.COLUMN_LENGTH
                # Scroll down
                elif event.button == 5:
                    if self.end_list_heroes < len(self.list_heroes) - 1:
                        self.start_list_heroes += constants.TeamSelection.LINE_LENGTH
                    if self.end_list_heroes + constants.TeamSelection.LINE_LENGTH > len(self.list_heroes) - 1:
                        self.end_list_heroes = len(self.list_heroes)
                    else:
                        self.end_list_heroes += constants.TeamSelection.LINE_LENGTH

    def draw(self, mouse_pos):
        # Affiche le fond d'écran et la zone des détails
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.frame, self.frame_rect)
        # Affiche le nom du joueur
        self.screen.blit(self.render_text_name, self.render_text_name_rect)
        # Affiche les boutons texte
        for button in self.list_buttons_text:
            button.draw(self.screen, mouse_pos)
        # Affiche les boutons image
        for button in self.list_buttons_image:
            button.draw(self.screen, mouse_pos)
        token_x, token_y = constants.TeamSelection.START_TOKEN_X, constants.TeamSelection.START_TOKEN_Y
        for ind in range(self.start_list_heroes, self.end_list_heroes):
            # Affiche les tokens
            self.list_heroes[ind].token_rect.left = token_x
            self.list_heroes[ind].token_rect.top = token_y
            self.screen.blit(self.list_heroes[ind].token, self.list_heroes[ind].token_rect)
            token_x += constants.TeamSelection.MARGIN_X
            if token_x >= constants.TeamSelection.LIMIT_RIGHT:
                token_x = constants.TeamSelection.START_TOKEN_X
                token_y += constants.TeamSelection.MARGIN_Y
            # Affiche le nom des héros en or et l'entoure si il est sélectionné dans l'équipe. En blanc sinon
            self.list_heroes[ind].name_text_rect.centerx = self.list_heroes[ind].token_rect.centerx
            self.list_heroes[ind].name_text_rect.top = \
                self.list_heroes[ind].token_rect.top + constants.TeamSelection.DIFF_TOKEN_TEXT
            if self.list_heroes[ind].search_hero_in_list(self.list_in_team):
                self.screen.blit(self.list_heroes[ind].name_text_in_team, self.list_heroes[ind].name_text_rect)
                pygame.draw.rect(self.screen, constants.Colors.GOLD, (self.list_heroes[ind].name_text_rect.x -
                                                                      constants.TeamSelection.SQUARE_SELECTED_DIFF,
                                                                      self.list_heroes[ind].name_text_rect.y -
                                                                      constants.TeamSelection.SQUARE_SELECTED_DIFF,
                                                                      self.list_heroes[ind].name_text_rect.width +
                                                                      constants.TeamSelection.SQUARE_SELECTED_DIFF * 2,
                                                                      self.list_heroes[ind].name_text_rect.height +
                                                                      constants.TeamSelection.SQUARE_SELECTED_DIFF *
                                                                      2), 1)
                # Affiche le nombre de héros d'un même type sélectionné si le héros n'est pas unique
                if not self.list_heroes[ind].unique:
                    nbr_heros_text = self.font_small.render(str(
                        self.list_heroes[ind].count_hero_in_list(self.list_in_team)), 1, constants.Colors.GOLD)
                    nbr_heros_text_rect = nbr_heros_text.get_rect()
                    nbr_heros_text_rect.right = self.list_heroes[ind].name_text_rect.right
                    nbr_heros_text_rect.top = self.list_heroes[ind].name_text_rect.bottom
                    self.screen.blit(nbr_heros_text, nbr_heros_text_rect)
            else:
                self.screen.blit(self.list_heroes[ind].name_text, self.list_heroes[ind].name_text_rect)
            # Affiche un carré blanc autour du token si il est survolé
            if self.list_heroes[ind].token_rect.collidepoint(mouse_pos):
                if not self.list_heroes[ind].is_inspected:
                    pygame.draw.rect(self.screen, constants.Colors.WHITE, (self.list_heroes[ind].token_rect.x -
                                                                           constants.TeamSelection.SQUARE_HOVERED_DIFF,
                                                                           self.list_heroes[ind].token_rect.y -
                                                                           constants.TeamSelection.SQUARE_HOVERED_DIFF,
                                                                           self.list_heroes[ind].token_rect.width +
                                                                           constants.TeamSelection.SQUARE_HOVERED_DIFF *
                                                                           2, self.list_heroes[ind].token_rect.height +
                                                                           constants.TeamSelection.SQUARE_HOVERED_DIFF *
                                                                           2), 3)
        # Affiche un carré or autour du token du héros inspecté
        if self.end_list_heroes >= self.list_heroes.index(self.current_hero) >= self.start_list_heroes:
            pygame.draw.rect(self.screen, constants.Colors.GOLD, (self.current_hero.token_rect.x -
                                                                  constants.TeamSelection.SQUARE_HOVERED_DIFF,
                                                                  self.current_hero.token_rect.y -
                                                                  constants.TeamSelection.SQUARE_HOVERED_DIFF,
                                                                  self.current_hero.token_rect.width +
                                                                  constants.TeamSelection.SQUARE_HOVERED_DIFF * 2,
                                                                  self.current_hero.token_rect.height +
                                                                  constants.TeamSelection.SQUARE_HOVERED_DIFF * 2), 3)
        # Affiche les informations du héros inspecté
        # Affiche la miniature
        self.current_hero.miniature_rect.centerx = self.frame_rect.centerx
        self.current_hero.miniature_rect.top = constants.TeamSelection.MINIATURE_INSPECTED_Y
        self.screen.blit(self.current_hero.miniature, self.current_hero.miniature_rect)
        # Affiche le nom
        self.current_hero.name_text_inspected_rect.centerx = self.frame_rect.centerx
        self.current_hero.name_text_inspected_rect.top = constants.TeamSelection.NAME_INSPECTED_Y
        self.screen.blit(self.current_hero.name_text_inspected, self.current_hero.name_text_inspected_rect)
        # Affiche les caractéristiques
        pos_details_y = constants.TeamSelection.START_DETAILS_Y
        for detail in self.current_hero.get_list_inspected(self.font_medium):
            detail_rect = detail.get_rect()
            detail_rect.left = constants.TeamSelection.DETAIL_INSPECTED_X
            detail_rect.top = pos_details_y
            pos_details_y += detail_rect.height
            self.screen.blit(detail, detail_rect)
        # Affiche les compétences
        skills_text = self.font_medium.render(constants.Texts.SKILLS, 1, constants.Colors.WHITE)
        pos_details_y += skills_text.get_rect().height
        self.screen.blit(skills_text, (constants.TeamSelection.DETAIL_INSPECTED_X, pos_details_y))
        pos_details_y += skills_text.get_rect().height
        for skill in self.current_hero.get_skills_inspected(self.font_small):
            skill_rect = skill.get_rect()
            skill_rect.left = constants.TeamSelection.DETAIL_INSPECTED_X
            skill_rect.top = pos_details_y
            pos_details_y += skill_rect.height
            self.screen.blit(skill, skill_rect)
        # Affiche le total des points
        total_points_text = self.font_large.render("{} / {}".format(sum([hero.cost for hero in self.list_in_team]),
                                                                    self.total_points), 1, constants.Colors.WHITE)
        total_points_text_rect = total_points_text.get_rect()
        total_points_text_rect.centerx = [button.rect.centerx for button in self.list_buttons_text if button.text ==
                                          constants.Texts.NEXT][0]
        total_points_text_rect.y = self.screen.get_rect().height - constants.TeamSelection.BOT_BUTTONS_TEXT
        self.screen.blit(total_points_text, total_points_text_rect)
        # Affiche la description
        description_text = self.font_medium.render(constants.Texts.DESCRIPTION, 1, constants.Colors.WHITE)
        pos_details_y += description_text.get_rect().height
        self.screen.blit(description_text, (constants.TeamSelection.DETAIL_INSPECTED_X, pos_details_y))
        pos_details_y += description_text.get_rect().height
        for text in self.current_hero.get_description_inspected(self.font_small):
            text_rect = text.get_rect()
            text_rect.left = constants.TeamSelection.DETAIL_INSPECTED_X
            text_rect.top = pos_details_y
            pos_details_y += text_rect.height
            self.screen.blit(text, text_rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def add_hero_in_team(self):
        """
        Ajoute un héros dans la liste des héros sélectionnés
        """
        self.list_in_team.append(self.current_hero)

    def del_hero_in_team(self):
        """
        Supprime un héros de la liste des héros sélectionnés
        """
        self.list_in_team.remove(self.current_hero.return_hero_from_list(self.list_in_team))

    def list_down(self):
        """
        Fait défiler la liste des héros vers le bas
        """
        if self.end_list_heroes < len(self.list_heroes) - 1:
            self.start_list_heroes += constants.TeamSelection.LINE_LENGTH
        if self.end_list_heroes + constants.TeamSelection.LINE_LENGTH > len(self.list_heroes) - 1:
            self.end_list_heroes = len(self.list_heroes)
        else:
            self.end_list_heroes += constants.TeamSelection.LINE_LENGTH

    def list_up(self):
        """
        Fait défiler la liste des héros vers le haut
        """
        self.start_list_heroes -= constants.TeamSelection.LINE_LENGTH
        self.end_list_heroes = \
            self.start_list_heroes + constants.TeamSelection.LINE_LENGTH * constants.TeamSelection.COLUMN_LENGTH

    def change_state_image_buttons(self):
        """
        Modifie létat des boutons images en fonction de la position du scroll
        """
        for button in self.list_buttons_image:
            if button.position == 1 and self.end_list_heroes < len(self.list_heroes):
                button.active = True
            elif button.position == 1 and self.end_list_heroes == len(self.list_heroes):
                button.active = False
            if button.position == 2 and self.start_list_heroes > 0:
                button.active = True
            elif button.position == 2 and self.start_list_heroes == 0:
                button.active = False

    def change_state_text_buttons(self):
        """
        Modifie l'état des boutons textes en fonctions des différents paramètres
        """
        for button in self.list_buttons_text:
            if button.text == constants.Texts.ADD:
                if self.current_hero.unique and self.current_hero.search_hero_in_list(self.list_in_team):
                    button.active = False
                else:
                    button.active = True
            elif button.text == constants.Texts.REMOVE:
                if self.current_hero.search_hero_in_list(self.list_in_team):
                    button.active = True
                else:
                    button.active = False
            elif button.text == constants.Texts.NEXT:
                if len(self.list_in_team) > 0 and sum([hero.cost for hero in self.list_in_team]) <= self.total_points:
                    button.active = True
                else:
                    button.active = False

    def start_overlay_load(self):
        """
        Démarre la page de l'overlay de chargement d'une équipe sauvegardée
        """
        capture = self.screen.copy()
        class_button = \
            overlay_load.OverlayLoad(self.screen, capture, self.clock, self.list_in_team, constants.Files.TEAMS_SAVE)
        to_load = class_button.run()
        if to_load is not None:
            self.list_in_team = to_load
            for hero in self.list_in_team:
                hero.update_images()

    def start_overlay_save(self):
        """
        Démarre la page de l'overlay de sauvegarde d'une équipe
        """
        capture = self.screen.copy()
        overlay_save.OverlaySave(self.screen, capture, self.clock, self.list_in_team, constants.Files.TEAMS_SAVE)

    def start_overlay_points_left(self):
        """
        Compare le nombre de points restants avec le prix du héros le moins cher dans une liste de héros non
        sélectionnés.
        Si la team du premier joueur est vide, affecte l'équipe et passe à la deuxième instance de la page (ou à
        l'overlay indiquant qu'il reste des points le cas échéant), à la page de sélection du deck sinon.
        """
        capture = self.screen.copy()
        heroes_left = set(self.list_heroes) - set(hero for hero in self.list_in_team
                                                  if hero.unique)
        if self.fplayer_team is None:
            for hero in self.list_in_team:
                # Indique le nom du joueur sur les héros sélectionnés
                hero.player_name = self.fplayer_name
            self.fplayer_team = self.list_in_team
            if min([hero.cost for hero in heroes_left]) < self.total_points - \
                    sum([hero.cost for hero in self.list_in_team]):
                overlay_points_left_team_selection.OverlayPointsLeftTeamSelection(self.screen, capture, self.clock,
                                                                                  self.total_points, self.fplayer_name,
                                                                                  self.splayer_name, self.fplayer_team,
                                                                                  self.splayer_team)
                self.fplayer_team = None
            else:
                self.__init__((self.screen, self.clock, self.total_points, self.fplayer_name, self.splayer_name,
                               self.fplayer_team, None, list()))
        else:
            for hero in self.list_in_team:
                # Indique le nom du joueur sur les héros sélectionnés
                hero.player_name = self.splayer_name
            self.splayer_team = self.list_in_team
            if min([hero.cost for hero in heroes_left]) < self.total_points - \
                    sum([hero.cost for hero in self.list_in_team]):
                overlay_points_left_team_selection.OverlayPointsLeftTeamSelection(self.screen, capture, self.clock,
                                                                                  self.total_points, self.fplayer_name,
                                                                                  self.splayer_name, self.fplayer_team,
                                                                                  self.splayer_team)
                self.splayer_team = None
            else:
                deck_selection.DeckSelection((self.screen, self.clock, self.total_points, self.fplayer_name,
                                              self.splayer_name, self.fplayer_team, self.splayer_team, None, None,
                                              list()))

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            self.get_event(pygame.event.get(), mouse_pos)
            self.change_state_image_buttons()
            self.change_state_text_buttons()
            self.draw(mouse_pos)
