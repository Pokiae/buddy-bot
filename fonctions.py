import zoneinfo

import discord
from discord import Forbidden
import variables as vr
import os


def ready():
    print("{} est prêt !".format(vr.client.user.name))
    vr.guild = vr.client.get_guild(900780989683499079)


#async def giving_entry_permissions(reaction, user):
    #if reaction.message.id == vr.entry_message:
        #await user.add_roles(vr.guild.get_role(895348987232653445))
        #await user.remove_roles(vr.guild.get_role(900736184207163393))


#async def removing_entry_permissions(reaction, user):
    #if reaction.message.id == vr.entry_message:
        #await user.add_roles(vr.guild.get_role(900736184207163393))


async def get_info_mps(message):
    user = message.author.id
    if message.channel.type is discord.ChannelType.private and user != vr.moi:
        try:
            if vr.dictionary_for_all[user]:
                return
        except KeyError:
            vr.dictionary_for_all[user] = {}
            vr.dictionary_for_all[user]['requested_roles'] = []
            vr.dictionary_for_all[user]['channel'] = message.channel
            vr.dictionary_for_all[user]['tentative'] = 3
            for each_key in vr.dictionary_pw.keys():
                if each_key in message.content:
                    vr.dictionary_for_all[user]['requested_roles'].append(each_key)
            if not vr.dictionary_for_all[user]['requested_roles']:
                del[vr.dictionary_for_all[user]]
                return
            vr.dictionary_for_all[user]['registration_to_do'] = vr.dictionary_for_all[user]['requested_roles']
            vr.registration[user] = True
            await message.channel.send(f"Vous avez demandé à avoir le rôle suivant : "
                                       f"{vr.dictionary_for_all[user]['registration_to_do'][0]}")
            print(vr.dictionary_for_all)


async def registration(message):
    if message.channel.type is discord.ChannelType.private and vr.registration[message.channel.recipient.id] and message.content.startswith('Vous avez demandé à avoir le rôle suivant') and message.author.id == vr.moi:
        for user in vr.dictionary_for_all.keys():
            if vr.dictionary_for_all[user]['channel'] == message.channel:
                await vr.dictionary_for_all[user]['channel'].send('Entrez le mot de passe pour : {}'.format(vr.dictionary_for_all[user]['registration_to_do'][0]))
                vr.dictionary_registration_on_going[user] = vr.dictionary_for_all[user]['registration_to_do'][0]


async def try_next_role_password(message):
    user = message.author.id
    print(user)
    try:
        await message.channel.send("Vous avez demandé à avoir le rôle suivant : {}".format(vr.dictionary_for_all[user]['registration_to_do'][0]))
    except IndexError:
        await message.channel.send("Fin de l'attribution des rôles, si vous n'avez pas eu tous les rôles nécessaires, veuillez patienter 1h avant de réessayer ou contacter un administrateur du serveur.")
        print('ici')
        #vr.dictionnary_for_all[user]['Try Time'] = ZoneInfo('Europe/Paris')
        print(vr.dictionary_for_all)
        vr.registration[user] = False
        vr.dictionary_for_all[user]['requested_roles'].clear()
        print(vr.registration)


async def analyse_answer_password(message):
    user = message.author.id
    try:
        if vr.registration[user] and message.channel.type is discord.ChannelType.private and message.content == vr.dictionary_pw[vr.dictionary_registration_on_going[user]]:
            member = vr.guild.get_member(user)
            await member.add_roles(vr.guild.get_role(vr.dictionary_alias_to_roles[vr.dictionary_registration_on_going[user]]))
            vr.dictionary_for_all[user]['tentative'] = 3
            vr.dictionary_for_all[user]['registration_to_do'].pop(0)
            await try_next_role_password(message)

        elif vr.registration[user] and message.channel.type is discord.ChannelType.private and vr.dictionary_for_all[user]['tentative'] > 0:
            await message.channel.send("Le mot de passe n'est pas le bon, il vous reste {} tentatives.".format(vr.dictionary_for_all[user]['tentative']))
            vr.dictionary_for_all[user]['tentative'] -= 1

        elif vr.registration[user] and message.channel.type is discord.ChannelType.private and vr.dictionary_for_all[user]['tentative'] == 0:
            await message.channel.send("Vous avez épuisé toutes vos tentatives, la demande du rôle {} est annulées, vous pourrez la reprendre plus tard.".format(vr.dictionary_registration_on_going[message.author.id]))
            vr.dictionary_for_all[user]['tentative'] = 3
            vr.dictionary_for_all[user]['registration_to_do'].pop(0)
            await try_next_role_password(message)
    except KeyError:
        pass


