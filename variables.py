import os
import discord
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv(dotenv_path="config")

guild = 0

moi = int(os.getenv('MOI'))

administrator_list = [int(os.getenv('ADMINISTRATOR_LIST'))]

message_under_watching = []

dictionary_emoji_to_roles = {}

entry_message = 897906221196148766


reaction_choosen = []

config_message = 0

config_role = False

content_message = ''

i = 0

temporary_dictionary = {}


key_words = ['mdl', 'cvl', 'journal', 'jeux', 'theatre', 'ecodelegue', 'delegue', 'administration', 'ambassadeur']

dictionary_for_all = {}

dictionary_pw = {"mdl": "1234", "cvl": 'joli mot de passe'}

registration = {}

dictionary_registration_on_going = {}

dictionary_alias_to_roles = {'mdl': 903672011958653018, 'cvl': 903671942580666409}


