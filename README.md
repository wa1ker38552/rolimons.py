# Rolimons
*An unofficial Python API wrapper for Rolimons*

rolimons.py is an api wrapper for [rolimons](https://rolimons.com) It allows you to fetch data from the official rolimons api as well as data that can only be scraped. 

**Getting Started**<br>
`pip install rolimons`

**Quick Start 🛠️**
```py
import rolimons

player = rolimons.player(name='Roblox')
print(player.rap, player.value)

item = rolimons.item(1365767)
print(item.rap, item.value)

sales = item.get_recent_sales()
for sale in sales:
  print(sale.timestamp, sale.old_rap, sale.new_rap)
  
for player in rolimons.utils().get_leaderboard():
  print(player.name, player.value, player.rap)
```
