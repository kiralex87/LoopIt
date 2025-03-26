from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def generate_circular_route(lat, lon, radius_km, points=36):
    route = []
    radius_deg = radius_km / 111.32
    for i in range(points):
        angle = 2 * math.pi * i / points
        dx = radius_deg * math.cos(angle)
        dy = radius_deg * math.sin(angle)
        point = [lon + dx / math.cos(math.radians(lat)), lat + dy]
        route.append(point)
    route.append(route[0])
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": route
        },
        "properties": {}
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-route', methods=['POST'])
def generate_route():
    data = request.get_json()
    lat = float(data['start'][0])
    lon = float(data['start'][1])
    distance_km = float(data['distance'])
    route = generate_circular_route(lat, lon, distance_km / 2)
    return jsonify({'route': route})

if __name__ == '__main__':
    app.run(debug=True)