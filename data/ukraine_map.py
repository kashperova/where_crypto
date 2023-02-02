import folium
import pandas as pd
from shapely.geometry import Point, Polygon
import geopandas as gpd
import geopy.distance
from sqlite3 import connect
import urllib.request, json


# cities = ["Zhytomyr", "Zaporizhzhia", "Vinnytsia", "Uzhhorod", "Ternopil", "Sumy", "Rivne", "Poltava", "Dnipro",
#          "Mykolaiv", "Odesa", "Lviv", "Lutsk", "Kyiv", "Kropyvnytskyi", "Khmelnytskyi", "Kherson", "Ivano-Frankivsk",
#          "Kharkiv", "Chernivtsi", "Chernihiv", "Cherkasy"]
#
# electonics = ["Foxtrot", "Stylus"]
# markets = ["Varus"]
# gas_stations = ["WOG"]
# pharmacy = ["ANC"]
#
# dfrm = pd.DataFrame({'lat': [], 'lng': [], 'category': [], 'company': []})
# link = ""
# for i in electonics:
#     for j in cities:
#         link = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + i + "+in+"  + j + "&key=AIzaSyDNAlAn-Kd_OsoR7gisnOwrxhingfX7wRA"
#         with urllib.request.urlopen(link) as url:
#             data = json.load(url)
#         if data["results"]:
#             df1 = pd.DataFrame(data["results"][0]["geometry"]["location"], index=[0])
#             for t in range(1,len(data["results"])):
#                 df2 = pd.DataFrame(data["results"][t]["geometry"]["location"], index=[t])
#                 df1 = pd.concat([df1, df2], axis=0, ignore_index=True)
#             category = ["electronics" for s in range(len(data["results"]))]
#             company = [i for k in range(len(data["results"]))]
#             df1['company'] = company
#             df1['category'] = category
#             dfrm = pd.concat([dfrm, df1], axis=0, ignore_index=True)
#     link = ""
# link = ""
# for i in markets:
#     for j in cities:
#         link = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + i + "+in+"  + j + "&key=AIzaSyDNAlAn-Kd_OsoR7gisnOwrxhingfX7wRA"
#         with urllib.request.urlopen(link) as url:
#             data = json.load(url)
#         if data["results"]:
#             df1 = pd.DataFrame(data["results"][0]["geometry"]["location"], index=[0])
#             for t in range(1,len(data["results"])):
#                 df2 = pd.DataFrame(data["results"][t]["geometry"]["location"], index=[t])
#                 df1 = pd.concat([df1, df2], axis=0, ignore_index=True)
#             category = ["markets" for s in range(len(data["results"]))]
#             company = [i for k in range(len(data["results"]))]
#             df1['company'] = company
#             df1['category'] = category
#             dfrm = pd.concat([dfrm, df1], axis=0, ignore_index=True)
#     link = ""
# link = ""
# for i in gas_stations:
#     for j in cities:
#         link = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + i + "+in+"  + j + "&key=AIzaSyDNAlAn-Kd_OsoR7gisnOwrxhingfX7wRA"
#         with urllib.request.urlopen(link) as url:
#             data = json.load(url)
#         if data["results"]:
#             df1 = pd.DataFrame(data["results"][0]["geometry"]["location"], index=[0])
#             for t in range(1,len(data["results"])):
#                 df2 = pd.DataFrame(data["results"][t]["geometry"]["location"], index=[t])
#                 df1 = pd.concat([df1, df2], axis=0, ignore_index=True)
#             category = ["gas_stations" for s in range(len(data["results"]))]
#             company = [i for k in range(len(data["results"]))]
#             df1['company'] = company
#             df1['category'] = category
#             dfrm = pd.concat([dfrm, df1], axis=0, ignore_index=True)
#     link = ""
# link = ""
# for i in pharmacy:
#     for j in cities:
#         link = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + i + "+in+"  + j + "&key=AIzaSyDNAlAn-Kd_OsoR7gisnOwrxhingfX7wRA"
#         with urllib.request.urlopen(link) as url:
#             data = json.load(url)
#         if data["results"]:
#             df1 = pd.DataFrame(data["results"][0]["geometry"]["location"], index=[0])
#             for t in range(1,len(data["results"])):
#                 df2 = pd.DataFrame(data["results"][t]["geometry"]["location"], index=[t])
#                 df1 = pd.concat([df1, df2], axis=0, ignore_index=True)
#             category = ["pharmacy" for s in range(len(data["results"]))]
#             company = [i for k in range(len(data["results"]))]
#             df1['company'] = company
#             df1['category'] = category
#             dfrm = pd.concat([dfrm, df1], axis=0, ignore_index=True)
#     link = ""
#
#
# dfrm['lat'] = dfrm['lat'].astype(float)
# dfrm['lng'] = dfrm['lng'].astype(float)
#
#
# conn = connect('../database.db')
# dfrm.to_sql('locations', conn)
#