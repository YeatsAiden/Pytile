from settings import *
from load_levels import *
from ui import Font, Button

pg.init()

window = pg.display.set_mode(WINDOW_SIZE, FLAGS)
display = pg.Surface(DISPLAY_SIZE)
clock = pg.time.Clock()

pg.mouse.set_visible(MOUSE_VISIBLE)

current_dir = os.getcwd()
paths = {
    "tilesets_path": current_dir + "/assets/tilesets",
    "levels_path": current_dir + "/assets/levels",
    "fonts_path": current_dir + "/assets/fonts",
    "buttons_path": current_dir + "/assets/buttons",
    "cursors_path": current_dir + "/assets/cursor",
}

smol_font = Font(paths["fonts_path"] + "/" + "smol_font.png", [1, 2, 3], 1)

new_layer = Button(paths["buttons_path"] + "/" + "new_layer.png", display.get_width() - 36, 4)
next_layer = Button(paths["buttons_path"] + "/" + "next_layer.png")
prev_layer = Button(paths["buttons_path"] + "/" + "prev_layer.png")

cursor_image = pg.image.load(paths["cursors_path"] + "/" + "cursor.png").convert_alpha()

tile_sets = {file.split('.')[0]: make_tileset_dict(paths['tilesets_path'] + "/" + file, TILE_SIZE) for file in get_file_names(paths['tilesets_path'])}
level_loader = Load_levels(tile_sets, paths["levels_path"], TILE_SIZE)

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
    width_ratio = parent_surf.get_width() / child_surf.get_width()
    height_ratio = parent_surf.get_height() / child_surf.get_height()
    scale = min(width_ratio, height_ratio)
    # Changes child_surf size to a new size using scale variable.
    surf = pg.transform.scale(child_surf, (scale * child_surf.get_width(), scale * child_surf.get_height()))
    # This returns the values for centering the scalled surface
    xy_change = [(parent_surf.get_width() - surf.get_width()) // 2, (parent_surf.get_height() - surf.get_height()) // 2]

    return surf, xy_change, scale


scroll = pg.Vector2(0, 0)

xy_change = [0, 0]

scale = 1
# distance needed to make the display be in the center of the window
window_pos = pg.Vector2(-window.get_width()/2, -window.get_height()/2)
# Camera position

while True:
    display.fill("black")

    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x = (mouse_x - xy_change[0])/scale
    mouse_y = (mouse_y - xy_change[1])/scale

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()

    window_pos.y -= keys_pressed[pg.K_UP] * 5
    window_pos.y += keys_pressed[pg.K_DOWN] * 5
    window_pos.x += keys_pressed[pg.K_RIGHT] * 5
    window_pos.x -= keys_pressed[pg.K_LEFT] * 5

    scroll.x += (window_pos.x - scroll.x)/5
    scroll.y += (window_pos.y - scroll.y)/5

    if mouse_pressed[0]:
        level_map["layers"][current_layer]["data"][f"{int(mouse_x + window_pos.x)//TILE_SIZE}:{int(mouse_y + window_pos.y)//TILE_SIZE}"] = {
            "type": type,
            "tile_set": tile_set,
            "tile_id": tile_id
        }

    for y in range(int(window_pos.y)//TILE_SIZE, (int(window_pos.y) + display.get_height())//TILE_SIZE + 1):
        pg.draw.line(display, (50, 50, 50), (0, y * TILE_SIZE - scroll.y), (display.get_width(), y * TILE_SIZE - scroll.y), 2)
    
    for x in range(int(window_pos.x)//TILE_SIZE, (int(window_pos.x) + display.get_width())//TILE_SIZE + 1):
        pg.draw.line(display, (50, 50, 50), (x * TILE_SIZE - scroll.x, 0), (x * TILE_SIZE - scroll.x, display.get_height()), 2)

    pg.draw.line(display, (80, 80, 200), (0, 0 - scroll.y), (display.get_width(), 0 - scroll.y), 2)
    pg.draw.line(display, (200, 80, 80), (0 - scroll.x, 0), (0 - scroll.x, display.get_height()), 2)

    level_loader.draw_level(display, level_map, scroll)

    prev_layer.set_position(DISPLAY_WIDTH/2 - len(str(current_layer)) * 6 - 38, DISPLAY_HEIGHT - 36)
    prev_layer.draw(display)

    next_layer.set_position(DISPLAY_WIDTH/2 + len(str(current_layer)) * 6 + 6, DISPLAY_HEIGHT - 36)
    next_layer.draw(display)

    new_layer.draw(display)

    smol_font.draw_text(display, str(current_layer), DISPLAY_WIDTH/2 - len(str(current_layer)) * 6, 360, 1, 3)

    display.blit(cursor_image, [mouse_x, mouse_y])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F11:
                FULL_SCREEN = not FULL_SCREEN
                pg.display.set_mode((0, 0), FLAGS | pg.FULLSCREEN) if FULL_SCREEN else pg.display.set_mode(WINDOW_SIZE, FLAGS)

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
    display_cp, xy_change, scale = resize_surface(window, display)
    window.blit(display_cp, xy_change)

    pg.display.update()
    dt = clock.tick(FPS) / 1000