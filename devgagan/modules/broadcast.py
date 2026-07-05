import asyncio
import datetime
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ChatType
from devgagan import app
from config import OWNER_ID
from devgagan.core.mongo.db import get_broadcast_config, update_broadcast_config, add_broadcast_deletion

# Helper to check if sender is owner
def is_owner(user_id):
    owner_list = OWNER_ID if isinstance(OWNER_ID, list) else [OWNER_ID]
    return any(str(user_id) == str(o) for o in owner_list)

def get_broadcast_menu_keyboard(is_active, interval_mins, delete_after_mins, max_runs, run_count):
    del_after_text = f"{delete_after_mins}m" if delete_after_mins else "Disabled ❌"
    max_runs_text = f"{max_runs}" if max_runs else "No Limit ♾️"
    
    buttons = [
        [
            InlineKeyboardButton(f"⚡ Status: {'ACTIVE ✅' if is_active else 'INACTIVE ❌'}", callback_data="abc_toggle_status")
        ],
        [
            InlineKeyboardButton("📝 Set Message", callback_data="abc_set_msg"),
            InlineKeyboardButton("⏱️ Set Interval", callback_data="abc_set_interval")
        ],
        [
            InlineKeyboardButton(f"🗑️ Auto-Delete: {del_after_text}", callback_data="abc_set_delete_after"),
            InlineKeyboardButton(f"🔢 Max Runs: {max_runs_text}", callback_data="abc_set_max_runs")
        ],
        [
            InlineKeyboardButton("🔄 Reset Run Count", callback_data="abc_reset_runs"),
            InlineKeyboardButton("🚀 Send Now", callback_data="abc_send_now")
        ],
        [
            InlineKeyboardButton("❌ Close Menu", callback_data="abc_close")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def get_interval_keyboard():
    buttons = [
        [
            InlineKeyboardButton("30 Minutes", callback_data="abc_select_interval_30"),
            InlineKeyboardButton("1 Hour", callback_data="abc_select_interval_60")
        ],
        [
            InlineKeyboardButton("2 Hours", callback_data="abc_select_interval_120"),
            InlineKeyboardButton("4 Hours", callback_data="abc_select_interval_240")
        ],
        [
            InlineKeyboardButton("8 Hours", callback_data="abc_select_interval_480"),
            InlineKeyboardButton("12 Hours", callback_data="abc_select_interval_720")
        ],
        [
            InlineKeyboardButton("24 Hours", callback_data="abc_select_interval_1440")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="abc_back")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def get_delete_after_keyboard():
    buttons = [
        [
            InlineKeyboardButton("Disabled (Don't Delete)", callback_data="abc_select_delete_after_0")
        ],
        [
            InlineKeyboardButton("2 Minutes", callback_data="abc_select_delete_after_2"),
            InlineKeyboardButton("5 Minutes", callback_data="abc_select_delete_after_5")
        ],
        [
            InlineKeyboardButton("10 Minutes", callback_data="abc_select_delete_after_10"),
            InlineKeyboardButton("15 Minutes", callback_data="abc_select_delete_after_15")
        ],
        [
            InlineKeyboardButton("30 Minutes", callback_data="abc_select_delete_after_30"),
            InlineKeyboardButton("60 Minutes", callback_data="abc_select_delete_after_60")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="abc_back")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def get_max_runs_keyboard():
    buttons = [
        [
            InlineKeyboardButton("No Limit (Infinite)", callback_data="abc_select_max_runs_0")
        ],
        [
            InlineKeyboardButton("1 Time", callback_data="abc_select_max_runs_1"),
            InlineKeyboardButton("2 Times", callback_data="abc_select_max_runs_2")
        ],
        [
            InlineKeyboardButton("5 Times", callback_data="abc_select_max_runs_5"),
            InlineKeyboardButton("10 Times", callback_data="abc_select_max_runs_10")
        ],
        [
            InlineKeyboardButton("20 Times", callback_data="abc_select_max_runs_20"),
            InlineKeyboardButton("50 Times", callback_data="abc_select_max_runs_50")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="abc_back")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def send_auto_broadcast_to_all(manual=False):
    config = await get_broadcast_config()
    message_text = config.get("message")
    if not message_text:
        return 0, 0

    delete_after_mins = config.get("delete_after_mins", 0)
    
    sent_count = 0
    failed_count = 0
    async for dialog in app.get_dialogs():
        chat = dialog.chat
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
            try:
                sent_msg = await app.send_message(chat.id, message_text)
                sent_count += 1
                
                # If auto-delete is enabled, schedule the deletion
                if delete_after_mins > 0:
                    delete_at = datetime.datetime.now() + datetime.timedelta(minutes=delete_after_mins)
                    await add_broadcast_deletion(chat.id, sent_msg.id, delete_at)
                    
                await asyncio.sleep(0.5)  # Avoid rate limits
            except Exception:
                failed_count += 1
                
    return sent_count, failed_count

@app.on_message(filters.command(["autobroadcast", "abc"]) & filters.private)
async def auto_broadcast_menu_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    if not is_owner(user_id):
        await message.reply_text("❌ **Access Denied:** Only the bot owner can use this command.")
        return

    config = await get_broadcast_config()
    msg_text = config.get("message", "None")
    interval = config.get("interval_mins", 60)
    is_active = config.get("is_active", False)
    delete_after_mins = config.get("delete_after_mins", 0)
    max_runs = config.get("max_runs", 0)
    run_count = config.get("run_count", 0)

    preview_text = (
        f"📢 **Automated Message Broadcast Settings**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚡ **Status:** `{'Active' if is_active else 'Inactive'}`\n"
        f"⏱️ **Interval:** `every {interval} minutes`\n"
        f"🗑️ **Auto-Delete After:** `{f'{delete_after_mins} mins' if delete_after_mins > 0 else 'Disabled'}`\n"
        f"🔢 **Runs Limit:** `{max_runs if max_runs > 0 else 'No Limit'}`\n"
        f"📊 **Current Run Count:** `{run_count}` times sent\n\n"
        f"📝 **Current Custom Message:**\n"
        f"----------------------------------------\n"
        f"{msg_text}\n"
        f"----------------------------------------\n\n"
        f"Use the settings below to manage the automatic broadcast:"
    )

    await message.reply_text(
        preview_text,
        reply_markup=get_broadcast_menu_keyboard(is_active, interval, delete_after_mins, max_runs, run_count)
    )

@app.on_callback_query(filters.regex(r"^abc_(toggle_status|set_msg|set_interval|send_now|close|back|set_delete_after|set_max_runs|reset_runs|select_interval_\d+|select_delete_after_\d+|select_max_runs_\d+)$"))
async def auto_broadcast_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if not is_owner(user_id):
        await callback_query.answer("❌ Access Denied!", show_alert=True)
        return

    data = callback_query.data
    config = await get_broadcast_config()

    if data == "abc_close":
        await callback_query.message.delete()
        return

    elif data == "abc_toggle_status":
        new_status = not config.get("is_active", False)
        await update_broadcast_config({"is_active": new_status})
        await callback_query.answer(f"Broadcast status: {'Activated' if new_status else 'Deactivated'}")

    elif data == "abc_reset_runs":
        await update_broadcast_config({"run_count": 0})
        await callback_query.answer("Run count reset to 0!")

    elif data == "abc_set_interval":
        await callback_query.message.edit_text(
            "⏱️ **Select Broadcast Interval:**\n\nChoose the time frequency for the broadcast message:",
            reply_markup=get_interval_keyboard()
        )
        return

    elif data == "abc_set_delete_after":
        await callback_query.message.edit_text(
            "🗑️ **Select Auto-Delete Duration:**\n\nChoose how long the sent broadcast messages should stay in the chat before being automatically deleted:",
            reply_markup=get_delete_after_keyboard()
        )
        return

    elif data == "abc_set_max_runs":
        await callback_query.message.edit_text(
            "🔢 **Select Maximum Run Limit:**\n\nChoose how many times the automated broadcast should send messages before automatically disabling itself:",
            reply_markup=get_max_runs_keyboard()
        )
        return

    elif data.startswith("abc_select_interval_"):
        mins = int(data.split("_")[-1])
        await update_broadcast_config({"interval_mins": mins})
        await callback_query.answer(f"Interval set to {mins} minutes")

    elif data.startswith("abc_select_delete_after_"):
        mins = int(data.split("_")[-1])
        await update_broadcast_config({"delete_after_mins": mins})
        await callback_query.answer(f"Auto-delete set to {f'{mins} minutes' if mins > 0 else 'Disabled'}")

    elif data.startswith("abc_select_max_runs_"):
        runs = int(data.split("_")[-1])
        await update_broadcast_config({"max_runs": runs})
        await callback_query.answer(f"Max runs set to {f'{runs} times' if runs > 0 else 'No Limit'}")

    elif data == "abc_back":
        pass  # Just falls through to refresh page

    elif data == "abc_send_now":
        await callback_query.message.edit_text("🚀 **Broadcasting message to all chats in the background...**")
        sent, failed = await send_auto_broadcast_to_all(manual=True)
        await callback_query.message.reply_text(
            f"✅ **Broadcast Completed!**\n\n"
            f"• Successfully sent: `{sent}` chats\n"
            f"• Failed/skipped: `{failed}` chats"
        )

    elif data == "abc_set_msg":
        await callback_query.message.delete()
        ask = await client.ask(user_id, "📝 **Send your custom broadcast message now (formatting bold/italic/blockquote is fully supported!).**\n\n> Send /cancel to abort.")
        if ask.text == "/cancel":
            await ask.reply("Action cancelled.")
        else:
            # Preserve all markdown formatting entities
            message_text = ask.text.markdown if hasattr(ask.text, 'markdown') else ask.text
            await update_broadcast_config({"message": message_text})
            await ask.reply("✅ **Broadcast message saved successfully (with formatting)!**")
        
        await asyncio.sleep(0.5)
        await auto_broadcast_menu_cmd(client, ask)
        return

    # Refresh page
    config = await get_broadcast_config()
    msg_text = config.get("message", "None")
    interval = config.get("interval_mins", 60)
    is_active = config.get("is_active", False)
    delete_after_mins = config.get("delete_after_mins", 0)
    max_runs = config.get("max_runs", 0)
    run_count = config.get("run_count", 0)

    preview_text = (
        f"📢 **Automated Message Broadcast Settings**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚡ **Status:** `{'Active' if is_active else 'Inactive'}`\n"
        f"⏱️ **Interval:** `every {interval} minutes`\n"
        f"🗑️ **Auto-Delete After:** `{f'{delete_after_mins} mins' if delete_after_mins > 0 else 'Disabled'}`\n"
        f"🔢 **Runs Limit:** `{max_runs if max_runs > 0 else 'No Limit'}`\n"
        f"📊 **Current Run Count:** `{run_count}` times sent\n\n"
        f"📝 **Current Custom Message:**\n"
        f"----------------------------------------\n"
        f"{msg_text}\n"
        f"----------------------------------------\n\n"
        f"Use the settings below to manage the automatic broadcast:"
    )

    await callback_query.message.edit_text(
        preview_text,
        reply_markup=get_broadcast_menu_keyboard(is_active, interval, delete_after_mins, max_runs, run_count)
    )
