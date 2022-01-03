# Получить топ-3 фотографий пользователя:
from users_data import session


def get_photo(user_id):
    """Получение топ3 фото пользователя"""
    photo_id = session.method('photos.get', {'owner_id': user_id,
                                             'album_id': 'profile',
                                             'extended': 1,
                                             # 'count': 3,

                                             })
    list_top = []
    for photo in (photo_id['items']):
        id_ph = photo['id']
        likes = photo['likes']['count']
        comments = photo['comments']['count']
        like_comment = likes + comments

        # print(like_comment, id_ph)
        ts = like_comment, id_ph
        list_top.append(ts)
        list_top.sort(reverse=True)

    # print(list_top)
    list_photos = []
    for t in list_top[:3]:
        top3 = t[1]
        list_photos.append(top3)
        # return top3

    return list_photos

