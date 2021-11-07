from datetime import datetime, timezone, timedelta
import discord
from discord import Forbidden
import variables as vr


def ready():
    print("{} est prêt !".format(vr.client.user.name))
    vr.guild = vr.client.get_guild(900780989683499079)


async def giving_all_member_arriving_role():
    get_icone_id()
    member_reacted = await get_member_reacted()
    for member in vr.guild.members:
        if member.id != vr.moi and member not in member_reacted: await member.add_roles(vr.guild.get_role(vr.arriving_role_id))


def get_icone_id():
    guild_emojis = vr.guild.emojis
    for emoji in guild_emojis:
        if emoji.name.startswith("icne"):
            vr.coche_id = emoji.id


async def get_member_reacted():
    channel = vr.guild.get_channel(vr.rules_channel)
    rule_message = await channel.fetch_message(vr.entry_message)
    rule_reactions = rule_message.reactions
    for reaction in rule_reactions:
        try:
            if reaction.emoji.id == vr.coche_id:
                member_reacted = await reaction.users().flatten()
                print(member_reacted)
            return member_reacted
        except AttributeError:
            print("Error: no id")
            pass
        except UnboundLocalError:
            print("Error: coche_reaction not found")
            return None


async def giving_entry_permissions(reaction, user):
    is_message_entry = reaction.message.id == vr.entry_message
    is_reaction_coche = reaction.emoji.id == vr.coche_id
    if is_message_entry and is_reaction_coche:
        await user.add_roles(vr.guild.get_role(vr.member_role_id))
        await user.remove_roles(vr.guild.get_role(vr.arriving_role_id))


async def removing_entry_permissions(reaction, user):
    is_message_entry = reaction.message.id == vr.entry_message
    is_reaction_coche = reaction.emoji.id == vr.coche_id
    if is_message_entry and is_reaction_coche:
        await user.add_roles(vr.guild.get_role(vr.arriving_role_id))


async def get_roles_requested(message):
    user = message.author.id
    for key in vr.passwords.keys():
        if key in message.content:
            if key not in vr.user_infos[user]['requested_roles']:
                vr.user_infos[user]['requested_roles'].append(key)
        print(vr.user_infos[user]['requested_roles'])
    if not vr.user_infos[user]['requested_roles']:
        del[vr.user_infos[user]]
        return
    for requested_role in vr.user_infos[user]['requested_roles']:
        for role in vr.user_infos[user]['roles']:
            role_id = role.id
            if role_id in vr.alias_to_roles.values():
                vr.user_infos[user]['requested_roles'].remove(requested_role)
                await vr.user_infos[user]['channel'].send(f"```\nVous possédez déjà le rôle {requested_role}.\n```")
        print(vr.user_infos[user]['requested_roles'])
    is_requested_role_full = vr.user_infos[user]['requested_roles']
    if is_requested_role_full:
        vr.is_registrating[user] = True
        await message.channel.send(f"{vr.sentence_requested_role}{vr.user_infos[user]['requested_roles'][0]}\n```")
    else:
        vr.is_registrating[user] = False


async def get_info_mps(message):

    user = message.author.id
    is_channel_private = message.channel.type is discord.ChannelType.private
    is_not_my_message = user != vr.moi
    is_user_not_in_database = vr.user_infos.get(user) is None
    print(vr.user_infos.get(user))
    member = vr.guild.get_member(user)

    if is_channel_private and is_not_my_message:
        if is_user_not_in_database:

            vr.user_infos[user] = {}
            vr.user_infos[user]['requested_roles'] = []
            vr.user_infos[user]['channel'] = message.channel
            vr.user_infos[user]['tentative'] = 3
            vr.user_infos[user]['roles'] = member.roles

            await get_roles_requested(message)
        else:
            is_registrating = vr.is_registrating[user]
            if not is_registrating:
                try:
                    if 'next_try' in vr.user_infos[user]:
                        if datetime.now(timezone.utc) > vr.user_infos[user]['next_try']:
                            await get_roles_requested(message)
                    else:
                        await get_roles_requested(message)
                except KeyError:
                    pass


