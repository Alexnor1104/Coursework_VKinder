from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

with open('../file/token2.txt', 'r') as file_object:
    token2 = file_object.read().strip()

vk = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            # Сообщение от пользователя(прослушивание)
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "как дела":
                write_msg(event.user_id, "Отлично, а у тебя?")
            elif request == "отлично":
                write_msg(event.user_id, "Это просто великолепно!")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, 'Введи "help" для вызова команд для меня!')
