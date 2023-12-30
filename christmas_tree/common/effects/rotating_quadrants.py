import time

import numpy as np

from christmas_tree.common.utils import effect


@effect(name="Rotating quadrants")
def rotating_quadrants(pixels, coords):
    colors = {
        0: (128, 0, 0),
        1: (0, 128, 0),
        2: (0, 0, 128),
        3: (128, 128, 0),
    }

    w = 1.5
    start = time.time()
    while True:
        t = time.time() - start
        rotation_angle = w * t

        for i in coords:
            x, y, z = coords[i]

            angle = np.arctan2(y, x)
            adjusted_angle = (angle - rotation_angle) % (2 * np.pi)
            quadrant = int(4 * adjusted_angle / (2 * np.pi)) % 4

            pixels[i] = colors[quadrant]

        pixels.show()
        time.sleep(0.01)
