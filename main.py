import os
import random
import discord
from discord.ext import tasks

# Constants
CHANNEL_ID = 850284466680758282
USER_IDS = [
    771060320474103868, 330617931362729985, 364836085592752139,
    236893809886232577, 414517713168367617, 323122393591709696,
    464767634483838977, 236860833882177536, 236240664340201482,
    298091789649313795, 312579123585351680
]

# Configuring bot intents and client
intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready.")
    daily_assignment.start()

@tasks.loop(hours=24)
async def daily_assignment():
    shuffled_user_ids = random.sample(USER_IDS, len(USER_IDS))
    master_list_ids = []
    total_podch = 0
    announcement_text = "Кто чья сегодня?\n"
    
    while shuffled_user_ids:
        user_id = shuffled_user_ids.pop()
        podch_count = random.choices([0, 1, 2, 3], [0.105, 0.65, 0.25, 0.05])[0]
        if podch_count == 0 or not shuffled_user_ids:
            master_list_ids.append((user_id, []))
            continue
        if total_podch + podch_count > len(shuffled_user_ids):
            podch_count = len(shuffled_user_ids) - total_podch
        total_podch += podch_count
        subordinates = random.sample(shuffled_user_ids, podch_count)
        for sub_id in subordinates:
            shuffled_user_ids.remove(sub_id)
        master_list_ids.append((user_id, subordinates))
    
    for master_id, subs in master_list_ids:
        master_mention = (await client.fetch_user(master_id)).mention
        if not subs:
            announcement_text += f'{master_mention} не подчиняется никому!\n'
        else:
            subs_mentions = ', '.join([(await client.fetch_user(sub_id)).mention for sub_id in subs])
            announcement_text += f'У {master_mention} в подчинении: {subs_mentions}!\n'
    announcement_text += "Список считается окончательным и обжалованию не подлежит."
    
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(announcement_text)
    for special_announcement in ["Сегодня не натурал", "Сегодня не уважает ветеранов"]:
        user_mention = (await client.fetch_user(random.choice(USER_IDS))).mention
        await channel.send(f'{special_announcement}: {user_mention}')

if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
