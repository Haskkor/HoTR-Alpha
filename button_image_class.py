import pygame

__author__ = "Jérémy Farnault"


class ButtonImage:
    """
    OBJETS BOUTONS IMAGE
    """

    def __init__(self, **kwargs):
        self.image_base = None
        self.image_hovered = None
        self.image_disabled = None
        self.on_clic = None
        self.parameters = None
        self.surface = None
        self.active = True
        self.position = None
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
        self.image_base = pygame.image.load(self.image_base)
        self.image_hovered = pygame.image.load(self.image_hovered)
        self.image_disabled = pygame.image.load(self.image_disabled)
        self.rect = self.image_base.get_rect()
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

    def draw(self, screen, mouse_pos):
        """
        Affiche les boutons à l'écran
        """
        if not self.active:
            screen.blit(self.image_disabled, self.rect)
        elif self.rect.collidepoint(mouse_pos):
            screen.blit(self.image_hovered, self.rect)
        else:
            screen.blit(self.image_base, self.rect)
