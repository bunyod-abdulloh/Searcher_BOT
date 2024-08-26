from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger

from bot.keyboards.inline.buttons import main_menu
from loader import db, bot

router = Router()

main_buttons_uz = main_menu(
    search_region="Hudud bo'yicha qidirish", callback_region="region_uz",
    search_all="Umumiy qidirish", callback_all="all_uz"
)


@router.message(CommandStart())
async def do_start(message: types.Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    try:
        await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    except Exception as error:
        logger.info(error)

    await message.answer(text="Assalomu alaykum!", reply_markup=main_buttons_uz)


@router.message(F.photo)
async def get_photo(message: types.Message):
    await message.answer(
        text=f"<code>{message.photo[-1].file_id}</code>"
    )
