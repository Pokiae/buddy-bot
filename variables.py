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

emoji_to_roles = {}



reaction_choosen = []

config_message = 0

config_role = False

content_message = ''

i = 0


key_words = ['mdl', 'cvl', 'journal', 'jeux', 'theatre', 'ecodelegue', 'delegue', 'administration', 'ambassadeur']

user_infos = {}

passwords = {"mdl": "1234", "cvl": 'joli mot de passe'}

is_registrating = {}

alias_to_roles = {'mdl': 901476152433078303, 'cvl': 903671942580666409}

sentence_requested_role = "```\nVous avez demandé à avoir le rôle suivant : "

coche_id = 906823454664310794

rules_channel = 900814173754261515

entry_message = 906823454664310794

