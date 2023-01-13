from bs4 import BeautifulSoup
import requests

class Item:
  def __init__(self, id, raw=None):
    self.id = id
    if raw is None:
      self.raw = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
    else:
      self.raw = raw
    self.name = self.raw[str(self.id)][0]

    if self.raw[str(self.id)][3] == -1:
      self.value = self.raw[str(self.id)][2]
    else:
      self.value = self.raw[str(self.id)][3]
    self.rap = self.raw[str(self.id)][2]

  def sales_data(self):
    request = requests.get(f'https://www.rolimons.com/itemsales/{self.id}')
    soup = BeautifulSoup(request.text, 'html.parser')

    data = []
    raw1 = soup.find_all('div', attrs={'class': 'activity_links_section d-flex float-left'})
    raw2 = soup.find_all('div', attrs={'class': 'activity_stats_section d-flex justify-content-around'})
    
    for i, item in enumerate(raw2):
      timestamp = BeautifulSoup(str(raw1[i]), 'html.parser').find('div', attrs={'class': 'activity_entry_timestamp my-auto'}).get_text()
      search = BeautifulSoup(str(item), 'html.parser')
      sales = [it.get_text() for it in search.find_all('div', attrs={'class': 'activity_stat_data'})]
      data.append({
        'old_rap': sales[1],
        'new_rap': sales[2],
        'price': search.find('div', attrs={'class': 'pl-1'}).get_text(),
        'timestamp': timestamp
      })
    return data
