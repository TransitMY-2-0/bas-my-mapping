import json
import re
import os

# Extract geojson and pois from HTML file
def extract_from_html(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    geojson_pattern = r"(?:let|const|var)\s+geojson\s*=\s*({.*?})\s*;"
    pois_pattern = r"(?:let|const|var)\s+pois\s*=\s*(\[.*?\])\s*;"

    geojson_match = re.search(geojson_pattern, html, re.DOTALL)
    pois_match = re.search(pois_pattern, html, re.DOTALL)

    base = os.path.splitext(html_file)[0]
    semantic_data_directory = "semantic_data/"
    if geojson_match:
        #with open(f"{base}_route.geojson", "w", encoding="utf-8") as f:
        #    json.dump(json.loads(geojson_match.group(1)), f, indent=2)
        routes = json.loads(geojson_match.group(1))
        with open(f"{semantic_data_directory}{routes['name']}_route.geojson", "w", encoding="utf-8") as f:
            json.dump(routes, f, indent=2)
        print(f"Created {routes['name']}_route.geojson")

    if pois_match:
        pois = json.loads(pois_match.group(1))

        features = [
            {
                "type": "Feature",
                "properties": {"name": p.get("name")},
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(p["lng"]), float(p["lat"])]
                }
            }
            for p in pois
        ]

        #with open(f"{base}_pois.geojson", "w", encoding="utf-8") as f:
        #    json.dump({"type": "FeatureCollection", "features": features},f,indent=2)
        pois_geojson = {"type": "FeatureCollection", "features": features} 

        with open(f"{semantic_data_directory}{routes['name']}_pois.geojson", "w", encoding="utf-8") as f:
            json.dump(pois_geojson, f, indent=2)
        print(f"Created {routes['name']}_pois.geojson")

    return routes, pois_geojson

def main():
    # change the filename here
    extract_from_html("map.html")
    

if __name__ == "__main__":
    main()
