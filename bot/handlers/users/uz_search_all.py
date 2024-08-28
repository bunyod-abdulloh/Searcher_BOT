from aiogram import Router, F, types
from aiogram.enums import InlineQueryResultType
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.buttons import search_all_buttons, check_inline_query
from loader import db
from bot.states.user_states import SearchAllUz

router = Router()
all_buttons_uz = search_all_buttons(
    search_text="Qidirish", back_text="Ortga", back_callback="back_main_uz"
)


async def inline_searcher(books, i_query: types.InlineQuery):
    result = []
    for book in books:
        shop = await db.select_shop_by_id(
            id_=book['shop_id']
        )
        if book['amount'] == 0:
            pass
        else:
            result.append(
                types.InlineQueryResultArticle(
                    type=InlineQueryResultType.ARTICLE,
                    id=str(book['id']),
                    title=book['book'],
                    description=f"Do'kon: {shop['name']}\nNarx: {book['price']} so`m",
                    thumbnail_url=shop['image'],
                    parse_mode="HTML",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"<b>Kitob nomi:</b> {book['book']}\n<b>Narxi:</b> {book['price']} so`m\n\n"
                                     f"<b>Manzil:</b> {shop['region']}, {shop['city']}, {shop['address']}\n\n"
                                     f"<b>Telefon raqam:</b> {shop['phone']}\n\n"
                                     f"<a href='{shop['map']}'>Manzilni xaritada ko`rish</a>",
                        link_preview_options=types.LinkPreviewOptions(url=f"{shop['image']}")
                    ), reply_markup=check_inline_query()
                ))
    await i_query.answer(
        results=result, is_personal=True, cache_time=1, button=types.InlineQueryResultsButton(
            text="Pastdan tepaga suring", start_parameter="startst"
        ),
    )


@router.callback_query(F.data == "all_uz")
async def region_uz_one(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Kerakli tugmani bosing", reply_markup=all_buttons_uz
    )
    await state.set_state(SearchAllUz.Q1)


@router.callback_query()
@router.inline_query()
async def inline_query_handler(i_query: types.InlineQuery):
    query_ = i_query.query

    if len(query_) > 0:
        book_like = await db.select_book_like(
            text=query_
        )
        await inline_searcher(
            books=book_like, i_query=i_query
        )
    else:
        all_books = await db.select_books()
        await inline_searcher(
            books=all_books, i_query=i_query
        )


@router.message(F.text == "rasm")
async def send_rasm(message: types.Message):
    await message.answer_photo(
        photo="https://i.postimg.cc/wMHK6zMv/BOOKUz.jpg",
        caption="caption"
    )
