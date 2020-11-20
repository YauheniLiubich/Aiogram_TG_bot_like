import requests
import json
from data.config import token, id_vk_group, id_vk_group_album

"""url для получения токена"""
# url = 'https://oauth.vk.com/authorize?client_id=7623503&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,wall,offline&response_type=token&v=5.124'

# id группы и альбома, куда нужно загрузить фото
group_id = int(id_vk_group)
album_id = int(id_vk_group_album)


def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_upload_server():
    r = requests.get('https://api.vk.com/method/photos.getUploadServer', params={'access_token': token,
                                                                                 'album_id': album_id,
                                                                                 'group_id': group_id,
                                                                                 'v': 5.124}).json()
    # write_json(r, 'upload_server.json')
    return r["response"]['upload_url']


def send_photo_to_album(photo_name):
    """Если нужно создать альбом"""
    # r = requests.get('https://api.vk.com/method/photos.createAlbum', params={'access_token': token,
    #                                                                          'title': 'Альбом',
    #                                                                          'group_id': group_id,
    #                                                                          'v': 5.124}).json()
    # write_json(r, 'album.json')

    """1. Получаем адрес сервера для загрузки фотографии. photos.getUploadServer"""
    upload_url = get_upload_server()

    """2.Подготовить файл. POST запрос"""
    file = {'file1': open(photo_name, 'rb')}
    ur = requests.post(upload_url, files=file).json()
    # write_json(ur, 'upload_photos.json')

    """3. Сохраняем файл на сервере. photos.save"""
    result = requests.get('https://api.vk.com/method/photos.save', params={'access_token': token,
                                                                           'album_id': ur['aid'],
                                                                           'group_id': ur['gid'],
                                                                           'server': ur['server'],
                                                                           'photos_list': ur['photos_list'],
                                                                           'hash': ur['hash'],
                                                                           'v': 5.124}).json()

    return result['response'][0]['album_id'], result['response'][0]['id']


if __name__ == '__main__':
    send_photo_to_album()
