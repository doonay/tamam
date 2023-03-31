from django.core.management.base import BaseCommand
from tamam_app.models import PsAllModel

#--------------django--------------

from bs4 import BeautifulSoup
import requests
import json

SESSION = requests.session()

class PsDealParser:

    def parser(self):
        headers = {
            'authority': 'store.playstation.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'AMCVS_BD260C0F53C9733E0A490D45%40AdobeOrg=1; s_ecid=MCMID%7C56170425550306891274349170939569695023; AMCV_BD260C0F53C9733E0A490D45%40AdobeOrg=-1124106680%7CMCIDTS%7C19445%7CMCMID%7C56170425550306891274349170939569695023%7CMCAAMLH-1680602370%7C6%7CMCAAMB-1680602370%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1680004771s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; at_check=true; s_cc=true; eucookiepreference=accept; sc_emcid=pa-co-422379; sc_emcid_login=pa-co-422379; sc-cmp-id=pa-co-422379; sc-cmp-type=emcid; _evga_9736={%22uuid%22:%228cc03ca20058d760%22}; _sfid_c0f4={%22anonymousId%22:%228cc03ca20058d760%22%2C%22consents%22:[]}; _gcl_au=1.1.1388417241.1679997598; _fbp=fb.1.1679997597951.1955744231; s_fid=0CE6E77AB84BF040-01BDCE87AADEA036; _gcl_aw=GCL.1679999041.CjwKCAjwoIqhBhAGEiwArXT7K5DL3tHQKfyW36AxUkCJdRmesn504coDGoTWbyz-MOPOyNS3JvyxqBoCpIYQAvD_BwE; _gcl_dc=GCL.1679999041.CjwKCAjwoIqhBhAGEiwArXT7K5DL3tHQKfyW36AxUkCJdRmesn504coDGoTWbyz-MOPOyNS3JvyxqBoCpIYQAvD_BwE; bm_sz=749D0D3DC1ECE1DCAD8FA87A8CD76D3A~YAAQL16MT00ihhSHAQAA873KJxOU1iTek2oPHwsseL8Pkfwrq8rfYfeTmQvU3p7ZdPLBc67Crlb+6oKOFsSbaBynQAnoJ2BNz09gyjKDkCT0dGuNJ4trfSo2ClWZ6al+bN4JrdWZnDFsuV/DRPwISwlphfFeOR0331gENulGrPHIie4QcNb8LxRFec/zDgnaehoi7bw7YkOuN67/0IkBlaU5x0haVBfUqSTFX1e+br652naQqEOZhbc7B4ZZ4xaVes4pb1UJMT8g+6xIBKEcOD/qQzT0T+7HYx7Lyp1nT5dSX6uqX0DKl1VHyVtf/HtXpym6JqIZG0fo+hS5iTzFfLmXzLp0Hbz++GXqSpqDbphW8WAh9sidqSMpUpmkjfOL9dXmX0PWRaxWEi8uupGKJIfd5U1Mg77x25s3zy5TppY4dI1i9/Tna8BE9pYs7RyzVl+m2fyo9p1q6ERp2v8iTugNHzBD3WyMmow8ua+7TNtyg4o+K29myc4UB6tHb+uFSq64RskhAg1UhOx4ctf77cNAhGiOlaBDWzQJmn3dU9b69EqQ+qCa0uc8QLgBbVsuwf/AuA0Fhwa8B6CTHgjjOrIAEoAqW7swzMSEd2Ahxhhcr6GFbNv5mY2e+SX2Ck0=~3682608~4535873; gpv_Page=web%3Apdc%3Asite-map; s_sq=%5B%5BB%5D%5D; mbox=session#48f09d02bfa94abda6a4d4c0181400c0#1680001983|PC#48f09d02bfa94abda6a4d4c0181400c0.35_0#1743243832; da_sid=6CF1C4508E3AAE8DF0F3AA13B371D08764|3|0|3; da_lid=5FC2F7639A7AEA1665A2BB99F1739A8CD7|0|0|0; da_intState=0; _abck=FBA7B473171F1BF0395DCB9441080568~-1~YAAQ5WfAwXpbyhKHAQAADJLiJwnrulwkZvSYtfsj7ogEYCn2J+2vDeVZNunLInUfg44XngsvWT3DJR/wD+ffwjXaBL11wyYqOukE+km0tKyvwj+17moYVr4mkehtKQUhSe8Gw8Ke7aulyA9UQz7CIf/lXafV9xSsce0y6bncIAo+6XwglxvO61BrXCi5s0KPHTJACTloIHFQXNkN7eNI4MCxiKLBQZffxcJtP9D3m0oE3TQ7NlyvXHZ0P84VEfml4ZKmrZHTCkDJbpd2ERVcMOb7PBGtJ2dJ2v4bx/cXrvtSiRgEedeVoz85TQXSyqaEK9JZVwSc4TZTiZ4026sD0r0FbKShkYO1x8pYwgmtBk64TxeSvFwNZxxHmYl4ivvbZfNIaZt31TmxmoPytRmaub4qi/h5uGstnwD6FK0U/5iFqRViVhG3l8/ZW8BllVUBDUBRrHjfNIiUmJfu4KWtJSqyI3Strw==~-1~-1~-1',
            'if-none-match': 'W/"510ba-mamOeiZ/NtieptnKAS3GBxIbCYA"',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        last_game = 1
        game_count = 0
        page_count = 1

        while game_count <= last_game:
            # Внимание! В РФ адрес может быть другой!
            url = f'https://store.playstation.com/tr-tr/category/44d8bb20-653e-431e-8ad0-c0a365f68d2f/{page_count}'
            r = SESSION.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            
            #last_game = int(soup.find('div', {'class': "psw-t-body psw-c-t-2"}).get_text().split(' ')[0])
            #print(soup.find('div', {'class': ["psw-t-body", "psw-c-t-2"]}))
            
            json_string = soup.find('script', {'id': "__NEXT_DATA__"}).get_text() #id="__NEXT_DATA__" type="application/json">
            json_data = json.loads(json_string)
            
            try:
                last_game = int(json_data['props']['apolloState'][f'$CategoryGrid:44d8bb20-653e-431e-8ad0-c0a365f68d2f:tr-tr:{str(game_count)}:24.pageInfo']['totalCount'])
            except KeyError:
                print(f'Скорее всего это финиш и последняя страница не имеет 24 игры.\nlast_game = {last_game}, game_count = {game_count}, page_count = {page_count}')
                break

            temp_products = json_data['props']['apolloState'][f'CategoryGrid:44d8bb20-653e-431e-8ad0-c0a365f68d2f:tr-tr:{str(game_count)}:24']['products']
            products = []
            for p in temp_products:
                products.append(p['id'])

            for product in products:
                title = json_data['props']['apolloState'][product]['name']
                price_id = json_data['props']['apolloState'][product]['price']['id']
                if json_data['props']['apolloState'][price_id]['basePrice'] == 'Uygun Değil':
                    print('[', game_count, '/', last_game, ']','Нет в наличии', title)
                    game_count += 1
                    continue
                elif json_data['props']['apolloState'][price_id]['basePrice'] == 'Ücretsiz':
                    print('[', game_count, '/', last_game, ']','Бесплатно', title)
                    game_count += 1
                    continue
                else:    
                    base_price = int(json_data['props']['apolloState'][price_id]['basePrice'].strip().replace(',','').replace('.','').replace(' TL', ''))

                media_id = json_data['props']['apolloState'][product]['media'][-1]['id']

                title = json_data['props']['apolloState'][product]['name']

                try:
                    discount = json_data['props']['apolloState'][price_id]['discountText'].strip().replace('-%', '')
                except AttributeError:
                    print(title, 'пишет, что скидки нет. Проверить!')
                    discount = 0

                if json_data['props']['apolloState'][price_id]['discountedPrice'].strip() == 'Dahil':
                    print('[', game_count, '/', last_game, ']','Включая (дословно)', title)
                    discounted_price = 0
                else:
                    discounted_price = int(json_data['props']['apolloState'][price_id]['discountedPrice'].strip().replace(',','').replace('.','').replace(' TL', ''))

                psgame = PsAllModel(
                    ps_id = json_data['props']['apolloState'][product]['id'],
                    title = title,
                    platforms = json_data['props']['apolloState'][product]['platforms']['json'],
                    base_price = base_price,
                    discounted_price = discounted_price,
                    discount = discount,
                    is_free = json_data['props']['apolloState'][price_id]['isFree'],
                    is_exclusive = json_data['props']['apolloState'][price_id]['isExclusive'],
                    is_tied_to_subscription = json_data['props']['apolloState'][price_id]['isTiedToSubscription'],
                    img = json_data['props']['apolloState'][media_id]['url']
                    #---
                    #таймстрап должен сам подставляться
                    ).save()
                print('[', game_count, '/', last_game, ']','Внесли в базу', title)
                game_count += 1
            page_count += 1


#--------------django--------------

class Command(BaseCommand):
    help = 'PsAllModel'

    def handle(self, *args, **options):
        parser = PsDealParser()
        parser.parser()

