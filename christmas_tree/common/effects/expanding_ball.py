import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect


@effect(name="Expanding sphere")
def expanding_ball(pixels, coords):
    color = np.random.randint(0, 256, 3)
    decay = 1.05
    start = time.time()
    while True:
        t = time.time() - start
        radius = np.abs(np.sin(t))

        for i in coords:
            x, y, z = coords[i]
            if x**2 + y**2 + z**2 <= radius**2:
                pixels[i] = tuple(color)
            else:
                pixels[i] = decayed_color(pixels[i], decay)

        pixels.show()
        time.sleep(0.01)
