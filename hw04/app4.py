#!/usr/bin/env python3
import gpiod
from flask import Flask, render_template, request

app = Flask(__name__)

# Define sensors GPIOs
button_offsets = [14, 15, 12, 13]  # GPIO pins for buttons

# Define actuators GPIOs
led_offsets = [18, 28]  # GPIO pins for LEDs

CHIP = '1'

# Initialize GPIO for buttons
chip = gpiod.Chip(CHIP)
button_lines = chip.get_lines(button_offsets)
button_lines.request(consumer="app4.py", type=gpiod.LINE_REQ_DIR_IN)

# Initialize GPIO for LEDs
led_lines = chip.get_lines(led_offsets)
led_lines.request(consumer="app4.py", type=gpiod.LINE_REQ_DIR_OUT)

# Turn LEDs OFF 
led_lines.set_values([0, 0])

@app.route("/")
def index():
    # Read GPIO Status for buttons
    button_values = button_lines.get_values()
    templateData = {
        'button1': button_values[0],
        'button2': button_values[1],
        'button3': button_values[2],
        'button4': button_values[3],
        'ledRed': led_lines.get_values()[0],
        'ledGreen': led_lines.get_values()[1]
    }
    return render_template('index3.html', **templateData)
    
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName in ["ledRed", "ledGreen"]:
        index = ["ledRed", "ledGreen"].index(deviceName)
        led_values = led_lines.get_values()
        if action == "on":
            led_values[index] = 1
        elif action == "off":
            led_values[index] = 0
        led_lines.set_values(led_values)

    setlines = button_lines.get_values()  # Use setlines for button values
    templateData = {
        'button1': setlines[0],
        'button2': setlines[1],
        'button3': setlines[2],
        'button4': setlines[3],
        'ledRed': led_lines.get_values()[0],
        'ledGreen': led_lines.get_values()[1]
    }
    return render_template('index3.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
