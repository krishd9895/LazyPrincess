# with Love @LazyDeveloperr 💘
# Subscribe YT @LazyDeveloperr - to learn more about this for free...

import math
import json
import asyncio
import shutil
import os
import requests
from database.users_chats_db import db
from pyrogram.types import Thumbnail
from database.add import add_user_to_database
from lazybot.ran_text import random_char
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from database.lazy_utils import  humanbytes
from pyrogram import Client
from pyrogram import filters
from Script import script
import time
from urllib.parse import urlparse
from info import LOG_CHANNEL, DOWNLOAD_LOCATION, HTTP_PROXY, AUTH_CHANNEL, BANNED_USERS, CHUNK_SIZE,ADMINS,PRIME_DOWNLOADERS
from PIL import Image
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private & filters.user(ADMINS) & filters.regex(pattern=".*http.*"))
async def echo(client, message):
    if LOG_CHANNEL:
        try:
            log_message = await message.forward(LOG_CHANNEL)
            log_info = "Message Sender Information\n"
            log_info += "\nFirst Name: " + message.from_user.first_name
            log_info += "\nUser ID: " + str(message.from_user.id)
            log_info += "\nUsername: @" + message.from_user.username if message.from_user.username else ""
            log_info += "\nUser Link: " + message.from_user.mention
            await log_message.reply_text(
                text=log_info,
                disable_web_page_preview=True,
                quote=True
            )
        except Exception as error:
            print(error)
    if not message.from_user:
        return await message.reply_text("What the hell is this 🤐")

    logger.info(message.from_user)
    url = message.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    print(f"{url}")
    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in message.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(url)
        logger.info(file_name)
    else:
        for entity in message.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                url = url[o:o + l]

    ######################## 
    if "youtu" in url or "youtube" in url:
        try:
            ydl_opts = {}
            if youtube_dl_username and youtube_dl_password:
                ydl_opts['username'] = youtube_dl_username
                ydl_opts['password'] = youtube_dl_password

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', 'undefined')
                video_duration = info_dict.get('duration', 'undefined')
                video_filesize = info_dict.get('filesize', 0)

                namee = video_title
                size = humanbytes(video_filesize) if video_filesize else 'undefined'

                usr_id = message.chat.id
                user_data = await db.get_user_data(usr_id)
                if not user_data:
                    await message.edit("Failed to fetch your data from database!")
                    return
                upload_as_doc = user_data.get("upload_as_doc", False)
                upload_type = f" {'🎥 ᴠɪᴅᴇᴏ' if upload_as_doc else '🗃️ ғɪʟᴇ'}"

                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            "🎬 Download Video",
                            callback_data=f"video|{randint(1000, 9999)}"
                        ),
                        InlineKeyboardButton(
                            "🎵 Download Audio",
                            callback_data=f"audio|{randint(1000, 9999)}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔒 Close",
                            callback_data='close'
                        )
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(inline_keyboard)

                await client.send_message(
                    chat_id=message.chat.id,
                    text=f"⏯<b>File Name:</b> {namee}\n\n🧬<b>File Size:</b> {size} \n<b>⩙ Upload Type:</b> {upload_type}",
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML,
                    reply_to_message_id=message.id
                )

        except Exception as e:
            logger.error(f"Error processing YouTube link: {e}")
            await message.reply_text("Failed to process YouTube link.")
            
    else:
        try:
            xLAZY_BAAPUx_d_size = requests.head(url)
            xLAZY_BAAPUx_t_length = int(xLAZY_BAAPUx_d_size.headers.get("Content-Length", 0))
            xLAZY_BAAPUx_path = urlparse(url).path
            xLAZY_BAAPUx_u_name = os.path.basename(xLAZY_BAAPUx_path)
            total_length = humanbytes(xLAZY_BAAPUx_t_length)
            logger.info(total_length)
            size = total_length
            namee = xLAZY_BAAPUx_u_name

            usr_id = message.chat.id
            user_data = await db.get_user_data(usr_id)
            if not user_data:
                await message.edit("Failed to fetch your data from database!")
                return
            upload_as_doc = user_data.get("upload_as_doc", False)
            upload_type = f" {'🎥 ᴠɪᴅᴇᴏ' if upload_as_doc else '🗃️ ғɪʟᴇ'}"

            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        "🎬 Download Media",
                        callback_data=f"media|{randint(1000, 9999)}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔒 Close",
                        callback_data='close'
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)

            await client.send_message(
                chat_id=message.chat.id,
                text=f"⏯<b>File Name:</b> {namee}\n\n🧬<b>File Size:</b> {size} \n<b>⩙ Upload Type:</b> {upload_type}",
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )

        except Exception as e:
            logger.error(f"An error occurred: {e}")

