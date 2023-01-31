import glob
import os
import sqlite3
import altair as alt
import pandas as pd
import pycountry
from django.http import JsonResponse
from django.shortcuts import render, redirect
from data.countries import all_countries_code_name, all_countries_off_name, all_countries_name, countries_dfrm
from data.crypto_map import merge
from data.legal_statistics import dfrm_legal, dfrm_predicted
import altair_saver

conn = sqlite3.connect('../database.db')
c = conn.cursor()


def home(request):
    return render(request, 'index.html')


def home_page_return(request):
    return redirect('/')


def prepare_text(country):
    chart = str(country) + '.png'
    legality = str(merge[(merge["Country or territory"] == country)].Legality.values[0])
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
    country = country[10:]
    chart, legality, legal_currency, date, votes, number = prepare_text(country)
    return render(request, 'get_info.html', {'chart': chart, 'legality': legality, 'country': country,
                                             'legal_currency': legal_currency, 'date': date,
                                             'votes': votes, 'number': number})


def search(request):
    country = request.GET.get('search_country', 0)
    if country == 0:
        return render(request, 'index.html', {"unknown_country": True, "value": "None"})

    code_suitable = []
    name_suitable = []
    off_name_suitable = []

    if (country in all_countries_code_name) or (country in all_countries_name)\
            or (country in all_countries_off_name):
        chart, legality, legal_currency, date, votes, number = prepare_text(country)
        return render(request, 'get_info.html', {'chart': chart, 'legality': legality, 'country': country,
                                                 'legal_currency': legal_currency, 'date': date,
                                                 'votes': votes, 'number': number})

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
