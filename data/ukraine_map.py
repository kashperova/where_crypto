import folium
import pandas as pd
from shapely.geometry import Point, Polygon
import geopandas as gpd
import geopy.distance
from sqlite3 import connect


# conn = connect('../static/database.db')

# locations = pd.read_csv('../static/Locations.csv', header=0)
# locations['Coordinats'] = locations['Coordinats'].apply(lambda x: x.split())
# locations["lat"] = locations['Coordinats'].apply(lambda x: x[0])
# locations["lon"] = locations['Coordinats'].apply(lambda x: x[1])
# locations = locations.drop("Coordinats", axis=1)
# locations['lat'] = locations['lat'].astype(float)
# locations['lon'] = locations['lon'].astype(float)
# locations.to_sql('locations', conn)

# locations = pd.read_sql('SELECT * FROM locations', conn)
# locations = locations.drop("index", axis=1)
#
# geometry = [Point(xy) for xy in zip(locations["lat"], locations["lon"])]
#
# crs = {'init': 'epsg:4326'}
# geo_df_places = gpd.GeoDataFrame(locations, crs=crs, geometry=geometry)
#
# geo_df_places.columns = ['Company', 'Category', 'lat', 'lon', 'geometry']
#
# points = []
#
# for i in range(len(geometry)):
#     points.append(tuple([geometry[i].x, geometry[i].y]))
#
# ukraine_map = folium.Map(location=[50.450001, 30.523333], zoom_start=14, prefer_canvas=True)
#
# # add a markers
# for index in range(len(points)):
#     folium.Marker(points[index], popup="Company: " + geo_df_places.loc[index]["Company"]
#                                        + "\n" + "Category: " + geo_df_places.loc[index]["Category"]).add_to(ukraine_map)
