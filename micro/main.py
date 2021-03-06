import os
from os import unlink

from flask import Flask, Response
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
    if new == 1 or not os.path.exists(garden_path):
        if os.path.exists(garden_path):
            unlink(garden_path)
        garden_logic.create_garden(5, 4, garden_path)

    with open(garden_path) as f:
        garden_data = json.load(f)
    return jsonify(garden_data)


@app.route('/api/garden/update', methods=['POST'])
def update_status():
    payload = request.get_json(force=True)
    x = payload['location']['x']
    y = payload['location']['y']
    z = payload['location']['z']
    state = payload['state']

    garden = garden_logic.Garden()
    garden.update_state(x, y, z, state)
    garden.save()

    return Response(status=200)


@app.route('/api/garden/update_plant', methods=['POST'])
def update_plant():
    payload = request.get_json(force=True)
    x = payload['location']['x']
    y = payload['location']['y']
    z = payload['location']['z']
    plant = payload['plant']

    garden = garden_logic.Garden()
    garden.update_plant(x, y, z, plant)
    garden.add_suggestions()
    garden.save()

    return jsonify(garden.data['tiles'][x][y][z])


@app.route('/api/garden/events')
def get_events():
    date = request.args.get('date', '1970-01-01')
    garden = garden_logic.Garden()
    return jsonify(garden.generate_events(date))


@app.route('/api/forecast')
def get_weather_forecast():
    return jsonify({
        'weather': [
            {
                'sun_prob': 20,
                'rain_prob': 45
            },
            {
                'sun_prob': 10,
                'rain_prob': 50
            },
            {
                'sun_prob': 0,
                'rain_prob': 78
            },
            {
                'sun_prob': 0,
                'rain_prob': 80
            },
            {
                'sun_prob': 100,
                'rain_prob': 0
            },
        ]
    })


@app.after_request
def after_request(response):
    # Add Access control headers
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6677, debug=True)
