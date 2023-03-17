# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands

CHANNEL_ID = 850284466680758282

# Здесь вы можете указать список пользователей, за которыми нужно следить
WATCH_LIST = ["00.#3516", "Vaflz#3717"]
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)
user_id = 464767634483838977

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
                await channel.send(f"{user.mention}!Эй, Даунил,{member.mention} зашел в канал {after.channel.name}, заходи, опущенка")
            else:
                await channel.send(f"{user.mention}!Эй, Даунил, {member.mention} вышел из канала {before.channel.name}, давай уже съебывай нахуй отсюда")


client.run(os.environ["DISCORD_TOKEN"])
