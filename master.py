import os
from dotenv import load_dotenv
import fonctions as fc
import variables as vr

load_dotenv(dotenv_path=".env")

client = vr.client


@client.event
async def on_ready():
    fc.ready()
    await fc.giving_all_member_arriving_role()


@client.event
async def on_message(message):
    await fc.registration(message)
    await fc.analyse_answer_password(message)
    await fc.get_info_mps(message)


@client.event
async def on_raw_reaction_add(payload):
    await fc.giving_entry_permissions(payload)
    await fc.message_watching_on_add(payload)


@client.event
async def on_raw_reaction_remove(payload):
    await fc.removing_entry_permissions(payload)
    await fc.message_watching_on_remove(payload)


@client.event
async def on_member_remove(member):
    fc.remove_on_leaving(member)


client.run(os.getenv("TOKEN"))
