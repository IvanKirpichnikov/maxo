from maxo.types.api.callback_keyboard_button import CallbackKeyboardButton
from maxo.types.api.chat_keyboard_button import ChatKeyboardButton
from maxo.types.api.link_keyboard_button import LinkKeyboardButton
from maxo.types.api.message_keyboard_button import MessageKeyboardButton
from maxo.types.api.open_app_keyboard_button import OpenAppKeyboardButton
from maxo.types.api.request_contact_keyboard_button import RequestContactKeyboardButton
from maxo.types.api.request_geo_location_button import RequestGeoLocationKeyboardButton

KeyboardButtons = (
    CallbackKeyboardButton
    | ChatKeyboardButton
    | LinkKeyboardButton
    | RequestGeoLocationKeyboardButton
    | RequestContactKeyboardButton
    | OpenAppKeyboardButton
    | MessageKeyboardButton
)
