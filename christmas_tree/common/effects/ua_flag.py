from christmas_tree.common.utils import block_execution, effect


@effect(name="UA flag")
def ua_flag(pixels, coords):
    for i in coords:
        x, y, z = coords[i]
        if y >= 0:
            pixels[i] = (0, 87, 183)
        else:
            pixels[i] = (255, 221, 0)

    pixels.show()
    block_execution()
