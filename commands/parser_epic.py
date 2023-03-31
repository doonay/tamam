#(python manage.py -h) - получение справки по всем командам, но покруче

from django.core.management.base import BaseCommand
from third_app.models import EpicGameModel

#--------------django--------------

import requests, json
import cloudscraper
#from datetime import datetime



scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

def parser(os):

	if os == 'mac':
		os_tag = '10719' #Mac OS
	elif os == 'win':
		os_tag = '9547' #Windows:


	url = f'https://store.epicgames.com/graphql?operationName=searchStoreQuery&variables=%7B%22allowCountries%22:%22TR%22,%22category%22:%22games%2Fedition%2Fbase%22,%22count%22:1,%22country%22:%22TR%22,%22keywords%22:%22%22,%22locale%22:%22en-US%22,%22sortBy%22:%22relevancy,viewableDate%22,%22sortDir%22:%22DESC,DESC%22,%22start%22:0,%22tag%22:%22{os_tag}%22,%22withPrice%22:true%7D&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%227d58e12d9dd8cb14c84a3ff18d360bf9f0caa96bf218f2c5fda68ba88d68a437%22%7D%7D'
	total_data = json.loads(scraper.get(url).text)['data']['Catalog']['searchStore']
	total_games = total_data["paging"]["total"]
	step = 200
	game_count = 0
	for start in range(0, total_games, 200):
		url = f'https://store.epicgames.com/graphql?operationName=searchStoreQuery&variables=%7B%22allowCountries%22:%22TR%22,%22category%22:%22games%2Fedition%2Fbase%22,%22count%22:{step},%22country%22:%22TR%22,%22keywords%22:%22%22,%22locale%22:%22en-US%22,%22sortBy%22:%22relevancy,viewableDate%22,%22sortDir%22:%22DESC,DESC%22,%22start%22:{start},%22tag%22:%22{os_tag}%22,%22withPrice%22:true%7D&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%227d58e12d9dd8cb14c84a3ff18d360bf9f0caa96bf218f2c5fda68ba88d68a437%22%7D%7D'

		data = json.loads(scraper.get(url).text)['data']['Catalog']['searchStore']
		elements = data['elements']
		for e in elements:
			title = e['title']
			epic_id = e['id']
			img = e['keyImages'][0]['url']
			price_now = e['currentPrice']
			discountPrice = e['price']['totalPrice']['discountPrice']
			discount = e['price']['totalPrice']['discount']
			if discount == 0:
				flag_is_discount = False
			else:
				flag_is_discount = True
			price_past = e['price']['totalPrice']['originalPrice']
			






			platforms = []
			platforms.append(os)

			try:
				game = EpicGameModel(
					epic_id = epic_id,
					title = title,
					img = img,
					platforms = platforms,
					price_now = price_now,
					flag_is_discount = flag_is_discount,
					discount = discount,
					price_past = price_past
					#timestrap подставляется сам на уровне модели
				).save()
			except:
				game = EpicGameModel.objects.get(epic_id = epic_id)
				game.platforms = game.platforms.append(os)

			game_count += 1
			print('[', game_count, '/', total_games, ']','Внесли в базу', title)
		
	


#--------------django--------------

class Command(BaseCommand):
	help = 'EpicGameModel'

	def handle(self, *args, **options):
		parser('mac') #Mac OS
		parser('win') #Windows