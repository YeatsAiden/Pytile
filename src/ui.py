from settings import *
import settings
from core_funcs import *


class Button:
    def __init__(self, x: int, y: int, surface_path: pg.Surface):
        self.button_img = pg.image.load(surface_path).convert()
        self.rect = self.button_img.get_rect()
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

    def draw(self, surf: pg.Surface):
        surf.blit(self.button_img, (self.rect.x, self.rect.y))

        
class Font:
    def __init__(self, path: str, include: list[int, int, int], step: int) -> None:
        self.characters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789", "!@#$%^&*()`~-_=+\\|[]}{';:/?.>,<"]

        self.font = self.load_font(path, include, step)
    
    def load_font(self, path: str, include: list[int, int, int], step: int):
        font_img = pg.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        characters = []
        font = {}
        x_pos = 0
        for x in range(font_img.get_width()):
            for y in range(font_img.get_height()):
                color = font_img.get_at((x, y))

                if color == (255, 0, 0, 255):
                    character = clip_img(font_img, x_pos, 0, x - x_pos, font_img.get_height())
                    x_pos = x + 1

                    if y == 1:
                        cp_surface = character.copy()
                        character = pg.Surface((cp_surface.get_width(), cp_surface.get_height() + step))
                        character.blit(cp_surface, (0, step))
                    characters.append(character)
        
        for i in include:
            for character in self.characters[i]:
                font[character] = characters[len(font)]
        
        return font
    
    def draw_text(self, surface: pg.Surface, text: str, x: int, y: int, space: int, size: int):
        x_pos = 0
        for letter in text:
            if letter == " ":
                x_pos += space * size
            else:
                character_img = pg.transform.scale_by(self.font[letter], size)
                surface.blit(character_img, (x + x_pos, y))
                x_pos += character_img.get_width() + size





