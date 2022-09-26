# rolimons.py
A Python API wrapper for Rolimons.

RoliPY is an API wrapper for Rolimons that includes several features that other wrappers for Rolimons don't include. The project is being actively maintained currently.

**Getting Started** <br/>
`pip install rolimons`

# Documentaton
The wrapper contains a class along with 2 subclasses to handle and organize data. These include Rolimons, Item, and User classes.

**rolimons** <br/>
Functions defined:

`leaderboard()` Fetches a list of players from the Rolimons leaderboard. <br/>
Example:
```py
rolimons.leaderboard()
```
> `[{'name': Roblox, 'rank': 1, 'value': 100000, 'rap': 100000}, ...]`

`leaks()` Fetches a list of recently leaked Roblox items. <br/>
Example:
```py
for leak in rolimons.leaks():
  print(leak['timestamp'])
  print(leak['name'])
  print(leak['image'])
```
> ```
> 123456
> Valkrie Helm
> https://tr.rbxcdn.com/...
`new_limiteds()` Fetches a list of recent items that have become limiteds. <br/>
Example:
```py

.new_limiteds(limit=10)
```
> `[{'name': Valkrie Helm, 'rap': 100000}, ...]` <br/>

`get_trade_ads()` Fetches a list of recent trade ads. <br/>
Example:
```py
rolimons.get_trade_ads()
```
> `[{'user': John Doe, 'offering': [<rolimons.Item Object>, ...], 'requesting': [<rolimons.Item Object>]}, ...]`

Note: If a trade does not have a request for items, it will switch out the `request` key with the `tag` key. <br/>
`get_market_activity()` Fetches a list of recently sold items tracked by rolimons <br/>
Example:
```py
for item in rolimons.get_market_activity():
  print(item['item'])
  print(item['old_rap'])
  print(item['new_rap'])
  print(item['timestamp'])
```
> ```
> <rolimons.Item Object>
> 1000
> 1200
> 123456

**rolimons.User** <br/>
Parameters: <br/> <br/> 
You can search for a user by id or by name when passing it as a parameter. To search for id, use `rolimons.User(id=12345)` and to search for name, use `rolimons.User(username='Roblox')`

Attributes: <br/> <br/> 
`self.id` User id <br/>
`self.username` User name <br/>
`self.value` Total value <br/>
`self.rap` Total rap <br/>
`self.trade_ads` Total trade ads sent <br/>
`self.inventory` All items in users inventory in `<rolimons.Item Object>` <br/>

Functions defined: <br/> <br/> 
`get_metadata()` Refreshes all data for the specified user. This includes, rap, value, inventory, and trade_ads <br/>
Example:
```py
user = rolimons.User(username='Roblox')
user.rap

user.get_metadata()
user.rap
```
> ```
> 10000
> 10001

`get_thumbnail` Returns Roblox headshot thumbnail <br/>
Example:
```py
with open('image.png', 'wb') as file:
  im = rolimons.User(username='Roblox').get_thumbnail()
  file.write(requests.get(im).content)
```
`get_inventory_timestamps()` Fetches all saved timestamps of past inventory <br/>
Example: 
```py
for timestamp in rolimons.User(name='Roblox').get_inventory_timestamps():
  print(timestamp)
```
> `123456`
> `...`

`get_inventory_history(timestamp)` Fetches inventory history for a timestamp obtained from `get_inventory_timestamps()` <br/>
Example:
```py
user = rolimons.User(name='roblox')
timestamp = user.get_inventory_timestamps()[0]
for item in user.get_inventory_history(timestamp):
  print(item.name)
```
> `Classic Roblox Fedora`
> `...`

`query_user(username)` Searches Roblox to match username to an id <br/>
Note: This function cannot be used on the client end.

**rolimons.Item** <br/>
Parameters: <br/> <br/> 
You can only search for item by id, `rolimons.Item(12345)`. An additional parameter you can pass in is `raw` which is the raw marketplace table containing item values. This is so that you don't hit rate limits if you try to keep searching for items. You have to pass in the 'items' key from the itemtable not the entire table.
```py
raw_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']

items = [12345, ...]
objects = []
for item in items:
  objects.append(rolimons.Item(item, raw=raw_data))
 ```

Attributes: <br/> <br/>
`self.id` Item id <br/>
`self.name` Item name <br/>
`self.value` Item value <br/>
`self.rap` Item rap <br/>

Functions defined: <br/> <br/> 
`sales_data()` Gets rolimons sales data about item
Example:
```py
for sale in rolimons.Item(12345).sales_data():
  print(sale['timestamp'])
  print(sale['price'])
  print(sale['old_rap'])
  print(sale['new_rap'])
```
> ```
> 123456
> 1000
> 900
> 950

**rolimons.Client** <br/>
The only parameter is your Rolimons cookie which should look something like `_ga=GA1...`
```py
client = rolimons.Client('cookie')
```

Attributes: <br/><br/>
`self.token` Rolimons cookie <br/>
`self.client` request.Session object with your Rolimons cookie in headers. Used for your own tests outside of class

Functions defined: <br/><br/>
`update_wishlist(wishlist)` Updates and overrides your Rolimons wishlist. Enter values in list format and returns request status code. <br/>
Example:
```py
client = rolimons.Client('token')
status_code = client.update_wishlist([12345, 54321])
print(status_code)
```
> `200`

`update_asking({id: [tags]})` Updates and overrides your asking tags on Rolimons. A dictionary with the item id as key and list of tags as values will be required as parameter returns status code<br/>
Example:
```py
client = rolimons.Client('token')
status_code = client.update_asking({12345: ['overpay', 'upgrades'], 54321': ['nft']})
print(status_code)
```
> `200`

`add_player(username)` Adds a player to Rolimons. The only parameter is username. Returns status code <br/>
Example:
```py
client = discord.Client('token')
status_code = client.add_player('Roblox')
print(status_code)
```
> `200`

`post_trade_ad(request, offering, id)`Posts a trade ad to Rolimons. Simply add the tag names in request and the client will automatically upload them with the trade ad. <br/>
Example:
```py
client = discord.Client('token')
client.post_trade_ad([12345, ...], [12345, 'adds', 'upgrade'], 1)
```
