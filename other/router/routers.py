from aiogram import types, Router,F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from other.db.db_manager import CurrencyRequestDB
from other.utils.utils_func import string_queryset, format_datetime

from other.db.db_manager import CurrenciesData

other_routers = Router()





prefix_currencies_solo = 'prefix_currencies_solo'
name_app = "Различные функции"
list_currencies = "Курсы валют"


@other_routers.callback_query(lambda c: c.data == "app_other_menu")
async def handle_other_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Курс валюты", callback_data="other_list_currencies")
    builder.button(text="Другая опция", callback_data="other_other_option")
    builder.adjust(1)
    await callback.message.edit_text(f"Выбери действие в разделе {name_app}:", reply_markup=builder.as_markup())


@other_routers.callback_query(lambda c: c.data == "other_list_currencies")
async def handle_other_list_currencies(callback: types.CallbackQuery):
    try:
        rate_object = CurrenciesData()
        data = await rate_object.get_curr_list()
        builder = InlineKeyboardBuilder()

        date = format_datetime(await rate_object.get_date_curr())  # Используем await
        for obj in data:
            builder.button(text=f"{obj}", callback_data=f"{prefix_currencies_solo}{obj}")
        builder.adjust(6)
        await callback.message.answer(
            text=f"Выбери действие в разделе: {name_app}/"
                 f"{list_currencies}:\n"
                 f'Данные на {date} ЦБ',
            reply_markup=builder.as_markup()
        )
    except Exception as e:
        await callback.message.answer(text='Данные отсутствуют')



@other_routers.callback_query(F.data.startswith(prefix_currencies_solo))
async def handle_currency_selection(callback: types.CallbackQuery):
    try:
        currency = callback.data.replace(prefix_currencies_solo, "")
        rate_object = CurrenciesData
        user_id = callback.from_user.id
        data = await rate_object().get_solo_curr(currency)

        queryset = await CurrencyRequestDB.get_last_currency_request(user_id, currency)
        builder = InlineKeyboardBuilder()
        builder.button(text="Курс валюты", callback_data="other_list_currencies")
        await callback.message.answer(
            f"Стоимость {data['name']}({currency}): {data['value']}\n"
            f'История запросов:\n'
            f'{string_queryset(queryset)}',reply_markup=builder.as_markup()
        )
        user_name = callback.from_user.first_name + " " + callback.from_user.last_name
        await CurrencyRequestDB.save_currency_request(user_id,currency,user_name)

    except Exception:
        await callback.message.answer(text='Данные отсутствуют')



