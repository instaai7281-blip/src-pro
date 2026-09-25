# ---------------------------------------------------
# File Name: topic_mirror.py
# Description: Mirror all topics and messages from a source forum group
#              to a target forum group using server-side copy (no download).
# ---------------------------------------------------

import asyncio
from pyrogram import filters, raw
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode
from devgagan import app
from config import OWNER_ID, LOG_GROUP
from devgagan.core.get_func import get_user_branding_tag, strip_links_except_youtube, format_caption_to_html, clean_surrogates


async def resolve_group_id(client, identifier):
    identifier = str(identifier).strip()
    if identifier.lstrip('-').isdigit():
        chat = await client.get_chat(int(identifier))
        return chat.id, chat
    if 't.me/' in identifier:
        parts = [p for p in identifier.split('/') if p]
        username = parts[-1] if not parts[-1].isdigit() else parts[-2]
        identifier = username
    username_clean = identifier.lstrip('@')
    try:
        r = await client.invoke(raw.functions.contacts.ResolveUsername(username=username_clean))
        if r.chats:
            cid = r.chats[0].id
            if not str(cid).startswith('-'):
                cid = int(f"-100{cid}")
            chat = await client.get_chat(cid)
            return cid, chat
        elif r.users:
            return r.users[0].id, r.users[0]
    except Exception:
        pass
    chat = await client.get_chat(f"@{username_clean}")
    return chat.id, chat


async def get_all_forum_topics(client, chat_id):
    topics = []
    offset_id = 0
    while True:
        try:
            result = await client.invoke(
                raw.functions.channels.GetForumTopics(
                    channel=await client.resolve_peer(chat_id),
                    q="",
                    offset_date=0,
                    offset_id=offset_id,
                    offset_topic=0,
                    limit=100,
                )
            )
        except Exception as e:
            print(f"[MIRROR] get_all_forum_topics error: {e}")
            break
        if not result.topics:
            break
        for topic in result.topics:
            topics.append({
                "id": topic.id,
                "title": topic.title,
                "icon_emoji_id": getattr(topic, 'icon_emoji_id', None),
            })
        if len(result.topics) < 100:
            break
        offset_id = result.topics[-1].id
    return topics


async def create_topic_in_target(client, target_chat_id, title, icon_emoji_id=None):
    import random
    try:
        result = await client.invoke(
            raw.functions.channels.CreateForumTopic(
                channel=await client.resolve_peer(target_chat_id),
                title=title[:128],
                icon_emoji_id=icon_emoji_id,
                random_id=random.randint(1, 2**31 - 1),
            )
        )
        if result and result.updates:
            for upd in result.updates:
                if hasattr(upd, 'id'):
                    return upd.id
    except Exception as e:
        print(f"[MIRROR] create_topic error for '{title}': {e}")
    return None


