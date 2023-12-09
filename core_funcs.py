from settings import *


def clip_img(surf, x, y, width, height):
    # It makes clips of all your FAILURES >:]
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())


def get_file_names(dir_path):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            files.append(path.split("/")[-1])
    return files


def get_dir_names(dir_path):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, path)):
            files.append(path)
    return sorted(files)


# Event loop decorator function
def event_loop(func):
    def wrapper(events):
        for event in events:
            func(event)
    return wrapper


def load_images(path):
    img_names = get_file_names(path)
    images = {}

    for name in img_names:
        img_path = path + "/" + name
        img = pg.image.load(img_path).convert()
        img.set_colorkey((0, 0, 0))
        images[name.split(".")[0]] = img

    return images