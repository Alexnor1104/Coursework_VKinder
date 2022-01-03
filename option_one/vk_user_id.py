from users_data import *
from vk_photo import get_photo
from random import randrange
import db


# users_id = '107265371'

def get_users_check():
    data = get_users(event.user_id)
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
    data['age'] = 25
    if data['sex'] == 2:
        data['sex'] = 1
    elif data['sex'] == 0 or 'sex' not in data:
        print('Введите пол: ')
    else:
        data['sex'] = 2

    return data


def get_user_search():
    data = get_users_check()
    fields = session.method("users.search", {
        "fields": ['city,sex,photo_400_orig,bdate,domain,activities,photo_id'],
        # "count": "10",
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

        check = db.read_users_id()

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
            add_photo = ''

            if request == 'привет':
                write_msg(event.user_id, f'Привет, {get_users(event.user_id)["first_name"]}'
                                         f'! Для поиска кандидатов введи "Поиск"')

            elif request == 'поиск':
                users_ids = get_user_search()[0]
                links_user = get_user_search()[1]
                # write_msg(event.user_id, f"Ваш id, {event.user_id}")
                write_msg(event.user_id, "Идет поиск кандидата...")
                write_msg(event.user_id, links_user)
                write_msg(event.user_id, f'Имя кандидата: {get_user_search()[2]}')

                # Добавляет топ3 фото кандидата:
                for photo in get_photo(users_ids):
                    add_photo = attachments.append('photo{}_{}_{}'.format(users_ids, photo, users_ids))
                write_msg(event.user_id, add_photo)

                # Добавляем найденного кандидата в таблицу:
                db.insert_users(users_ids, get_user_search()[2], links_user)

            # временный запрос фото, для проверки (выводит список id):
            elif request == 'photo':
                write_msg(event.user_id, f'Список id фото топ3 {get_photo(get_user_search()[0])}')

            # запрос id пользователя для разработчика:
            elif request == 'user_id':
                write_msg(event.user_id, f'Ваш id {event.user_id}, id кандидата {get_user_search()[0]}')

            else:
                write_msg(event.user_id, f'{get_users(event.user_id)["first_name"]}! Введи "Поиск"')

# print(get_user_search())
