from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
from tqdm import tqdm

from christmas_tree.common.settings import PATH_SAVE, TOTAL_LEDS

### Adjust these three parameters if lots of LEDs cannot be detected
LOWER_THRESHOLD = 135
UPPER_THRESHOLD = 255
MAX_DIST = 40
###
ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]

Point = namedtuple("Point", ["x", "y"])

# get height and width of images from one of the frames
path = Path("frames") / str(ANGLES[0]) / "0.jpg"
frame = cv2.imread(str(path))
height, width, _ = frame.shape


def _get_uv(center: Point, width: int, height: int) -> Point:
    px, py = center

    u = 2 / width * px - 1
    v = -2 / height * py + 1

    return Point(u, v)


def _compute_naive_positions(image: np.ndarray) -> List[Point]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, LOWER_THRESHOLD, UPPER_THRESHOLD, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            centers.append(Point(cX, cY))

    return centers


def _compute_correct_positions(contour_centers: List[Point]) -> Optional[Point]:
    if len(contour_centers) == 0:
        return None

    if len(contour_centers) == 1:
        return contour_centers[0]

    min_dist = float("inf")
    for i in range(len(contour_centers)):
        for j in range(i, len(contour_centers)):
            if i == j:
                continue

            xi, yi = contour_centers[i]
            xj, yj = contour_centers[j]

            dist2 = (xi - xj) ** 2 + (yi - yj) ** 2

            if dist2 < min_dist:
                min_dist = dist2

    if min_dist < MAX_DIST**2:
        centers = np.array(contour_centers).mean(axis=0)
        return Point(int(centers[0]), int(centers[1]))

    return None


def _get_map_from_index_to_position(angle: int) -> Dict[int, Point]:
    map_index_to_position = {}

    total_errors = 0
    for i in range(TOTAL_LEDS):
        path = Path("frames") / str(angle) / f"{i}.jpg"
        frame = cv2.imread(str(path))
        contour_centers = _compute_naive_positions(frame)

        center = _compute_correct_positions(contour_centers)
        if center is None:
            total_errors += 1
            map_index_to_position[i] = None
        else:
            map_index_to_position[i] = _get_uv(center, width, height)

    return map_index_to_position


def get_map_index_to_angle_position() -> Dict[int, Dict[int, Point]]:
    # map_index_to_angle_position = map from LED index to a map from angle to LED position
    angles_to_centers = {}
    map_index_to_angle_position = defaultdict(dict)

    for angle in tqdm(ANGLES):
        map_index_to_position = _get_map_from_index_to_position(angle)
        angles_to_centers[angle] = map_index_to_position

        for i in range(TOTAL_LEDS):
            map_index_to_angle_position[i][angle] = map_index_to_position[i]

    return map_index_to_angle_position


def validate_led_positions(map_index_to_angle_position: Dict[int, Dict[int, Point]]) -> None:
    total_no_centers = 0
    for i in range(TOTAL_LEDS):
        num_angles_center_is_defined = sum(el is not None for el in map_index_to_angle_position[i].values())

        if num_angles_center_is_defined < 1:
            print(f"No center can be found for {i} LED")
            total_no_centers += 1

    print("Total no LED positions found:", total_no_centers)


def get_frames_to_xyz(map_index_to_angle_position: Dict[int, Dict[int, Point]]) -> Dict[int, tuple]:
    # frames_to_xyz = map from LED index to LED position
    frames_to_xyz = {}
    for i in range(TOTAL_LEDS):
        sum_x = 0
        sum_z = 0
        sum_y = 0

        non_nulls = 0
        for angle in ANGLES:
            radian = np.pi / 180 * angle
            center = map_index_to_angle_position[i][angle]
            if center is not None:
                sum_x += center.x * np.cos(radian)
                sum_z += center.x * np.sin(radian)
                sum_y += center.y

                non_nulls += 1

        if non_nulls > 0:
            x = 1 / non_nulls * sum_x
            z = 1 / non_nulls * sum_z
            y = 1 / non_nulls * sum_y

            frames_to_xyz[i] = (x, y, z)
        else:
            frames_to_xyz[i] = None

    return frames_to_xyz


def save_to_file(frames_to_xyz: Dict[int, tuple]):
    with open(PATH_SAVE, "w") as file:
        for i in range(TOTAL_LEDS):
            coordinates = frames_to_xyz[i]
            if coordinates is not None:
                x, y, z = coordinates
            line = f"{i}, {x*6}, {y}, {z*6}\n"
            file.write(line)


if __name__ == "__main__":
    map_index_to_angle_position = get_map_index_to_angle_position()
    validate_led_positions(map_index_to_angle_position)
    frames_to_xyz = get_frames_to_xyz(map_index_to_angle_position)
    save_to_file(frames_to_xyz)
