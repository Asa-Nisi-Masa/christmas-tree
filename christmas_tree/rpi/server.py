import sys
from pathlib import Path

import board
import neopixel
from flask import Flask, jsonify, render_template, request

from christmas_tree.common import effect_registry
from christmas_tree.common.settings import (
    GPIO_PIN,
    PATH_SAVE,
    PIXEL_BRIGHTNESS,
    TOTAL_LEDS,
)
from christmas_tree.common.utils import load_coordinates
from christmas_tree.rpi.light_show import LightShow

pixels = neopixel.NeoPixel(
    getattr(board, GPIO_PIN),
    TOTAL_LEDS,
    auto_write=False,
    pixel_order=neopixel.RGB,
    brightness=PIXEL_BRIGHTNESS,
)

pixels.fill((0, 0, 0))
pixels.show()

if not Path(PATH_SAVE).exists():
    print(f"Couldn't find {PATH_SAVE} - server will be started for the initial coordinate capturing")
else:
    coords = load_coordinates(PATH_SAVE)
    light_show = LightShow(pixels, coords)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", effects=effect_registry.get_display_names())


@app.route("/ping")
def ping():
    return "pong"


@app.route("/process", methods=["POST"])
def process_data():
    selected_effects = request.json.get("selected_effects", [])
    light_show.show_effects(selected_effects)

    return jsonify({"message": "Received!"})


@app.route("/fire/<int:led_id>", methods=["POST", "DELETE"])
def control(led_id):
    if request.method == "POST":
        pixels[led_id] = (84, 84, 84)
        pixels.show()

        return "", 204

    if request.method == "DELETE":
        pixels[led_id] = (0, 0, 0)
        pixels.show()

        return "", 204


@app.route("/clear", methods=["DELETE"])
def clear():
    pixels.fill((0, 0, 0))
    pixels.show()
    return "", 204


@app.route("/fill", methods=["POST"])
def fill():
    pixels.fill((16, 16, 16))
    pixels.show()

    return "", 204


if __name__ == "__main__":
    try:
        app.run("0.0.0.0", port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
