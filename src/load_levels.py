from settings import *
from core_funcs import *


class Load_levels:
    def __init__(self, tile_sets: dict, levels_dir: str, tile_size: int) -> None:
        self.levels = {}

        for path in get_file_names(levels_dir):
            with open(levels_dir + '/' + path) as f:
                level_json_data = json.load(f)
                self.levels[path.split(".")[0]] = level_json_data

        self.tile_size = tile_size
        self.tile_sets = tile_sets

        self.rects = self.make_rects_dict(self.levels)


    def make_rects_dict(self, levels: dict):
        rects = {}
        for level in levels:
            for layer in levels[level]["layers"]:
                rects[level] = {
                    "layers": {
                        layer: []
                    }
                }
                for tile in levels[level]["layers"][layer]["data"]:
                    if levels[level]["layers"][layer]["data"][tile]["type"]:
                        x, y = map(int, tile.split(":"))
                        rect = pg.Rect(x, y, self.tile_size, self.tile_size)
                        rects[level]["layers"][layer].append(rect)
        return rects


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


    def draw_level(self, surf: pg.Surface, level: dict, scroll: pg.Vector2):
        for layer in level["layers"]:
            for tile in level["layers"][layer]["data"]:
                x, y = map(int, tile.split(":"))
                surf.blit(self.tile_sets[level["layers"][layer]["data"][tile]["tile_set"]][level["layers"][layer]["data"][tile]["tile_id"]], (x * self.tile_size - scroll.x, y * self.tile_size - scroll.y))


