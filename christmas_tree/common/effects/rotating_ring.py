import time

import numpy as np

from christmas_tree.common.utils import effect, random_color


@effect(name="Rotating ring")
def rotating_ring(pixels, coords):
    width = 0.07
    theta = 0.08
    color = random_color()

    if np.random.uniform() > 0.5:
        axis = np.array([0.9, -0.7, -0.7])
    else:
        axis = np.array([0.15, -0.37, -0.37])

    axis = axis / np.linalg.norm(axis)

    def Rx(theta):
        return np.array(
            [
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)],
            ]
        )

    def Ry(theta):
        return np.array(
            [
                [np.cos(theta), 0, -np.sin(theta)],
                [0, 1, 0],
                [np.sin(theta), 0, np.cos(theta)],
            ]
        )

    def Rz(theta):
        return np.array(
            [
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1],
            ]
        )

    rx = Rx(theta)
    ry = Ry(theta)
    rz = Rz(theta)

    while True:
        axis = rz.dot(ry.dot(rx.dot(axis)))
        for i in coords:
            x, y, z = coords[i]
            dot = np.array([x, y, z]).dot(axis)

            if abs(dot) < width:
                pixels[i] = color
            else:
                pixels[i] = (0, 0, 0)

        pixels.show()
        time.sleep(0.01)
