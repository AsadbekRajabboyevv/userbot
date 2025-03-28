from telethon import TelegramClient, events
import asyncio
import time

API_ID = YOUR API HASH FROM my.telegram.org
API_HASH = 'YOUR API HASH FROM my.telegram.org'
client = TelegramClient("userbot_session", API_ID, API_HASH)

user_messages = {}
last_seen_time = time.time()

async def update_last_seen():
    """ Foydalanuvchi so‘nggi online bo‘lgan vaqtini yangilaydi """
    global last_seen_time
    me = await client.get_me()
    user = await client.get_entity(me.id)
    if hasattr(user.status, 'was_online'):
        last_seen_time = user.status.was_online.timestamp()
    else:
        last_seen_time = time.time() 
async def is_user_offline_for_5_minutes():
    """ Agar foydalanuvchi **5 daqiqadan ko‘p offline bo‘lsa**, True qaytaradi """
    global last_seen_time
    current_time = time.time()
    return (current_time - last_seen_time) > 300  # 300 sekund (5 daqiqa)

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:
        chat_id = event.chat_id
        current_time = time.time()

        if await is_user_offline_for_5_minutes(): 
            if chat_id not in user_messages:
                user_messages[chat_id] = []

            user_messages[chat_id] = [t for t in user_messages[chat_id] if current_time - t < 60]
            message_count = len(user_messages[chat_id])

            user_messages[chat_id].append(current_time)

            if message_count == 0:
                await event.reply("Men hozir tarmoqda emasman. Iltimos, keyinroq yozing! 📵")
            elif message_count == 1:
                await event.reply("Hozir javob bera olmayman, keyinroq yozing! ⏳")
            else:
                await event.reply("Men hozir bandman, iltimos keyinroq yozing! 🚀")

async def monitor_status():
    """ Foydalanuvchi holatini har 1 daqiqada yangilash """
    while True:
        await update_last_seen()
        await asyncio.sleep(60)  

async def main():
    await client.start()
    print("✅ Userbot ishga tushdi! 5 daqiqa offline bo‘lsa, avtomatik javob beradi.")

    asyncio.create_task(monitor_status())  # Holatni kuzatishni boshlash
    await client.run_until_disconnected()

asyncio.run(main())
