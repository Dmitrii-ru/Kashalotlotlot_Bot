from aiogram import Bot, Dispatcher, types, Router,F
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from settings import media_file_path, media_file_path_delete
import aiohttp
from aiogram.types import FSInputFile

class FileUploadStates(StatesGroup):
    waiting_for_preparing_data_file = State()



zaek_routers = Router()


zaek_buttons_name = {
    'name_app': "ZAEK",
    'crm':"Подготовить данные для CPM"
}

@zaek_routers.callback_query(lambda c: c.data == "app_zaek_menu")
async def zaek_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text=zaek_buttons_name['crm'], callback_data="zaek_menu/preparing_data_loading_into")
    builder.button(text="Другая опция", callback_data="zaek_other_option")
    builder.adjust(1)
    await callback.message.edit_text(f"Выбери действие в разделе {zaek_buttons_name.get('name_app','')}:", reply_markup=builder.as_markup())


@zaek_routers.callback_query(lambda c: c.data == "zaek_menu/preparing_data_loading_into")
async def preparing_data_loading_into(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text= f'{zaek_buttons_name.get("name_app","").upper()}'
              f'/{zaek_buttons_name.get("crm","Обработка файла").upper()}.\n'
              'Файл должен быть excel.\n'
             'Должен содержать лист Запрос.\n'
             'Должны быть колонки Арт,Кол.\n'
             'Пожалуйста, загрузите файл.'

    )
    await state.set_state(FileUploadStates.waiting_for_preparing_data_file)




@zaek_routers.message(F.document.file_name.endswith(".xlsx"))
async def handle_document(message: types.Message, state: FSMContext, bot: Bot):
    file_path = None
    new_file_path = None
    try:
        current_state = await state.get_state()
        if current_state == FileUploadStates.waiting_for_preparing_data_file:
            await message.reply(f"Запускаю:\n{zaek_buttons_name['crm']}\nОжидайте")
            document = message.document
            file_path = media_file_path(message.document.file_name)
            await bot.download(document, destination=file_path)

            preparing_data_loading_into_api = 'http://127.0.0.1:8001/zaek/api/upload-xlsx/'
            async with aiohttp.ClientSession() as session:
               with open(file_path, 'rb') as file:
                   files = {'file': file}
                   async with session.post(preparing_data_loading_into_api, data=files) as response:
                       if response.status == 200:
                            content_type = response.headers.get('Content-Type', '')
                            if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type:
                                print('')
                                content_disposition = response.headers.get('Content-Disposition', '')
                                new_file_path = media_file_path(f'Обработанная {message.document.file_name}')
                                with open(new_file_path, "wb") as output_file:
                                    output_file.write(await response.read())
                                file_to_send = FSInputFile(new_file_path)
                                await message.reply_document(file_to_send,caption='Файл обработан')
                                media_file_path_delete(new_file_path)
                       elif response.status == 400:
                           try:
                               response_data = await response.json()
                               error_message = response_data.get('error', 'Неизвестная ошибка')
                           except Exception:
                               error_message = await response.text()
                           error_message = error_message.replace(
                               "[", "").replace(
                               "]", "").replace(
                               "'", "").replace(
                               "\\", "\n").strip()

                           await message.reply(f"Ошибка: {error_message}")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")

    finally:
        try:
            media_file_path_delete(file_path)
            media_file_path_delete(new_file_path)
        except Exception as e:
            pass
    await state.clear()





