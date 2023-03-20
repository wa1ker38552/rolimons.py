import requests
from bs4 import BeautifulSoup
from .exceptions import RateLimitError
from .exceptions import InvalidItemDetails


class item:
  def __str__(self):
    return self.name
    
  def __init__(self, id: int, itemdetails: dict=None):
    if itemdetails is None:
      itemdetails = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()
      if not itemdetails['success']:
        raise RateLimitError('Rate limit exceeded for this itemdetails endpoint')

    try:
      item = itemdetails['items'][str(id)]
      self.id: int = id
      self.name: str = item[0]
      self.acronym: str = item[1] if item[1] != '' else None
      self.rap: int = item[2]
      self.value: int = item[3] if item[3] != -1 else item[1]
      self.default_value: int = item[4]
      self.demand: int = item[5] if item[5] != -1 else None
      self.trend: int = item[6] if item[6] != -1 else None
      self.projected: bool = 1 in [item[7]]
      self.hyped: bool = 1 in [item[8]]
      self.rare: bool = 1 in [item[9]]
    except KeyError:
      raise InvalidItemDetails('Invalid itemdetails dictionary passed in')

  def get_sales_data(self):
    request = requests.get(f'https://www.rolimons.com/item/{self.id}')
    soup = BeautifulSoup(request.text, 'html.parser')
    tags = [tag.get_text() for tag in soup.find_all('h5', attrs={'class': 'card-title mb-1 text-light text-truncate stat-data'})]
    tags = [tags[3], tags[5], tags[11], tags[10], soup.find_all('div', attrs={'class': 'value-stat-data'})[0].get_text()]
    return sales(tags)

  def get_recent_sales(self):
    request = requests.get(f'https://www.rolimons.com/itemsales/{self.id}')
    soup = BeautifulSoup(request.text, 'html.parser')
    timestamps = [tag.get_text() for tag in soup.find_all('div', attrs={'class': 'activity_entry_timestamp my-auto'})]
    meta = soup.find_all('div', attrs={'class': 'activity_stats_section d-flex justify-content-around'})
    sales = []
    for i, timestamp in enumerate(timestamps):
      sales_price = BeautifulSoup(str(meta[i]), 'html.parser').find_all('div', attrs={'class': 'pl-1'})[0].get_text()
      sales_rap_change = [tag.get_text().replace('\n', '') for tag in BeautifulSoup(str(meta[i]), 'html.parser').find_all('div', attrs={'class': 'activity_stat_data'})]
      sales.append(sale([timestamp, sales_price, sales_rap_change[0], sales_rap_change[1]]))
    return sales

  def get_ownership_data(self):
    request = requests.get(f'https://www.rolimons.com/item/{self.id}')
    soup = BeautifulSoup(request.text, 'html.parser')
    tags = [tag.get_text() for tag in soup.find_all('div', attrs={'class': 'value-stat-data'})]
    return owner(tags)


class sales:
  def __init__(self, data: list):
    self.average_daily_sales: int = data[0]
    self.rap_after_sale: int = data[1]
    self.original_price: int = data[2]
    self.sellers: int = data[3]
    self.best_price: int = data[4]

class sale:
  def __init__(self, data: list):
    self.timestamp: int = data[0]
    self.sales_price: int = data[1]
    self.old_rap: int = data[2]
    self.new_rap: int = data[3]

class owner:
  def __init__(self, data: dict):
    self.total_copies: int = data[0]
    self.avaliable_copies: int = data[1]
    self.premium_copies: int = data[2]
    self.deleted_copies: int = data[3]
    self.owners: int = data[4]
    self.premium_owners: int = data[5]
    self.hoarded_copies: int = data[6]
    self.percent_hoarded: float = data[7].replace('%', '')
