import os
import osmnx as ox
import networkx as nx
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_circular_route(lat, lng, distance_meters=5000):
    """
    יוצר מסלול מעגלי על מדרכות אמיתיות סביב נקודת התחלה נתונה.
    """
    try:
        # מושכים רשת רחובות להולכי רגל
        G = ox.graph_from_point((lat, lng), dist=3000, network_type='walk')
        print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")
        
        if len(G.nodes) == 0:
            raise ValueError("No graph data found around the location.")
        
        # מוצאים את הצומת הקרוב ביותר
        start_node = ox.distance.nearest_nodes(G, lng, lat)
        
        try:
            # מנסים לבנות מסלול עגול
            route = ox.routing.route_circular(G, start_node, radius=distance_meters / 2)
            return G, route
        except Exception as e:
            print(f"Failed to create route at {distance_meters} meters: {e}")
            # fallback - מנסים לבנות מסלול קצר יותר
            route = ox.routing.route_circular(G, start_node, radius=2000)
            return G, route
        
    except Exception as e:
        print(f"Error loading graph or creating route: {e}")
        return None, None

@app.route('/route', methods=['GET'])
def route():
    """
    נקודת קצה שמקבלת קואורדינטות ומחזירה מסלול ריצה מעגלי במדרכות.
    """
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        distance = float(request.args.get('distance', 5000))  # מרחק ברירת מחדל 5 ק"מ

        G, route = get_circular_route(lat, lng, distance)

        if G is None or route is None:
            return jsonify({"error": "Unable to generate route"}), 400

        # המרת הצמתים לרשימת קואורדינטות
        route_coords = []
        for node in route:
            point = G.nodes[node]
            route_coords.append({
                "lat": point['y'],
                "lng": point['x']
            })

        return jsonify({
            "route": route_coords
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "LoopIt API is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # ל-Render
    app.run(host='0.0.0.0', port=port)
