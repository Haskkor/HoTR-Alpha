import pygame
import sys

import constants
from button_image_class import ButtonImage
from button_text_class import ButtonText
from load_class import Load
from save_class import Save

__author__ = "Jérémy Farnault"


def leave():
    pygame.quit()
    sys.exit()


class OverlayLoad:
    """
    OVERLAY POUR LE CHARGEMENT
    """

    def __init__(self, screen, capture, timer, list_to_save, filename):
        self.screen = screen
        self.capture = capture
        self.clock = timer
        self.to_return = None
        self.cancel = False
        self.list_to_save = list_to_save
        self.filename = filename
        # Polices
        self.font_medium = pygame.font.SysFont(constants.Fonts.ARIAL, 18)
        self.font_medium.set_bold(True)
        self.font_large = pygame.font.SysFont(constants.Fonts.ARIAL, 28)
        self.font_large.set_bold(True)
        # Création de l'overlay
        self.overlay = pygame.Surface((constants.Window.SCREEN_WIDTH, constants.Window.SCREEN_HEIGHT))
        self.overlay.fill(constants.Colors.BLACK)
        self.overlay.set_alpha(constants.Colors.OVERLAY_ALPHA)
        # Création des boutons et du texte
        self.list_buttons = list()
        centery = self.screen.get_rect().centery + constants.Modals.POS_ELEM_LOAD
        self.list_buttons.append(ButtonText(font=self.font_large, text=constants.Texts.LOAD, active=False,
                                            pos_centery=centery,
                                            pos_centerx=self.screen.get_rect().centerx - constants.Modals.POS_TEXT_LDC))
        self.list_buttons.append(ButtonText(font=self.font_large, text=constants.Texts.DELETE, active=False,
                                            pos_centery=centery, pos_centerx=self.screen.get_rect().centerx))
        self.list_buttons.append(ButtonText(font=self.font_large, text=constants.Texts.CANCEL, active=True,
                                            pos_centery=centery,
                                            pos_centerx=self.screen.get_rect().centerx + constants.Modals.POS_TEXT_LDC))
        self.list_buttons_rects = [button.rect for button in self.list_buttons]
        self.text = self.font_large.render(constants.Texts.MODAL_LOAD, 1, constants.Colors.WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.screen.get_rect().centerx
        self.text_rect.centery = constants.Modals.POS_TEXT_LOAD_TEAM_TITLE
        # Récupération de la liste de sauvegardes
        load_object = Load(self.filename)
        self.save_object = Save(self.filename)
        self.list_saves = load_object.load
        # Création des boutons images
        self.list_buttons_image = list()
        pos_left = self.screen.get_rect().width / 8 * 5 + constants.Overlays.BUTTON_ARROWS_MARGIN_MODAL
        pos_top = self.screen.get_rect().height / 4 * 3
        self.list_buttons_image.append(ButtonImage(image_base=constants.ImagesPath.BUTTON_ARROW_DOWN_BASE,
                                                   image_hovered=constants.ImagesPath.BUTTON_ARROW_DOWN_HOVERED,
                                                   image_disabled=constants.ImagesPath.BUTTON_ARROW_DOWN_DISABLED,
                                                   pos_top=pos_top - constants.TeamSelection.BUTTON_ARROWS_PADDING,
                                                   pos_left=pos_left, on_clic=self.list_down, active=True, position=1))
        self.list_buttons_image.append(ButtonImage(image_base=constants.ImagesPath.BUTTON_ARROW_UP_BASE,
                                                   image_hovered=constants.ImagesPath.BUTTON_ARROW_UP_HOVERED,
                                                   image_disabled=constants.ImagesPath.BUTTON_ARROW_UP_DISABLED,
                                                   pos_top=pos_top - 2 * constants.TeamSelection.BUTTON_ARROWS_PADDING,
                                                   pos_left=pos_left, on_clic=self.list_up, position=2))
        self.list_buttons_image_rects = [button.rect for button in self.list_buttons_image]
        # Transformation des textes ne rentrant pas dans la fenêtre des sauvegardes
        for save, team in self.list_saves.items():
            if self.font_medium.size(save)[0] > (screen.get_rect().width / 4):
                temp_save = save
                while self.font_medium.size(temp_save + constants.Texts.SUSPENSION)[0] > \
                        (self.screen.get_rect().width / 4 - constants.Modals.FRAME_LOAD_THICK * 3):
                    temp_save = temp_save[:-1]
                self.list_saves[temp_save + constants.Texts.SUSPENSION] = self.list_saves[save]
                del self.list_saves[save]
        # Création des ButtonText des sauvegardes
        self.list_saves_text = [ButtonText(use="saves_list", surface=self.screen, font=self.font_medium, text=save,
                                           function="", parameters=team) for save, team in self.list_saves.items()]
        # Trie la liste des sauvegardes par ordre alphabétique
        list_sorted = False
        while not list_sorted:
            list_sorted = True
            for i in range(1, len(self.list_saves_text)):
                if self.list_saves_text[i].text < self.list_saves_text[i - 1].text:
                    self.list_saves_text[i], self.list_saves_text[i - 1] = self.list_saves_text[i - 1], \
                                                                           self.list_saves_text[i]
                    list_sorted = False
        self.list_saves_text_rects = [save_text.rect for save_text in self.list_saves_text]
        self.start_list_saves = 0
        self.end_list_saves = len(self.list_saves_text) \
            if constants.Modals.MAX_SAVES_IN_LIST > len(self.list_saves_text) else constants.Modals.MAX_SAVES_IN_LIST
        self.to_load = ""

    def get_event(self, events, mouse_pos_rect):
        for event in events:
            if event.type == pygame.QUIT:
                leave()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Clic sur les sauvegardes
                    idx = mouse_pos_rect.collidelist(self.list_saves_text_rects)
                    if idx > -1:
                        if self.list_saves_text[idx].active:
                            for save in self.list_saves_text:
                                save.active = True
                            self.list_saves_text[idx].active = False
                            self.to_load = self.list_saves_text[idx].text
                            for but in self.list_buttons:
                                if but.text == constants.Texts.DELETE or but.text == constants.Texts.LOAD:
                                    but.active = True
                        else:
                            if self.list_saves_text[idx].text == self.to_load:
                                self.to_return = self.list_saves[self.to_load]
                    # Clic sur les boutons texte
                    elif mouse_pos_rect.collidelist(self.list_buttons_rects) > -1:
                        idx = mouse_pos_rect.collidelist(self.list_buttons_rects)
                        if self.list_buttons[idx].active:
                            if self.list_buttons[idx].text == constants.Texts.CANCEL:
                                self.cancel = True
                            elif self.list_buttons[idx].text == constants.Texts.LOAD:
                                self.to_return = self.list_saves[self.to_load]
                            else:
                                self.save_object.delete_elem(self.to_load)
                                to_delete = [elem for elem in self.list_saves_text if elem.text == self.to_load][0]
                                self.list_saves_text.remove(to_delete)
                                if self.end_list_saves > len(self.list_saves_text):
                                    self.end_list_saves = len(self.list_saves_text)
                                self.list_saves_text_rects = [save_text.rect for save_text in self.list_saves_text]
                                self.to_load, to_delete = "", ""
                                for but in self.list_buttons:
                                    if but.text == constants.Texts.DELETE or but.text == constants.Texts.LOAD:
                                        but.active = False
                    # Clic sur les boutons image
                    elif mouse_pos_rect.collidelist(self.list_buttons_image_rects) > -1:
                        idx = mouse_pos_rect.collidelist(self.list_buttons_image_rects)
                        if self.list_buttons_image[idx].active:
                            self.list_buttons_image[idx].on_clic()
                    # Clic sur aucun élément
                    else:
                        self.to_load = ""
                        for s in self.list_saves_text:
                            s.active = True
                        for but in self.list_buttons:
                            if but.text == constants.Texts.DELETE or but.text == constants.Texts.LOAD:
                                but.active = False
                # Scroll up
                elif event.button == 4:
                    if self.start_list_saves > 0:
                        self.list_up()
                # Scroll down
                elif event.button == 5:
                    if self.end_list_saves < len(self.list_saves_text):
                        self.list_down()

    def draw(self, mouse_pos, mouse_pos_rect):
        # Affiche la page de la sélection de l'équipe
        self.screen.blit(self.capture, (0, 0))
        # Affiche l'overlay, les boutons et le texte
        self.screen.blit(self.overlay, (0, 0))
        for button in self.list_buttons:
            button.draw(self.screen, mouse_pos)
        self.screen.blit(self.text, self.text_rect)
        pygame.draw.rect(self.screen, constants.Colors.WHITE, (self.screen.get_rect().centerx -
                                                               self.screen.get_rect().width / 8,
                                                               self.screen.get_rect().centery -
                                                               self.screen.get_rect().height / 4,
                                                               self.screen.get_rect().width / 4,
                                                               self.screen.get_rect().height / 2),
                         constants.Modals.FRAME_LOAD_THICK)
        # Affiche les boutons image
        for button in self.list_buttons_image:
            button.draw(self.screen, mouse_pos)
        # Affiche la liste des sauvegardes
        for ind in range(self.start_list_saves, self.end_list_saves):
            self.list_saves_text_rects[ind].left = self.screen.get_rect().centerx - self.screen.get_rect().width / 8 + \
                                                   constants.Modals.FRAME_LOAD_THICK * 2
            self.list_saves_text_rects[ind].top = \
                self.screen.get_rect().centery / 2 + constants.Modals.FRAME_LOAD_THICK * 2 + \
                self.list_saves_text[ind].height * (ind - self.start_list_saves)
            if self.list_saves_text[ind].active:
                if self.list_saves_text_rects[ind].collidepoint(mouse_pos):
                    self.screen.blit(self.list_saves_text[ind].render_hover, self.list_saves_text_rects[ind])
                else:
                    self.screen.blit(self.list_saves_text[ind].render_base, self.list_saves_text_rects[ind])
            else:
                self.screen.blit(self.list_saves_text[ind].render_inactive, self.list_saves_text_rects[ind])
        # Affiche le hover des boutons text
        if mouse_pos_rect.collidelist(self.list_buttons_rects) > -1:
            idx = mouse_pos_rect.collidelist(self.list_buttons_rects)
            if self.list_buttons[idx].active:
                self.screen.blit(self.list_buttons[idx].render_hover, self.list_buttons[idx].rect)
        # Affiche le hover des images
        elif mouse_pos_rect.collidelist(self.list_buttons_image_rects) > -1:
            idx = mouse_pos_rect.collidelist(self.list_buttons_image_rects)
            if self.list_buttons_image[idx].active:
                self.screen.blit(self.list_buttons_image[idx].image_hovered, self.list_buttons_image[idx].rect)
        self.clock.tick(constants.Framerate.FRAMERATE)
        pygame.display.flip()

    def list_down(self):
        """
        Fait défiler vers le bas la liste des sauvegardes
        """
        if self.end_list_saves < len(self.list_saves_text):
            self.start_list_saves += 1
            self.end_list_saves += 1

    def list_up(self):
        """
        Fait défiler vers le haut la liste des sauvegardes
        """
        self.start_list_saves -= 1
        self.end_list_saves = self.start_list_saves + constants.Modals.MAX_SAVES_IN_LIST

    def change_state_image_buttons(self):
        """
        Change l'état des boutons images
        """
        for button in self.list_buttons_image:
            if button.position == 1:
                if self.end_list_saves < len(self.list_saves_text):
                    button.active = True
                elif self.end_list_saves == len(self.list_saves_text):
                    button.active = False
            if button.position == 2:
                if self.start_list_saves > 0:
                    button.active = True
                elif self.start_list_saves == 0:
                    button.active = False

    def run(self):
        done = False
        while not done:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 0, 0)
            self.get_event(pygame.event.get(), mouse_pos_rect)
            if self.to_return is not None:
                return self.to_return
            if self.cancel:
                return
            self.change_state_image_buttons()
            self.draw(mouse_pos, mouse_pos_rect)
