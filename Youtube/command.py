# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/YouTube-Video-Download-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/YouTube-Video-Download-Bot



from pyrogram import Client, filters
import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from Youtube.config import Config
from Youtube.script import Translation
from Youtube.forcesub import handle_force_subscribe


#########################

currentTime = datetime.datetime.now()
hour = currentTime.hour

if 5 <= hour < 12:
    wish = "🌅 Rise & Vibe — Good Morning!"
elif 12 <= hour < 17:
    wish = "☀️ Mid-day Mood Loading… Good Afternoon!"
elif 17 <= hour < 21:
    wish = "🌆 Good Evening! Let the chill vibes flow ✨"
else:
    wish = "🌙 Night Vibes Only — Enjoy the Music!"





########################🎊 Lisa | NT BOTS 🎊######################################################
@Client.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.delete()

# About command handler
# @Client.on_message(filters.private & filters.command("about"))
async def about_disabled(client, message):
    if Config.CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    await message.reply_text(
        text=Translation.ABOUT_TXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('⛔️ Close', callback_data='cancel')]
        ]
    ))

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# 🎯 Popup Handlers (Each Button Independent)
@Client.on_callback_query(filters.regex(r"^update$"))
async def update_soon(client, cq: CallbackQuery):
    await cq.answer("📰 Updates section coming soon — stay tuned!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^support$"))
async def support_soon(client, cq: CallbackQuery):
    await cq.answer("💬 Support group launching soon!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^dev$"))
async def dev_soon(client, cq: CallbackQuery):
    await cq.answer("👩‍💻 Developer info coming soon!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^settings$"))
async def settings_soon(client, cq: CallbackQuery):
    await cq.answer("⚙️ Custom settings under development!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^music$"))
async def music_soon(client, cq: CallbackQuery):
    await cq.answer("🎧 Enjoy ✨", show_alert=True)

@Client.on_callback_query(filters.regex(r"^video$"))
async def video_soon(client, cq: CallbackQuery):
    await cq.answer("🎬 Video tools feature coming soon!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^converter$"))
async def converter_soon(client, cq: CallbackQuery):
    await cq.answer("📦 File converter tool coming soon!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^ai$"))
async def ai_soon(client, cq: CallbackQuery):
    await cq.answer("🧠 AI tools integration coming soon!", show_alert=True)

@Client.on_callback_query(filters.regex(r"^help$"))
async def help_soon(client, cq: CallbackQuery):
    await cq.answer("📚 Help & Commands section coming soon!", show_alert=True)

@Client.on_callback_query(filters.regex("cancel"))
async def cancel(client, cq: CallbackQuery):
    await cq.message.delete()

# 🚀 Start Command
# @Client.on_message(filters.command("start"))
async def start_disabled(client, message):
    # Optional: prevent spam in public groups if not admin
    if message.chat.type in ["group", "supergroup"]:
        await message.reply_text(
            "🤖 Bot is active in this group!\n"
            "Use me in private for full features 🔗",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Open Private Chat", url=f"https://t.me/{client.me.username}?start=start")]
            ])
        )
        return

    await message.reply_text(
        text=Translation.START_TEXT.format(message.from_user.first_name, wish),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📍 Update Channel", callback_data="update"),
                InlineKeyboardButton("👥 Support Group", callback_data="support"),
            ],
            [
                InlineKeyboardButton("👩‍💻 Developer", callback_data="dev"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            ],
            [
                InlineKeyboardButton("🎧 Music", callback_data="music"),
                InlineKeyboardButton("🎬 Video Tools", callback_data="video"),
            ],
            [
                InlineKeyboardButton("📦 File Converter", callback_data="converter"),
                InlineKeyboardButton("🧠 AI Tools", callback_data="ai"),
            ],
            [
                InlineKeyboardButton("📚 Help & Commands", callback_data="help"),
            ],
            [
                InlineKeyboardButton("⛔️ Close", callback_data="cancel"),
            ]
        ])
    )

# Help command handler
# @Client.on_message(filters.command("help"))
async def help_disabled(client, message):
    help_text = """
Welcome to the YouTube Video Uploader Bot!

To upload a YouTube video, simply send me the YouTube link.

Enjoy using the bot!

©️ Channel : @NT_BOT_CHANNEL
    """
    await message.reply_text(help_text)


########################🎊 Lisa | NT BOTS 🎊######################################################
