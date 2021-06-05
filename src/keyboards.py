from vkbottle import Keyboard, KeyboardButtonColor, Text

from locale import locale


KEYBOARD_COMMON_RU = Keyboard()
KEYBOARD_COMMON_RU.add(
    Text(locale["ru"]["keyboard_common"]["rate"]), KeyboardButtonColor.PRIMARY
)
KEYBOARD_COMMON_RU.add(
    Text(locale["ru"]["keyboard_common"]["wallets"]), KeyboardButtonColor.SECONDARY
)

KEYBOARD_WALLETS_RU = Keyboard()
KEYBOARD_WALLETS_RU.add(
    Text(locale["ru"]["keyboard_wallets"]["add"]), KeyboardButtonColor.POSITIVE
)
KEYBOARD_WALLETS_RU.row()
KEYBOARD_WALLETS_RU.add(
    Text(locale["ru"]["keyboard_wallets"]["remove"]), KeyboardButtonColor.NEGATIVE
)
KEYBOARD_WALLETS_RU.row()
KEYBOARD_WALLETS_RU.add(
    Text(locale["ru"]["keyboard_wallets"]["edit"]), KeyboardButtonColor.PRIMARY
)
KEYBOARD_WALLETS_RU.row()
KEYBOARD_WALLETS_RU.add(
    Text(locale["ru"]["keyboard_wallets"]["transactions"]),
    KeyboardButtonColor.SECONDARY,
)
KEYBOARD_WALLETS_RU.row()
KEYBOARD_WALLETS_RU.add(
    Text(locale["ru"]["keyboard_wallets"]["back"]), KeyboardButtonColor.NEGATIVE
)
