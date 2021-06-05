import os
import json

from vkbottle.bot import Bot, Message

from bitcoinutils.setup import setup
from bitcoinutils import constants
from bitcoinutils.keys import PrivateKey

from aiohttp import ClientSession

from locale import locale
from keyboards import KEYBOARD_COMMON_RU, KEYBOARD_WALLETS_RU


def getAddressByWIF(wif):
    private = PrivateKey.from_wif(wif)
    public = private.get_public_key()
    address = public.get_segwit_address()
    return address.to_string()


def getStorage():
    file = open("storage.json")
    data = file.read()
    file.close()
    return json.loads(data)


def editStorage(data):
    file = open("storage.json", "w")
    file.write(str(data).replace("'", '"'))
    file.close()


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


@bot.on.message(text="Мои кошельки")
async def wallets(message: Message):
    storage = getStorage()
    if str(message.peer_id) not in storage["users"]:
        storage["users"][str(message.peer_id)] = {"wallets": []}
        editStorage(storage)
    wallets = storage["users"][str(message.peer_id)]["wallets"]
    text = f'{locale["ru"]["wallets"]}\n'
    for wallet in wallets:
        text += f"{wallet}\n"
    await message.answer(text, keyboard=KEYBOARD_WALLETS_RU)


@bot.on.message()
async def common(message: Message):
    await message.answer(locale["ru"]["common"], keyboard=KEYBOARD_COMMON_RU)


bot.run_forever()
