import os
import discord
from dotenv import load_dotenv


client = discord.Client()

load_dotenv(dotenv_path="config")
#int(os.getenv('ID_GUILD'))
guild = client.get_guild(900780989683499079)

moi = int(os.getenv('MOI'))

administrator_list = [int(os.getenv('ADMINISTRATOR_LIST'))]

message_under_watching = []

dictionary_emoji_to_roles = {}


reaction_choosen = []

config_message = 0

config_role = False

content_message = ''

i = 0

temporary_dictionary = {}


key_words = ['mdl', 'cvl', 'journal', 'jeux', 'theatre', 'ecodelegue', 'delegue', 'administration', 'ambassadeur']

dictionnary_for_all = {}

dictionnary_pw = {"mdl": "1234", "cvl": 'joli mot de passe'}

registration = False

dictionnary_registration_on_going = {}

dictionnary_alias_to_roles = {'mdl': 901476152433078303, 'cvl': 903671942580666409}