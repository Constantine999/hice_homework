import asyncio
from random import choice
from time import perf_counter

import aiohttp

from DummyMessenger import PORTS


def get_senders(total: int = 100) -> list[dict[str, str]]:
    """Генерирует список из total словарей с рандомными значениями"""
    senders: tuple[str, ...] = \
        ("Джеймс Гослинг", "Деннис Ритчи", "Бьёрн Страуструп", "Гвидо ван Россум", "Брендан Эйх",
         "Ларри Уолл", "Расмус Лердорф", "Юкихиро Мацумото", "Джон Маккарти", "Никлаус Вирт"
         )

    with open("./text.txt", encoding="utf-8") as text:
        result: list[str] = list(map(str.strip, text.readlines()))

    return [dict(name=choice(senders), text=choice(result)) for _ in range(total)]


async def send_request(data_to_send: dict[str, str]) -> None:
    """Корутина для отправления запроса на сервер"""
    async with aiohttp.ClientSession() as session:
        port: int = choice(PORTS)
        await session.post(
            url=f"http://127.0.0.1:{port}/api/v1/client/",
            json=data_to_send,
            ssl=False
        )


async def generator_group_coroutines() -> None:
    """Генерирует группу с корутинами"""
    await asyncio.gather(*[send_request(sender) for sender in get_senders()])


async def main() -> None:
    """Запускает тест"""
    print("Тест запущен\nИдёт отправка запросов\nОжидаем завершения теста...\n")
    requests: int = 5000
    start = perf_counter()
    await asyncio.gather(*[generator_group_coroutines() for _ in range(50)])
    duration = perf_counter() - start

    print("Тест завершен\n")
    print(f"Отправлено запросов = {requests}")
    print(f"Количество использованных серверов = {len(PORTS)}")
    print(f"Общая пропускная способность всех запросов = {round(duration, 3)} сек.")
    print(f"Среднее время выполнения одного запроса = {round(duration / requests, 3)} сек.")


asyncio.run(main())
