import requests
from bs4 import BeautifulSoup
import os
import json


save_dir = "./images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 目标网页 URL
url = "https://ai-bot.cn/"

response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, 'html.parser')
data = []
one_title = soup.select('#content > div.content > div > div > div > h4')
for i in range(len(one_title)):
    t1 = one_title[i].text.replace('\n', '').replace(' ', '')
    d1 = {
        "title": t1.strip(),
        "tags": [],
    }
    data.append(d1)

f1 = soup.select(f'#content > div.content > div > div > div.row.io-mx-n2')
for j in range(len(f1)):

    d2 = []
    url_cards = f1[j].select('.url-card')
    for k in range(len(url_cards)):
        url = url_cards[k].select('a')[0]["data-url"]
        name = url_cards[k].select('a > div > div.url-info.flex-fill > div > strong')[0].text
        desc = url_cards[k].select('a > div > div.url-info.flex-fill > p')[0].text.strip()

        icon_url = url_cards[k].select('a > div > div > img')[0]["data-src"]
        icon_name =icon_url.split("/")[-1]

        response = requests.get(icon_url)
        with open(os.path.join(save_dir, icon_name), "wb") as f:
            f.write(response.content)

        d3 = {
            "url": url,
            "name": name,
            "desc": desc.replace('\n', '').replace(' ', ''),
            "icon_url": icon_name,
        }
        print(d3)
        d2.append(d3)
    data[j]["tags"] = d2

with open("data.json", "w") as f:
    json.dump(data, f,indent=None)


# 读取json内容
# with open("data.json", "r") as f:
#     data = json.load(f)
#
# for v in data:
#     print(v)

