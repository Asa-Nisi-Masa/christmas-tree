import board
import neopixel
import time
import numpy as np

from christmas_tree.common.utils import load_coordinates, effect, mix, decayed_color, random_color
from christmas_tree.common.effects.spiral import spiral

pixels = neopixel.NeoPixel(board.D21, 500, auto_write=False, pixel_order=neopixel.RGB, brightness=0.2)

coords = load_coordinates("coordinates.csv")


pixels.fill((0, 0, 0))
pixels.show()
try:
    spiral(pixels, coords)
except KeyboardInterrupt:
    pass
finally:
    pixels.fill((0, 0, 0))
    pixels.show()