async def iter_topic_messages(client, chat_id, topic_id):
    messages = []
    offset_id = 0
    while True:
        try:
            result = await client.invoke(
                raw.functions.messages.GetReplies(
                    peer=await client.resolve_peer(chat_id),
                    msg_id=topic_id,
                    offset_id=offset_id,
                    offset_date=0,
                    add_offset=0,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
        except Exception as e:
            print(f"[MIRROR] iter_topic_messages error for topic {topic_id}: {e}")
            break
        if not result.messages:
            break
        batch = list(result.messages)
        messages.extend(batch)
        if len(batch) < 100:
            break
        offset_id = batch[-1].id
    messages.sort(key=lambda m: m.id)
    return messages


async def mirror_topic_messages(client, src_chat_id, src_topic_id, tgt_chat_id, tgt_topic_id, sender, status_msg=None):
    branding = get_user_branding_tag(sender)
    copied = 0
    failed = 0
    try:
        raw_msgs = await iter_topic_messages(client, src_chat_id, src_topic_id)
    except Exception as e:
        print(f"[MIRROR] Failed to fetch messages for topic {src_topic_id}: {e}")
        return 0, 0

    total = len(raw_msgs)
    for i, raw_msg in enumerate(raw_msgs):
        msg_id = raw_msg.id
        if msg_id == src_topic_id:
            continue
        for attempt in range(2):
            try:
                pyro_msg = await client.get_messages(src_chat_id, msg_id)
                if not pyro_msg or pyro_msg.empty:
                    break
                _raw_cap = str(pyro_msg.caption or (pyro_msg.text if not pyro_msg.media else '') or '')
                _clean_cap = strip_links_except_youtube(clean_surrogates(_raw_cap))
                if _clean_cap.strip():
                    _final_cap = f"{_clean_cap.strip()}\n\n> **{branding}**"
                else:
                    _final_cap = f"> **{branding}**"
                _cap_html = format_caption_to_html(clean_surrogates(_final_cap))

                await client.copy_message(
                    chat_id=tgt_chat_id,
                    from_chat_id=src_chat_id,
                    message_id=msg_id,
                    caption=_cap_html if pyro_msg.media else None,
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=tgt_topic_id,
                )
                copied += 1
                break
            except FloodWait as fw:
                await asyncio.sleep(fw.value + 2)
            except Exception as e:
                if attempt == 1:
                    print(f"[MIRROR] Failed to copy msg {msg_id}: {e}")
                    failed += 1
                await asyncio.sleep(0.5)

        if status_msg and (i + 1) % 15 == 0:
            try:
                await status_msg.edit(
                    f"⚡ **Copying...**\n\nProgress: {i+1}/{total} | ✅ {copied} | ❌ {failed}"
                )
            except Exception:
                pass
        await asyncio.sleep(0.4)

    return copied, failed


async def ensure_forum_enabled(client, chat_id):
    try:
        await client.invoke(
            raw.functions.channels.ToggleForum(
                channel=await client.resolve_peer(chat_id),
                enabled=True,
            )
        )
        return True
    except Exception as e:
        print(f"[MIRROR] Could not enable forum on target: {e}")
        return False


@app.on_message(filters.command("topicmirror") & filters.user(OWNER_ID))
async def topic_mirror_cmd(client, message):
    """
    Usage: /topicmirror @source_group @target_group
    Or:    /topicmirror @source_group   (uses LOG_GROUP as target)
    """
    sender = message.chat.id
    parts = message.command[1:]

    if not parts:
        await message.reply(
            "📋 **Topic Mirror — Usage:**\n\n"
            "/topicmirror @source @target\n\n"
            "Or with LOG_GROUP as target:\n"
            "/topicmirror @source\n\n"
            "**Requirements:**\n"
            "• Bot must be **admin** in both groups\n"
            "• Source must be a **forum** (Topics-enabled) supergroup\n"
            "• Target must be a **supergroup** (Topics will be auto-enabled)"
        )
        return

    src_identifier = parts[0]
    tgt_identifier = parts[1] if len(parts) > 1 else str(LOG_GROUP)

    status = await message.reply("🔍 **Resolving groups...**")

    try:
        src_id, src_chat = await resolve_group_id(client, src_identifier)
    except Exception as e:
        await status.edit(f"❌ **Could not resolve source group:**\n{e}")
        return

    try:
        tgt_id, tgt_chat = await resolve_group_id(client, tgt_identifier)
    except Exception as e:
        await status.edit(f"❌ **Could not resolve target group:**\n{e}")
        return

    await status.edit(
        f"✅ **Groups resolved:**\n\n"
        f"📤 Source: **{src_chat.title}** ({src_id})\n"
        f"📥 Target: **{tgt_chat.title}** ({tgt_id})\n\n"
        f"🔎 Fetching topics..."
    )

    # Enable forum on target if needed
    tgt_info = await client.get_chat(tgt_id)
    if not getattr(tgt_info, 'is_forum', False):
        await status.edit(f"{status.text}\n⚙️ Enabling forum mode on target...")
        ok = await ensure_forum_enabled(client, tgt_id)
        if not ok:
            await status.edit(
                f"✅ **Groups resolved.**\n\n"
                f"⚠️ **Warning:** Could not auto-enable Topics on target.\n"
                f"Please enable **Topics** in target group settings manually, then retry."
            )
            return

    try:
        topics = await get_all_forum_topics(client, src_id)
    except Exception as e:
        await status.edit(f"❌ **Failed to fetch topics:**\n{e}")
        return

    if not topics:
        await status.edit(
            "⚠️ **No topics found in source.**\n"
            "Make sure the source group has Topics/Forum mode enabled."
        )
        return

    await status.edit(
        f"📋 **Found {len(topics)} topics.**\n\n"
        f"Starting mirror... This may take a while ⏳"
    )

    total_copied = 0
    total_failed = 0
    topic_results = []

    for idx, topic in enumerate(topics):
        src_topic_id = topic['id']
        title = topic['title']
        icon_emoji_id = topic.get('icon_emoji_id')

        try:
            await status.edit(
                f"⚡ **Topic {idx+1}/{len(topics)}:** {title}\n"
                f"Creating in target..."
            )
        except Exception:
            pass

        # General topic (ID=1) always exists
        if src_topic_id == 1:
            tgt_topic_id = 1
        else:
            tgt_topic_id = await create_topic_in_target(
                client, tgt_id, title, icon_emoji_id=icon_emoji_id
            )
            if not tgt_topic_id:
                topic_results.append(f"❌ {title} — could not create topic")
                continue
            await asyncio.sleep(1.5)

        try:
            await status.edit(
                f"⚡ **Topic {idx+1}/{len(topics)}:** {title}\n"
                f"Copying messages..."
            )
        except Exception:
            pass

        copied, failed = await mirror_topic_messages(
            client, src_id, src_topic_id, tgt_id, tgt_topic_id, sender, status_msg=status
        )
        total_copied += copied
        total_failed += failed
        topic_results.append(f"{'✅' if failed == 0 else '⚠️'} {title} — {copied} copied, {failed} failed")
        await asyncio.sleep(2)

    # Final summary
    lines = "\n".join(topic_results[:25])
    if len(topic_results) > 25:
        lines += f"\n_...and {len(topic_results) - 25} more_"

    await status.edit(
        f"🎉 **Topic Mirror Complete!**\n\n"
        f"📤 **Source:** {src_chat.title}\n"
        f"📥 **Target:** {tgt_chat.title}\n\n"
        f"📊 **Summary:**\n"
        f"• Topics: {len(topics)}\n"
        f"• Messages copied: ✅ {total_copied}\n"
        f"• Messages failed: ❌ {total_failed}\n\n"
        f"**Per-topic:**\n{lines}",
        parse_mode=ParseMode.MARKDOWN
    )