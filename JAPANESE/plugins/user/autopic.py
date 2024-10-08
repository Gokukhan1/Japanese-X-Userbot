import asyncio
from datetime import datetime
from pathlib import Path
from random import choice
from shutil import copyfile

from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters, Client
from config import OWNER_ID
from config import CMD_HANDLER
from JAPANESE.nxtgenhelper.basic import eor
from .help import *


__XOR = []
FIRST_TIME = True
DIM = [(100, 200), (1280, 200), (1280, 1600), (100, 1600)]


async def _autopic(_, delay):
    global FIRST_TIME

    while bool(__XOR):
        await asyncio.sleep(delay)
        original = "JAPANESE/SAKURA/autopic-template.jpg"
        photo = "pic.png"
        copyfile(original, photo)
        current_time = datetime.now().strftime(
            f'%H:%M %d-%m-%y\nA Samurai should always be prepared\nfor death.\nwhether his own or\nsomeone else.'
        )
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("JAPANESE/SAKURA/autopic-font-ubuntu.ttf", 60)
        drawn_text.text(choice(DIM), current_time, font=fnt, fill=(0, 0, 0))
        img.save(photo)
        try:
            if not FIRST_TIME:
                async for pic in _.get_chat_photos("me", limit=1):
                    await _.delete_profile_photos(pic.file_id)
                    await asyncio.sleep(2)
            await _.set_profile_photo(photo=photo)
            FIRST_TIME = False
        except Exception as exc:
            print("Autopic Error: " + exc)
        finally:
            Path(photo).unlink()


@Client.on_message(filters.command(["autopic"], cmd) & filters.me)
async def autopic_nobi(_, m):
    global __XOR
    arc = await eor(m, "...")
    if bool(__XOR):
        __XOR[0].cancel()
        t = "`Autopic Stopped Successfully.`"
        __XOR.clear()
    else:
        _task = _autopic(_, delay=300)
        task = asyncio.create_task(_task)
        __XOR.append(task)
        t = "`Started Autopic.`"
    await arc.edit_text(t)


add_command_help(
    "•─╼⃝𖠁 Aᴜᴛᴏ ᴘɪᴄ",
    [
       ["autopic", "Cʜᴀɴɢᴇ ʏᴏᴜʀ DP ᴇᴠᴇʀʏ 5 ᴍɪɴᴜᴛᴇ Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴏᴘ ᴀᴜᴛᴏ ᴘɪᴄ ᴛʀʏ ᴀᴜᴛᴏᴘɪᴄ ᴀɢᴀɪɴ ᴛᴏ sᴛᴏᴘ ɪᴛ."],
        ],
  )
