def redata_logic(one_product):
    redata_dict = {}
    redata_dict["platform"] = 'xbox'
    redata_dict["product_id"] = one_product["ProductId"]
    redata_dict['title'] = one_product['LocalizedProperties'][0]['ProductTitle'] # строго для поля с кодировкой utf8
    # Пока жестко прописываю платформу, написать алгоритм поиска всех возможных подплатформ
    redata_dict["sub_platforms"] = ['XBOX']
    try:
        base_price = int(one_product["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["ListPrice"] * 100)
        redata_dict["base_price"] = base_price
    except:
        base_price = 0
    try:    
        discounted_price = int(one_product["DisplaySkuAvailabilities"][0]["Availabilities"][0]["OrderManagementData"]["Price"]["WholesalePrice"])
        redata_dict["discounted_price"] = discounted_price
        redata_dict["discount"] = int((base_price - discounted_price) / (base_price / 100))  # back percentage
    except:
        redata_dict["discounted_price"] = 0
        redata_dict["discount"] = 0
    try:
        # Квадратная картинка, если вдруг понадобится, сейчас используем прямоугольную с надписью
        # redata_dict["image_square"] = f'https:{one_page_item["LocalizedProperties"][0]["Images"][1]["Uri"]}'
        redata_dict["img"] = f'https:{one_product["LocalizedProperties"][0]["Images"][6]["Uri"]}' # + '?h=60&format=jpg'
    except:
        redata_dict["img"] = None
        #!!! продумать изображение по умолчанию, если парсер не нашел!!!
    #all_pages_items.append(redata_dict)
    #return all_pages_items
    return redata_dict
