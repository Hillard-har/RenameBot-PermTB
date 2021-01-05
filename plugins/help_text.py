import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import time
import os
import sqlite3
import asyncio

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import script

import pyrogram

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram.errors import UserNotParticipant

from plugins.rename_file import rename_doc


@Client.on_message(filters.command(["help"]))
def help_user(bot, update):
    bot.send_message(
        chat_id=update.chat.id,
        text=script.HELP_USER,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="⭕️ Contact DEV ⭕️", url="https://t.me/prgofficial")]]),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["start"]))
def send_start(bot, update):
    # logger.info(update)
    
    bot.send_message(
        chat_id=update.chat.id,
        text=script.START_TEXT.format(update.from_user.first_name),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["upgrade"]))
def upgrade(bot, update):
    # logger.info(update)

    bot.send_message(
        chat_id=update.chat.id,
        text=script.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

    
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.voice | filters.video_note))
async def rename_cb(bot, update):

    p = await update.reply_text('ᴘʀᴏᴄᴇssɪɴɢ ʀᴇϙᴜᴇsᴛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...😴', True)
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
           user = await bot.get_chat_member(update_channel, update.chat.id)
           if user.status == "kicked":
               await p.edit_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**",True)
               return
        except UserNotParticipant:
            #await p.delete()
            await p.edit_text(
                text="⚠️ 𝐒𝐎𝐑𝐑𝐘 𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆 𝐂𝐀𝐍𝐂𝐄𝐋𝐋𝐄𝐃 **\n\nʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="♥️ 𝙹𝚘𝚒𝚗", url=f"https://t.me/Anylink_Movies")]
              ]) 
            )
            return
        except Exception:
            await p.edit_text("⛔ sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ. ᴄᴏɴᴛᴀᴄᴛ @stemlime_bot")
            return
    chat_id = update.chat.id
    if bot.CURRENT_PROCESSES.get(chat_id, 0) == Config.MAX_PROCESSES_PER_USER:
        await p.edit_text(
            text=script.MAX_PROCESS,
            #chat_id=update.chat.id,
            #reply_to_message_id=update.message_id
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔐 CLOSE", callback_data = 'close')]])
        )
        return
    
    file = update.document or update.video or update.audio or update.voice or update.video_note
    try:
        filename = file.file_name
    except:
        filename = "Not Available"

    await p.delete()
    await bot.send_message(
        chat_id=update.chat.id,
        text="<b>ғɪʟᴇ ɴᴀᴍᴇ :</b> : <code>{}</code> \n\nSelect the desired option below 😇".format(filename),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="📝 RENAME 📝", callback_data="rename_button")],
                                                [InlineKeyboardButton(text="✖️ CANCEL ✖️", callback_data="cancel_e")]]),
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True   
    )   


async def cancel_extract(bot, update):
    
    await bot.send_message(
        chat_id=update.chat.id,
        text="Process Cancelled 🙃",
    )
