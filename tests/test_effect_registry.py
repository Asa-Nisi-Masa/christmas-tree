from christmas_tree.common.effect_registry import EffectRegistry


def test_effect_registry_discovery():
    registry = EffectRegistry()

    effect_names = registry.get_display_names()
    assert len(effect_names) > 0, "Expected some effects to be discovered"

    # should be able to get each effect as a callable
    for effect_name in effect_names:
        effect_func = registry.get_effect(effect_name)
        assert callable(effect_func), f"Effect '{effect_name}' is not callable"
        assert hasattr(effect_func, "is_effect"), f"Effect '{effect_name}' missing is_effect attribute"
