import pygame as pg

def polarity(num):
    """
    Returns the polarity of the given number.
    """
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0


class Vector(object):
    """
    My own vector class, with blackjack and hookers.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        """
        Update x and y at once.
        """
        self.x = x
        self.y = y

    def add(self, vector):
        """
        Add a vector to this vector.
        """
        self.x += vector.x
        self.y += vector.y

    def get(self):
        """
        Returns the contents of this vector as tuple.
        """
        return self.x, self.y


def draw_text(display, font_name, text, size, color, x, y):
    """ draw text to the screen at position x, y """
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display.blit(text_surface, text_rect)