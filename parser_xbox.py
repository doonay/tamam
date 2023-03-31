#(python manage.py -h) - получение справки по всем командам, но покруче

from django.core.management.base import BaseCommand
from third_app.models import XboxGameModel

#--------------django--------------

import requests
import json

def parser():
  headers = {
    'authority': 'catalog.gamepass.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Tue, 28 Mar 2023 04:17:37 GMT',
    'if-none-match': '"0x8DB2F435CFBE303"',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  }

  url = 'https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=ru-ru&market=RU'

  session = requests.session()
  r = session.get(url)


  all_xbox_games_ids = json.loads(r.text)
  ids_list = []
  for xbox_game in range(1, len(all_xbox_games_ids), 1):
    ids_list.append(all_xbox_games_ids[xbox_game]['id'])

  last_game = len(ids_list) - 1
  ids_list = ','.join(ids_list)

  url = f'https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={ids_list}&market=RU&languages=RU-RU&MS-CV=DGU1mcuYo0WMMp+F.1'
  r = session.get(url)
  data = json.loads(r.text)['Products']

  game_count = 0
  for card in data:
    title = card['LocalizedProperties'][0]['ProductTitle']
    #print('title', title)

    img = 'https:' + card['LocalizedProperties'][0]['Images'][4]['Uri'] + '?h=60&format=jpg'
    #print('img', img)

    xbox_id = card['ProductId']
    #print('ProductId:', xbox_id)

    platforms = ['XBOX']
    #print('platforms:', platforms)

    release_date = card['MarketProperties'][0]['OriginalReleaseDate']

    price_now = float(card["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["ListPrice"])
    #print('base_price', base_price)

    try:
      price_past = float(card["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["WholesalePrice"])
      #print('discounted_price', discounted_price)
      discount = int((base_price - discounted_price) / (base_price / 100))
      #print('discount', discount)
      flag_is_discount = True
    except:
      price_past = 0
      discount = 0
      flag_is_discount = False
      #print('discounted_price', discounted_price)
      #print('discount', discount)
    
    #print('---')
    

    game = XboxGameModel(
      xbox_id = xbox_id,
      title = title,
      img = img,
      platforms = platforms,
      release_date = release_date,
      price_now = price_now,
      #---
      flag_is_discount = flag_is_discount,
      discount = discount,
      price_past = price_past
      #timestrap подставляется сам на уровне модели
    ).save()

    game_count += 1
    print('[', game_count, '/', last_game, ']','Внесли в базу', title)
    
    


#--------------django--------------

class Command(BaseCommand):
  help = 'PsAllModel'

  def handle(self, *args, **options):
    parser()
