import pandas as pd
import altair as alt
from data.crypto_map import merge
import pycountry
import altair_saver

def my_theme():
    return {
        'config': {
            'range': {'category': ['#8200ff', '#ca27ff', "#ffffff", "#808080"]}
        }
    }


alt.themes.register('my_theme', my_theme)
alt.themes.enable('my_theme')

alt.renderers.enable('altair_saver', fmts=['vega-lite', 'png'])


world_map = alt.Chart(merge).mark_geoshape(
).encode(
    color='Legality:N'
).properties(
    width=1000,
    height=600
).configure_legend(labelLimit=0, labelColor='white').configure_title(fontSize=14).configure(background='black')

world_map = world_map.configure_legend(labelLimit=0, labelColor='white')
world_map.save('../static/images/world_map.png')


# def my_theme_updated():
#     return {
#         'config': {
#             'range': {'category': ['#ca27ff']}
#         }
#     }
#
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
#         ethereum = randrange((100 - bitcoin) - 40)
#         tether = randrange((100 - bitcoin - ethereum) - 20)
#         others = 100 - (bitcoin + tether + ethereum)
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
