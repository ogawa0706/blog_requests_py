from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd

url_1 = 'https://ameblo.jp/tsuji-nozomi/entrylist-'
url_2 = '.html'
path = r'格納先フォルダパス\20241206.xlsx'

name_list = []
url_list = []

res = requests.get(url_1 + '1' + url_2)
soup = bs4(res.text, "html.parser")
data = soup.find("a", {'class' : 'skin-paginationEnd skin-btnIndex js-paginationEnd'})
end = data.get('href')
end = end.replace('/tsuji-nozomi/entrylist-', '')
end = end.replace('.html', '')
end = int(end) + 1

i = 1
while i < end:
  res = requests.get(url_1 + str(i) + url_2)
  if res.status_code != 200:
    break
  else:
    print(i,'ページ目：',url_1 + str(i) + url_2)

  soup = bs4(res.text, "html.parser")
  datas =soup.find_all("h2", {'data-uranus-component' : 'entryItemTitle'})
  for data in datas:
    name_list.append( data.find("a").text )
    url_list.append( 'https://ameblo.jp/' + data.find("a").get('href') )

  i +=1

df = pd.DataFrame({"Title":name_list, "URL":url_list})
df.to_excel(path, sheet_name='Sheet1')
