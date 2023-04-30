import os
import random
import aiohttp
import discord
import aioredis
from discord.ext import tasks
from datetime import datetime
import json
import copy


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

variations_ivan = [
    "%дни% дней без нейросетевого двачера от Ивана.",
    "%дни% дней без нейросетевого двачера от Ивана, как же долго это продолжается...",
    "%дни% дней без нейросетевого двачера от Ивана, может, пора вернуться?",
    "%дни% дней без нейросетевой машины."
]


@client.event
async def on_ready():
    print("Bot is ready")
    say_about_techdemo_nice.start()
    clean_spam.start()
    kto_chiya.start()


@client.event
async def on_voice_state_update(member, before, after):
    if (member.name + "#" + member.discriminator in WATCH_LIST) or (
            member.name + "#" + member.discriminator in DAUNIL_LIST):
        if not await check_spam():
            return
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
            if after.channel is None:
                return
            channel = client.get_channel(CHANNEL_ID)
            user = await client.fetch_user(DAUNIL_ID)
            counter = int(await redis.get(CURRENT_WATCHER_COUNT))
            if counter > 0:
                await channel.send(
                    "Чмоня "
                    + f"{user.mention}! успешно зашла на канал "
                    + f"{after.channel.name}, хоть кто-то его спас от одиночества")


async def check_spam():
    await redis.incr("SPAM_COUNT")
    spamming = int(await redis.get("SPAM_COUNT"))
    user = await client.fetch_user(DAUNIL_ID)
    if spamming == 4:
        text_channel = client.get_channel(CHANNEL_ID)
        await text_channel.send(f"{user.mention} хватит спамить, шлюшка")
        return True
    if spamming > 4:
        return False
    return True


async def proceed_mute_action(member, before, after):
    if False:
        if before.self_mute and not after.self_mute:
            # User was unmuted
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
        if not await check_spam():
            return
        user = await client.fetch_user(DAUNIL_ID)
        await message.channel.send(f"{user.mention}" + " " + random.choice(massage_on_message))


@client.event
async def on_message_edit(before, after):
    if str(before.message.author) in DAUNIL_LIST:
        if not await check_spam():
            return
        user = await client.fetch_user(DAUNIL_ID)
        await after.message.channel.send(f"{user.mention} обосрался?")


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    if str(message.author) in DAUNIL_LIST:
        if not await check_spam():
            return
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
    if before.member.name + "#" + before.member.discriminator in DAUNIL_LIST:
        if before.activity != after.activity:
            if after.activity is not None and after.activity.type == discord.ActivityType.playing:
                game = after.activity.name
                print(f"{after.name} вместо развития играет в {game}!")
            else:
                game = before.activity.name
                print(f"{after.name} позорно слился в {game} и плачет ;'(")


async def get_balabola(text):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                      '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Origin': 'https://yandex.ru',
        'Referer': 'https://yandex.ru/',
    }

    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": text, "intro": random.randrange(0, 7, 6), "filter": 1}
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=json.dumps(payload), headers=headers) as response:
            resp_json = await response.json()
            return text + " " + resp_json["text"]


@tasks.loop(hours=8)
async def say_about_techdemo_nice():
    channel = client.get_channel(CHANNEL_ID)
    date_string = os.environ["TECH_DEMO_COUNTER_START_DATE"]
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    today = datetime.now()
    difference_in_days = (today - date_obj).days
    user = await client.fetch_user(DAUNIL_ID)
    user2 = await client.fetch_user(771060320474103868)
    await channel.send(f"{user.mention}!\n" + await get_balabola(f"{difference_in_days} дней без технодемки даниила"))
    await channel.send(f"{user2.mention}!\n" + await get_balabola(
        random.choice(variations_ivan).replace("%дни%", str(difference_in_days - 17))))

@tasks.loop(hours=24)
async def kto_chiya():
    list_user_ids = [771060320474103868, 330617931362729985, 364836085592752139, 236893809886232577, 414517713168367617, 323122393591709696, 464767634483838977, 236860833882177536, 236240664340201482, 295268744001748993, 298091789649313795]
    random.shuffle(list_user_ids)
    free_user_ids = copy.deepcopy(list_user_ids)
    random.shuffle(free_user_ids)
    master_list_ids = []
    total_podch = 0
    spisok = "Кто чья сегодня?\n"
    for user in free_user_ids:
        if not (user in list_user_ids):
            continue
        list_user_ids.remove(user)
        podch_count = random.choices([0, 1, 2, 3], [0.105, 0.65, 0.25, 0.05])[0]
        if podch_count == 0:
            master_list_ids.append([user, []])
            continue
        if (total_podch + podch_count) >= len(free_user_ids):
            podch_count = len(list_user_ids) - total_podch
        total_podch += podch_count
        mlist = []
        for i in range(podch_count):
            if len(list_user_ids) == 0:
                break
            n = random.choice(list_user_ids)
            list_user_ids.remove(n)
            mlist.append(n)
        master_list_ids.append([user, mlist])

    for master in master_list_ids:
        user = await client.fetch_user(master[0])
        if len(master[1]) == 0:
            spisok+=f'{user.mention} не подчиняется никому!\n'
        else:
            spisok += f'У {user.mention} в подчинении: {", ".join([(await client.fetch_user(x)).mention for x in master[1]])}!\n'
    spisok += "Список считается окончательным и обжалованию не подлежит."
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(spisok)

@tasks.loop(minutes=2)
async def clean_spam():
    await redis.set("SPAM_COUNT", 0)


client.run(os.environ["DISCORD_TOKEN"])
