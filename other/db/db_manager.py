from datetime import datetime
from db.db_manager import BaseDB
from users.db.db_manager import UserDB
from users.db.models import User
from other.db.models import UserCurrencyRequest, Currency
from sqlalchemy import select, desc,delete, and_, not_
from base_api import RequestsApiAsync
from db.db_redis import RedisCli
import locale

class CurrencyRequestDB(BaseDB):
    """Класс для работы с запросами валют к базе данных."""

    @staticmethod
    async def get_or_create_currency(code: str):
        """Получает или создаёт валюту."""
        async def _get_or_create_currency(session):
            result = await session.execute(select(Currency).where(Currency.code == code))
            currency = result.scalars().first()
            if not currency:
                currency = Currency(code=code, count=1)
                session.add(currency)
            else:
                currency.count += 1
            await session.commit()
            await session.refresh(currency)
            return currency

        return await BaseDB.execute_with_session(_get_or_create_currency)

    @staticmethod
    async def save_currency_request(user_id: int, currency: str, username: str):
        """Сохраняет запрос пользователя о валюте в базу данных."""
        async def _save_currency_request(session):
            user = await UserDB.get_or_create_user(user_id, username)
            currency_obj = await CurrencyRequestDB.get_or_create_currency(currency)

            new_request = UserCurrencyRequest(
                user_id=user.user_id,
                currency_id=currency_obj.id,
                timestamp=datetime.utcnow()
            )
            session.add(new_request)
            await session.commit()
            await session.refresh(new_request)
            return new_request

        return await BaseDB.execute_with_session(_save_currency_request)

    @staticmethod
    async def get_last_currency_request(user_id: int, currency: str):
        """Возвращает 3 последних запроса пользователя по валюте."""
        async def _get_last_currency_request(session):
            query = (
                select(UserCurrencyRequest)
                .join(UserCurrencyRequest.user)
                .join(UserCurrencyRequest.currency)
                .filter(
                    User.user_id == user_id,
                    Currency.code == currency
                )
                .order_by(desc(UserCurrencyRequest.timestamp))
                .limit(3)
            )
            result = await session.execute(query)
            last_three_requests = result.scalars().all()

            if last_three_requests:
                last_three_ids = [request.id for request in last_three_requests]

                delete_query = (
                    delete(UserCurrencyRequest)
                    .where(
                        and_(
                            UserCurrencyRequest.user_id == user_id,
                            UserCurrencyRequest.currency_id == Currency.id,
                            Currency.code == currency,
                            not_(UserCurrencyRequest.id.in_(last_three_ids))
                        )
                    )
                )
                await session.execute(delete_query)
                await session.commit()
            return last_three_requests

        return await BaseDB.execute_with_session(_get_last_currency_request)

    @staticmethod
    async def get_currency_codes_sorted_by_count():
        """Возвращает список кодов валют, отсортированных по количеству запросов."""
        async def _get_currency_codes_sorted_by_count(session):
            query = select(Currency.code).order_by(Currency.count.desc())
            result = await session.execute(query)
            return result.scalars().all()

        return await BaseDB.execute_with_session(_get_currency_codes_sorted_by_count)








class CurrenciesData(RequestsApiAsync,RedisCli):
    """Получение данных валюты"""

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    name_redis_currencies = 'currencies'

    def __init__(self):
        RequestsApiAsync.__init__(self, api_url='https://www.cbr-xml-daily.ru/daily_json.js')
        RedisCli.__init__(self)
        self.list_curr_name= f'{self.name_redis_currencies}_list_currencies'
        self.data_list_curr= f'{self.name_redis_currencies}_date_list_currencies'
        self.solo_curr_name = f'{self.name_redis_currencies}_solo'


    async def get_curr(self):
        """Создаем в редис курсы валют """

        response = await self.get_response()
        if response:
            data = response
            if data:
                await self.filter_count_curr(data)
                for key, values in data['Valute'].items():

                    key_obj = f'{self.solo_curr_name}_{key}'
                    await self.rd_create_obj(key_obj, {
                        'name': values['Name'],
                        'value': values['Value']
                    })
                await self.rd_create_obj(self.data_list_curr, data['Date'],)


    async def filter_count_curr(self,data):
        """Сортируем список салют по популярности"""
        data_list = await CurrencyRequestDB.get_currency_codes_sorted_by_count()
        response_list  = list(data['Valute'].keys())
        a = set(response_list)
        b = set(data_list)
        result_list = list(a - b)
        data = data_list + result_list
        await self.rd_create_obj(self.list_curr_name, data)


    async def get_curr_list(self):
        list_curr = await self.rd_get_obj(self.list_curr_name)
        if not list_curr:
            await self.get_curr()
        list_curr = await self.rd_get_obj(self.list_curr_name)
        return  list_curr


    async def get_solo_curr(self, key):
        key_obj = f'{self.solo_curr_name}_{key}'
        solo_curr =  await self.rd_get_obj(key_obj)
        if not solo_curr:
            await self.get_curr()
        solo_curr = await  self.rd_get_obj(key_obj)
        return solo_curr


    async def get_date_curr(self):
        date_curr = await self.rd_get_obj(self.data_list_curr)
        if not date_curr:
            await self.get_curr()
        date_curr = await self.rd_get_obj(self.data_list_curr)
        return date_curr
