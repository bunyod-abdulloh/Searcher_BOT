from aiogram import Router, F, types
from aiogram.enums import InlineQueryResultType, ParseMode, InputMediaType
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.buttons import search_all_buttons
from loader import db
from bot.states.user_states import SearchAllUz

router = Router()
all_buttons_uz = search_all_buttons(
    search_text="Qidirish", back_text="Ortga", back_callback="back_main_uz"
)


@router.callback_query(F.data == "all_uz")
async def region_uz_one(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Kerakli tugmani bosing", reply_markup=all_buttons_uz
    )
    await state.set_state(SearchAllUz.Q1)


@router.inline_query()
async def region_uz_two(inline_query: types.InlineQuery, state: FSMContext):
    # all_books = await db.select_books()
    query_ = inline_query.query
    # book = await db.select_book(book=inline_query.query)

    result_search = []

    if len(query_) > 0:
        book_like = await db.select_book_like(
            text=query_
        )
        for book in book_like:
            shop = await db.select_shop_by_id(
                id_=book['shop_id']
            )
            result_search.append(
                types.InlineQueryResultCachedPhoto(
                    type=InlineQueryResultType.PHOTO,
                    id=str(book['id']),
                    photo_file_id=shop['image'],
                    title="TITLE",
                    caption="DESCRIPTION",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"Hello, this is result {book['book']}", parse_mode="HTML"
                    )
                )
            )
        await inline_query.answer(
            results=result_search, is_personal=True
        )
    # else:
    #     try:
    #         for book in all_books:
    #             shop = await db.select_shop_by_id(id_=book['shop_id'])
    #             all_results.append(
    #                 types.InlineQueryResultPhoto(
    #                     id=str(book['id']),
    #                     type=InlineQueryResultType.PHOTO,
    #                     title=book['book'],
    #                     description="decription",
    #                     caption="caption",
    #                     parse_mode=ParseMode.HTML,
    #                     photo_url="https://i1.wp.com/mohirdev.uz/wp-content/uploads/Telegram-bot.png",
    #                     thumbnail_url="https://i1.wp.com/mohirdev.uz/wp-content/uploads/Telegram-bot.png",
    #                     input_message_content=types.InputTextMessageContent(
    #                         message_text='booklar', parse_mode=ParseMode.HTML
    #                     ),
    #                 )
    #             )
    #     except Exception as e:
    #         print(e)
    #     await inline_query.answer(
    #         results=all_results, switch_pm_parameter="button", switch_pm_text="Pastdan tepaga suring",
    #         is_personal=True
    #     )
    #     print(all_results)
# f"Narxi: {book['price']}00 so'm\nDo'kon: {shop['name']} | "
#                                 f"Manzil: {shop['address']}"


@router.message(F.text == "rasm")
async def send_rasm(message: types.Message):
    await message.answer_photo(
        photo="https://i.postimg.cc/wMHK6zMv/BOOKUz.jpg",
        caption="caption"
    )