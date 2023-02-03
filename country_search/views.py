import glob
import os
import sqlite3
import pandas as pd
import pycountry
from django.http import JsonResponse
from django.shortcuts import render, redirect
from data.countries import all_countries_code_name, all_countries_off_name, all_countries_name, countries_dfrm
from data.crypto_map import status_by_country
from data.legal_statistics import dfrm_legal, dfrm_predicted
# from data.ukraine_map import ukraine_map
import altair_saver
import folium
from shapely.geometry import Point, Polygon
import geopandas as gpd
import geopy.distance
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()


def get_ukraine_map(request):
    locations = pd.read_sql('SELECT * FROM locations', conn)
    locations = locations.drop("index", axis=1)

    geometry = [Point(xy) for xy in zip(locations["lat"], locations["lng"])]

    crs = {'init': 'epsg:4326'}
    geo_df_places = gpd.GeoDataFrame(locations, crs=crs, geometry=geometry)

    points = []

    for i in range(len(geometry)):
        points.append(tuple([geometry[i].x, geometry[i].y]))

    ukraine_map = folium.Map(location=[50.450001, 30.523333], zoom_start=14, prefer_canvas=True)

    # add a markers
    for index in range(len(points)):
        folium.Marker(points[index], popup="Company: " + geo_df_places.loc[index]["company"]
                                           + "\n" + "Category: " + geo_df_places.loc[index]["category"]).add_to(ukraine_map)

    map = ukraine_map._repr_html_()
    context = {'map': map}
    return render(request, 'ukraine_map.html', context)


def home(request):
    return render(request, 'index.html')


def home_page_return(request):
    return redirect('/')


def prepare_text(country):
    chart = str(country) + '.png'
    legality = str(status_by_country[(status_by_country["Country or territory"] == country)].Legality.values[0])
    legal_currency_countries = list(dfrm_legal.name.values)
    legal_currency = False
    date = ""
    votes = 0
    number = 0
    if country in legal_currency_countries:
        legal_currency = True
        date = str(dfrm_legal[dfrm_legal.name == country].time)
    else:
        votes = int(dfrm_predicted[dfrm_predicted.name == country].voteAmount)
        number = int(dfrm_predicted[dfrm_predicted.name == country].index[0])+1
        if number == 1:
            number = str(number) + 'st'
        elif number == 2:
            number = str(number) + 'nd'
        elif number == 3:
            number = str(number) + 'rd'
        else:
            number = str(number) + 'th'
    return chart, legality, legal_currency, date, votes, number


def get_info(request):
    country = request.GET.get('selected_country', 0)
    country = country[4:]
    chart, legality, legal_currency, date, votes, number = prepare_text(country)
    return render(request, 'get_info.html', {'chart': chart, 'legality': legality, 'country': country,
                                             'legal_currency': legal_currency, 'date': date,
                                             'votes': votes, 'number': number})


def search(request):
    t = request.GET.get('search_country')
    t = t.rstrip('+')
    t = t.lstrip(' ')
    country = t.rstrip(' ')
    code_suitable = []
    name_suitable = []
    off_name_suitable = []

    if (country.lower() in all_countries_code_name) or (country.lower() in all_countries_name)\
            or (country.lower() in all_countries_off_name):
        country = country.lower()
        country = country[0].upper() + country[1:]
        chart, legality, legal_currency, date, votes, number = prepare_text(country)
        return render(request, 'get_info.html', {'chart': chart, 'legality': legality, 'country': country,
                                                 'legal_currency': legal_currency, 'date': date,
                                                 'votes': votes, 'number': number})
    for i in all_countries_code_name:
        if i.startswith(country.lower()):
            code_suitable.append(i)
    for i in all_countries_name:
        if i.startswith(country.lower()):
            name_suitable.append(i)
    for i in all_countries_off_name:
        if i.startswith(country.lower()):
            off_name_suitable.append(i)

    if code_suitable or name_suitable or off_name_suitable:
        codes = countries_dfrm[countries_dfrm["code"].isin(code_suitable)]
        names = countries_dfrm[countries_dfrm["name"].isin(name_suitable)]
        off_names = countries_dfrm[countries_dfrm["official_name"].isin(off_name_suitable)]
        joined_dfrm = pd.DataFrame.from_dict({"code": [], "name": [], "official_name": []})
        joined_dfrm = pd.concat([joined_dfrm, codes], axis=0, ignore_index=True)
        joined_dfrm = pd.concat([joined_dfrm, names], axis=0, ignore_index=True)
        joined_dfrm = pd.concat([joined_dfrm, off_names], axis=0, ignore_index=True)

        selected_countries = list(joined_dfrm["name"].values)
        selected_countries = [i[0].upper() + i[1:] for i in selected_countries]
        countries = pycountry.countries
        search_result = []
        for country in countries:
            for selected in selected_countries:
                if country.name == selected:
                    search_result.append(str(country.flag) + "  " + str(country.name))
        return render(request, 'search.html', {'names': set(search_result)})

    return render(request, 'index.html', {"unknown_country": True, "value": country})


