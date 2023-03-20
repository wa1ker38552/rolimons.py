import rolimons

for ad in rolimons.utils().get_recent_ads():
  print(f"New ad from {ad.user.name} ({ad.user.id})")
  print(f"Offering: {ad.offer.items}, {ad.offer.tags}")
  print(f"Requesting: {ad.request.items}, {ad.request.tags}")
