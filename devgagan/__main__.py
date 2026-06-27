# ---------------------------------------------------
# File Name: __main__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

import asyncio
import importlib
import gc
from pyrogram import idle
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler

# ----------------------------Bot-Start---------------------------- #

loop = asyncio.get_event_loop()

# Function to schedule expiry checks
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)  # Check every hour
        gc.collect()

# Function to broadcast upgrade plans daily at 7 PM
async def daily_plans_broadcast_task():
    try:
        from devgagan.core.mongo.users_db import get_all_registered_users
        from devgagan.core.func import chk_user
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        from devgagan import app
        
        users = await get_all_registered_users()
        upgrade_msg = (
            "⚡ **𝖴𝗉𝗀𝗋𝖺𝖽𝖾 𝗍𝗈 𝖯𝖱𝖮!** ⚡\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✨ **𝖴𝗇𝗅𝗈𝖼𝗄 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌:**\n"
            "• **𝖴𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖡𝖺𝗍𝖼𝗁 𝖫𝗂𝗆𝗂𝗍𝗌** (5000+ files!)\n"
            "• **𝖲𝗎𝗉𝖾𝗋 𝖥𝖺𝗌𝗍 𝖯𝖺𝗋𝖺𝗅𝗅𝖾𝗅 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗀** 🚀\n"
            "• **𝖭𝗈 𝖠𝖽𝗌 & 𝖢𝗎𝗌𝗍𝗈𝗆 𝖡𝗋𝖺𝗇𝖽𝗂𝗇𝗀** 🏷️\n"
            "• **𝖣𝗂𝗋𝖾𝖼𝗍 𝖱𝖾𝗌𝖾𝗅𝗅𝖾𝗋 𝖲𝗎𝗉𝗉𝗈𝗋𝗍** 👑\n\n"
            "👉 Use `/plans` to view details & upgrade today!"
        )
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
                [InlineKeyboardButton("💬 Contact Now", url="https://t.me/CHOSEN_ONEx_bot")],
            ]
        )
        
        count = 0
        for uid in users:
            try:
                freecheck = await chk_user(None, uid)
                if freecheck == 1:
                    await app.send_message(uid, upgrade_msg, reply_markup=buttons)
                    count += 1
                    await asyncio.sleep(0.1)
            except Exception:
                pass
        print(f"[DAILY BROADCAST] Sent daily plans upgrade message to {count} free users.")
    except Exception as e:
        print(f"[DAILY BROADCAST] Error: {e}")

async def schedule_daily_plans_broadcast():
    import datetime
    last_sent_date = None
    while True:
        now = datetime.datetime.now()
        if now.hour == 19 and now.minute == 0:
            current_date = now.date()
            if last_sent_date != current_date:
                print(f"[DAILY BROADCAST] Starting daily 7 PM upgrade plans broadcast...")
                await daily_plans_broadcast_task()
                last_sent_date = current_date
        await asyncio.sleep(30)

async def devggn_boot():
    # Restore custom thumbnails from DB on startup
    from devgagan.core.mongo.db import load_all_thumbnails
    from config import THUMBNAIL_DIR
    try:
        await load_all_thumbnails(THUMBNAIL_DIR)
    except Exception as e:
        print(f"Failed to load thumbnails: {e}")

    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)

    # Load Youtube downloader package modules dynamically
    import glob
    from os.path import basename
    youtube_mod_files = glob.glob("Youtube/*.py")
    for f in youtube_mod_files:
        mod_name = basename(f)[:-3]
        if mod_name not in ["__init__", "config"]:
            try:
                importlib.import_module(f"Youtube.{mod_name}")
                print(f"Loaded Youtube module: {mod_name}")
            except Exception as e:
                print(f"Failed to load Youtube module {mod_name}: {e}")

    print("""
---------------------------------------------------
Bot Deployed successfully ...
Description: A Pyrogram bot for downloading files from Telegram channels or groups 
                and uploading them back to Telegram.
Author: Gagan
GitHub: https://github.com/devgaganin/
Telegram: https://t.me/team_spy_pro
YouTube: https://youtube.com/@dev_gagan
Created: 2025-01-11
Last Modified: 2025-01-11
Version: 2.0.5
License: MIT License
---------------------------------------------------
""")

    asyncio.create_task(schedule_expiry_check())
    asyncio.create_task(schedule_daily_plans_broadcast())
    print("Auto removal and daily plans broadcast started ...")
    await idle()
    print("Bot stopped...")


if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #
