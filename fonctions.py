from datetime import datetime, timezone, timedelta
import discord
from discord import Forbidden
import variables as vr
import config as cf
import hashlib
import pickle


def ready():
    print("{} est prêt !".format(vr.client.user.name))
    vr.guild = vr.client.get_guild(cf.id_guild)


def initiate_admin_list():
    try:
        with open('ADMIN.pickle', 'rb') as f:
            cf.administrator_list = pickle.load(f)
    except FileNotFoundError:
        pass


async def giving_all_member_arriving_role():
    get_icone_id()
    member_reacted = await get_member_reacted()
    for member in vr.guild.members:
        if member.id != cf.moi and member not in member_reacted: await member.add_roles(vr.guild.get_role(cf.arriving_role_id))


def get_icone_id():
    guild_emojis = vr.guild.emojis
    for emoji in guild_emojis:
        if emoji.name.startswith("icne"):
            vr.coche_id = emoji.id


async def get_member_reacted():
    channel = vr.guild.get_channel(cf.rules_channel)
    rule_message = await channel.fetch_message(cf.entry_message)
    rule_reactions = rule_message.reactions
    for reaction in rule_reactions:
        try:
            if reaction.emoji.id == vr.coche_id:
                member_reacted = await reaction.users().flatten()
            return member_reacted
        except AttributeError:
            pass
        except UnboundLocalError:
            print("Error: coche_reaction not found")
            return None


async def giving_entry_permissions(payload):
    is_message_entry = payload.message_id == cf.entry_message
    is_reaction_coche = payload.emoji.id == vr.coche_id
    if is_message_entry and is_reaction_coche:
        await payload.member.add_roles(vr.guild.get_role(cf.basic_member_role_id))
        await payload.member.remove_roles(vr.guild.get_role(cf.arriving_role_id))


async def removing_entry_permissions(payload):
    is_message_entry = payload.message_id == cf.entry_message
    is_reaction_coche = payload.emoji.id == vr.coche_id
    if is_message_entry and is_reaction_coche:
        await payload.member.add_roles(vr.guild.get_role(cf.arriving_role_id))


async def get_roles_requested(message):
    user = message.author.id
    for key in vr.passwords.keys():
        if key in message.content:
            if key not in cf.user_infos[user]['requested_roles']:
                cf.user_infos[user]['requested_roles'].append(key)
    if not cf.user_infos[user]['requested_roles']:
        del[cf.user_infos[user]]
        return
    for requested_role in cf.user_infos[user]['requested_roles']:
        for role in cf.user_infos[user]['roles']:
            role_id = role.id
            if role_id in cf.alias_to_roles.values():
                cf.user_infos[user]['requested_roles'].remove(requested_role)
                await cf.user_infos[user]['channel'].send(f"```\nVous possédez déjà le rôle {requested_role}.\n```")
        print(cf.user_infos[user]['requested_roles'])
    is_requested_role_full = cf.user_infos[user]['requested_roles']
    if is_requested_role_full:
        vr.is_registrating[user] = True
        await message.channel.send(f"{vr.sentence_requested_role}{cf.user_infos[user]['requested_roles'][0]}\n```")
    else:
        vr.is_registrating[user] = False


def create_database(message, member):
    user = message.author.id
    cf.user_infos[user]={}
    cf.user_infos[user]['requested_roles'] = []
    cf.user_infos[user]['channel'] = message.channel
    cf.user_infos[user]['tentative'] = 3
    cf.user_infos[user]['roles'] = member.roles


def clean_database(user):
    cf.user_infos[user].pop('requested_roles')
    cf.user_infos[user].pop('channel')
    cf.user_infos[user].pop('tentative')
    cf.user_infos[user].pop('roles')


async def get_info_mps(message):

    user = message.author.id
    is_channel_private = message.channel.type is discord.ChannelType.private
    is_not_my_message = user != cf.moi
    is_user_not_in_database = cf.user_infos.get(user) is None
    member = vr.guild.get_member(user)

    if is_channel_private and is_not_my_message:
        if is_user_not_in_database:

            create_database(message, member)

            await get_roles_requested(message)
        else:
            is_registrating = vr.is_registrating[user]
            if not is_registrating:
                try:
                    if 'next_try' in cf.user_infos[user]:
                        if datetime.now(timezone.utc) > cf.user_infos[user]['next_try']:
                            create_database(message, member)
                            await get_roles_requested(message)
                    else:
                        create_database(message, member)
                        await get_roles_requested(message)
                except KeyError:
                    pass


async def registration(message):
    is_private_channel = message.channel.type is discord.ChannelType.private
    try:
        is_registrating = vr.is_registrating[message.author.id]
        print(is_registrating)
        user_has_requested_role = message.content.startswith(vr.sentence_requested_role)
        print(user_has_requested_role)
        print(vr.sentence_requested_role)
        print(message.content)
        is_my_message = message.author.id == cf.moi
        print(message.author.id)
        if is_private_channel and is_registrating and user_has_requested_role and is_my_message:
            for user in cf.user_infos.keys():
                if cf.user_infos[user]['channel'] == message.channel:
                    requested_role = vr.guild.get_role(cf.alias_to_roles[cf.user_infos[user]['requested_roles'][0]])
                    requested_role = requested_role.name
                    await cf.user_infos[user]['channel'].send(f"```\nEntrez le mot de passe pour : "
                                                              f"{requested_role} "
                                                              f"({cf.user_infos[user]['requested_roles'][0]})\n```")
    except KeyError:
        print("Key_error")
        pass


