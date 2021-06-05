import os

from vkbottle.bot import Bot, Message

from bitcoinutils.setup import setup
from bitcoinutils import constants
from bitcoinutils.keys import PrivateKey

from aiohttp import ClientSession

from locale import locale
from keyboards import KEYBOARD_COMMON_RU


def getAddressByWIF(wif):
    private = PrivateKey.from_wif(wif)
    public = private.get_public_key()
    address = public.get_segwit_address()
    return address.to_string()


TOKEN = os.environ["TOKEN"]
constants.NETWORK_SEGWIT_PREFIXES["mainnet"] = "sugar"

bot = Bot(TOKEN)
setup()


@bot.on.message(text="Курс")
async def currency(message: Message):
    session = ClientSession()
    response = await session.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=sugarchain&vs_currencies=rub"
    )
    data = await response.json()
    currency = data["sugarchain"]["rub"]
    await message.answer(f"{locale['ru']['currency']}{currency}")
    await session.close()


@bot.on.message()
async def common(message: Message):
    await message.answer(locale["ru"]["common"], keyboard=KEYBOARD_COMMON_RU)


bot.run_forever()
