import time

import numpy as np

from christmas_tree.common.utils import effect, mix


@effect(name="Colored wave")
def colored_wave(pixels, coords):
    v = 0.5
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    wave_p_start = np.array([-1, -1, 0])
    wave_p_start = wave_p_start / np.linalg.norm(wave_p_start)

    start = time.time()
    while True:
        t = time.time() - start
        for i in coords:
            x, y, z = coords[i]
            r = np.array([x, y, z]) + 1e-5

            F = np.sin(0.3 * 2 * np.pi * (r.dot(wave_p_start) - v * t))

            if F < -1 / 3:
                u = F * 1.5 + 1.5
                color = mix(red, green, u)
            elif F < 1 / 3:
                u = F * 1.5 + 0.5
                color = mix(green, blue, u)
            else:
                u = F * 1.5 - 0.5
                color = mix(blue, red, u)

            pixels[i] = color

        pixels.show()
        time.sleep(0.001)
