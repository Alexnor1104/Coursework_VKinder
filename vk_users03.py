from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint

with open('file/token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('file/token2.txt', 'r') as file_object:
    token2 = file_object.read().strip()

session = vk_api.VkApi(token=token)
vk = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def get_users(user_id):
    user_ids = session.method('users.get', {
        'user_ids': user_id,
        'fields': ['verified,sex,bdate,city']

    })

    user_data = []

    for users in user_ids[0].values():
        user_data.append(users)

    return user_data


def get_user_search():
    data = get_users(event.user_id)
    fields = session.method("users.search", {
        "fields": ['city,sex,photo_400_orig,bdate,domain,activities,photo_id'],
        "count": "5",
        "sex": data[5],
        "age_to": 19,
        "status": data[6],
        'hometown': data[-1]['title'],
    })
    print(data)
    # pprint(fields['items'])
    photo_oll = []
    links_oll = []
    for domain in fields['items']:
        user_id = domain['id']
        domains = domain['domain']
        photos = domain['photo_id']

        photo = 'photo{}_{}'.format(photos, user_id)
        links = f'Ссылка на профиль: https://vk.com/{domains}'

        photo_oll.append(photo)
        links_oll.append(links)
    return photo_oll, links_oll


for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            # Сообщение от пользователя(прослушивание)
            request = event.text.lower()

            if request == 'поиск':
                # write_msg(event.user_id, f"Ваш id, {event.user_id}")
                write_msg(event.user_id, f"{get_users(event.user_id)[0]}! Идет поиск кандидатов...")

                for link in get_user_search()[1]:
                    write_msg(event.user_id, link)

            elif request == 'привет':
                write_msg(event.user_id, f'Привет, {get_users(event.user_id)[0]}! Для поиска кандидатов введи "Поиск"')

            else:
                write_msg(event.user_id, f'Привет {get_users(event.user_id)[0]}! Введи "Поиск"')