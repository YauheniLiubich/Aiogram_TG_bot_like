import re
import requests
from .photo_to_album import send_photo_to_album

from data.config import token, id_vk_group


def get_link(text):
    return re.search("(?P<url>https?://[^\s]+)", text).group("url")


def send(text, photo_name=None):
    id_group = -int(id_vk_group)
    try:
        attachments = get_link(text)
    except:
        attachments = None
    if photo_name is not None:
        try:
            album_id, photo_id = send_photo_to_album(photo_name)
            attachments = f'photo{id_group}_{photo_id}'  # id фото в альбоме
        except:
            attachments = None
    data = (
        ('v', '5.124'),
        ('access_token', token),
        ('owner_id', id_group),  # если нужно выкладывать в паблик параметр должен быть отрицательным
        ('message', text),
        ('attachments', attachments),
        ('friends_only', 0),
        ('from_group', 1)
    )
    response = requests.post('https://api.vk.com/method/wall.post?', data=data)
    print('Send End')
