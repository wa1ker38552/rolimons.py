from rolimons.client import Client
from rolimons.items import Item
from rolimons.users import User

# core libraries
import json
import requests
from bs4 import BeautifulSoup

def get_inverse_index(response, i1, i2):
  end = response.index(i1)
  x = end
  while response[x] != i2: x -= 1
  return response[x+1:end]

def get_index(response, i1, i2):
  start = response.index(i1)+len(i1)
  x = start
  while response[x] != i2: x += 1
  return response[start:x]

def leaderboard():
  request = requests.get('https://rolimons.com/leaderboard')
  soup = BeautifulSoup(request.text, 'html.parser') 
  raw = soup.find_all('div', attrs={'class': 'pb-2 mb-3 item_cell shadow_md_35 shift_up_md mx-0'})
  
  data = []
  for item in raw:
    dat = [x for x in item.get_text().split('\n') if x.strip()]
    data.append({
      'name': dat[0],
      'rank': dat[2].replace('#', ''),
      'value': dat[4].replace(',', '').replace('R$ ', ''),
      'rap': dat[6].replace(',', '').replace('R$ ', '')
    })
  return data

def leaks():
  request = requests.get('https://rolimons.com/leaks')
  data = []
  for line in request.text.split('\n'):
    if '<script>var leaks        = ' in line:
      raw = json.loads(line.replace('<script>var leaks        = ', '')[:-1])
      for item in raw:
        data.append({
          'timestamp': item[0],
          'name': item[5],
          'image': item[6]
        })
  return data

def new_limiteds():
  request = requests.get('https://rolimons.com')
  soup = BeautifulSoup(request.text, 'html.parser')
  raw1 = soup.find_all('a', attrs={'class': 'items_slider_title'})
  raw2 = soup.find_all('div', attrs={'class': 'items_slider_info_section'})

  data = []
  for i, item in enumerate(raw1): 
    data.append({
      'name': item.get_text(),
      'rap': raw2[i].get_text().strip().split('\n')[1].replace(',', '')
    })
  return data

def get_value_changes():
  request = requests.get('https://www.rolimons.com/valuechanges')
  soup = BeautifulSoup(request.text, 'html.parser')
  raw = soup.find_all('span', attrs={'class': 'change_stat text-light text-truncate'})
  print(raw)
  for item in raw: print(item.get_text())

def get_trade_ads(limit=50):
  request = requests.get('https://www.rolimons.com/tradeadsapi/getrecentads').json()
  raw = request['trade_ads']

  if limit > request['trade_ad_count']: limit = 50
  data = []

  raw_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
  for i in range(limit):
    pre = {
      'user': raw[i][3],
      'offering': [Item(x, raw=raw_data) for x in raw[i][4]['items']]
    }
    try:
      pre['request'] = [Item(x, raw=raw_data) for x in raw[i][5]['items']]
    except KeyError:
      pre['tags'] = raw[i][5]['tags']
    data.append(pre)
  return data

def get_market_activity():
  raw_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
  request = requests.get('https://www.rolimons.com/api/activity')

  data = []
  for item in request.json()['activities']:
    data.append({
      'item': Item(item[2], raw=raw_data),
      'old_rap': item[3],
      'new_rap': item[4],
      'timestamp': item[0]
    })
  return data
