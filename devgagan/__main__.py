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
    print("Auto removal started ...")
    await idle()
    print("Bot stopped...")


if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #
