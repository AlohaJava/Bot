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

massage_on_message = [
    'снова что-то высрал. Господи, что же несет эта проститутка',
    'это было в твоей жопе или будет?',
    'опять обмазался говном и всем об этом сообщает...'
    'фу навонял'
    ')))'
    ')))))'
    ')))))))))'
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
                    f"{user.mention}! Эй, Даунил, {member.mention} зашел в канал {after.channel.name}, заходи, опущенка")
            else:
                await channel.send(
                    f"{user.mention}! Эй, Даунил, {member.mention} вышел из канала {before.channel.name}, давай уже съебывай нахуй отсюда")


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
async def on_voice_state_update(member, before, after):
    if before.message.author == client.user:
        return

    if str(before.message.author) in daun_list:
        user = await client.fetch_user(user_id)
        await after.message.channel.send(f"{user.mention} покорно завалил ебало")


client.run(os.environ["DISCORD_TOKEN"])
