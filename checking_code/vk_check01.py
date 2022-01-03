import vk_api
import re
import datetime
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType

from pprint import pprint

with open('../file/token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('../file/token2.txt', 'r') as file_object:
    token2 = file_object.read().strip()

session = vk_api.VkApi(token=token)
vk = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk)

users_id = '107265371'


def get_users(user_id):
    user_ids = session.method('users.get', {
        'user_ids': user_id,
        'fields': ['verified,sex,bdate,city']

    })

    return user_ids[0]


# get_users(users_id)
print(get_users(users_id))


def get_users_check():
    data = get_users(users_id)
    if 'title' not in data['city'] or 'city' not in data:
        data['city']['title'] = input('Введите город: ')

    # if 'bdate' not in data or not re.findall(r"\d{1,2}.\d{1,2}.\d{4}", data['bdate']):
    #     # bdate = input('Введите год: ')
    #     bdate = data['bdate'] = input('Введите год "дд.мм.гггг": ')
    # else:
    #     print('Год верен!')
    # Сегодняшняя дата:
    # a = datetime.datetime.today().year
    # print(a)
    # data['age'] = int(input('Введите возраст: '))
    data['age'] = 30
    if data['sex'] == 2:
        data['sex'] = 1
    elif data['sex'] == 0 or 'sex' not in data:
        print('Введите пол: ')
    else:
        data['sex'] = 2

    return data
    # print(data['sex'])


# get_users_check()


def get_user_search():
    data = get_users_check()
    fields = session.method("users.search", {
        "fields": ['city,sex,photo_400_orig,bdate,domain,activities,photo_id'],
        "count": "10",
        "sex": data['sex'],
        "age_to": data['age'],
        "status": data['verified'],
        'hometown': data['city']['title'],

    })
    # print(data)

    # pprint(fields['items'])
    photo_oll = []
    links_oll = []
    # if fields['items']['is_closed'] == 'True':
    #     print('Профиль закрыт')
    for domain in fields['items']:

        check = [436396707, 423523572, 298753623, 229542919, 178089053]


        # check = db.read_users_id()
        if not domain['is_closed'] and domain['id'] not in check:
            user_id = domain['id']
            domains = domain['domain']
            # photos = domain['photo_id']
            user_name = domain['first_name']

            # photo = 'photo{}_{}'.format(photos, user_id)
            links = f'Ссылка на профиль: https://vk.com/{domains}'

            links_oll.append(user_id)
            links_oll.append(links)
            links_oll.append(user_name)

    return links_oll[:3]

        # return photo_oll, links_oll


print(get_user_search())
print(get_user_search()[0])
print(get_user_search()[1])
print(get_user_search()[2])
