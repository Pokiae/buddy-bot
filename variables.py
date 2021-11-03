import os
import discord
from dotenv import load_dotenv

client = discord.Client()

load_dotenv(dotenv_path="config")

guild = client.get_guild(os.getenv('ID_GUILD'))

moi = int(os.getenv('MOI'))

administrator_list = [int(os.getenv('ADMINISTRATOR_LIST'))]

message_under_watching = []

roles_in_guild = []

dictionary_emoji_to_roles = {}


reaction_choosen = []

config_message = 0

config_role = False

content_message = ''

i = 0

temporary_dictionary = {}
