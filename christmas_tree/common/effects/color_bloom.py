import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect, random_color


@effect(name="Color Bloom")
def color_bloom(pixels, coords):
    bloom_center = np.random.uniform(-1, 1, 3)
    bloom_color = random_color()
    max_radius = 1.5
    expansion_speed = 0.075
    decay = 1.05

    bloom_radius = 0.0
    while True:
        for i in coords:
            pixels[i] = decayed_color(pixels[i], decay)

        for i in coords:
            x, y, z = coords[i]
            dist = np.linalg.norm(np.array([x, y, z]) - bloom_center)

            if dist < bloom_radius:
                brightness = max(0, 255 * (1 - dist / bloom_radius))
                pixels[i] = tuple(int(c * (brightness / 255)) for c in bloom_color)

        bloom_radius += expansion_speed
        if bloom_radius > max_radius:
            bloom_center = np.random.uniform(-1, 1, 3)
            bloom_color = random_color()
            bloom_radius = 0.0

        pixels.show()
        time.sleep(0.01)
