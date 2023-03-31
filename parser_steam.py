#(python manage.py -h) - получение справки по всем командам, но покруче

from django.core.management.base import BaseCommand
from third_app.models import SteamGameModel

#--------------django--------------

from bs4 import BeautifulSoup
import requests
from math import ceil

SESSION = requests.session()

class Parser:

    def get_soup(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'steamCountry=TR%7C62115100472feedb7761b1ac744145af; browserid=3016886840460041906; sessionid=f0e13adc67eab473b4b4ea1a; timezoneOffset=10800,0; _ga=GA1.2.120033062.1678096978; Steam_Language=english; birthtime=1101848401; lastagecheckage=1-0-2005; steamLoginSecure=76561199446648789%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQxOV8yMjNBOTg4MF80NjRBNSIsICJzdWIiOiAiNzY1NjExOTk0NDY2NDg3ODkiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY3OTM0OTcxOCwgIm5iZiI6IDE2NzA2MjI2MjksICJpYXQiOiAxNjc5MjYyNjI5LCAianRpIjogIjBEMThfMjIzRjNDQjZfN0U2RDEiLCAib2F0IjogMTY3ODg4MjQzMSwgInJ0X2V4cCI6IDE2OTczNTI1OTksICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIyMTIuMTU0Ljg3LjE0OCIsICJpcF9jb25maXJtZXIiOiAiMjEyLjE1NC44Ny4xNDgiIH0.mtQIoimsxpYRI6p36xaqfEQbDfN5_4sYhhQLRG55I4gz0ifms7qzg1-5ZrP1cOLc-_KhNWLV5s5dk6unz6cZAw; _gid=GA1.2.1508730785.1679262635; strResponsiveViewPrefs=touch; recentapps=%7B%221716740%22%3A1679345369%2C%22730%22%3A1679318193%2C%22578080%22%3A1679314290%2C%22271590%22%3A1679312870%2C%221331550%22%3A1679264311%2C%22221100%22%3A1679138018%2C%22557260%22%3A1678124543%2C%221324560%22%3A1678099036%7D; app_impressions=1279270@1_7_7_230_150_79|1414000@1_7_7_230_150_79|1184890@1_7_7_230_150_79|1269820@1_7_7_230_150_79|1211830@1_7_7_230_150_79|1246400@1_7_7_230_150_79|1944360@1_7_7_230_150_80|864700@1_7_7_230_150_80|2113530@1_7_7_230_150_80|1709050@1_7_7_230_150_80|2277070@1_7_7_230_150_80|2257400@1_7_7_230_150_80|810040@1_7_7_230_150_80|1642260@1_7_7_230_150_80|1388870@1_7_7_230_150_80|1123450@1_7_7_230_150_80|1269640@1_7_7_230_150_80|841164@1_7_7_230_150_80|623613@1_7_7_230_150_80|614008@1_7_7_230_150_80|567360@1_7_7_230_150_80|991064@1_7_7_230_150_80|1350780@1_7_7_230_150_80|1641250@1_7_7_230_150_80|1502770@1_7_7_230_150_80|434069@1_7_7_230_150_80|313420@1_7_7_230_150_80|345681@1_7_7_230_150_80|1198410@1_7_7_230_150_80|1454010@1_7_7_230_150_82|1240210@1_7_7_230_150_82|2245320@1_7_7_230_150_82',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }
            
        r = SESSION.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    #--------------discounts

    def get_discount(self, game):
        discount = int(game.find('div', {'class': 'col search_discount responsive_secondrow'}).find('span').get_text().strip().replace('-', '').replace('%', ''))
        #print('discount', discount)
        return discount

    def get_price_now(self, game):
        price_now = int(game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'}).get('data-price-final'))
        #print('price_now', price_now)
        return price_now

    def get_price_past(self, game, price_now, discount):
        price_past = int(int(price_now*100)/(100-discount)) # back percentage
        #print('price_past', price_past)
        return price_past

    #-------------------------

    def get_game_link(self, game):
        game_link = game.get('href').split('?')[0]
        #print('game_link', game_link)
        return game_link

    def get_steam_id(self, game):
        '''
        <a
        class="search_result_row ds_collapse_flag"
        data-ds-appid="1983230" data-ds-itemkey="App_1983230" data-ds-steam-deck-compat-handled="true" data-ds-tagids="[19,16598,15045,4191,3839,1697,4295]" data-gpnav="item" data-search-page="1" href="https://store.steampowered.com/app/1983230/Vallen/?snr=1_7_7_230_150_1" onmouseout="HideGameHover( this, event, 'global_hover' )" onmouseover="GameHover( this, event, 'global_hover', {&quot;type&quot;:&quot;app&quot;,&quot;id&quot;:1983230,&quot;public&quot;:1,&quot;v6&quot;:1} );">
        '''

        steam_id = game.get('data-ds-appid')
        #print('steam_id', steam_id)
        return steam_id

    def get_img(self, game):
        img = game.find('div', {'class': 'col search_capsule'}).find('img').get('src').split('?')[0]
        #print('img', img)
        return img

    def get_title(self, game):
        title = game.find('span', {'class': 'title'}).get_text()
        #print('title', title)
        return title

    def get_platforms(self, game):
        temp_platforms = game.find('div', {'class': 'col search_name ellipsis'}).find('div').find_all('span')
        platforms = []
        for platform in temp_platforms:
            try:
                platforms.append(platform.get('class')[1])
            except:
                # Тут ['vr_supported'] скипаю это
                pass
        platforms = platforms
        #print('platforms', platforms)
        return platforms

    def get_release_date(self, game):
        try:
            release_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).get_text()
        except:
            release_date = None #!!! записать в модель, что бывает нан!!!
        #print('release_date', release_date)
        return release_date

    def get_price_now(self, game):
        price_now = int(game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'}).get('data-price-final'))
        #print('price_now', price_now)
        return price_now












    def parser(self, url):

        #games_from_one_page = []
        soup = self.get_soup(url)
        items = soup.find_all('a', {'class':"search_result_row ds_collapse_flag"})
        
        #temp_one_page = []    
        for game in items:
            steam_id = self.get_steam_id(game)
            title = self.get_title(game)
            game_link = self.get_game_link(game)
            print(game_link)
            release_date = self.get_release_date(game)
            platforms = self.get_platforms(game)
            img = self.get_img(game)
            price_now = self.get_price_now(game)
            
            try:
                string = game.find('div', {'class': 'col search_price responsive_secondrow'}).get_text().strip()
                if string == 'Демо' or string == 'Бесплатно': # or string == 'Free'
                    continue # пропускаем бесплатные
                elif string == '': #пустой ценник
                    flag_inner_prices = True
                    # ------>    пока скипаю пустые ценники!!!
                else: # Тут нормальный обычный ценник без скидки
                    try: #ищем в базе существующий стим айди, если есть, обновляем только цены
                        sg = SteamGameModel.objects.get(steam_id=steam_id)
                        sg.price_now = price_now
                        sg.discount = 0
                        sg.price_past = 0
                        sg.flag_is_discount = False
                        #---
                        sg.flag_inner_prices = False
                        sg.inner_prices = []
                        #таймстрап должен сам подставляться
                        sg.save()
                        print('обычная цена. обновили ценник')
                        
                    except SteamGameModel.DoesNotExist: #если игры в базе нет, заносим
                        sg = SteamGameModel(
                        steam_id=steam_id,
                        title=title,
                        game_link=game_link,
                        img=img,
                        platforms=platforms,
                        release_date=release_date,
                        price_now=price_now,
                        flag_is_discount=False,
                        discount = 0,
                        price_past = 0,
                        #---
                        flag_inner_prices=False,
                        inner_prices=[],
                        #таймстрап должен сам подставляться
                        ).save()
                        print('обычная цена. внесли в базу')

            except: # Вот тут скидка!
                try: #ищем в базе существующий стим айди, если есть, обновляем только цены
                    discount = self.get_discount(game)
                    price_past = self.get_price_past(game, price_now, discount)

                    sg = SteamGameModel.objects.get(steam_id=steam_id)
                    sg.price_now = price_now
                    sg.flag_is_discount = True
                    sg.discount = discount
                    sg.price_past = price_past
                    #---
                    sg.flag_inner_prices = False
                    sg.inner_prices = []
                    #таймстрап должен сам подставляться
                    sg.save()
                    print('скидки. игра уже есть в базе, обновили ценник')
                except SteamGameModel.DoesNotExist: #если игры в базе нет, заносим
                    discount = self.get_discount(game)
                    price_past = self.get_price_past(game, price_now, discount)
                    
                    sg = SteamGameModel(
                    steam_id=steam_id,
                    title=title,
                    game_link=game_link,
                    img=img,
                    platforms=platforms,
                    release_date=release_date,
                    price_now=price_now,
                    flag_is_discount = True,
                    discount = discount,
                    price_past=price_past,
                    #---
                    flag_inner_prices=False,
                    inner_prices=[],
                    #таймстрап должен сам подставляться
                    ).save()
                    print('скидки. внесли в базу')




def get_games_count():
    """
    Метод возвращает список игр
    """
    #games_count = soup.find('div', {'class': "search_pagination_left"}).get_text().strip().split(' ')[-1]
    #showing 1 - 50 of 122857 - это вообще все игры
    games_count = 100 # пока берем первые 100 игр из всего списка
    return games_count


            
def main():
    # самые свежие игры
    for games in range(0, get_games_count(), 100):
        url = f'https://store.steampowered.com/search/results/?query&start={games}&count=100&sort_by=Released_DESC&hidef2p=1'
        print(url)
        p = Parser()
        p.parser(url)
        #games_from_one_page = parser(url)
        #for game in games_from_one_page:
        #    print(game)

        #самые дорогие игры
        #url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&sort_by=Price_DESC&hidef2p=1'
        #самые ревьюированные игры
        #url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&sort_by=Reviews_ASC&hidef2p=1'
        #самые популярные игры
        #url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&hidef2p=1'



#--------------django--------------

class Command(BaseCommand):
    help = 'SteamGameModel'

    def handle(self, *args, **options):
        main()
'''
if __name__ == '__main__':
    main()
'''

