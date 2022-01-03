import vk_api
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


def get_user_search():

    fields = session.method("users.search", {
        "fields": ['city,sex,photo_400_orig,bdate,domain,activities,photo_id'],
        "count": "5",
        "sex": int('1'),
        "age_to": 17,
        "status": 6,
        'hometown': 'Краснодар',
        'offset': 0

    })

    # pprint(fields['items'])
    for domain in fields['items']:
        user_id = domain['id']
        domains = domain['domain']
        photos = domain['photo_id']

        # pprint(photos)
        # print(f'Ссылка на профиль: https://vk.com/{domains}')

        photo = 'photo{}_{}'.format(photos, user_id)
        links = f'Ссылка на профиль: https://vk.com/{domains}'

        return photo, links


pprint(get_user_search())


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
            # photo = attachments.append(get_user_search()[0])
            #

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
                write_msg(event.user_id, "Это бот! Введи 'Профиль!'")
            elif request == "профиль":
                write_msg(event.user_id, get_user_search()[1])
                write_msg(event.user_id, attachments.append(get_user_search()[0]))
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == "help":
                write_msg(event.user_id,
                          """
                          возраст: до                                 
                                положительное число
                          
                          пол:     
                                1 — женщина;
                                2 — мужчина;
                                0 — любой (по умолчанию)
                          
                          город:
                           название города строкой
                          Ye gjcvj
                          семейное положение: 
                                1 — не женат (не замужем);
                                2 — встречается;
                                3 — помолвлен(-а);
                                4 — женат (замужем);
                                5 — всё сложно;
                                6 — в активном поиске;
                                7 — влюблен(-а);
                                8 — в гражданском браке.
                          """)
            else:
                write_msg(event.user_id, 'Введи "help" для вызова команд для меня!')
