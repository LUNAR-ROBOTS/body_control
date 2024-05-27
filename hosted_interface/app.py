from flask import Flask, render_template, request, jsonify, send_file
from picamera2 import Picamera2
import time

app = Flask(__name__)
picam2 = Picamera2()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action1', methods=['POST'])
def action1():
    print("Action 1 triggered!")
    return "Action 1 triggered!"

@app.route('/action2', methods=['POST'])
def action2():
    print("Action 2 triggered!")
    return "Action 2 triggered!"

@app.route('/action3', methods=['POST'])
def action3():
    print("Action 3 triggered!")
    return "Action 3 triggered!"

@app.route('/action4', methods=['POST'])
def action4():
    print("Action 4 triggered!")
    return "Action 4 triggered!"

@app.route('/joystick', methods=['POST'])
def joystick():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    print(f"Joystick moved to position: x={x}, y={y}")
    return jsonify({"status": "success", "x": x, "y": y})

@app.route('/take_picture', methods=['POST'])
def take_picture():
    file_path = '/tmp/picture.jpg'
    picam2.start_preview()
    time.sleep(2)  # Give some time for the camera to adjust
    picam2.capture_file(file_path)
    picam2.stop_preview()
    return send_file(file_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)