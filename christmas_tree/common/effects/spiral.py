import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect, random_color


@effect(name="Spiral")
def spiral(pixels, coords):
    decay = 1.2
    theta = 0.4
    width = 0.25
    radius = 0.7
    color = random_color()

    vec = np.random.uniform(-1, 1, 2)
    vec = vec / np.linalg.norm(vec)
    R = np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)],
        ]
    )

    start = time.time()
    while True:
        t = time.time() - start

        height = 0.5 * np.sin(1 * t) - 0.1
        vec = R.dot(vec) / np.linalg.norm(vec)
        vec = radius * vec
        for i in coords:
            x, y, z = coords[i]
            v = np.array([x, y, z])

            vec2 = np.array([vec[0], height, vec[1]])
            if np.abs(np.linalg.norm(vec2 - v)) < width:
                pixels[i] = color
            else:
                pixels[i] = decayed_color(pixels[i], decay)

        pixels.show()
        time.sleep(0.01)
