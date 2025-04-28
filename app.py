import os
import math
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_circular_route(lat, lng, distance_meters=5000):
    # שלב 1: למשוך גרף מדרכות סביב נקודת ההתחלה
    G = ox.graph_from_point((lat, lng), dist=2000, network_type='walk')

    # שלב 2: למצוא את הצומת הכי קרוב לנקודת ההתחלה
    start_node = ox.distance.nearest_nodes(G, lng, lat)

    # שלב 3: לנסות לבנות מסלול מעגלי
    try:
        route = ox.routing.route_circular(G, start_node, radius=distance_meters/2)
        return G, route
    except Exception as e:
        print(f"Failed to create route: {e}")
        return None, None

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
    
