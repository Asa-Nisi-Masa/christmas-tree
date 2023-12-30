import time

import numpy as np

from christmas_tree.common.utils import effect


@effect(name="Rotating stripes")
def rotating_stripes(pixels, coords):
    navy = (0, 0, 128)
    white = (64, 64, 64)
    red = (128, 0, 0)

    colors = {
        0: navy,
        1: white,
        2: red,
    }

    num_colors = len(colors)

    w = 1
    start = time.time()
    while True:
        t = time.time() - start
        rotation_angle = w * t

        for i in coords:
            x, y, z = coords[i]

            angle = np.arctan2(z, x)
            adjusted_angle = (angle - rotation_angle) % (2 * np.pi)
            quadrant = int(num_colors * adjusted_angle / (2 * np.pi)) % num_colors

            pixels[i] = colors[quadrant]

        pixels.show()
        time.sleep(0.01)
