import os
import discord
from dotenv import load_dotenv
import fonctions as fc

load_dotenv(dotenv_path="config")

client = discord.Client()

@client.event
async def on_ready():
    print("Le bot est prêt.")


@client.event
async def on_message(message):

    await fc.command_reaction(message)

    await fc.clean_up_error(message)

    fc.identify_config_message(message)

    await fc.command_begin_indent(message)

    await fc.associate_emojis_roles(message)

    await fc.add_message_under_watching(message)



@client.event
async def on_reaction_add(reaction, user):

    fc.add_reaction_to_list(reaction, user)

    await fc.add_role(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):

    await fc.remove_role(reaction, user)

    await fc.remove_reaction_from_list(reaction, user)




client.run(os.getenv("TOKEN"))
