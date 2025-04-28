import os
import osmnx as ox
import networkx as nx
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route', methods=['GET'])
def route():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        distance = float(request.args.get('distance', 5000))  # ברירת מחדל 5 ק"מ

        G = ox.graph_from_point((lat, lng), dist=3000, network_type='walk')
        start_node = ox.distance.nearest_nodes(G, lng, lat)

        try:
            route = ox.routing.route_circular(G, start_node, radius=distance/2)
        except:
            route = ox.routing.route_circular(G, start_node, radius=2000)  # fallback למרחק קטן יותר

        if not route:
            return jsonify({"error": "Unable to generate route"}), 400

        route_coords = [{"lat": G.nodes[node]['y'], "lng": G.nodes[node]['x']} for node in route]

        return jsonify({"route": route_coords})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
