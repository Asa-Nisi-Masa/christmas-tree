import os
import signal
import time
from functools import wraps
from typing import Callable, Dict, Optional, Tuple
import numpy as np

import psutil


def decayed_color(color: Tuple[int], decay: float) -> Tuple[int]:
    return tuple(int(c / decay) for c in color)


def random_color() -> Tuple[int]:
    return tuple([
        np.random.randint(0, 256),
        np.random.randint(0, 256),
        # assigning 'blue' component a lower value
        # otherwise, at least in my case, there is a visual
        # bias towards whiteish-blueish colors
        np.random.randint(0, 128),
    ])


def mix(color1: Tuple[int], color2: Tuple[int], u: float) -> Tuple[int]:
    return (
        int((1 - u) * color1[0] + u * color2[0]),
        int((1 - u) * color1[1] + u * color2[1]),
        int((1 - u) * color1[2] + u * color2[2]),
    )


def effect(_func: Optional[Callable] = None, *, name: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        _wrapped.is_effect = True
        _wrapped.name = name
        return _wrapped

    if callable(_func):
        return decorator(_func)

    return decorator


def block_execution():
    # need to have a way toblock execution because
    # the effect's duration and its interruption
    # is handled from 'outside'
    time.sleep(10**6)


def load_coordinates(path: str) -> Dict[int, Tuple[float]]:
    with open(path, "r") as file:
        raw = file.read().split("\n")[:-1]

    coords = {}
    for line in raw:
        i, x, y, z = line.split(", ")
        i = int(i)
        x = float(x)
        y = float(y)
        z = float(z)

        coords[i] = (x, y, z)

    return coords


def kill_child_processes():
    process = psutil.Process()
    children = process.children(recursive=True)
    for child in children:
        os.kill(child.pid, signal.SIGKILL)
        time.sleep(0.1)
