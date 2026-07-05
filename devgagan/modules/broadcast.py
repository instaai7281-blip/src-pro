import asyncio
import datetime
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ChatType
from devgagan import app
from config import OWNER_ID
from devgagan.core.mongo.db import get_broadcast_config, update_broadcast_config

# Helper to check if sender is owner
def is_owner(user_id):
    owner_list = OWNER_ID if isinstance(OWNER_ID, list) else [OWNER_ID]
    return any(str(user_id) == str(o) for o in owner_list)

def get_broadcast_menu_keyboard(is_active, interval_mins):
    buttons = [
        [
            InlineKeyboardButton(f"⚡ Status: {'ACTIVE ✅' if is_active else 'INACTIVE ❌'}", callback_data="abc_toggle_status")
        ],
        [
            InlineKeyboardButton("📝 Set Custom Message", callback_data="abc_set_msg"),
            InlineKeyboardButton("⏱️ Set Interval", callback_data="abc_set_interval")
        ],
        [
            InlineKeyboardButton("🚀 Send Broadcast Now", callback_data="abc_send_now")
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

async def send_auto_broadcast_to_all():
    config = await get_broadcast_config()
    message_text = config.get("message")
    if not message_text:
        return 0, 0

    sent_count = 0
    failed_count = 0
    async for dialog in app.get_dialogs():
        chat = dialog.chat
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
            try:
                await app.send_message(chat.id, message_text)
                sent_count += 1
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

    preview_text = (
        f"📢 **Automated Message Broadcast Settings**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚡ **Status:** `{'Active' if is_active else 'Inactive'}`\n"
        f"⏱️ **Interval:** `{interval}` minutes (e.g. every {interval // 60}h {interval % 60}m)\n\n"
        f"📝 **Current Custom Message:**\n"
        f"----------------------------------------\n"
        f"{msg_text}\n"
        f"----------------------------------------\n\n"
        f"Use the settings below to manage the automatic broadcast:"
    )

    await message.reply_text(
        preview_text,
        reply_markup=get_broadcast_menu_keyboard(is_active, interval)
    )

@app.on_callback_query(filters.regex(r"^abc_(toggle_status|set_msg|set_interval|send_now|close|back|select_interval_\d+)$"))
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

    elif data == "abc_set_interval":
        await callback_query.message.edit_text(
            "⏱️ **Select Broadcast Interval:**\n\nChoose the automatic time frequency for the broadcast message:",
            reply_markup=get_interval_keyboard()
        )
        return

    elif data.startswith("abc_select_interval_"):
        mins = int(data.split("_")[-1])
        await update_broadcast_config({"interval_mins": mins})
        await callback_query.answer(f"Broadcast interval set to {mins} minutes")

    elif data == "abc_back":
        pass  # Just falls through to refresh page

    elif data == "abc_send_now":
        await callback_query.message.edit_text("🚀 **Broadcasting message to all chats in the background...**")
        sent, failed = await send_auto_broadcast_to_all()
        await callback_query.message.reply_text(
            f"✅ **Broadcast Completed!**\n\n"
            f"• Successfully sent: `{sent}` chats\n"
            f"• Failed/skipped: `{failed}` chats"
        )
        # Fall through to refresh

    elif data == "abc_set_msg":
        await callback_query.message.delete()
        ask = await client.ask(user_id, "📝 **Send your custom broadcast message now.**\n\n> Send /cancel to abort.")
        if ask.text == "/cancel":
            await ask.reply("Action cancelled.")
        else:
            await update_broadcast_config({"message": ask.text})
            await ask.reply("✅ **Broadcast message saved successfully!**")
        
        await asyncio.sleep(0.5)
        # Resend menu
        await auto_broadcast_menu_cmd(client, ask)
        return

    # Refresh page
    config = await get_broadcast_config()
    msg_text = config.get("message", "None")
    interval = config.get("interval_mins", 60)
    is_active = config.get("is_active", False)

    preview_text = (
        f"📢 **Automated Message Broadcast Settings**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚡ **Status:** `{'Active' if is_active else 'Inactive'}`\n"
        f"⏱️ **Interval:** `{interval}` minutes (every {interval // 60}h {interval % 60}m)\n\n"
        f"📝 **Current Custom Message:**\n"
        f"----------------------------------------\n"
        f"{msg_text}\n"
        f"----------------------------------------\n\n"
        f"Use the settings below to manage the automatic broadcast:"
    )

    await callback_query.message.edit_text(
        preview_text,
        reply_markup=get_broadcast_menu_keyboard(is_active, interval)
    )
