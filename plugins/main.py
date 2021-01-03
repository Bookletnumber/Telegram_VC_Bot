import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import owner_id, sudo_chat_id, jio_saavn_api
from youtube_search import YoutubeSearch

#Global vars
s = None # For subprocess
m = None # For message

# Ping

@Client.on_message(filters.command(["ping"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def ping(_, message: Message):
    j = await message.reply_text("Wait, Pinging all Datacenters`")
    result = ""
    for i in range(1, 6):
        datacenter = (f"https://cdn{i}.telesco.pe")
        ping1 = round(requests.head(datacenter).elapsed.total_seconds() * 1000)
        result += f'`DC{i} - {ping1}ms`\n'
    await j.edit(result)

# Start

@Client.on_message(filters.command(["start"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def start(_, message: Message):
    await message.reply_text("Hi I'm Telegram Voice Chat Bot, Pressing /help wen?")

# Help

@Client.on_message(filters.command(["help"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def help(_, message: Message):
    await message.reply_text('''Currently These Commands Are Supported.
/start To Start The bot.
/help To Show This Message.
/ping To Ping All Datacenters Of Telegram.
/stop To Stop Any Playing Music.
"/jiosaavn <song_name>" To Play A Song From Jiosaavn.
"/ytsearch <song_name>" To Search For A Song On Youtube.
"/youtube <song_link>" To Play A Song From Youtube.

NOTE: Do Not Assign These Commands To Bot Via BotFather''')

# Jiosaavn

@Client.on_message(filters.command(["jiosaavn"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def jiosaavn(_, message: Message):
    global s
    global m
    if len(message.command) != 2:
        await message.reply_text("/jiosaavn requires one argument")
        return

    query = message.command[1]
    m = await message.reply_text("Searching...")
    r = requests.get(f"{jio_saavn_api}{query}")


    sname = r.json()[0]['song']
    slink = r.json()[0]['media_url']
    ssingers = r.json()[0]['singers']
    await m.edit(f"Playing {sname}-{ssingers}")
    s = await asyncio.create_subprocess_shell(f"mpv {slink} --no-video", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await s.communicate()
    await m.delete()


# Youtube Searching

@Client.on_message(filters.command(["ytsearch"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def youtube_search(_, message: Message):

    if len(message.command) != 2:
        await message.reply_text("/youtube requires one argument")
        return

    query = message.command[1]
    m = await message.reply_text("Searching....")
    results = YoutubeSearch(query, max_results=4).to_dict()
    i = 0
    text = ""
    while i < 4:
        text += f"Title - {results[i]['title']}\n"
        text += f"Duration - {results[i]['duration']}\n"
        text += f"Views - {results[i]['views']}\n"
        text += f"Channel - {results[i]['channel']}\n"
        text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
        i += 1
    await m.edit(text, disable_web_page_preview=True)


# Youtube Playing

@Client.on_message(filters.command(["youtube"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def youtube(_, message: Message):
    global m
    global s
    if len(message.command) != 2:
        await message.reply_text("/youtube requires one argument")
        return

    query = message.command[1]
    m = await message.reply_text("Playing")
    s = await asyncio.create_subprocess_shell(f"mpv {query} --no-video", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await s.communicate()
    await m.delete()


# Stop

@Client.on_message(filters.command(["stop"]) & (filters.chat(int(sudo_chat_id))) & (filters.user(owner_id)))
async def stop(_, message: Message):
    s.terminate()
    try:
        await m.delete()
    except:
        pass

    i = await message.reply_text("Stopped!")
    await asyncio.sleep(5)
    await i.delete()



