import contextvars
import functools
import os
import random
import time

import discord
import threading
import schedule
import asyncio
import aioredis

# start bot and run redis
intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)
redis = aioredis.from_url(os.environ["REDIS_URL"])

CHANNEL_ID = 850284466680758282
WATCH_LIST = ["00.#3516", "Vaflz#3717", "EinsOrange#4068"]
DAUNIL_ID = 464767634483838977
DAUNIL_LIST = ['Кудряшев Даниил#2761']
CURRENT_WATCHER_COUNT = "CURRENT_WATCHER_COUNT"

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
    await proceed_watcher_entered(member, before, after)
    await proceed_daun_entered(member, before, after)
    await proceed_mute_action(member, before, after)


async def proceed_watcher_entered(member, before, after):
    if member.name + "#" + member.discriminator in WATCH_LIST:
        if before.channel != after.channel:
            channel = client.get_channel(CHANNEL_ID)
            user = await client.fetch_user(DAUNIL_ID)
            if after.channel is not None:
                if user in channel.members:
                    return
                await channel.send(
                    f"{user.mention}! Эй, "
                    + random.choice(god_names)
                    + f", {member.mention} зашел в канал {after.channel.name}, заходи, опущенка")
                await redis.incr(CURRENT_WATCHER_COUNT)
            else:
                if user not in channel.members:
                    return
                await channel.send(
                    f"{user.mention}! Эй, "
                    + random.choice(god_names)
                    + f", {member.mention} вышел из канала {before.channel.name}, давай уже съебывай нахуй отсюда")
                await redis.decr(CURRENT_WATCHER_COUNT)


async def proceed_daun_entered(member, before, after):
    if member.name + "#" + member.discriminator in DAUNIL_LIST:
        if before.channel != after.channel:
            channel = client.get_channel(CHANNEL_ID)
            user = await client.fetch_user(DAUNIL_ID)
            counter = await redis.get(CURRENT_WATCHER_COUNT)
            if counter > 0:
                await channel.send(
                    "Чмоня "
                    + f"{user.mention}! успешно зашла на канал "
                    + f"{before.channel.name}, хоть кто-то его спас от одиночества")


async def proceed_mute_action(member, before, after):
    await redis.incr("SPAM_COUNT")
    spamming = redis.get("SPAM_COUNT")
    if spamming == 3:
        text_channel = client.get_channel(CHANNEL_ID)
        await text_channel.send(f"{member.mention} хватит спамить, шлюшка")
        return
    if spamming > 3:
        return
    if member.name + "#" + member.discriminator in DAUNIL_LIST:
        if before.self_mute and not after.self_mute:
            # User was unmuted, do nothing
            text_channel = client.get_channel(CHANNEL_ID)
            await text_channel.send(f"{member.mention} развалил ебало, сейчас снова будет нести хуйню.")
            return
        elif not before.self_mute and after.self_mute:
            # User was muted, send message to text channel
            text_channel = client.get_channel(CHANNEL_ID)
            await text_channel.send(f"{member.mention} покорно завалил ебало.")
            return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.author) in DAUNIL_LIST:
        user = await client.fetch_user(DAUNIL_ID)
        await message.channel.send(f"{user.mention}" + " " + random.choice(massage_on_message))


@client.event
async def on_message_edit(before, after):
    if before.message.author == client.user:
        return

    if str(before.message.author) in DAUNIL_LIST:
        user = await client.fetch_user(DAUNIL_ID)
        await after.message.channel.send(f"{user.mention} обосрался?")


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    if str(message.author) in DAUNIL_LIST:
        user = await client.fetch_user(DAUNIL_ID)
        await message.channel.send(f"{user.mention} выронил кал из жопы и быстро съел")


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if str(user) in DAUNIL_LIST:
        channel = client.get_channel(CHANNEL_ID)
        user = await client.fetch_user(DAUNIL_ID)
        await channel.send(f"{user.mention} всем похуй на твое мнение {reaction}")


@client.event
async def on_member_update(before, after):
    if member.name + "#" + member.discriminator in DAUNIL_LIST:
        if before.activity != after.activity:
            if after.activity is not None and after.activity.type == discord.ActivityType.playing:
                game = after.activity.name
                print(f"{after.name} вместо развития играет в {game}!")
            else:
                game = before.activity.name
                print(f"{after.name} позорно слился в {game} и плачет ;'(")


async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


async def say_about_techdemo_nice():
    channel = client.get_channel(CHANNEL_ID)
    user = await client.fetch_user(DAUNIL_ID)
    await redis.incr("TECH_DEMO_DAYS")
    days = redis.get("TECH_DEMO_DAYS")
    await channel.send(f"Дней без технодемки {user.mention}: {days} (((")


async def clean_spam():
    await redis.set("SPAM_COUNT", 0)


schedule.every().day.at("15:00").do(asyncio.to_thread, say_about_techdemo_nice)
schedule.every().minute.do(asyncio.to_thread, say_about_techdemo_nice)


# Define a function to run the scheduler in a new thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(5)


# Start the scheduler in a new thread
thread = threading.Thread(target=run_scheduler)
thread.start()

client.run(os.environ["DISCORD_TOKEN"])
