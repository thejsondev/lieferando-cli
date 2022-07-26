from doctest import ELLIPSIS_MARKER
from pydoc import resolve
from matplotlib import category
from art import text2art
import requests
import pgeocode
import os
def __main__():
    os.system('clear')
    postal_code = input("Enter your postal code: \n")
    #request get url
    url = "https://public.opendatasoft.com/api/records/1.0/search/?q="+postal_code+"&rows=0&facet=plz_name&dataset=georef-germany-postleitzahl"
    #request get url
    response = requests.get(url)
    #convert json to python dict
    data = response.json()
    print(data)
    my_area = find_my_area(postal_code)
    my_area_restaurants = restaurants_near_me(my_area['deliveryAreaId'],my_area['postalCode'],my_area['lat'],my_area['lng'])['restaurants']
    local_restaurants = []
    for i,restaurant in enumerate(my_area_restaurants):
        local_restaurants.append(my_area_restaurants[restaurant]['primarySlug'])
        print(str(i+1) + ' - ' + my_area_restaurants[restaurant]['primarySlug'])
    restaurant_number = int(input("Enter the number of the restaurant you want to order from: \n"))
    os.system('clear')
    restaurant_name = local_restaurants[restaurant_number-1]
    restaurant_data = get_restaurants(restaurant_name)
    restaurant_title = restaurant_data['brand']['name']
    restaurant_address = restaurant_data['location']['streetName'] + ' ' + restaurant_data['location']['streetNumber'] + '\n' + restaurant_data['location']['postalCode'] + ' ' + restaurant_data['location']['city']
    print(text2art(restaurant_title) + '\n')
    print('Restaurant: ' + restaurant_title)
    print('Address: ' + restaurant_address + '\n')
    print('\n\n')
    print('Categoies\n---------------\n')
    menu = restaurant_data['menu']
    categories = menu['categories']
    for i,category in enumerate(categories):
        print(str(i+1) + ' - ' + category['name'])
    category_number = int(input("Enter the number of the category you want to order from: \n"))
    os.system('clear')

    product_ids = categories[category_number-1]['productIds']
    local_products = []
    for i,product_id in enumerate(product_ids):
        local_products.append(product_id)
        print(str(i+1) + ' - ' + menu['products'][product_id]['name'] + ' ', end = '')
        for index,j in enumerate(menu['products'][product_id]['variants']):
            if(j['name']):
                print(j['name'] + ' ', end = '')
            print(str(j['prices']['delivery']) + '€'  , end = '')
            if len(menu['products'][product_id]['variants']) > 1 and index < len(menu['products'][product_id]['variants'])-1:
                print('|', end = '')
        print('\n')
    product_number = int(input("Enter the number of the product you want to order from: \n"))
    os.system('clear')
    product_id = local_products[product_number-1]


def get_restaurants(restaurant_name):
    headers = {
        'authority': 'cw-api.takeaway.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'cache-control': 'no-cache',
        'origin': 'https://www.lieferando.de',
        'pragma': 'no-cache',
        'referer': 'https://www.lieferando.de/',
        'sec-ch-ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'x-country-code': 'de',
        'x-language-code': 'en',
        'x-requested-with': 'XMLHttpRequest',
        'x-session-id': '1ac81442-0bf0-4f7a-8d27-94cd8907460c',
    }

    params = {
        'slug': restaurant_name,
    }

    response = requests.get('https://cw-api.takeaway.com/api/v31/restaurant', params=params, headers=headers)
    return response.json()
def find_my_area(postalcode):
    headers = {
        'authority': 'cw-api.takeaway.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'de',
        'cache-control': 'no-cache',
        'origin': 'https://www.lieferando.de',
        'pragma': 'no-cache',
        'referer': 'https://www.lieferando.de/',
        'sec-ch-ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'x-country-code': 'de',
        'x-language-code': 'de',
        'x-requested-with': 'XMLHttpRequest',
        'x-session-id': '1ac81442-0bf0-4f7a-8d27-94cd8907460c',
    }

    params = {
        'locationSlug': postalcode,
    }

    response = requests.get('https://cw-api.takeaway.com/api/v31/location/validate', params=params, headers=headers)
    return response.json()
def restaurants_near_me(area_id,postal_code,lat,lng):
    headers = {
        'authority': 'cw-api.takeaway.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'de',
        'cache-control': 'no-cache',
        'origin': 'https://www.lieferando.de',
        'pragma': 'no-cache',
        'referer': 'https://www.lieferando.de/',
        'sec-ch-ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'x-country-code': 'de',
        'x-language-code': 'de',
        'x-requested-with': 'XMLHttpRequest',
        'x-session-id': '1ac81442-0bf0-4f7a-8d27-94cd8907460c',
    }

    params = {
        'deliveryAreaId': area_id,
        'postalCode': postal_code,
        'lat': lat,
        'lng': lng,
        'limit': '0',
        'isAccurate': 'true',
    }

    response = requests.get('https://cw-api.takeaway.com/api/v31/restaurants', params=params, headers=headers)
    return response.json()
__main__()