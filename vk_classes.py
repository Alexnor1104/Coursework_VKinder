import requests
from pprint import pprint

with open('file/token.txt', 'r') as file_object:
    token = file_object.read().strip()


def search_groups(sorting=3):
    params = {
        # 'q': q,
        'access_token': token,
        'v': '5.131',
        'sort': sorting,
        'count': 5,
        'fields': 'sex,relation,bdate,city,photo_400_orig,first_name,domain,about',

        'age_to': 20,
        'sex': 0,
        'hometown': 'Краснодар',
        'status': 6,

    }

    req = requests.get('https://api.vk.com/method/users.search', params).json()
    # print(req)
    req = req['response']['items']
    return req


target_groups = search_groups()
pprint(target_groups)

