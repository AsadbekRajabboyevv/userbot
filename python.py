from telethon import TelegramClient, events
import asyncio
import time

API_ID = 29224816
API_HASH = '2c9169727c27900894036e23aa19b5ed'
client = TelegramClient("userbot_session", API_ID, API_HASH)

user_messages = {}

async def is_user_offline():
    """ Foydalanuvchi HOZIR offline ekanligini tekshirish """
    me = await client.get_me()
    user = await client.get_entity(me.id)
    if hasattr(user.status, 'was_online'):
        last_seen = user.status.was_online.timestamp()  # So‘nggi ko‘rgan vaqti (timestamp)
        return (time.time() - last_seen) > 0  # Agar foydalanuvchi hozir offline bo‘lsa, True qaytaradi
    return True  # Agar holati noma’lum bo‘lsa, offline deb hisoblaymiz

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:  # Faqat shaxsiy xabarlarga javob beradi
        chat_id = event.chat_id
        current_time = time.time()

        if await is_user_offline():  # **Agar hozir offline bo‘lsa**
            if chat_id not in user_messages:
                user_messages[chat_id] = []

            # 1 daqiqa ichidagi xabarlarni filtrlaymiz
            user_messages[chat_id] = [t for t in user_messages[chat_id] if current_time - t < 60]
            message_count = len(user_messages[chat_id])

            # Yangi xabar vaqtini saqlash
            user_messages[chat_id].append(current_time)

            # Javob berish
            if message_count == 0:
                await event.reply("Men hozir tarmoqda emasman. Iltimos, keyinroq yozing!")
            elif message_count == 1:
                await event.reply("Hozir javob bera olmayman, keyinroq yozing!")
            else:
                await event.reply("Men hozir bandman, iltimos keyinroq yozing!")

async def main():
    await client.start()
    print("✅ Userbot ishga tushdi! Agar siz offline bo‘lsangiz, avtomatik javob beradi.")
    await client.run_until_disconnected()

asyncio.run(main())
