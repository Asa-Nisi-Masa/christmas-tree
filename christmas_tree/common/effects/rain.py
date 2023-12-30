import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect, random_color


@effect(name="Rain")
def rain(pixels, coords):
    xr1, zr1 = np.random.uniform(-0.5, 0.5, 2)
    xr2, zr2 = np.random.uniform(-0.5, 0.5, 2)
    xr3, zr3 = np.random.uniform(-0.5, 0.5, 2)

    yr1 = np.random.uniform(1, 2)
    yr2 = np.random.uniform(1, 2)
    yr3 = np.random.uniform(1, 2)

    color = random_color()

    size = 0.15
    decay = 1.5
    v = 0.1

    while True:
        for i in coords:
            x, y, z = coords[i]

            dist2_1 = (x - xr1) ** 2 + (y - yr1) ** 2 + (z - zr1) ** 2
            dist2_2 = (x - xr2) ** 2 + (y - yr2) ** 2 + (z - zr2) ** 2
            dist2_3 = (x - xr3) ** 2 + (y - yr3) ** 2 + (z - zr3) ** 2
            if dist2_1 < size**2:
                pixels[i] = color
            elif dist2_2 < size**2:
                pixels[i] = color
            elif dist2_3 < size**2:
                pixels[i] = color
            else:
                pixels[i] = decayed_color(pixels[i], decay)

        yr1 -= v
        yr2 -= v
        yr3 -= v

        if yr1 < -1:
            xr1, zr1 = np.random.uniform(-0.5, 0.5, 2)
            yr1 = np.random.uniform(1, 2)
        if yr2 < -1:
            xr2, zr2 = np.random.uniform(-0.5, 0.5, 2)
            yr2 = np.random.uniform(1, 2)
        if yr3 < -1:
            xr3, zr3 = np.random.uniform(-0.5, 0.5, 2)
            yr3 = np.random.uniform(1, 2)

        pixels.show()
        time.sleep(0.01)
