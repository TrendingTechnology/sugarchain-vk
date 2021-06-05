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


async def getBalance(address):
    session = ClientSession()
    response = await session.get(f"https://api.sugarchain.org/balance/{address}")
    data = json.loads(await response.text())
    balance = data["result"]["balance"]
    await session.close()
    return balance


def getStorage():
    file = open("storage.json")
    data = file.read()
    file.close()
    return json.loads(data)


def editStorage(data):
    file = open("storage.json", "w")
    file.write(str(data).replace("'", '"'))
    file.close()


states = {}

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
    text = f'{locale["ru"]["wallets"]}\n\n'
    for wallet in wallets:
        address = getAddressByWIF(wallet)
        balance = await getBalance(address)
        text += f"{wallet} ({address}:{balance})\n\n"
    await message.answer(text, keyboard=KEYBOARD_WALLETS_RU)


@bot.on.message(text="Добавить")
async def add(message: Message):
    states[message.peer_id] = "add"
    await message.answer(locale["ru"]["add"])


@bot.on.message()
async def common(message: Message):
    if message.peer_id in states and states[message.peer_id] == "add":
        storage = getStorage()
        if str(message.peer_id) not in storage["users"]:
            storage["users"][str(message.peer_id)] = {"wallets": []}
        storage["users"][str(message.peer_id)]["wallets"].append(message.text)
        editStorage(storage)
        del states[message.peer_id]
        await message.answer(locale["ru"]["success_add"])
    else:
        await message.answer(locale["ru"]["common"], keyboard=KEYBOARD_COMMON_RU)


bot.run_forever()
