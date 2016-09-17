from os import unlink

from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from garden_logic import Plants
import garden_logic

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/plants')
def get_plants():
    plants = Plants()
    return jsonify(plants.data)


@app.route('/api/garden')
def get_garden():
    garden_path = './garden.json'

    new = int(request.args.get('new', 0))
    print(new)
    if new == 1:
        print('here')
        unlink(garden_path)
        garden_logic.create_garden(5, 4, garden_path)

    with open(garden_path) as f:
        garden_data = json.load(f)
    return jsonify(garden_data)


@app.after_request
def after_request(response):
    # Add Access control headers
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6677, debug=True)
