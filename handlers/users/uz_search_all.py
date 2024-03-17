from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboards.inline.buttons import search_all_buttons
from loader import db
from states.user_states import SearchAllUz

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


@router.inline_query(SearchAllUz.Q1)
async def region_uz_two(inline_query: types.InlineQuery, state: FSMContext):
    all_books = await db.select_books()
    query_ = inline_query.query
    # book = await db.select_book(book=inline_query.query)
    all_results = []
    search_result = []
    if len(query_) > 0:
        pass
    else:
        for book in all_books:
            shop = await db.select_shop_by_id(id_=book['shop_id'])
            all_results.append(
                types.InlineQueryResultCachedPhoto(
                    id=str(book['id']),
                    photo_file_id=shop['image'],
                    title=book['book'],
                    description=f"Narxi: {book['price']}00 so'm\nDo'kon: {shop['name']} | Manzil: {shop['address']}",
                    caption="Bu caption",
                    input_message_content=types.InputTextMessageContent(
                        message_text='book[1]'
                    ),
                )
            )
        print(all_results)
        await inline_query.answer(
            results=all_results, cache_time=0, switch_pm_parameter="button", switch_pm_text="Pastdan tepaga suring"
        )

