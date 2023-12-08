from settings import *

pg.init()

window = pg.display.set_mode(WINDOW_SIZE, FLAGS)
display = pg.Surface(DISPLAY_SIZE)

clock = pg.time.Clock()
fps = 60


def resize_surface(parent_surf : pg.Surface, child_surf : pg.Surface):
    # Checks how the display should scale depending on the window size.
    scale = min(parent_surf.get_width() / child_surf.get_width(), parent_surf.get_height() / child_surf.get_height())
    # Changes child_surf size to a new size using scale variable.
    surf = pg.transform.scale(child_surf, (scale * child_surf.get_width(), scale * child_surf.get_height()))
    # This returns the values for centering the scalled surface
    xy_change = [round((parent_surf.get_width() - surf.get_width()) / 2), round((parent_surf.get_height() - surf.get_height()) / 2)]

    return surf, xy_change


full_screen = False

while True:
    display.fill("black")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F11:
                full_screen = not full_screen
                pg.display.set_mode((0, 0), FLAGS | pg.FULLSCREEN) if full_screen else pg.display.set_mode(WINDOW_SIZE, FLAGS)
                
    # Resizing display to window size
    display, xy_change = resize_surface(window, display)
    window.blit(display, xy_change)

    pg.display.update()
    dt = clock.tick(fps) / 1000