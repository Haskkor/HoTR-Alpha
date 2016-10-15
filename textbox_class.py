import pygame
import constants

__author__ = "Jérémy Farnault"


class TextBox:
    """
    OBJETS TEXTBOX
    """

    def __init__(self, rect, **kwargs):
        self.rect = pygame.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.id = None,
        self.command = None,
        self.active = True
        self.error = False
        self.font_color = constants.Colors.WHITE
        self.outline_color = constants.Colors.WHITE
        self.error_color = constants.Colors.RED
        self.outline_width = 2
        self.active_color = constants.Colors.GOLD
        self.font = pygame.font.Font(None, self.rect.height + 4)
        self.clear_on_enter = False
        self.inactive_on_enter = True
        self.process_kwargs(kwargs)

    def process_kwargs(self, kwargs):
        defaults = {}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in constants.Textbox.ACCEPTED:
                self.buffer.append(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos[0], event.pos[1])

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
            if self.render_rect.width > self.rect.width - 6:
                offset = self.render_rect.width - (self.rect.width - 6)
                self.render_area = pygame.Rect(offset, 0, self.rect.width - 6, self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0, 0))
        if pygame.time.get_ticks() - self.blink_timer > constants.Textbox.BLINK_TIMER:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def draw(self, surface):
        if self.error:
            outline_color = self.error_color
        elif self.active:
            outline_color = self.active_color
        else:
            outline_color = self.outline_color
        outline = self.rect.inflate(self.outline_width * 2, self.outline_width * 2)
        pygame.draw.rect(surface, outline_color, outline, self.outline_width)
        if self.rendered:
            surface.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color, (curse.right + 1, curse.y, 2, curse.h))
