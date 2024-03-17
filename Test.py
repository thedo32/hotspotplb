import altair as alt
import folium
import pandas as pd
from folium.plugins import MarkerCluster
import plotly.express as px
import pydeck as pdk
from folium.plugins import FastMarkerCluster
from streamlit_float import *
from streamlit_folium import st_folium

callback = """\
                            function (row) {
                                    var icon, marker;
                                    icon = L.AwesomeMarkers.icon({
                                        icon: "fire", iconColor: "#86BCDC", iconSize: [5,5]});
                                    marker = L.marker(new L.LatLng(row[0], row[1]) );
                                    marker.setIcon(icon);
                                    return marker;
                            };
                            """

# draw basemap
m = folium.Map(location=[-3.1940, 117.5540],
                               tiles = 'cartodbdarkmatter',
                               zoom_start=2, control_scale=True)

# Get x and y coordinates for each point
# points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
# points_gjson.add_to(m)
# Get x and y coordinates for each point
points = pd.read_csv('maps/idns.csv')

# Extract latitude and longitude columns
marker_cluster = MarkerCluster(callback=callback)
for _, row in points.iterrows():
       popup = f"Latitude: {row['Latitude']}<br>Longitude: {row['Longitude']}"
       folium.Marker([row['Latitude'], row['Longitude']], popup=popup).add_to(marker_cluster)

marker_cluster.add_to(m)

# Add maps to streamlit
st_folium(m, height=450, use_container_width=True)