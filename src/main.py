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
    peer = str(message.peer_id)
    storage = getStorage()
    if peer not in storage["users"]:
        storage["users"][peer] = {"wallets": []}
        editStorage(storage)
    wallets = storage["users"][peer]["wallets"]
    text = f'{locale["ru"]["wallets"]}\n\n'
    for wallet in wallets:
        address = getAddressByWIF(wallet)
        balance = await getBalance(address)
        text += f"{wallet} ({address}:{balance / 1e8})\n\n"
    await message.answer(text, keyboard=KEYBOARD_WALLETS_RU)


@bot.on.message(text="Добавить")
async def add(message: Message):
    peer = str(message.peer_id)
    states[peer] = "add"
    await message.answer(locale["ru"]["add"])


@bot.on.message(text="Удалить")
async def remove(message: Message):
    peer = str(message.peer_id)
    states[peer] = "remove"
    await message.answer(locale["ru"]["add"])


@bot.on.message()
async def common(message: Message):
    peer = str(message.peer_id)
    if peer in states:
        storage = getStorage()
        if peer not in storage["users"]:
            storage["users"][peer] = {"wallets": []}
        if states[peer] == "add":
            storage["users"][peer]["wallets"].append(message.text)
            editStorage(storage)
            del states[peer]
            await message.answer(locale["ru"]["success_add"])
        if states[peer] == "remove":
            storage["users"][peer]["wallets"].remove(message.text)
            editStorage(storage)
            del states[peer]
            await message.answer(locale["ru"]["success_remove"])
    else:
        await message.answer(locale["ru"]["common"], keyboard=KEYBOARD_COMMON_RU)


bot.run_forever()
