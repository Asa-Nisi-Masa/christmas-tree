import time

from christmas_tree.common.utils import effect


@effect(name="Cyllinders")
def cyllinders(pixels, coords):
    colors = {
        0: (222, 49, 99),
        1: (0, 0, 139),
    }
    dr = 1 / len(colors)

    while True:
        for i in coords:
            x, y, z = coords[i]

            dist2 = x**2 + z**2

            for j, color in colors.items():
                if dist2 < ((j + 1) * dr) ** 2:
                    pixels[i] = color
                    break

        pixels.show()
        time.sleep(0.1)
