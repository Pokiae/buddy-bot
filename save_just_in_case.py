import os
import discord
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

client = discord.Client()

guild = client.get_guild(os.getenv('ID_GUILD'))
moi = int(os.getenv('MOI'))
administrator_list = [int(os.getenv('ADMINISTRATOR_LIST'))]
message_under_watching = [os.getenv('MESSAGE_UNDER_WATCHING')]
roles_in_guild = []
dictionary_emoji_to_roles = {}
print(dictionary_emoji_to_roles)

reaction_choosen = []
config_message = 0
config_role = False
content_message = ''
i = 0
temporary_dictionary = {}



def reinitialisation():
    global config_message
    global config_role
    global content_message_with_reaction
    global i
    global temporary_dictionary
    global channel_message_for_reaction

    config_message = 0
    config_role = False
    content_message_with_reaction = ''
    i = 0
    temporary_dictionary = {}
    channel_message_for_reaction = 0


@client.event
async def on_ready():
    print("Le bot est prêt.")


@client.event
async def on_message(message):

    global message_under_watching
    global reaction_choosen
    global config_message
    global config_role
    global content_message
    global i
    global dictionary_emoji_to_roles
    global temporary_dictionary

    if message.content.startswith("$reac") and message.author.id in administrator_list:

        content_message = message.content.removeprefix('$reac')
        print(content_message)

        await message.channel.send("Bonjour !\nVotre commande a bien été prise en compte. Réagissez à ce message avec les emojis que vous souhaitez utiliser pour ce message :\n```\n" + content_message + "\n```\nLorsque vous avez choisi toutes vos réactions, envoyez '$end'")
        await message.delete()

    if message.content.startswith('Bonjour !') and message.author.id == moi:
        config_message = message

    if message.content.endswith('Veuillez réessayer après avoir mis des réactions.') and message.author.id == moi:
        await message.delete(delay=5)

    if message.content.startswith('$end') and message.author.id in administrator_list:

        try:
            await message.channel.send('Bien compris, à présent quel rôle voulez-vous attribuer à cet emoji : ' + reaction_choosen[0])
            await config_message.delete()
            config_role = True
        except IndexError:
            await message.channel.send("Il semblerait que vous n'ayez pas mis de réactions, avouez que c'est problématique. Veuillez réessayer après avoir mis des réactions.")

    if message.author.id in administrator_list and config_role and message.content != '$end':

        print('i='+str(+i))
        print('reaction ='+str(len(reaction_choosen)-1))

        if i<=len(reaction_choosen)-1:

            await message.channel.send('Bien, à présent quel rôle voulez-vous attribuer à cet emoji : ' + reaction_choosen[i] + "\n*Si vous avez déjà donné un rôle à cet emoji, tapez 'fin'*")

            try:
                temporary_dictionary[reaction_choosen[i]] = message.role_mentions[0]
            except IndexError:
                pass
            i+=1

            print(temporary_dictionary)

        else:
            config_roles = False
            messages_to_suppr = await message.channel.history(limit=len(reaction_choosen)*2+3).flatten()

            for m in messages_to_suppr:
                await m.delete()

            await message.channel.send(content_message + '\n\n*Signé :* Buddy')

            dictionary_emoji_to_roles.update(temporary_dictionary)
            os.environ['DICTIONARY_EMOJIS_ROLES'] = str(dictionary_emoji_to_roles)
            reinitialisation()

            print(dictionary_emoji_to_roles)

    if message.content.endswith('Buddy') and message.author.id == moi:

        message_under_watching.append(message)
        os.environ['MESSAGE_UNDER_WATCHING'] = str(message_under_watching)
        print('Je suis en train de mettre des réactions')

        for each_reaction in reaction_choosen:
            await message.add_reaction(each_reaction)
        reaction_choosen = []




@client.event
async def on_reaction_add(reaction, user):

    if user.id in administrator_list and reaction.message == config_message:

        reaction_choosen.append(reaction.emoji)

        print(reaction_choosen)

    if reaction.message in message_under_watching and user.id != moi:

        try:
            await user.add_roles(dictionary_emoji_to_roles[reaction.emoji],reason='A demandé un rôle sous le message !')
        except KeyError:
            pass


@client.event
async def on_reaction_remove(reaction, user):

    if reaction.message in message_under_watching:

        try:
            await user.remove_roles(dictionary_emoji_to_roles[reaction.emoji], reason='A retiré sa demande de rôle sous le message !')
        except KeyError:
            pass




client.run(os.getenv("TOKEN"))
