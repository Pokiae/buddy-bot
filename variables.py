import os
import discord
from dotenv import load_dotenv
from main import client

load_dotenv(dotenv_path="config")

guild = client.get_guild(os.getenv('ID_GUILD'))

moi = os.getenv('MOI')

administrator_list = os.getenv('ADMINISTRATOR_LIST')

message_under_watching = os.getenv('MESSAGE_UNDER_WATCHING')

roles_in_guild = []

dictionary_emoji_to_roles = os.getenv('DICTIONARY_EMOJIS_ROLES')


reaction_choosen = []

config_message = 0

config_role = False

content_message = ''

i = 0

temporary_dictionary = {}