async def registration(message):
    is_private_channel = message.channel.type is discord.ChannelType.private
    try:
        is_registrating = vr.is_registrating[message.channel.recipient.id]
        print(message.content)
        user_has_requested_role = message.content.startswith(vr.sentence_requested_role)
        is_my_message = message.author.id == vr.moi
        if is_private_channel and is_registrating and user_has_requested_role and is_my_message:
            for user in vr.user_infos.keys():
                if vr.user_infos[user]['channel'] == message.channel:
                    requested_role = vr.guild.get_role(vr.alias_to_roles[vr.user_infos[user]['requested_roles'][0]])
                    requested_role = requested_role.name
                    await vr.user_infos[user]['channel'].send(f"```\nEntrez le mot de passe pour : "
                                                              f"{requested_role} "
                                                              f"({vr.user_infos[user]['requested_roles'][0]})\n```")
    except KeyError:
        pass


async def try_next_role_password(message):
    user = message.author.id
    try:
        await message.channel.send(f"{vr.sentence_requested_role}{vr.user_infos[user]['requested_roles'][0]}\n```")
    except IndexError:
        await message.channel.send(f"```\n"
                                   f"Fin de l'attribution des rôles, si vous n'avez pas eu tous les rôles nécessaires, "
                                   f"veuillez patienter 1h avant de réessayer ou contacter un administrateur.\n```")
        current_time = datetime.now(timezone.utc)
        next_try = current_time + timedelta(hours=1)
        vr.user_infos[user]['next_try'] = next_try
        vr.is_registrating[user] = False
        vr.user_infos[user]['requested_roles'].clear()


async def analyse_answer_password(message):

    user = message.author.id
    is_channel_private = message.channel.type is discord.ChannelType.private
    print(vr.user_infos)

    try:
        is_registrating = vr.is_registrating[user]
        is_password_correct = message.content == vr.passwords[vr.user_infos[user]['requested_roles'][0]]
        how_many_tentative_left = vr.user_infos[user]['tentative']

        if is_registrating and is_channel_private and is_password_correct:
            member = vr.guild.get_member(user)
            requested_role = vr.guild.get_role(vr.alias_to_roles[vr.user_infos[user]['requested_roles'][0]])

            try:
                await member.add_roles(requested_role)
                vr.user_infos[user]['roles'].append(requested_role)
                await vr.user_infos[user]['channel'].send(f"```\nLe rôle : *{requested_role}* "
                                                          f"vous a été attribué avec succès\n```")
            except Forbidden:
                await vr.user_infos[user]['channel'].send(f"```\nErreur de permissions pour le rôle *{requested_role}*,"
                                                          f" contactez un administrateur pour lui en faire part.\n```")
                pass
            vr.user_infos[user]['tentative'] = 3
            vr.user_infos[user]['requested_roles'].pop(0)

            await try_next_role_password(message)

        elif is_registrating and is_channel_private and how_many_tentative_left > 0:
            await message.channel.send(f"```\nLe mot de passe n'est pas le bon, il vous reste "
                                       f"{how_many_tentative_left} tentatives.```\n")
            vr.user_infos[user]['tentative'] -= 1
            print(vr.user_infos[user])

        elif is_registrating and is_channel_private and how_many_tentative_left == 0:
            await message.channel.send(f"```\nVous avez épuisé toutes vos tentatives, la demande du rôle "
                                       f"{vr.user_infos[user]['requested_roles'][0]} est annulées, vous "
                                       f"pourrez la réessayer plus tard.```\n")

            vr.user_infos[user]['tentative'] = 3
            vr.user_infos[user]['requested_roles'].pop(0)

            await try_next_role_password(message)
    except KeyError:
        pass
    except IndexError:
        pass


async def command_reaction(message):

    is_command_called = message.content.startswith("$reac")
    is_author_admin = message.author.id in vr.administrator_list

    if is_command_called and is_author_admin:

        vr.content_message = message.content.removeprefix('$reac')

        await message.channel.send(f"Bonjour !"
                                   f"\nVotre commande a bien été prise en compte. "
                                   f"Réagissez à ce message avec les emojis que vous souhaitez utiliser pour :"
                                   f"\n```\n{vr.content_message}\n```"
                                   f"\nLorsque vous avez choisi toutes vos réactions, envoyez '$end'")
        await message.delete()


