from vkbottle import Keyboard, KeyboardButtonColor, Text

from locale import locale


KEYBOARD_COMMON_RU = Keyboard()
KEYBOARD_COMMON_RU.add(
    Text(locale["ru"]["keyboard_common"]["rate"]), KeyboardButtonColor.PRIMARY
)
KEYBOARD_COMMON_RU.add(
    Text(locale["ru"]["keyboard_common"]["wallets"]), KeyboardButtonColor.SECONDARY
)
