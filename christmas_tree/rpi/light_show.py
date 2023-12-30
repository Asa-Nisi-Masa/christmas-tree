import multiprocessing
import time
from typing import List

import numpy as np

from christmas_tree.common import effect_registry
from christmas_tree.common.utils import kill_child_processes


class LightShow:
    def __init__(self, pixels, coords):
        self._pixels = pixels
        self._coords = coords
        self._current_process = None

    def show_effects(self, effect_names: List[str]):
        kill_child_processes()

        self._pixels.fill((0, 0, 0))
        self._pixels.show()

        if len(effect_names) == 0:
            return
        elif len(effect_names) == 1:
            duration = float("inf")
        else:
            duration = 20

        parent_process = multiprocessing.Process(
            target=self._run_in_separate_proc, args=(effect_names, duration)
        )
        parent_process.start()

    def _show_single_effect(self, effect_name: str):
        effect = effect_registry.get_effect(effect_name)
        effect(self._pixels, self._coords)

    def _run_in_separate_proc(self, effect_names: List[str], duration: float):
        index = 0
        num_effects = len(effect_names)

        while True:
            # this propagates to the effects, otherwise all repeated runs of an effect will have the same internal seed
            np.random.seed(int(time.time()))

            ename = effect_names[index % num_effects]
            if self._current_process is not None and self._current_process.is_alive():
                self._current_process.terminate()
                self._current_process.join()

            self._current_process = multiprocessing.Process(target=self._show_single_effect, args=(ename,))
            self._current_process.start()

            self._current_process.join(timeout=duration)
            if self._current_process.is_alive():
                self._current_process.terminate()
                self._current_process.join()

            index += 1
