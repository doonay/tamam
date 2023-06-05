import aiohttp
import asyncio
from tamam_logger import tamam_logger
from async_db_insert import async_db_insert
#from db_insert import db_insert_batch
import json



async def get_product_data(session, ids_list):
    url = f'https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={ids_list}&market=RU&languages=RU-RU&MS-CV=DGU1mcuYo0WMMp+F.1'
    async with session.get(url) as response:
        product_data = await response.json()
    return product_data['Products']

async def get_all_products():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=20)) as session:
        url = 'https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=ru-ru&market=RU'
        async with session.get(url) as response:
            all_xbox_games_ids = await response.json()
        #ids_list = [game['id'] for game in all_xbox_games_ids[1:]]
        ids_list = []
        for game in all_xbox_games_ids[1:]:
            ids_list.append(game['id'])

        tasks = []
        chunk_size = 10  # Количество идентификаторов в пакете
        #id_chunks = [ids_list[i:i + chunk_size] for i in range(0, len(ids_list), chunk_size)]
        # Создаем пустой список для хранения фрагментов идентификаторов
        id_chunks = []
        # Итерируемся по диапазону от 0 до длины списка идентификаторов (ids_list)
        # с шагом, равным размеру фрагмента (chunk_size)
        for i in range(0, len(ids_list), chunk_size):
            # Создаем фрагмент идентификаторов, включая элементы списка от i до i + chunk_size
            chunk = ids_list[i:i + chunk_size]
            # Добавляем фрагмент в список id_chunks
            id_chunks.append(chunk)

        for chunk in id_chunks:
            tasks.append(get_product_data(session, ','.join(chunk)))

        product_results = await asyncio.gather(*tasks)
        '''
        print(type(product_results))
        with open('test_products.json', 'w', encoding='utf8') as file:
            json.dump(product_results[0][0], file, ensure_ascii=False)
        '''
        all_pages_items = []
        for all_pages_item in product_results: 
            #one_page_items = []
            for one_page_item in all_pages_item:
                redata_dict = {}

                redata_dict["product_id"] = one_page_item["ProductId"]
                redata_dict["title"] = one_page_item["LocalizedProperties"][0]["SortTitle"]
                # Пока жестко прописываю платформу, ибо заведомо знаю, что это икс бокс
                redata_dict["platforms"] = ['XBOX']
                try:
                    base_price = int(one_page_item["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["ListPrice"] * 100)
                    redata_dict["base_price"] = base_price
                except:
                    base_price = 0
                try:    
                    discounted_price = int(one_page_item["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["WholesalePrice"])
                    redata_dict["discounted_price"] = discounted_price
                    redata_dict["discount"] = int((base_price - discounted_price) / (base_price / 100))  # back percentage
                except:
                    redata_dict["discounted_price"] = 0
                    redata_dict["discount"] = 0
                try:
                    # Квадратная картинка, если вдруг понадобится, сейчас используем прямоугольную с надписью
                    # redata_dict["image_square"] = f'https:{one_page_item["LocalizedProperties"][0]["Images"][1]["Uri"]}'
                    redata_dict["img"] = f'https:{one_page_item["LocalizedProperties"][0]["Images"][6]["Uri"]}' # + '?h=60&format=jpg'
                except:
                    redata_dict["img"] = None
                    #!!! продумать изображение по умолчанию, если парсер не нашел!!!
                all_pages_items.append(redata_dict)

        TABLE_NAME = __name__
        # Запуск асинхронной функции из синхронной функции
        asyncio.run(async_db_insert(TABLE_NAME, all_pages_items))



        with open('test_products.txt', 'w', encoding='utf8') as file:
            json.dump(all_pages_items, file, ensure_ascii=False)
        '''
        count = 1
        for p in product_results:
            for z in p:
                print(count, type(z))
                count+=1
                with open('test_products.json', 'w', encoding='utf8') as file:
                    json.dump(product_results, file, ensure_ascii=False)
        '''

        '''
        with open('test_products.txt', 'a', encoding='utf8') as file:
            file.write(str(products[0]))
            file.write('---------------------------------------')
            file.write(str(products[1]))
        '''
        #with open('test_products.txt', 'a', encoding='utf8') as file:
        #    file.write(str(product))
        '''
        products = []
        print(type(product_results)) #list
        print(type(product_results[0])) #list
        #list[list[dict{}]]
        cards = product_results[0][0]

        print(cards, type(cards))
        '''
        #for card in cards:
        '''
            game_id = card['ProductId']
            print(game_id)
            title = card['LocalizedProperties'][0]['ProductTitle']
            print(title)
            platforms = ['XBOX']
            print(platforms)
            float_base_price = card["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["ListPrice"]
            base_price = int(float_base_price * 100)
            print(base_price)
            try:
                float_discounted_price = card["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["WholesalePrice"]
                discounted_price = int(float_discounted_price * 100)
                print(discounted_price)
                discount = int((base_price - discounted_price) / (base_price / 100))  # back percentage
                print(discount)
            except:
                discounted_price = 0
                print(discounted_price)
                discount = 0
                print(discount)
            img = 'https:' + \
                card['LocalizedProperties'][0]['Images'][4]['Uri'] + \
                '?h=60&format=jpg'
            print(img)
            
        '''
        '''
        for result in product_results:
            products.extend(result)
        '''
    #return products

def xbox_parser():
    company = 'xbox'
    games_list = []
    products = asyncio.run(get_all_products())
    #products = fileparse()
    game_count = 1
    #last_game = len(products)
    
    '''
    for card in products:
        game_id = card['ProductId']
        title = card['LocalizedProperties'][0]['ProductTitle']
        platforms = ['XBOX']
        float_base_price = card["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["ListPrice"]
        base_price = int(float_base_price * 100)
        try:
            float_discounted_price = card["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["WholesalePrice"]
            discounted_price = int(float_discounted_price * 100)
            discount = int((base_price - discounted_price) / (base_price / 100))  # back percentage
        except:
            discounted_price = 0
            discount = 0
        img = 'https:' + \
            card['LocalizedProperties'][0]['Images'][4]['Uri'] + \
            '?h=60&format=jpg'
        
        games_dict = {
            'game_id': game_id,
            'title': title,
            'platforms': platforms,
            'base_price': base_price,
            'discounted_price': discounted_price,
            'discount': discount,
            'img': img
        }
        games_list.append(games_dict)

        tamam_logger("INFO", f"[{game_count}/{last_game}] '{title}' was successfully scraped")
        game_count += 1

    tamam_logger("INFO", f"Adding {len(games_list)} games to database:")
    #db_insert_batch(company, games_list)
    with open('test_products.txt', 'w', encoding='utf8') as file:
        file.write(str(games_list))
    '''
if __name__ == '__main__':
    #xbox_parser()

    test_data = [
        {
            "product_id": "4TEST",
            "title": "4The Walking Test",
            "platforms": ["XBOX"],
            "base_price": 1998,
            "discounted_price": 13,
            "discount": 99,
            "img": "4https://store-image"
        }
    ]
    
    import os
    TABLE_NAME = os.path.basename(__file__).split('.')[0]
    print(TABLE_NAME)
    asyncio.run(async_db_insert(TABLE_NAME, test_data))