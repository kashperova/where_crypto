import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry
import altair as alt
import geopandas
# from altair_saver import save
# import lxml


def alpha3code(column):
    CODE = []
    for country in column:
        try:
            code = pycountry.countries.get(name=country).alpha_3
            # .alpha_3 means 3-letter country code
            # .alpha_2 means 2-letter country code
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE


link_for_scarpping = "https://en.wikipedia.org/wiki/Legality_of_cryptocurrency_by_country_or_territory#Detail_by_country_or_territory"
features = ["Country", "Legality"]

table_class = "wikitable sortable jquery-tablesorter"
response = requests.get(link_for_scarpping)

soup = BeautifulSoup(response.text, 'html.parser')
data = soup.find_all('table', {'class': "wikitable sortable"})

details_by_country = pd.read_html(str(data))

status_by_country = pd.DataFrame(details_by_country[0])
for i in range(1, len(details_by_country)):
    df2 = pd.DataFrame(details_by_country[i])
    status_by_country = pd.concat([status_by_country, df2], axis=0, ignore_index=True)

legality_list = status_by_country["Legality"].values

status_str_start_with = ['Illegal', 'Legal / Use discouraged by central bank',
                         'Legal / Banking ban', 'Not considered currency',
                         'Legal to trade and hold / Illegal as a payment tool, banking ban',
                         'Legal / Illegal to buy with local currency', 'Not regulated',
                         'Unknown', 'Ban on mining'
                         ]

for i in range(len(legality_list)):
    flag = 1
    for j in status_str_start_with:
        if legality_list[i].startswith(j):
            legality_list[i] = legality_list[i][:len(j)]
            flag = 0
    if flag and legality_list[i].startswith('Legal'):
        legality_list[i] = legality_list[i][:5]

status_by_country["Legality"] = legality_list
cnts = pycountry.countries
all_countries = []
for country in cnts:
    all_countries.append(country.name)

# create a column for code
status_by_country['CODE'] = alpha3code(status_by_country["Country or territory"])
status_by_country.drop(index=status_by_country.index[:2], axis=0, inplace=True)
false_country_list = list(status_by_country[status_by_country["CODE"] == "None"]["Country or territory"].values)
country_list = list(status_by_country["Country or territory"].values)
for i in range(len(country_list)):
    if country_list[i] == "China (PRC)":
        country_list[i] = "China"
    elif country_list[i] == "Bolivia":
        country_list[i] = "Bolivia, Plurinational State of"
    elif country_list[i] == "Venezuela":
        country_list[i] = "Venezuela, Bolivarian Republic of"
    elif country_list[i] == "Iran":
        country_list[i] = "Iran, Islamic Republic of"
    elif country_list[i] == "Tanzania":
        country_list[i] = "Tanzania, United Republic of"
    elif country_list[i] == "South Korea":
        country_list[i] = "Korea, Republic of"
    elif country_list[i] == "Taiwan":
        country_list[i] = "Taiwan, Province of China"
    elif country_list[i] == "Vietnam":
        country_list[i] = "Viet Nam"
    elif country_list[i] == "Brunei":
        country_list[i] = "Brunei Darussalam"
    elif country_list[i] == "Czech Republic":
        country_list[i] = "Czechia"
    elif country_list[i] == "Russia":
        country_list[i] = "Russian Federation"

misssed_countires = []
misssed_countires = list(set(all_countries) - set(country_list))

status_by_country['Country or territory'] = country_list
unknown_countires = {"Country or territory": misssed_countires,
                     "Legality": ["Unknown" for i in range(len(misssed_countires))]}
unknown_countires['CODE'] = alpha3code(unknown_countires["Country or territory"])
status_by_country['CODE'] = alpha3code(status_by_country["Country or territory"])

df2 = pd.DataFrame.from_dict(unknown_countires)
status_by_country = pd.concat([status_by_country, df2], axis=0, ignore_index=True)

status_by_country.at[69, 'Legality'] = "Illegal"
status_by_country.at[66, 'Legality'] = "Illegal"
#
# status_by_country['Legality'].replace(['Legal / Banking ban',
#        'Legal / Use discouraged by central bank',
#        'Not considered currency', 'Not regulated',
#        'Legal to trade and hold / Illegal as a payment tool, banking ban',
#        'Ban on mining', 'Legal / Illegal to buy with local currency'],
#                                  "Legal", inplace=True)


