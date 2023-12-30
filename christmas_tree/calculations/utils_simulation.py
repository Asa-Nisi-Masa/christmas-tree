from pythreejs import (
    AmbientLight,
    DirectionalLight,
    Mesh,
    MeshBasicMaterial,
    OrbitControls,
    PerspectiveCamera,
    Renderer,
    Scene,
    SphereBufferGeometry,
)


class NeoPixel(list):
    def __setitem__(self, index, new_value):
        material = super().__getitem__(index)
        material.color = self._to_color_hex(new_value)
        super().__setitem__(index, material)

    def _to_color_hex(self, color_rgb):
        return "#%02x%02x%02x" % color_rgb

    def _to_color_rgb(self, color_hex):
        return tuple(int(color_hex[i : i + 2], 16) for i in (0, 2, 4))

    def show(self):
        pass

    def fill(self, color_rgb):
        for i, material in enumerate(self):
            material.color = self._to_color_hex(color_rgb)
            super().__setitem__(i, material)

    def __getitem__(self, index):
        color_hex = super().__getitem__(index).color
        return self._to_color_rgb(color_hex.lstrip("#"))


def build_renderer_and_mats(coords):
    camera = PerspectiveCamera(position=[10, 6, 10], aspect=2)
    camera.lookAt([0, 0, 0])

    scene = Scene()
    controls = OrbitControls(controlling=camera)

    dir_light = DirectionalLight(color="white", position=[3, 5, 1], intensity=0.6)
    amb_light = AmbientLight(color="white", intensity=0.5)
    scene.add(dir_light)
    scene.add(amb_light)

    materials = NeoPixel()
    for index in coords:
        coord = coords[index]
        material = MeshBasicMaterial(color="#000000", opacity=0.5, transparent=True)
        materials.append(material)
        sphere = Mesh(SphereBufferGeometry(0.1), material)
        sphere.position = tuple(coord)
        scene.add(sphere)

    return Renderer(scene=scene, camera=camera, controls=[controls], width=800, height=400), materials
