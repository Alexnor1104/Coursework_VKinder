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

