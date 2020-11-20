import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

token = str(os.getenv("token"))  # для api vk

# id администраторов
admins = [
    os.getenv("ADMIN_ID"),

]

bot_name = 'bot_name'


name_discussion_group = 'name_discussion_group'


# id каналов
channels = [id_channel, ]

channels_comment_id = 'channels_comment_id'


id_vk_group = 'id_vk_group'
id_vk_group_album = 'id_vk_group_album'


ip = os.getenv("ip")
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')

DATABASE = str(os.getenv('DATABASE'))


PGUSER = 'defold-bot'
PGPASSWORD = 'defoldbot'
DATABASE = 'defold-bot'
PGUSER = 'postgres'
PGPASSWORD = 'AllenWalker007'
DATABASE = 'gyno'




POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"
