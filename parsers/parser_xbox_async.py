import aiohttp
import asyncio
from db_insert_batch import db_insert_batch


async def get_all_xbox_game_ids(session):
    url = 'https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=ru-ru&market=RU'
    async with session.get(url) as response:
        all_xbox_games_ids = await response.json()
        ids_list = [game['id'] for game in all_xbox_games_ids[1:]]
        return ','.join(ids_list)


async def get_product_data(session, ids_list):
    url = f'https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={ids_list}&market=RU&languages=RU-RU&MS-CV=DGU1mcuYo0WMMp+F.1'
    async with session.get(url) as response:
        product_data = await response.json()
        return product_data['Products']


async def xbox_parser():
    company = 'xbox'
    games_list = []
    try:
        async with aiohttp.ClientSession() as session:
            ids_list = await get_all_xbox_game_ids(session)
            product_data = await get_product_data(session, ids_list)
            game_count = 1
            last_game = len(product_data)
            for card in product_data:
                game_id = card['ProductId']
                title = card['LocalizedProperties'][0]['ProductTitle']
                platforms = ['XBOX']
                float_base_price = card["DisplaySkuAvailabilities"][0][
                    "Availabilities"][0]["OrderManagementData"]["Price"]["ListPrice"]
                base_price = int(float_base_price * 100)

                try:
                    float_discounted_price = card["DisplaySkuAvailabilities"][0][
                        "Availabilities"][0]["OrderManagementData"]["Price"]["WholesalePrice"]
                    discounted_price = int(float_discounted_price * 100)
                    discount = int((base_price - discounted_price) /
                                   (base_price / 100))  # back percentage
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

                print(
                    f'[INFO] [{game_count}/{last_game}] "{title}" was successfully scraped')
                game_count += 1

    except aiohttp.ClientError as e:
        print(f'[ERROR] An error occurred during the request: {str(e)}')

    print(f'[INFO] Adding {len(games_list)} games to database...')
    db_insert_batch(company, games_list)
    print('done!')


async def test_xbox_parser():
    company = 'xbox'
    games_list = []

    # ----test2.1
    games_dict = {
        'game_id': "9MT8PTGVHX2P",
        'title': "Halo: Коллекция Мастера Чифа",
        'platforms': "{XBOX}",
        'base_price': 3997,
        'discounted_price': 0,
        'discount': 100,
        'img': "https://store-images.s-microsoft.com/image/apps.16930.13817186670444302.148c432a-9fce-4c7d-bf13-8a2bd3a527b3.99d16324-9915-41d7-a388-fa5dd98940cb?h=60&format=jpg"
    }
    # ----test2.2
    '''
    games_dict = {
        'game_id': "9MT8PTGVHX2P",
        'title': "Halo: Коллекция Мастера Чифа",
        'platforms': "{XBOX}",
        'base_price': 0,
        'discounted_price': 0,
        'discount': 0,
        'img': "https://store-images.s-microsoft.com/image/apps.16930.13817186670444302.148c432a-9fce-4c7d-bf13-8a2bd3a527b3.99d16324-9915-41d7-a388-fa5dd98940cb?h=60&format=jpg"
    }
    '''
    # ----test3
    # ----test3

    games_list.append(games_dict)
    print(f'[INFO] Adding {len(games_list)} games to database...')
    db_insert_batch(company, games_list)
    print('done!')


if __name__ == '__main__':
    asyncio.run(xbox_parser())
    # asyncio.run(test_xbox_parser())
