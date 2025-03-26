import os
import math
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_circular_route(lat, lon, radius_km, points=36):
    route = []
    radius_deg = radius_km / 111.32  # קירוב ממטרים למעלות
    for i in range(points):
        angle = 2 * math.pi * i / points
        dx = radius_deg * math.cos(angle)
        dy = radius_deg * math.sin(angle)
        point = [lon + dx / math.cos(math.radians(lat)), lat + dy]
        route.append(point)
    route.append(route[0])  # סוגר את הלולאה
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
    html_path = os.path.join(BASE_DIR, 'index.html')
    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html)

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
    
