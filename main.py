# This example requires the 'message_content' privileged intents

import os
import random

import discord
from discord.ext import commands

CHANNEL_ID = 850284466680758282

# Здесь вы можете указать список пользователей, за которыми нужно следить
WATCH_LIST = ["00.#3516", "Vaflz#3717"]
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)
user_id = 464767634483838977
daun_list = ['Кудряшев Даниил#2761']
starskvim = ['Starskvim#5342']

massage_on_message = [
    'снова что-то высрал. Господи, что же несет эта проститутка',
    'это было в твоей жопе или будет?',
    'опять обмазался говном и всем об этом сообщает...'
    'фу навонял'
    ')))'
    ')))))'
    ')))))))))'
]

god_names = [
    'Даунил',
    'Данилка',
    'Давалкин'
    'Технодемкин'
    'Дотер'
    'Данило'
    'Донный'
]


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_voice_state_update(member, before, after):
    if member.name + "#" + member.discriminator in WATCH_LIST:
        if before.channel != after.channel:
            channel = client.get_channel(CHANNEL_ID)
            user = await client.fetch_user(user_id)
            if after.channel is not None:
                await channel.send(
                    f"{user.mention}! Эй, "
                    + random.choice(god_names)
                    + f", {member.mention} зашел в канал {after.channel.name}, заходи, опущенка")
            else:
                await channel.send(
                    f"{user.mention}! Эй, "
                    + random.choice(god_names)
                    + f", {member.mention} вышел из канала {before.channel.name}, давай уже съебывай нахуй отсюда")
    # Replace USER_ID with the ID of the user you want to check for muting
    if member.name + "#" + member.discriminator in WATCH_LIST:
        if before.mute and not after.mute:
            # User was unmuted, do nothing
            text_channel = client.get_channel(CHANNEL_ID)
            await text_channel.send(f"{member.mention} развалил ебало, сейчас снова будет нести хуйню.")
            return
        elif not before.mute and after.mute:
            # User was muted, send message to text channel
            text_channel = client.get_channel(CHANNEL_ID)
            await text_channel.send(f"{member.mention} покорно завалил ебало.")
            return

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.author) in daun_list:
        user = await client.fetch_user(user_id)
        await message.channel.send(f"{user.mention}" + random.choice(massage_on_message))


@client.event
async def on_message_edit(before, after):
    if before.message.author == client.user:
        return

    if str(before.message.author) in daun_list:
        user = await client.fetch_user(user_id)
        await after.message.channel.send(f"{user.mention} обосрался?")


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    if str(message.author) in daun_list:
        user = await client.fetch_user(user_id)
        await message.channel.send(f"{user.mention} выронил кал из жопы и быстро съел")


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if str(user) in daun_list:
        channel = client.get_channel(CHANNEL_ID)
        user = await client.fetch_user(user_id)
        await channel.send(f"{user.mention} всем похуй на твое мнение {reaction}")

@client.event
async def on_member_update(before, after):
    if member.name + "#" + member.discriminator in daun_list:
        if before.activity != after.activity:
            if after.activity is not None and after.activity.type == discord.ActivityType.playing:
                game = after.activity.name
                print(f"{after.name} вместо развития играет в {game}!")
            else:
                game = before.activity.name
                print(f"{after.name} позорно слился в {game} и плачет ;'(")


client.run(os.environ["DISCORD_TOKEN"])