async def try_next_role_password(message):
    user = message.author.id
    try:
        await message.channel.send(f"{vr.sentence_requested_role}{cf.user_infos[user]['requested_roles'][0]}\n```")
    except IndexError:
        await message.channel.send(f"```\n"
                                   f"Fin de l'attribution des rôles, si vous n'avez pas eu tous les rôles nécessaires, "
                                   f"veuillez patienter 1h avant de réessayer ou contacter un administrateur.\n```")
        clean_database(user)
        current_time = datetime.now(timezone.utc)
        next_try = current_time + timedelta(hours=1)
        cf.user_infos[user]['next_try'] = next_try
        vr.is_registrating[user] = False
        cf.user_infos[user]['requested_roles'].clear()


async def analyse_answer_password(message):

    user = message.author.id
    is_channel_private = message.channel.type is discord.ChannelType.private
    try :
        try_password = bytes(message.content, encoding='ascii')
        try_password = hashlib.sha256(try_password).hexdigest()

        is_registrating = vr.is_registrating[user]
        is_password_correct = try_password == vr.passwords[cf.user_infos[user]['requested_roles'][0]]
        how_many_tentative_left = cf.user_infos[user]['tentative']

        if is_registrating and is_channel_private and is_password_correct:
            member = vr.guild.get_member(user)
            requested_role = vr.guild.get_role(cf.alias_to_roles[cf.user_infos[user]['requested_roles'][0]])

            try:
                await member.add_roles(requested_role)
                cf.user_infos[user]['roles'].append(requested_role)
                await cf.user_infos[user]['channel'].send(f"```\nLe rôle : *{requested_role}* "
                                                          f"vous a été attribué avec succès\n```")
            except Forbidden:
                await cf.user_infos[user]['channel'].send(f"```\nErreur de permissions pour le rôle *{requested_role}*,"
                                                          f" contactez un administrateur pour lui en faire part.\n```")
                pass
            cf.user_infos[user]['tentative'] = 3
            cf.user_infos[user]['requested_roles'].pop(0)

            await try_next_role_password(message)

        elif is_registrating and is_channel_private and how_many_tentative_left > 0:
            await message.channel.send(f"```\nLe mot de passe n'est pas le bon, il vous reste "
                                       f"{how_many_tentative_left} tentatives.```\n")
            cf.user_infos[user]['tentative'] -= 1

        elif is_registrating and is_channel_private and how_many_tentative_left == 0:
            await message.channel.send(f"```\nVous avez épuisé toutes vos tentatives, la demande du rôle "
                                       f"{cf.user_infos[user]['requested_roles'][0]} est annulées, vous "
                                       f"pourrez la réessayer plus tard.```\n")

            cf.user_infos[user]['tentative'] = 3
            cf.user_infos[user]['requested_roles'].pop(0)

            await try_next_role_password(message)
    except KeyError:
        pass
    except IndexError:
        pass
    except UnicodeEncodeError:
        pass


def key_emoji(emoji):
    if emoji.id is None:
        return str(emoji)
    else:
        return emoji.id


async def message_watching_on_add(payload):
    message = payload.message_id
    emoji = key_emoji(payload.emoji)
    if message in cf.message_under_watching.keys():
        if emoji in cf.message_under_watching[message].keys():
            await payload.member.add_roles(vr.guild.get_role(cf.message_under_watching[message][emoji]))


async def message_watching_on_remove(payload):
    message = payload.message_id
    emoji = key_emoji(payload.emoji)
    if message in cf.message_under_watching.keys():
        if emoji in cf.message_under_watching[message].keys():
            member = vr.guild.get_member(payload.user_id)
            await member.remove_roles(vr.guild.get_role(cf.message_under_watching[message][emoji]))


def remove_on_leaving(member):
    if member.id in cf.user_infos.key():
        cf.user_infos.pop(member.id)


def command_add_admin(message):
    if message.content.startswith('$add_admin$'):
        content = message.content.replace('$add_admin$', '')
        admin_to_add = content.split('$')
        admin_to_add = check_if_admin_real(admin_to_add)
        add_admin(admin_to_add)
        with open('ADMIN.pickle', 'wb') as f:
            pickle.dump(cf.administrator_list, f)


def check_if_admin_real(admin_to_add):
    for admin in admin_to_add:
        try:
            if vr.guild.get_member(int(admin)) is None:
                admin_to_add.remove(admin)
        except TypeError:
            admin_to_add.remove(admin)
    return admin_to_add


def add_admin(admin_to_add):
    for admin in admin_to_add:
        cf.administrator_list.append(admin)
