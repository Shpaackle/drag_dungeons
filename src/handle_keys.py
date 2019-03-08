from bearlibterminal import terminal

from map_objects import Point


def handle_keys(key):
    # if key is None:
    #     if terminal.has_input():
    #         key = terminal.read()

        if key == terminal.TK_H or key == terminal.TK_KP_4 or key == terminal.TK_LEFT:
            return {"move": Point(-1, 0)}
        elif key == terminal.TK_L or key == terminal.TK_KP_6 or key == terminal.TK_RIGHT:
            return {"move": Point(1, 0)}
        elif key == terminal.TK_K or key == terminal.TK_KP_8 or key == terminal.TK_UP:
            return {"move": Point(0, -1)}
        elif key == terminal.TK_J or key == terminal.TK_KP_2 or key == terminal.TK_DOWN:
            return {"move": Point(0, 1)}
        elif key == terminal.TK_Y or key == terminal.TK_KP_7:
            return {"move": Point(-1, -1)}
        elif key == terminal.TK_U or key == terminal.TK_KP_9:
            return {"move": Point(1, -1)}
        elif key == terminal.TK_B or key == terminal.TK_KP_1:
            return {"move": Point(-1, 1)}
        elif key == terminal.TK_N or key == terminal.TK_KP_3:
            return {"move": Point(1, 1)}
        elif key == terminal.TK_PERIOD or key == terminal.TK_KP_0 or key == terminal.TK_KP_PERIOD:
            return {"move": Point(0, 0)}
        elif key == terminal.TK_ESCAPE or key == terminal.TK_CLOSE:
            return {"exit": True}

        return {}
