from settings import *
from core_funcs import *


class Load_levels:
    def __init__(self, tile_sets, levels_dir, tile_size) -> None:
        self.levels = {}
        for path in get_file_names(levels_dir):
            with open(levels_dir + '/' + path) as f:
                level_json_data = json.load(f)
                self.levels[path.split(".")[0]] = level_json_data

        self.tile_size = tile_size
        self.tile_sets = tile_sets


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