world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world.columns = ['pop_est', 'continent', 'name', 'CODE', 'gdp_md_est', 'geometry']
merge = pd.merge(world, status_by_country, on='CODE')

location = pd.read_csv(
    'https://raw.githubusercontent.com/melanieshi0120/COVID-19_global_time_series_panel_data/master/data/countries_latitude_longitude.csv')
merge = merge.merge(location, on='name').sort_values(by='Legality', ascending=False).reset_index()

#
# def my_theme():
#     return {
#         'config': {
#             'range': {'category': ['#8200ff', '#ca27ff', "#ffffff", "#808080"]}
#         }
#     }
#
#
# alt.themes.register('my_theme', my_theme)
# alt.themes.enable('my_theme')
#
# alt.renderers.enable('altair_saver', fmts=['vega-lite', 'png'])
#
# world_map = alt.Chart(merge).mark_geoshape(
# ).encode(
#     color='Legality:N'
# ).properties(
#     width=1000,
#     height=600
# ).configure_legend(labelLimit=0, labelColor='white').configure_title(fontSize=14).configure(background='black')
#
# world_map = world_map.configure_legend(labelLimit=0, labelColor='white')
# world_map.save('../static/images/world_map.png')


# def my_theme_updated():
#     return {
#         'config': {
#             'range': {'category': ['#ca27ff']}
#         }
#     }
#

# alt.themes.register('my_theme_updated', my_theme_updated)
# alt.themes.enable('my_theme_updated')
#
#
# def visualize_all_maps():
#     countries = pycountry.countries
#     for c in countries:
#         alt.renderers.enable('altair_saver', fmts=['vega-lite', 'png'])
#         chart = alt.Chart(merge[(merge["Country or territory"] == c.name)]).mark_geoshape().encode(
#             color='Legality:N'
#         ).properties(
#             width=900,
#             height=500
#         ).configure_legend(labelLimit=0)
#         chart = chart.configure(background='black')
#         chart = chart.configure_legend(labelLimit=0, labelColor='white')
#         img_filename = '../static/images/countries/' + c.name + '.png'
#         chart.save(img_filename)
#
#
# visualize_all_maps()

#
# alt.themes.register('my_theme', my_theme)
# alt.themes.enable('my_theme')
#
#
# def visualize_all_pie_charts():
#     from random import randrange
#     countries = pycountry.countries
#     for c in countries:
#         alt.renderers.enable('altair_saver', fmts=['vega-lite', 'png'])
#         bitcoin = randrange(35, 46)
#         ethereum = randrange((100 - bitcoin)-40)
#         tether = randrange((100 - bitcoin-ethereum)-20)
#         others = 100 - (bitcoin+tether+ethereum)
#         columns = ["Bitcoin", "Ethereum", "Tether", "Others"]
#         values = [bitcoin, ethereum, tether, others]
#         info_dict = {"Crypto": columns, "Amount": values}
#         info_dfrm = pd.DataFrame.from_dict(info_dict)
#         info_dfrm["Amount"] = info_dfrm["Amount"].apply(lambda i: i / 100)
#         legacy_chart_pie = alt.Chart(info_dfrm).encode(
#             theta=alt.Theta("Amount:Q", stack=True),
#             radius=alt.Radius("Amount", scale=alt.Scale(type="sqrt", zero=True, rangeMin=80)),
#             color="Crypto:N"
#         )
#         c1 = legacy_chart_pie.mark_arc(innerRadius=20, stroke="#fff")
#         c2 = legacy_chart_pie.mark_text(radiusOffset=15).encode(text=alt.Text('Amount:Q', format='.0%'))
#         img_filename = '../static/images/pie_crypto_charts/' + c.name + '.png'
#         chart = alt.layer(c1, c2).configure_view(
#             stroke='transparent'
#         ).configure_axis(
#             domainWidth=0.8
#         ).configure(background='black').configure_legend(labelLimit=0, labelColor='white')
#         chart.save(img_filename)
#
#
# visualize_all_pie_charts()