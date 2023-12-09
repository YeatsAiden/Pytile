from settings import *
from core_funcs import *


class Load_tilesets:
    def __init__(self, tilesets_path) -> None:
        self.tilesets = {file.split('.')[0]: self.make_tileset_dict for file in get_file_names(tilesets_path)}
        # The color for determining tile size
        self.size_color = pg.Color(255, 0, 0, 255) 


    def make_tileset_dict(self, tileset_path):
        tileset = {}
        tileset_img = pg.image.load(tileset_path).convert()
        tileset["tile_size"] = self.get_tile_size(tileset_img)
        tileset["tile_imgs"] = []
        for y in range(tileset["tile_size"], tileset_img.get_height(), tileset["tile_size"]):
            for x in range(tileset["tile_size"], tileset_img.get_width(), tileset["tile_size"]):
                img = clip_img(tileset_img, x, y, tileset["tile_size"], tileset["tile_size"])

                if self.check_if_sprite_is_not_transparent(img):
                    tileset["tile_imgs"].append(img)
        
        return tileset


    def check_if_sprite_is_not_transparent(self, surf):
        for y in range(0, surf.get_height()):
            for x in range(0, surf.get_width()):
                if surf.get_at((x, y))[3] > 0:
                    return True
        return False
    

    def get_tile_size(self, surf):
        for y in range(0, surf.get_height()):
            for x in range(0, surf.get_width()):
                if surf.get_at((x, y)) == self.size_color:
                    return [x + 1, y + 1]
