import board
import neopixel
from flask import Flask, jsonify, render_template, request

from christmas_tree.common import effect_registry
from christmas_tree.common.settings import PATH_SAVE, TOTAL_LEDS
from christmas_tree.common.utils import load_coordinates
from christmas_tree.rpi.light_show import LightShow

pixels = neopixel.NeoPixel(board.D21, TOTAL_LEDS, auto_write=False, pixel_order=neopixel.RGB, brightness=0.5)

pixels.fill((0, 0, 0))
pixels.show()

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
    pixels.fill((255, 255, 255))
    pixels.show()

    return "", 204


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
