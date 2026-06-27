import yt_dlp
import requests
import os
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

@Client.on_callback_query(filters.regex(r"^download_"))
async def download_song_callback(client: Client, query: CallbackQuery):
    # ✅ Security check: only allow the same user who requested it
    if query.message and query.from_user and query.message.reply_to_message:
        if query.from_user.id != query.message.reply_to_message.from_user.id:
            return await query.answer("🚫 This button isn’t for you!", show_alert=True)

    url = query.data.replace("download_", "")
    await query.message.edit_text("⬇️ Downloading your song, please wait...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp3"):
                base, _ = os.path.splitext(filename)
                filename = f"{base}.mp3"

            title = info.get("title", "Unknown Title")
            performer = info.get("uploader", "Unknown Artist")
            thumb_url = info.get("thumbnail")

        # ✅ Download thumbnail locally
        thumb_path = None
        if thumb_url:
            try:
                r = requests.get(thumb_url, timeout=10)
                thumb_path = f"{os.path.splitext(filename)[0]}.jpg"
                with open(thumb_path, "wb") as f:
                    f.write(r.content)
            except Exception:
                thumb_path = None

        # ✅ Send audio with thumbnail
        await client.send_audio(
            chat_id=query.message.chat.id,
            audio=filename,
            title=f"🎵 {title}",
            performer=performer,
            thumb=thumb_path if thumb_path and os.path.exists(thumb_path) else None,
            caption=f"🎶 **{title}**\n👤 Artist: {performer}",
        )

        await query.message.delete()

        # ✅ Clean up temp files
        if os.path.exists(filename):
            os.remove(filename)
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception as e:
        await query.message.reply_text(f"❌ Failed to download: `{e}`")
