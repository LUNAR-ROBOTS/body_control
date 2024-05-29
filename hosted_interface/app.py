from flask import Flask, render_template, request, jsonify, send_file, Response
from picamera2 import Picamera2
import time
import cv2
import threading
import gpiozero

app = Flask(__name__)
picam2 = Picamera2()
streaming = False

def flicker_led():
    led = gpiozero.LED(17)
    for _ in range(5):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)

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
    threading.Thread(target=flicker_led).start()
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
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()
    time.sleep(2)  # Give some time for the camera to adjust
    picam2.capture_file(file_path)
    picam2.stop()
    return send_file(file_path, mimetype='image/jpeg')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    global streaming
    if not streaming:
        streaming = True
        threading.Thread(target=stream_video).start()
    return jsonify({"status": "streaming started"})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global streaming
    streaming = False
    return jsonify({"status": "streaming stopped"})

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream_video():
    global streaming
    config = picam2.create_video_configuration()
    picam2.configure(config)
    picam2.start()
    while streaming:
        time.sleep(1)
    picam2.stop()

def generate_video_stream():
    global streaming
    while streaming:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)