from settings import *
from core_funcs import *


# Note "YoU CAn ONlY InDEnT YoUR CoDE 4 TiMeS" :p
class Load_map:
    def __init__(self, levels_dir):
        self.level_paths = [path for path in get_file_names(levels_dir) if path.split('.')[1] == 'json']
        self.levels = {}
        for path in self.level_paths:
            with open(levels_dir + '/' + path) as f:
                self.level_json_data = json.load(f)
                self.levels[path.split(".")[0]] = [layer for layer in self.level_json_data["layers"]]
                self.tile_size = self.level_json_data["tilewidth"]

        self.tile_set_img = pg.image.load("assets/tileset/tile_set.png").convert_alpha()
        self.images_dict = self.make_image_dict(self.tile_set_img)


    def make_rects_array(self, layers, offset):
        array = {}
        collision_layer = {}

        for layer in layers:
            if layer["name"] == "middle_ground":
                collision_layer = layer 

        y = 0
        for row in collision_layer["data"]:
            x = 0
            for tile in row:
                if tile != 0:
                    rect = pg.FRect((x + offset[0]) * self.tile_size, (y + offset[1]) * self.tile_size, self.tile_size, self.tile_size)
                    array[f'{x}:{y}'] = rect
                x += 1
            y += 1

        return array
    
    
    def make_image_dict(self, tile_set_img):
        # Find out yourself :\, I already forgor how it works
        tile_imgs = {}
        for y in range(0, tile_set_img.get_height(), self.tile_size):
            for x in range(0, tile_set_img.get_width(), self.tile_size):
                img = clip_img(tile_set_img, x, y, self.tile_size, self.tile_size)

                if self.check_if_sprite_is_not_transparent(img):
                    tile_imgs[y // self.tile_size * tile_set_img.get_width() // self.tile_size + x // self.tile_size + 1] = img
        
        return tile_imgs


    def check_if_sprite_is_not_transparent(self, surf):
        for y in range(0, surf.get_height()):
            for x in range(0, surf.get_width()):
                color = surf.get_at((x, y))
                if color[3] > 0:
                    return True
        return False


    def get_area(self, surf, cam_pos, layers):
        # This finds the area on the map that will be rendered using your camera
        areas = []

        start_row = int(cam_pos[1] // self.tile_size) if cam_pos[1] > 0 else 0 
        end_row = int((cam_pos[1] + surf.get_height()) // self.tile_size) + 1 if cam_pos[1] > 0 else surf.get_height() // self.tile_size
        start_col = int(cam_pos[0] // self.tile_size) if cam_pos[0] > 0 else 0 
        end_col = int((cam_pos[0] + surf.get_width()) // self.tile_size) + 1 if cam_pos[0] > 0 else surf.get_width() // self.tile_size

        col_num = end_col - start_col
        row_num = end_row - start_row

        start_index = start_row * layers[0]["width"] + start_col
        end_index = min(start_index + col_num, start_index + layers[0]["width"] - start_col)

        for layer in layers:
            areas.append({
                "data": [layer["data"][start_index + i * layer["width"] : end_index + i * layer["width"]] for i in range(row_num)],
                "name": layer["name"],
                "visible": layer["visible"],
                })

        return areas, [start_col, start_row]


    def draw_level(self, surf, cam_pos, offset, layers):
        for layer in layers:
            if layer["visible"]:
                for y in range(0, len(layer['data'])):
                    for x in range(0, len(layer['data'][y])):
                        tile = layer['data'][y][x]
                        if tile != 0:
                            surf.blit(self.images_dict[tile], (x * self.tile_size, y * self.tile_size) - cam_pos + [offset[0] * self.tile_size, offset[1] * self.tile_size])