async def clean_up_error(message):

    is_message_error = message.content.endswith('Veuillez réessayer après avoir mis des réactions.')
    is_my_message = message.author.id == vr.moi

    if is_message_error and is_my_message:
        await message.delete(5)


def identify_config_message(message):

    is_config_message = message.content.startswith('Bonjour !')
    is_my_message = message.author.id == vr.moi

    if is_config_message and is_my_message:
        vr.config_message = message


async def command_begin_indent(message):

    is_command_finish_attribution = message.content.startswith('$end')
    is_author_admin = message.author.id in vr.administrator_list

    if is_command_finish_attribution and is_author_admin:
        try:
            await message.channel.send(f'Bien compris, à présent quel rôle voulez-vous attribuer à cet emoji : '
                                       f'{vr.reaction_choosen[0]}')
            await vr.config_message.delete()
            vr.config_role = True
        except IndexError:
            await message.channel.send(f"Il semblerait que vous n'ayez pas mis de réactions, avouez que c'est "
                                       f"problématique. Veuillez réessayer après avoir mis des réactions.")


async def associate_emojis_roles(message):

    is_author_admin = message.author.id in vr.administrator_list

    if is_author_admin and vr.config_role and message.content != '$end':
        if vr.i <= len(vr.reaction_choosen)-1:
            await message.channel.send(f"Bien, à présent quel rôle voulez-vous attribuer à cet emoji : "
                                       f"{vr.reaction_choosen[vr.i]}\n*Si vous avez déjà donné un rôle à cet emoji, "
                                       f"tapez 'fin'*")
            try:
                vr.emoji_to_roles[vr.reaction_choosen[vr.i]] = message.role_mentions[0]
            except IndexError:
                pass
            vr.i += 1

        else:
            vr.config_roles = False
            messages_to_suppr = await message.channel.history(limit=len(vr.reaction_choosen)*2+3).flatten()

            for m in messages_to_suppr:
                await m.delete()

            await message.channel.send(vr.content_message + '\n\n*Signé :* Buddy')

            reinitialisation()


async def add_message_under_watching(message):

    is_message_to_watch = message.content.endswith('Buddy')
    is_my_message = message.author.id == vr.moi

    if is_message_to_watch and is_my_message:

        vr.message_under_watching.append(message)

        for each_reaction in vr.reaction_choosen:
            await message.add_reaction(each_reaction)
        vr.reaction_choosen.clear()


def add_reaction_to_list(reaction, user):

    is_user_admin = user.id in vr.administrator_list
    is_reaction_under_config_message = reaction.message == vr.config_message

    if is_user_admin and is_reaction_under_config_message:

        vr.reaction_choosen.append(reaction.emoji)


async def add_role(reaction, user):

    is_reaction_under_message_to_watch = reaction.message in vr.message_under_watching
    is_not_my_reaction = user.id != vr.moi

    if is_reaction_under_message_to_watch and is_not_my_reaction:
        try:
            await user.add_roles(vr.emoji_to_roles[reaction.emoji], reason='A demandé un rôle sous le message !')
        except KeyError:
            pass
        except Forbidden:
            await reaction.message.channel.send(f"Le rôle n'a pas pu être ajouté, contacter un administrateur pour "
                                                f"plus d'informations.")
            print(f"Erreur d'attribution pour {user}")
            pass


async def remove_role(reaction, user):

    is_reaction_under_message_to_watch = reaction.message in vr.message_under_watching

    if is_reaction_under_message_to_watch:
        try:
            await user.remove_roles(vr.emoji_to_roles[reaction.emoji], reason=f'A retiré sa demande de rôle sous le '
                                                                              f'message !')
        except KeyError:
            pass


def remove_reaction_from_list(reaction, user):

    is_user_admin = user.id in vr.administrator_list
    is_reaction_under_config_message = reaction.message == vr.config_message

    if is_user_admin and is_reaction_under_config_message:
        vr.reaction_choosen.remove(reaction.emoji)


def reinitialisation():

    vr.reaction_choosen.clear()
    vr.config_message = 0
    vr.config_role = False
    vr.content_message_with_reaction = ''
    vr.i = 0
