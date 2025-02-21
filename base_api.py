import json
import aiohttp

class RequestsApiAsync:
    def __init__(self, api_url=None):
        self.api_url = api_url

    async def get_response(self):
        """Асинхронный метод для выполнения GET-запроса."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    if response.status == 200:
                        text = await response.text()
                        try:
                            data = json.loads(text)
                            return data
                        except json.JSONDecodeError as e:
                            print(f"Ошибка при декодировании JSON: {e}")
                            return None
                    else:
                        print(f"Ошибка: сервер вернул статус {response.status}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Ошибка при выполнении запроса: {e}")
                return None
