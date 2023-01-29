import glob
import os
import sqlite3
import altair as alt
import pandas as pd
import pycountry
from django.shortcuts import render
from data.countries import all_countries_code_name, all_countries_off_name, all_countries_name, countries_dfrm
from data.crypto_map import merge

conn = sqlite3.connect('../database.db')
c = conn.cursor()


# def create_map(country):
#     alt.renderers.enable('altair_saver', fmts=['vega-lite', 'png'])
#     chart = alt.Chart(merge[(merge["Country or territory"] == country)]).mark_geoshape().encode(
#         color=alt.Color('Legality', scale=alt.Scale(scheme='accent'))
#     ).properties(
#         width=900,
#         height=500
#     ).configure_legend(labelLimit=0)
#     chart = chart.configure(background='black')
#     chart = chart.configure_legend(labelLimit=0, labelColor='white')
#     current = os.getcwd()
#     chart.save(current + '/country.png')

def home(request):
    return render(request, 'index.html')


def get_info(request):
    country = request.GET.get('selected_country', 0)
    country = country[10:]
    # removing_files = glob.glob('../static/images/*.png')
    # for i in removing_files:
    #     if i == "country.png":
    #         os.remove(i)
    #     alt.renderers.enable('altair_saver', fmts=['vega-lite', 'png'])
    chart = alt.Chart(merge[(merge["Country or territory"] == country)]).mark_geoshape().encode(
            color=alt.Color('Legality', scale=alt.Scale(scheme='accent'))
        ).properties(
            width=900,
            height=500
        ).configure_legend(labelLimit=0)
    chart = chart.configure(background='black')
    chart = chart.configure_legend(labelLimit=0, labelColor='white')

    return render(request, 'get_info.html', {'country': chart.interactive()})



def search(request):
    country = request.GET.get('search_country', 0)
    if country == 0:
        return render(request, 'index.html', {"unknown_country": True, "value": "None"})

    code_suitable = []
    name_suitable = []
    off_name_suitable = []

    for i in all_countries_code_name:
        if i.startswith(country):
            code_suitable.append(i)
    for i in all_countries_name:
        if i.startswith(country):
            name_suitable.append(i)
    for i in all_countries_off_name:
        if i.startswith(country):
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
        countries = pycountry.countries
        search_result = []
        for country in countries:
            for selected in selected_countries:
                if country.name == selected:
                    search_result.append(str(country.flag) + "  " + str(country.alpha_3) + " - " + str(country.name))
        return render(request, 'search.html', {'names': set(search_result)})
    return render(request, 'index.html', {"unknown_country": True, "value": country})
