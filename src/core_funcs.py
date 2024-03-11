from settings import *


def clip_img(surf, x: int, y: int, width: int, height: int):
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())


def get_file_names(dir_path: str):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            files.append(path.split("/")[-1])
    return files


def get_dir_names(dir_path: str):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, path)):
            files.append(path)
    return sorted(files)


def load_images(path: str):
    img_names = get_file_names(path)
    images = {}

    for name in img_names:
        img_path = path + "/" + name
        img = pg.image.load(img_path).convert()
        img.set_colorkey((0, 0, 0))
        images[name.split(".")[0]] = img

    return images


def make_tileset_dict(tileset_path: str, tile_size: int):
    tileset = {}
    tileset_img = pg.image.load(tileset_path).convert()
    for y in range(0, tileset_img.get_height(), tile_size):
        for x in range(0, tileset_img.get_width(), tile_size):
            img = clip_img(tileset_img, x, y, tile_size, tile_size)

            if check_if_sprite_is_not_transparent(img):
                tileset[y * tileset_img.get_width()//tile_size + x] = img
    
    return tileset


def check_if_sprite_is_not_transparent(surface: pg.Surface):
    for y in range(0, surface.get_height()):
        for x in range(0, surface.get_width()):
            if surface.get_at((x, y))[3] > 0:
                return True
    return False