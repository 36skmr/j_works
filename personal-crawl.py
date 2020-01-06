import requests
import pprint
from bs4 import BeautifulSoup

# プロフィールはID以降の数字が変わる
island_url = "https://j-island.net/artist/person/id/"

personal = {}

# プロフィール分だけfor文でまわす、いったんべた書き
for num in range(1,10):
    url = island_url + str(num)

    response = requests.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, 'html.parser')

    artist_name = bs.select('span.artist-name')

    # tag
    div_tag_list = bs.select('div.artist-profile-area')

    if len(div_tag_list) > 0:

        # 名前
        name = artist_name[0].text
        # 趣味を取りだす
        dl_list = div_tag_list[0].select('dl')

        dd = dl_list[3].find('dd')
        # 全員が全員「。」で区切っていないため、半角スペースを「、」で置き換え
        dd = dd.text.replace(' ', '、')
        syumi_list = dd.split('、')
        personal[name] = syumi_list

pprint.pprint(personal)
