import requests
from bs4 import BeautifulSoup

# なぜかじーこ
island_url = "https://j-island.net/artist/person/id/13"

response = requests.get(island_url)
response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.text, 'html.parser')

# tag
div_tag_list = bs.select('div.artist-profile-area')

# 趣味を取りだす
personal = []
person = {}
dl_list = div_tag_list[0].select('dl')
#print(dl_list[3])

dd = dl_list[3].find('dd')
print(dd.text)
syumi_list = dd.text.split('、')
print(syumi_list)
