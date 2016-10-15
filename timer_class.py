import pygame

__author__ = "Jérémy Farnault"


class Timer:
    """
    OBJETS TIMER
    """

    def __init__(self, **kwargs):
        self.timer = pygame.time.get_ticks()
        self.timer_min = None
        self.timer_sec = None
        self.to_do = None
        self.parameters = None
        self.font = None
        self.color = None
        self.color_end = None
        self.timer_text = None
        self.render = None
        self.rect = None
        self.pos_centerx = None
        self.pos_centery = None
        self.pos_top = None
        self.pos_bottom = None
        self.pos_left = None
        self.pos_right = None
        self.top = None
        self.right = None
        self.bot = None
        self.left = None
        self.width = None
        self.height = None
        self.process_kwargs(kwargs)
        self.update_attributes()
        self.update_timer()

    def process_kwargs(self, kwargs):
        defaults = {}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def update_attributes(self):
        self.timer_text = self.font.render("00:00", 1, self.color)
        self.rect = self.timer_text.get_rect()
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

    def update_timer(self):
        """
        Met à jour le texte du timer
        """
        if pygame.time.get_ticks() - self.timer >= 1000:
            self.timer_sec -= 1
            self.timer = pygame.time.get_ticks()
            if self.timer_sec == 0 and self.timer_min == 0:
                if self.parameters is not None:
                    self.to_do(self.parameters)
                else:
                    self.to_do()
            elif self.timer_sec == -1:
                self.timer_min -= 1
                self.timer_sec = 59
        if self.timer_sec < 10 and self.timer_min == 0:
            self.timer_text = "0{}:0{}".format(self.timer_min, self.timer_sec)
            self.render = self.font.render(self.timer_text, 1, self.color_end)
        elif self.timer_sec < 10:
            self.timer_text = "0{}:0{}".format(self.timer_min, self.timer_sec)
            self.render = self.font.render(self.timer_text, 1, self.color)
        else:
            self.timer_text = "0{}:{}".format(self.timer_min, self.timer_sec)
            self.render = self.font.render(self.timer_text, 1, self.color)
