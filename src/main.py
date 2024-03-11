from settings import *
from load_levels import *
from ui import Text

pg.init()

window = pg.display.set_mode(WINDOW_SIZE, FLAGS)
display = pg.Surface(DISPLAY_SIZE)
clock = pg.time.Clock()

current_dir = os.getcwd()
paths = {
    "tilesets_path": current_dir + "/assets/tilesets",
    "levels_path": current_dir + "/assets/levels",
    "fonts_path": current_dir + "/assets/fonts",
}

fps = 60

text = Text(paths["fonts_path"])

tile_size = 16
tile_sets = {file.split('.')[0]: make_tileset_dict(paths['tilesets_path'] + "/" + file, tile_size) for file in get_file_names(paths['tilesets_path'])}

level_loader = Load_levels(tile_sets, paths["levels_path"], tile_size)

level_map = {
    "height": 1,
    "width": 1,
    "layers": {
        0: {
            "height": 1,
            "width": 1,
            "data": {},
        }
    },
}
current_layer = 0
# layer that is being edited
tile_id = 0
# tile in use
tile_set = "rock"
# tile set in use
type = 1
# 1 means the tile will have collisions, whereas 0 means the tile will have no collisions


def resize_surface(parent_surf : pg.Surface, child_surf : pg.Surface):
    # Checks how the display should scale depending on the window size.
    scale = min(parent_surf.get_width() / child_surf.get_width(), parent_surf.get_height() / child_surf.get_height())
    # Changes child_surf size to a new size using scale variable.
    surf = pg.transform.scale(child_surf, (scale * child_surf.get_width(), scale * child_surf.get_height()))
    # This returns the values for centering the scalled surface
    xy_change = [round((parent_surf.get_width() - surf.get_width()) / 2), round((parent_surf.get_height() - surf.get_height()) / 2)]

    return surf, xy_change


full_screen = False

scroll = pg.Vector2(0, 0)

scale = 0
xy_change = [0, 0]

window_pos = pg.Vector2(-window.get_width()/2, -window.get_height()/2)
# Camera position

while True:
    display.fill("black")

    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x += int(window_pos.x) - xy_change[0]
    mouse_y += int(window_pos.y) - xy_change[1]

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()

    window_pos.y -= keys_pressed[pg.K_UP] * 5
    window_pos.y += keys_pressed[pg.K_DOWN] * 5
    window_pos.x += keys_pressed[pg.K_RIGHT] * 5
    window_pos.x -= keys_pressed[pg.K_LEFT] * 5

    scroll.x += (window_pos.x - scroll.x)/5
    scroll.y += (window_pos.y - scroll.y)/5

    if mouse_pressed[0]:
        level_map["layers"][current_layer]["data"][f"{mouse_x//tile_size}:{mouse_y//tile_size}"] = {
            "type": type,
            "tile_set": tile_set,
            "tile_id": tile_id
        }

    for y in range(int(window_pos.y)//tile_size, (int(window_pos.y) + display.get_height())//tile_size + 1):
        pg.draw.line(display, (50, 50, 50), (0, y * tile_size - scroll.y), (display.get_width(), y * tile_size - scroll.y), 2)
    
    for x in range(int(window_pos.x)//tile_size, (int(window_pos.x) + display.get_width())//tile_size + 1):
        pg.draw.line(display, (50, 50, 50), (x * tile_size - scroll.x, 0), (x * tile_size - scroll.x, display.get_height()), 2)

    pg.draw.line(display, (80, 80, 200), (0, 0 - scroll.y), (display.get_width(), 0 - scroll.y), 2)
    pg.draw.line(display, (200, 80, 80), (0 - scroll.x, 0), (0 - scroll.x, display.get_height()), 2)

    level_loader.draw_level(display, level_map, scroll)

    text.draw_text(display, "hello world", "smol_font", 0 - scroll.x, 0 - scroll.y, 2, 5)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F11:
                full_screen = not full_screen
                pg.display.set_mode((0, 0), FLAGS | pg.FULLSCREEN) if full_screen else pg.display.set_mode(WINDOW_SIZE, FLAGS)

            if event.key == pg.K_n:
                level_map["layers"][len(level_map["layers"])] = {
                    "height": 1,
                    "width": 1,
                    "data": {},
                }

            if event.key == pg.K_s:
                with open(paths["levels_path"] + "/" + "level.json", "w") as f: 
                    json.dump(level_map, f)

            if event.key == pg.K_d:
                current_layer += 1
            if event.key == pg.K_a:
                current_layer -= 1

            current_layer = max(0, min(len(level_map["layers"]) - 1, current_layer))
                
    # Resizing display to window size
    display, xy_change = resize_surface(window, display)
    window.blit(display, xy_change)

    pg.display.update()
    dt = clock.tick(fps) / 1000