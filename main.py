import os
import random
import discord
from discord.ext import tasks
import copy
print(1+3)
# start bot and run redis
intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents, command_prefix='/')

CHANNEL_ID = 850284466680758282


@client.event
async def on_ready():
    kto_chiya.start()


@tasks.loop(hours=24)
async def kto_chiya():
    list_user_ids = [771060320474103868, 330617931362729985, 364836085592752139, 236893809886232577, 414517713168367617,
                     323122393591709696, 464767634483838977, 236860833882177536, 236240664340201482,
                     298091789649313795, 312579123585351680]
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
            spisok += f'{user.mention} не подчиняется никому!\n'
        else:
            spisok += f'У {user.mention} в подчинении: {", ".join([(await client.fetch_user(x)).mention for x in master[1]])}!\n'
    spisok += "Список считается окончательным и обжалованию не подлежит."
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(spisok)
    list_user_ids = [771060320474103868, 330617931362729985, 364836085592752139, 236893809886232577, 414517713168367617,
                     323122393591709696, 464767634483838977, 236860833882177536, 236240664340201482,
                     298091789649313795, 312579123585351680]
    user = await client.fetch_user(random.choice(list_user_ids))
    await channel.send(f'Сегодня не натурал: {user.mention}')
    user = await client.fetch_user(random.choice(list_user_ids))
    await channel.send(f'Сегодня не уважает ветеранов: {user.mention}')

client.run(os.environ["DISCORD_TOKEN"])
