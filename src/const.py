from bearlibterminal import terminal


TITLE = "Drag Dungeons"

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

CAMERA_WIDTH = 31
CAMERA_HEIGHT = 21

FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

FONT_PATH = "data/consolas10x10.png"

MAP_SETTINGS = {
    "map_height": 31,
    "map_width": 51,
    "tile_size": 10,
    "num_rooms": 100,
    "min_room_size": 3,
    "max_room_size": 7,
    "room_margin": 1,
    "extra_door_chance": 30,
    "max_monsters_per_room": 3
}

COLORS = {
    "transparent",
    "none",
    "black",
    "white",
    "grey",
    "gray",
    "red",
    "flame",
    "orange",
    "amber",
    "yellow",
    "lime",
    "chartreuse",
    "green",
    "sea",
    "turquoise",
    "cyan",
    "sky",
    "azure",
    "blue",
    "han",
    "violet",
    "purple",
    "fuchsia",
    "magenta",
    "pink",
    "crimson",
    }


class Layers:
    BACKGROUND = 0
    MAP = 10
    PLAYER = 20
    LIGHT = 40
    TESTING = 50


class Tiles:
    UNSEEN = "\uE004"
    FLOOR = "\uE000"
    CORRIDOR = "\uE001"
    WALL = "\uE002"
    CONNECT = "\uE003"
    DOOR_CLOSED = "\uE005"
    BLOCK = "\u2588"
    DOOR_OPEN = "\uE006"
    GOBLIN = "\uE007"
    ORC = "\uE008"
    PLAYER = "\uE009"
