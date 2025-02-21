from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from users.db.db_manager import UserDB

users_routers = Router()

app_name = 'Пользователь'


@users_routers.callback_query(lambda c: c.data == 'app_users')
async def handler_users_menu(callback:types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text='Информация о пользователе',callback_data='users_profile')
    builder.adjust(1)
    await callback.message.edit_text(f'Выбери действие в разделе: {app_name}',reply_markup=builder.as_markup())


@users_routers.callback_query(lambda c: c.data == "users_profile")
async def handle_other_list_currencies(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = await UserDB.get_or_create_user(user_id)


    builder = InlineKeyboardBuilder()




    await callback.message.answer(
        text=f"Выбери действие в разделе: {app_name}/"
             f"Профиль:\n"
             f'- Имя: {user.username}\n'
             f'- Дата создания: {user.created_at}'

             ,
        reply_markup=builder.as_markup()
    )



# other_buttons_name = {
#     'name_app': "Различные функции",
#     'list_currencies': "Курсы валют",
#     'prefix_currencies_solo':'curr_solo_'
# }
#
# prefix_currencies_solo = other_buttons_name.get('prefix_currencies_solo','curr_solo_')
#


# @other_routers.callback_query(lambda c: c.data == "app_other_menu")
# async def handle_other_menu(callback: types.CallbackQuery):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Курс валюты", callback_data="other_list_currencies")
#     builder.button(text="Другая опция", callback_data="other_other_option")
#     builder.adjust(1)
#     await callback.message.edit_text(f"Выбери действие в разделе {other_buttons_name.get('name_app','')}:", reply_markup=builder.as_markup())
#
#
#
# @other_routers.callback_query(lambda c: c.data == "other_list_currencies")
# async def handle_other_list_currencies(callback: types.CallbackQuery):
#     cls_data_redis = RatesData()
#     data = await cls_data_redis.get_curr_list()
#     builder = InlineKeyboardBuilder()
#     date = format_datetime(await cls_data_redis.get_date_curr())  # Используем await
#
#     for obj in data:
#         builder.button(text=f"{obj}", callback_data=f"{prefix_currencies_solo}{obj}")
#     builder.adjust(6)
#
#     await callback.message.answer(
#         text=f"Выбери действие в разделе: {other_buttons_name.get('name_app', '')}/"
#              f"{other_buttons_name.get('list_currencies', 'Курсы валют')}:\n"
#              f'Данные на {date} ЦБ',
#         reply_markup=builder.as_markup()
#     )
#
# @other_routers.callback_query(F.data.startswith(prefix_currencies_solo))
# async def handle_currency_selection(callback: types.CallbackQuery):
#     currency = callback.data.replace(prefix_currencies_solo, "")
#     cls_data_redis = RatesData
#     user_id = callback.from_user.id
#     data = await cls_data_redis().get_solo_curr(currency)
#     queryset = await CurrencyRequestDB.get_last_currency_request(user_id, currency)
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Курс валюты", callback_data="other_list_currencies")
#
#     await callback.message.answer(
#         f"Стоимость {data['name']}({currency}): {data['value']}\n"
#         f'История запросов:\n'
#         f'{string_queryset(queryset)}',reply_markup=builder.as_markup()
#     )
#
#     user_name = callback.from_user.first_name + " " + callback.from_user.last_name
#     await CurrencyRequestDB.save_currency_request(user_id,currency,user_name)
#
#


