import time

import numpy as np

from christmas_tree.common.utils import decayed_color, effect, mix


@effect(name="XZ rotation")
def xz_rotation(pixels, coords):
    def _resolve_color(angle, theta1, theta2, old_color):
        decay = 1.5

        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        theta_mod = theta1 % (2 * np.pi)

        if theta_mod < np.pi / 3:
            u = theta_mod / (np.pi / 3)
            color = mix(red, green, u)
        elif theta_mod < 2 * np.pi / 3:
            u = (theta_mod - np.pi / 3) / (np.pi / 3)
            color = mix(green, blue, u)
        else:
            u = (theta_mod - 2 * np.pi / 3) / (4 * np.pi / 3)
            color = mix(blue, red, u)

        if angle < theta2 and angle > theta1:
            return color

        if theta2 > theta1:
            return decayed_color(old_color, decay)

        if (angle > theta1 and angle < 2 * np.pi) or (angle < theta2 and angle > 0):
            return color

        return decayed_color(old_color, decay)

    w = 1
    start = time.time()
    while True:
        t = time.time() - start

        theta1 = (w * t) % 2 * np.pi
        theta2 = (w * t + np.pi / 6) % 2 * np.pi

        for i in coords:
            x, y, z = coords[i]
            angle = np.arctan2(z, x)

            if z < 0:
                angle = 2 * np.pi + angle

            pixels[i] = _resolve_color(angle, theta1, theta2, pixels[i])

        pixels.show()
        time.sleep(0.01)
