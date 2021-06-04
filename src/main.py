import os

from vkbottle.bot import Bot, Message

from locale import locale


TOKEN = os.environ["TOKEN"]

bot = Bot(TOKEN)


@bot.on.message()
async def common(message: Message):
    await message.answer(locale["ru"]["common"])


bot.run_forever()
