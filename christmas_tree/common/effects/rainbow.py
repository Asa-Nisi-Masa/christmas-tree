from christmas_tree.common.utils import block_execution, effect


@effect(name="Rainbow")
def rainbow(pixels, coords):
    colors = [
        (148, 0, 211),
        (75, 0, 130),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 127, 0),
        (255, 0, 0),
    ]
    dy = 2 / len(colors)
    buckets = [1]
    for i in range(len(colors)):
        buckets.append(buckets[i] - dy)

    for i in coords:
        x, y, z = coords[i]
        color = (0, 0, 0)
        for j in range(len(buckets) - 1):
            if y <= buckets[j] and y > buckets[j + 1]:
                color = colors[j]
                break
        pixels[i] = color

    pixels.show()
    block_execution()
