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
      dat = [x for x in item.get_text().split('\n') if x.strip()]
      data.append({
        'timestamp': raw1[i].get_text().split('\n')[1],
        'price': dat[1],
        'old_rap': dat[3],
        'new_rap': dat[5]
      })
    return data
