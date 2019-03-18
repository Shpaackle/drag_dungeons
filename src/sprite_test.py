# coding=utf-8

from bearlibterminal import terminal as blt


width = 2048
height = 3040


def main():
    blt.set("0xE000: data/ProjectUtumno_full.png, size=32x32")
    blt.set("font: data/mplus-1p-regular.ttf, size=32x32")

    blt.put(0, 0, "\uE002")

    hoffset = 0
    num_tiles = (width//32) * (height//32)

    blt.refresh()
    page = 0

    while True:
        blt.clear()
        blt.color("white")

        for j in range(16):
            blt.puts(hoffset+6+j*2, 1, "[color=orange]%X" % j)

        y = 0
        for i in range(0, 256):
            code = chr(ord("\uE000") + (page * 256) + i)
            if i % 16 == 0:
                blt.puts(hoffset, 2 + y * 1, " [color=orange]%04X" % ord(code))

            blt.put(hoffset + 6 + (i % 16) * 2, 2 + y * 1, code)

            if (i + 1) % 16 == 0: y += 1

        blt.put(19, 0, "\uE00F")

        blt.refresh()

        key = blt.read()

        if key in (blt.TK_CLOSE, blt.TK_ESCAPE):
            break
        elif key == blt.TK_UP and page < 23:
            page += 1
        elif key == blt.TK_DOWN and page > 0:
            page -= 1


if __name__ == '__main__':
    blt.open()
    blt.set("window: size=80x50, cellsize=auto")
    blt.color("white")
    main()
    blt.close()
