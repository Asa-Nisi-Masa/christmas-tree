import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect


@effect(name="Planar wave")
def planar_wave(pixels, coords):
    def _construct_wave():
        wave_p_start = np.random.randn(3)
        wave_p_start = wave_p_start / np.linalg.norm(wave_p_start)
        dp = -0.05 * wave_p_start

        return wave_p_start, dp

    decay = 1.5
    wave_width = 0.05

    wave_p_start, dp = _construct_wave()
    wave_p = wave_p_start.copy()
    color = tuple(np.random.randint(0, 256, 3))

    while True:
        wave_p_norm = np.linalg.norm(wave_p)
        for i in coords:
            x, y, z = coords[i]
            r = np.array([x, y, z])
            proj_r_onto_p = wave_p.dot(r) / wave_p_norm

            if abs(proj_r_onto_p - wave_p_norm) <= wave_width:
                pixels[i] = color
            else:
                pixels[i] = decayed_color(pixels[i], decay)

        pixels.show()
        wave_p += dp
        time.sleep(0.01)

        if np.linalg.norm(wave_p - wave_p_start) > 2:
            wave_p_start, dp = _construct_wave()
            wave_p = wave_p_start.copy()
            color = tuple(np.random.randint(0, 256, 3))
