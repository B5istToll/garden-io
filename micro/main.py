from flask import Flask
from flask import json
from flask import jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/plants')
def get_plants():
    # Load the plant data
    with open('data/plants.json') as f:
        plant_data = json.load(f)

    return jsonify(plant_data)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6677)
