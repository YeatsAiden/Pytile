from settings import *
import settings
from core_funcs import *


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.clicked = False
    

    def check_click(self):
        # get mouse position
        pos = list(pg.mouse.get_pos())
        mouse_pressed = pg.mouse.get_pressed()
        click = False

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and mouse_pressed[0] and not self.clicked:
            self.clicked = True
            click = True
        else:
            self.clicked = False

        # return if clicked
        return click

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))

        
class Text:
    def __init__(self) -> None:
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()`~-_=+\\|[]}{';:/?.>,<"

        for letter in characters:
            pass