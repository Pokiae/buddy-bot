import os
import discord
from dotenv import load_dotenv

intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv(dotenv_path=".env")

guild = 0

key_words = ['mdl', 'cvl', 'journal', 'jeux', 'theatre', 'ecodelegue', 'delegue', 'administration', 'ambassadeur', 'surveillant', 'musique']
passwords = {"mdl": os.getenv("PASS_MDL"),
             "cvl": os.getenv("PASS_CVL"),
             "journal": os.getenv("PASS_JOURNAL"),
             'jeux': os.getenv("PASS_JEUX"),
             'theatre': os.getenv("PASS_THEATRE"),
             'ecodelegue': os.getenv("PASS_ECODELEGUE"),
             'delegue': os.getenv("PASS_DELEGUE"),
             'administration': os.getenv("PASS_ADMDINISTRATION"),
             'ambassadeur': os.getenv("PASS_AMBASSADEUR"),
             'surveillant': os.getenv("PASS_SURVEILLANT"),
             'musique': os.getenv("PASS_AMBASSADEUR")}

is_registrating = {}
sentence_requested_role = "```\nVous avez demandé à avoir le rôle suivant : "
coche_id = None
