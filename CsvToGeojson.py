import csv
import geojson


# import folium
# from streamlit_folium import folium_static

def csv_to_geojson(csv_file, geojson_file):
    features = []
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Assuming your CSV has 'latitude' and 'longitude' columns
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            feature = geojson.Feature(
                geometry=geojson.Point((longitude, latitude)),
                properties=row
            )
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    with open(geojson_file, 'w') as f:
        geojson.dump(feature_collection, f, indent=2)

# Replace 'input.csv' and 'output.geojson' with your file names
csv_to_geojson('data/idns.csv', 'data/idns.geojson')