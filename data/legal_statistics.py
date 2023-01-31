import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time


link_legal_tender_countries = "https://coinmarketcap.com/legal-tender-countries/"

page = requests.get(link_legal_tender_countries)
soup = BeautifulSoup(page.content, 'html.parser') # Parsing content
data = soup.find("script", {"id": "__NEXT_DATA__"})
str_data = data.text
str_data = str_data.rstrip("'").lstrip("'")


res = json.loads(str_data)
res = res['props']
res = res['pageProps']
delete_keys = ['namespacesRequired', 'reqLang', 'globalMetrics', 'dailyVideos', 'pageSize', 'noindex']
for i in delete_keys:
    res.pop(i)

legal_list_dict = res['legalList']
predict_list_dict = res['predictionList']

dfrm_legal = pd.DataFrame(legal_list_dict[0])
for i in range(1, len(legal_list_dict)):
    df2 = pd.DataFrame(legal_list_dict[i])
    dfrm_legal = pd.concat([dfrm_legal, df2], axis=0, ignore_index=True)

dfrm_legal["time"] = dfrm_legal["time"].apply(lambda i: int(i)/1000)
dfrm_legal["time"] = dfrm_legal["time"].apply(lambda i: time.strftime("%d.%m.%Y", time.localtime(int(i))))


dfrm_predicted = pd.DataFrame(predict_list_dict[0])
for i in range(1,len(predict_list_dict)):
    df2 = pd.DataFrame(predict_list_dict[i])
    dfrm_predicted = pd.concat([dfrm_predicted, df2], axis=0, ignore_index=True)