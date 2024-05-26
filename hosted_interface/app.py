from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action1', methods=['POST'])
def action1():
    return "Action 1 triggered!"

@app.route('/action2', methods=['POST'])
def action2():
    return "Action 2 triggered!"

@app.route('/action3', methods=['POST'])
def action3():
    return "Action 3 triggered!"

@app.route('/action4', methods=['POST'])
def action4():
    return "Action 4 triggered!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)


