import time

import numpy as np

from christmas_tree.common.utils import effect, random_color


@effect(name="Simple blinking")
def simple_blinking(pixels, coords):
    w = np.random.uniform(0.5, 1.5)
    color = random_color()

    start = time.time()
    while True:
        t = time.time() - start
        weight_sin = np.clip(np.sin(w * (t - np.pi / (2 * w))), 0, 1)
        weight_cos = np.clip(np.cos(w * t), 0, 1)

        color_sin = tuple(map(lambda c: int(weight_sin * c),  color))
        color_cos = tuple(map(lambda c: int(weight_cos * c),  color))

        for i in coords:
            if i % 2 == 0:
                pixels[i] = color_sin
            else:
                pixels[i] = color_cos

        pixels.show()
        time.sleep(0.01)
