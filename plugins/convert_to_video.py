#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time
import shutil
from moviepy.editor import *
import random

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram
from helper_funcs.ran_text import random_char


from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from trnl import Trnl


@pyrogram.Client.on_message(pyrogram.filters.command(["convert2video"]))
async def convert_to_video(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    if update.reply_to_message is not None:
        nfh = random_char(5)
        download_location = Config.DOWNLOAD_LOCATION + "/" + f'{nfh}' + "/"
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_FILE,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_FILE,
                a,
                c_time
            )
        )
        # don't care about the extension
        if the_real_download_location is not None:
            await bot.edit_message_text(
                text=Translation.SAVED_RECVD_DOC_FILE,
                chat_id=update.chat.id,
                message_id=a.message_id
            )
            await a.delete()
            up = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.UPLOAD_START,
            reply_to_message_id=update.message_id
            )
            
            logger.info(the_real_download_location)
            # get the correct width, height, and duration for videos greater than 10MB
            # ref: message from @BotSupport
            width = 0
            height = 0
            duration = 0
            metadata = extractMetadata(createParser(the_real_download_location))
            clip = VideoFileClip(the_real_download_location)
            screen_time = random.randint(120,600)
            clip.save_frame(Config.DOWNLOAD_LOCATION + "/" + f'{nfh}' + "/" + "thbnl1.jpg", t = screen_time)
            V_WIDTH = clip.w
            V_HEIGHT = clip.h
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            #if not os.path.exists(thumb_image_path):
                #thumb_image_path = None
            #else:
                #metadata = extractMetadata(createParser(thumb_image_path))
                #if metadata.has("width"):
                    #width = metadata.get("width")
                #if metadata.has("height"):
                    #height = metadata.get("height")
                # get the correct width, height, and duration for videos greater than 10MB
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                #Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                #img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                #img.resize((90, height))
                #img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            # try to upload file
            c_time = time.time()
            if "@" in str(Trnl.sh2.acell('J2').value):
                chnl_id = update.message.chat.id
            else:
                chnl_id = int(Trnl.sh2.acell('J2').value)
            vcap = Trnl.sh2.acell('D2').value
            if "Series" in Trnl.sh2.acell('P3').value:
                vd_name = description
            else:
                vd_name = vcap + " | " + Trnl.sh2.acell('H2').value
            await bot.send_video(
                chat_id=chnl_id,
                video=the_real_download_location,
                caption=vd_name,
                duration=duration,
                width=V_WIDTH,
                height=V_HEIGHT,
                supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=Config.DOWNLOAD_LOCATION + "/" + f'{nfh}' + "/" + "thbnl1.jpg",
                reply_to_message_id=update.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    up,
                    c_time
                )
            )
            try:
                os.remove(the_real_download_location)
                os.remove(thumb_image_path)
                shutil.rmtree(download_location)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                chat_id=update.chat.id,
                message_id=up.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_DOC_FOR_C2V,
            reply_to_message_id=update.message_id
        )
    
            
