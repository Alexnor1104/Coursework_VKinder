from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

with open('../file/token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('../file/token2.txt', 'r') as file_object:
    token2 = file_object.read().strip()

vk = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk)
session = vk_api.VkApi(token=token)


def get_users(user_id):
    """Получаем данные от пользователя"""
    user_ids = session.method('users.get', {
        'user_ids': user_id,
        'fields': ['verified,sex,bdate,city']

    })
    return user_ids[0]


def get_users_check():
    data = get_users(id_user)

    if 'title' not in data['city'] or 'city' not in data:
        write_msg(id_user, 'Веди город:')
        # ждать ответа
        data['city']['title'] = request

    if data['sex'] == 2:
        data['sex'] = 1
    elif data['sex'] == 0 or 'sex' not in data:
        # ждать ответа
        write_msg(id_user, 'Веди пол:')
        data['sex'] = request
    else:
        data['sex'] = 2

    write_msg(id_user, 'Введи возраст:')

    # тут он должен остановится и ждать ответа от пользователя (типа функции input())
    data['age'] = int(request)  # по умолчанию вставляет последний введенный результат (поиск)

    return data


def get_user_search():
    data = get_users_check()
    fields = session.method("users.search", {
        "fields": ['city,sex,photo_400_orig,bdate,domain,activities,photo_id'],
        "count": "10",
        "sex": data['sex'],
        # "age_to": data['age'],
        "age_to": 30,
        "status": data['verified'],
        'hometown': data['city']['title'],

    })

    for domain in fields['items']:
        if not domain['is_closed']:
            user_id = domain['id']
            domains = domain['domain']
            # photos = domain['photo_id']
            user_name = domain['first_name']

            # photo = 'photo{}_{}'.format(photos, user_id)
            links = f'Ссылка на профиль: https://vk.com/{domains}'

            return user_id, links, user_name


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
            id_user = event.user_id

            attachments = []
            add_photo = ''

            if request == 'привет':
                write_msg(id_user, f'Привет {get_users(id_user)["first_name"]}')
            elif request == 'поиск':
                users_ids = get_user_search()[0]
                links_user = get_user_search()[1]
                write_msg(id_user, "Идет поиск кандидата...")
                write_msg(id_user, links_user)
                write_msg(id_user, f'Имя кандидата: {get_user_search()[2]}')


            else:
                write_msg(id_user, f'{get_users(id_user)["first_name"]}, Введи "Поиск"')
