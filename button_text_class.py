import constants

__author__ = "Jérémy Farnault"


class ButtonText:
    """
    OBJETS BOUTONS TEXTE
    """

    def __init__(self, **kwargs):
        self.render_base = None
        self.render_hover = None
        self.render_inactive = None
        self.on_clic = None
        self.parameters = None
        self.text = None
        self.font = None
        self.active = True
        self.pos_centerx = None
        self.pos_centery = None
        self.pos_top = None
        self.pos_bottom = None
        self.pos_left = None
        self.pos_right = None
        self.rect = None
        self.top = None
        self.right = None
        self.bot = None
        self.left = None
        self.width = None
        self.height = None
        self.process_kwargs(kwargs)
        self.update_attributes()

    def process_kwargs(self, kwargs):
        defaults = {}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def update_attributes(self):
        self.render_base = self.font.render(self.text, 1, constants.Colors.WHITE)
        self.render_hover = self.font.render(self.text, 1, constants.Colors.GOLD)
        self.render_inactive = self.font.render(self.text, 1, constants.Colors.DARK_SLATE_GRAY)
        self.rect = self.render_base.get_rect()
        self.update_rect()
        self.top = self.rect.top
        self.right = self.rect.right
        self.bot = self.rect.bottom
        self.left = self.rect.left
        self.width = self.rect.width
        self.height = self.rect.height

    def update_rect(self):
        """
        Met à jour les attributs de position du bouton selon ceux envoyés au constructeur
        """
        if self.pos_centerx is not None:
            self.rect.centerx = self.pos_centerx
        elif self.pos_left is not None:
            self.rect.left = self.pos_left
        elif self.pos_right is not None:
            self.rect.right = self.pos_right
        if self.pos_centery is not None:
            self.rect.centery = self.pos_centery
        elif self.pos_top is not None:
            self.rect.top = self.pos_top
        elif self.pos_bottom is not None:
            self.rect.bottom = self.pos_bottom

    def set_current_hero(self, hero):
        """
        Modifie le paramètre propre à la fenêtre de sélection de l'équipe
        """
        self.parameters[0] = hero

    def draw(self, screen, mouse_pos):
        """
        Affiche les boutons à l'écran
        """
        if not self.active:
            screen.blit(self.render_inactive, self.rect)
        elif self.rect.collidepoint(mouse_pos):
            screen.blit(self.render_hover, self.rect)
        else:
            screen.blit(self.render_base, self.rect)
