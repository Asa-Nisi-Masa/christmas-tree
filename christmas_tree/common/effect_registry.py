import importlib
import pkgutil
from pathlib import Path
from typing import Callable, Dict, List


class EffectRegistry:
    def __init__(self):
        self._effects = self._collect_effects()

    def get_effect(self, name: str) -> Callable:
        return self._effects[name]

    def get_display_names(self) -> List[str]:
        return list(self._effects.keys())

    def _collect_effects(self) -> Dict[str, Callable]:
        effects = {}

        module_dir = Path(__file__).parent
        effects_path = module_dir / "effects"

        for _, module_name, _ in pkgutil.iter_modules([str(effects_path)]):
            module = importlib.import_module(f"christmas_tree.common.effects.{module_name}")
            for attr_name in dir(module):
                attribute = getattr(module, attr_name)

                if hasattr(attribute, "is_effect"):
                    # if name available for effect, register using that.
                    # Otherwise default to the function name
                    if attribute.name is not None:
                        effects[attribute.name] = attribute
                    else:
                        effects[attr_name] = attribute

        return effects