async def command_reaction(message):
    if message.content.startswith("$reac") and message.author.id in vr.administrator_list:

        vr.content_message = message.content.removeprefix('$reac')

        await message.channel.send("Bonjour !\nVotre commande a bien été prise en compte. Réagissez à ce message avec les emojis que vous souhaitez utiliser pour ce message :\n```\n" + vr.content_message + "\n```\nLorsque vous avez choisi toutes vos réactions, envoyez '$end'")
        await message.delete()


async def clean_up_error(message):
    if message.content.endswith('Veuillez réessayer après avoir mis des réactions.') and message.author.id == vr.moi:
        await message.delete(5)


def identify_config_message(message):
    if message.content.startswith('Bonjour !') and message.author.id == vr.moi:
        vr.config_message = message


async def command_begin_indent(message):
    if message.content.startswith('$end') and message.author.id in vr.administrator_list:

        try:
            await message.channel.send('Bien compris, à présent quel rôle voulez-vous attribuer à cet emoji : ' + vr.reaction_choosen[0])
            await vr.config_message.delete()
            vr.config_role = True
        except IndexError:
            await message.channel.send("Il semblerait que vous n'ayez pas mis de réactions, avouez que c'est problématique. Veuillez réessayer après avoir mis des réactions.")


async def associate_emojis_roles(message):
    if message.author.id in vr.administrator_list and vr.config_role and message.content != '$end':

        if vr.i <= len(vr.reaction_choosen)-1:

            await message.channel.send('Bien, à présent quel rôle voulez-vous attribuer à cet emoji : ' + vr.reaction_choosen[vr.i] + "\n*Si vous avez déjà donné un rôle à cet emoji, tapez 'fin'*")

            try:
                vr.temporary_dictionary[vr.reaction_choosen[vr.i]] = message.role_mentions[0]
            except IndexError:
                pass
            vr.i += 1

        else:
            vr.config_roles = False
            messages_to_suppr = await message.channel.history(limit=len(vr.reaction_choosen)*2+3).flatten()

            for m in messages_to_suppr:
                await m.delete()

            await message.channel.send(vr.content_message + '\n\n*Signé :* Buddy')

            vr.dictionary_emoji_to_roles.update(vr.temporary_dictionary)
            os.environ['DICTIONARY_EMOJIS_ROLES'] = str(vr.dictionary_emoji_to_roles)
            reinitialisation()


async def add_message_under_watching(message):
    if message.content.endswith('Buddy') and message.author.id == vr.moi:

        vr.message_under_watching.append(message)
        os.environ['MESSAGE_UNDER_WATCHING'] = str(vr.message_under_watching)

        for each_reaction in vr.reaction_choosen:
            await message.add_reaction(each_reaction)
        vr.reaction_choosen = []


def add_reaction_to_list(reaction, user):
    if user.id in vr.administrator_list and reaction.message == vr.config_message:

        vr.reaction_choosen.append(reaction.emoji)


async def add_role(reaction, user):
    if reaction.message in vr.message_under_watching and user.id != vr.moi:

        try:
            await user.add_roles(vr.dictionary_emoji_to_roles[reaction.emoji],reason='A demandé un rôle sous le message !')
        except KeyError:
            pass
        except Forbidden:
            await reaction.message.channel.send("Le rôle n'a pas pu être ajouté, contacter un administrateur pour plus d'informations.")
            print("Erreur d'attribution")
            pass


async def remove_role(reaction, user):
    if reaction.message in vr.message_under_watching:

        try:
            await user.remove_roles(vr.dictionary_emoji_to_roles[reaction.emoji], reason='A retiré sa demande de rôle sous le message !')
        except KeyError:
            pass


def remove_reaction_from_list(reaction, user):
    if user.id in vr.administrator_list and reaction.message == vr.config_message:

        vr.reaction_choosen.remove(reaction.emoji)


def reinitialisation():

    vr.reaction_choosen = []
    vr.config_message = 0
    vr.config_role = False
    vr.content_message_with_reaction = ''
    vr.i = 0
    vr.temporary_dictionary = {}
