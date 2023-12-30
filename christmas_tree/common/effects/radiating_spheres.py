import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect, random_color


@effect(name="Radiating spheres")
def radiating_spheres(pixels, coords):
    decay = 1.01
    index = 0
    colors = (
        random_color(),
        random_color(),
    )

    start = time.time()
    while True:
        t = time.time() - start
        radius = np.abs(t / 3)

        for i in coords:
            x, y, z = coords[i]
            dist2 = x**2 + y**2 + z**2
            if dist2 <= radius**2:
                pixels[i] = tuple(colors[index])
            else:
                pixels[i] = decayed_color(pixels[i], decay)

        pixels.show()
        time.sleep(0.01)

        if radius > 1:
            start = time.time()
            index = (index + 1) % len(colors)
