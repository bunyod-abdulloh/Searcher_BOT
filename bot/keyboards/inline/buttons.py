from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def main_menu(search_region: str, callback_region: str, search_all: str, callback_all: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text=f"🔍 {search_region}",
                    callback_data=callback_region
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔎 {search_all}",
                    callback_data=callback_all
                )
            ]
        ]
    )
    return keyboard


def search_region_buttons(search_text: str, back_text: str, back_callback: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text=f"🔍 {search_text}", switch_inline_query_current_chat=""
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"⬅️ {back_text}", callback_data=back_callback
                )
            ]
        ]
    )
    return keyboard


def search_all_buttons(search_text: str, back_text: str, back_callback: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text=f"🔍 {search_text}", switch_inline_query_current_chat=""
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"⬅️ {back_text}", callback_data=back_callback
                )
            ]
        ]
    )
    return keyboard


def check_inline_query():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="🔍 Qidirish", switch_inline_query_current_chat=""
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Buyurtma qilish", url="https://t.me/muhib_dev"
                )
            ]
        ]
    )
    return keyboard
