# Получить топ-3 фотографий пользователя:
import vk_api

with open('../file/token.txt', 'r') as file_object:
    token = file_object.read().strip()

session = vk_api.VkApi(token=token)

users_id = '107265371'


def get_photo(user_id):
    """Получение топ3 фото пользователя"""
    photo_id = session.method('photos.get', {'owner_id': user_id,
                                             'album_id': 'wall',
                                             'extended': 1,
                                             # 'count': 3,

                                             })
    list_top = []
    # print(photo_id['items'])
    for photo in (photo_id['items']):
        id_ph = photo['id']
        likes = photo['likes']['count']
        comments = photo['comments']['count']
        # print(photo['sizes'])
        like_comment = likes + comments

        print(like_comment, id_ph)
        ts = like_comment, id_ph
        list_top.append(ts)
        list_top.sort(reverse=True)

    print(list_top)
    list_photos = []
    for t in list_top[:3]:
        top3 = t[1]
        list_photos.append(top3)
        print(top3)


get_photo(users_id)
# print(get_photo(users_id))
