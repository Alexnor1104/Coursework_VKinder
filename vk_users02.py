import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType

from pprint import pprint

with open('file/token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('file/token2.txt', 'r') as file_object:
    token2 = file_object.read().strip()

session = vk_api.VkApi(token=token)
vk = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk)


users_id = '668938039'


def get_users(user_id):
    user_ids = session.method('users.get', {
        'user_ids': user_id,
        'fields': ['verified,sex,bdate,city']

    })

    user_data = []

    for users in user_ids[0].values():
        user_data.append(users)

    return user_data


print(get_users(users_id))

# def check_condition():
#     if not get_users(users_id)[8]['title']:
#         print('Введите город')
#     elif not get_users(users_id)[7]:
#         print('Введите год')


def get_user_search():
    data = get_users(users_id)
    fields = session.method("users.search", {
        "fields": ['city,sex,photo_400_orig,bdate,domain,activities,photo_id'],
        "count": "5",
        "sex": data[5],
        "age_to": 25,
        "status": data[6],
        'hometown': data[-1]['title'],

    })

    pprint(fields['items'])
    photo_oll = []
    links_oll = []
    for domain in fields['items']:
        user_id = domain['id']
        domains = domain['domain']
        photos = domain['photo_id']
        user_name = domain['first_name']

        pprint(user_name)
        # print(f'Ссылка на профиль: https://vk.com/{domains}')

        photo = 'photo{}_{}'.format(photos, user_id)
        links = f'Ссылка на профиль: https://vk.com/{domains}'

        photo_oll.append(photo)
        links_oll.append(links)
    return photo_oll, links_oll


# pprint(get_user_search())


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                                'attachment': ','.join(attachments)
                                })


for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            # Сообщение от пользователя(прослушивание)
            request = event.text.lower()
            attachments = []
            add_photo = []
            # add_links = get_user_search()[1]
            # photo = attachments.append(get_user_search()[0])

            if request == "привет":
                write_msg(event.user_id, f"Хай, {get_users(users_id)[0]}")
                write_msg(event.user_id, 'Это бот! Введи "поиск!"')
            elif request == "поиск":
                # for i in get_user_search()[0]:
                #     add_photo = attachments.append(i)
                # write_msg(event.user_id, add_photo)

                for link in get_user_search()[1]:
                    write_msg(event.user_id, link)

            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, f'Привет {get_users(users_id)[0]}! введи "Поиск"')


# if __name__ == '__main__':
    # print(get_user_search())
    # print(get_users(users_id))
    # check_condition()
