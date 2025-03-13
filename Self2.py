from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.messages import CreateChatRequest
from telethon.tl.functions.channels import DeleteChannelRequest
import asyncio
import random

# 🔹 API DETAILS (Replace with your own)
api_id = "25350664"  
api_hash = "8ed95a3c8c25a1e90312f076be58800d"  

# 🚀 Client Initialization
client = TelegramClient("PraveenSelfBot", api_id, api_hash, system_version="4.16.30-vx")

# ✅ COMMANDS LIST (.cmds)
@client.on(events.NewMessage(pattern=r"\.cmds"))
async def cmds(event):
    commands = """
╭━〔 🚀 𝙋𝙧𝙖𝙫𝙚𝙚𝙣 𝘽𝙤𝙩 〕━╮
┃ 🆔 **.info** - User info
┃ 🔥 **.roast** - Roast user
┃ 🛑 **.stop roasting** - Stop roasting
┃ 💥 **.chud** - Spam abuses
┃ 🔇 **.mute** - Mute user
┃ 🔊 **.unmute** - Unmute user
┃ 🚫 **.block** - Block user
┃ 🚪 **.leave** - Leave group
┃ 🔎 **.id** - Get user ID
┃ 👥 **.mm** - Create group
┃ ❌ **.del gc** - Delete group
┃ 📌 **.pin** - Pin message
┃ 💬 **.spam (count) (msg)** - Spam text
╰━━━━━━━━━━━━━━━━━╯
"""
    await event.reply(commands)

# 🔍 INFO COMMAND (.info)
@client.on(events.NewMessage(pattern=r"\.info"))
async def info(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
    else:
        user = await event.get_sender()

    details = f"""
╭━〔 🔍 𝙐𝙎𝙀𝙍 𝙄𝙉𝙁𝙊 〕━╮
┃ 👤 **Name:** `{user.first_name} {user.last_name or ""}`
┃ 🆔 **User ID:** `{user.id}`
┃ 🔹 **Username:** `{user.username if user.username else "N/A"}`
┃ 📞 **Phone:** `{user.phone if user.phone else "Hidden"}`
┃ 🌍 **Profile:** [Click Here](tg://user?id={user.id})
╰━━━━━━━━━━━━━━━━━━╯
"""
    await event.reply(details, link_preview=False)

# 🔇 MUTE & UNMUTE COMMANDS
mute_users = set()

@client.on(events.NewMessage)
async def mute_messages(event):
    if event.sender_id in mute_users:
        await event.delete()

@client.on(events.NewMessage(pattern=r"\.mute"))
async def mute(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
        mute_users.add(user.id)
        await event.reply(f"🔇 **Muted:** `{user.first_name}`")
    else:
        await event.reply("❌ **Reply to a user to mute!**")

@client.on(events.NewMessage(pattern=r"\.unmute"))
async def unmute(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
        mute_users.discard(user.id)
        await event.reply(f"🔊 **Unmuted:** `{user.first_name}`")
    else:
        await event.reply("❌ **Reply to a user to unmute!**")

# 📌 PIN COMMAND
@client.on(events.NewMessage(pattern=r"\.pin"))
async def pin(event):
    if event.reply_to_msg_id:
        await client.pin_message(event.chat_id, event.reply_to_msg_id)
        await event.reply("📌 **Message Pinned!**")

# 💬 SPAM COMMAND
@client.on(events.NewMessage(pattern=r"\.spam (\d+) (.+)"))
async def spam(event):
    count = int(event.pattern_match.group(1))
    msg = event.pattern_match.group(2)
    for _ in range(count):
        await event.respond(msg)
        await asyncio.sleep(0.3)

# 🚫 BLOCK COMMAND
@client.on(events.NewMessage(pattern=r"\.block"))
async def block(event):
    if event.is_private:
        try:
            await client(BlockRequest(event.sender_id))
            await event.reply("🚫 **User Blocked!**")
        except Exception as e:
            await event.reply(f"❌ **Block Failed:** `{str(e)}`")
    else:
        await event.reply("❌ **Use this command in private chat!**")

# 🚪 LEAVE GROUP COMMAND
@client.on(events.NewMessage(pattern=r"\.leave"))
async def leave(event):
    if event.is_group:
        await event.reply("👋 **Leaving this group...**")
        await client.leave_chat(event.chat_id)

# 🔥 CHUD COMMAND (Fixed)
@client.on(events.NewMessage(pattern=r"\.chud"))
async def chud(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
        for _ in range(7):
            await event.respond(f"{user.first_name}, {random.choice(['Bhen ke lode!', 'Teri maa ki chut!', 'Maa chod dunga teri!'])}", reply_to=replied_user.id)
            await asyncio.sleep(1.5)
    else:
        await event.reply("❌ **Reply to someone to use `.chud`!**")

# 🔥 ROAST & STOP ROAST COMMAND
roast_users = set()

@client.on(events.NewMessage(pattern=r"\.roast"))
async def roast(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
        roast_users.add(user.id)
        await event.reply(f"🔥 **Roasting Started for** `{user.first_name}`!")
    else:
        await event.reply("❌ **Reply to a user to start roasting!**")

@client.on(events.NewMessage)
async def auto_roast(event):
    if event.sender_id in roast_users:
        await event.reply(random.choice(["{name}, tu debugging ka failed case hai!", "{name}, tera brain 404 error hai!"]).replace("{name}", "Bechara"))

@client.on(events.NewMessage(pattern=r"\.stop roasting"))
async def stop_roasting(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
        roast_users.discard(user.id)
        await event.reply(f"🛑 **Stopped roasting** `{user.first_name}`!")
    else:
        await event.reply("❌ **Reply to a user to stop roasting!**")

# 👥 CREATE GROUP COMMAND
@client.on(events.NewMessage(pattern=r"\.mm"))
async def create_group(event):
    if event.is_reply:
        replied_user = await event.get_reply_message()
        user = await client.get_entity(replied_user.sender_id)
        result = await client(CreateChatRequest(users=[user.id], title="🔥 Instant GC 🔥"))
        await event.reply(f"✅ **Group Created:** `{result.chats[0].title}`")
    else:
        await event.reply("❌ **Reply to create a group!**")

# ❌ DELETE GROUP COMMAND (Fixed)
@client.on(events.NewMessage(pattern=r"\.del gc"))
async def delete_group(event):
    if event.is_group:
        try:
            await event.reply("🛑 **Deleting group...**")
            await client(DeleteChannelRequest(event.chat_id))
        except Exception as e:
            await event.reply(f"❌ **Failed to delete group:** `{str(e)}`")
    else:
        await event.reply("❌ **Use this command in a group!**")

# 🚀 BOT START
print("🚀 Praveen Self-Bot is running...")
client.start()
client.run_until_disconnected()
