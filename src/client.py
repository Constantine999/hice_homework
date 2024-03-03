import asyncio
from random import choice
from time import perf_counter

import aiohttp


def get_senders() -> list[dict[str, str]]:
    """Генерирует список из 100 словарей с рандомными значениями"""
    senders: tuple[str, ...] = \
        ("Джеймс Гослинг", "Деннис Ритчи", "Бьёрн Страуструп", "Гвидо ван Россум", "Брендан Эйх",
         "Ларри Уолл", "Расмус Лердорф", "Юкихиро Мацумото", "Джон Маккарти", "Никлаус Вирт"
         )

    with open("./text.txt", encoding="utf-8") as text:
        result: list[str] = list(map(str.strip, text.readlines()))

    return [dict(name=choice(senders), text=choice(result)) for _ in range(100)]


async def send_request(data_to_send: dict[str, str]) -> None:
    """Корутина для отправления запроса на сервер"""
    async with aiohttp.ClientSession() as session:
        port: int = choice((9000, 10000))
        await session.post(
            url=f"http://127.0.0.1:{port}/api/v1/",
            json=data_to_send
        )


async def generator_group_coroutines() -> None:
    """Генерирует группу с корутинами"""
    await asyncio.gather(*[send_request(sender) for sender in get_senders()])


async def main() -> None:
    """Запускает тест"""
    start = perf_counter()
    await asyncio.gather(*[generator_group_coroutines() for _ in range(50)])
    duration = perf_counter() - start

    print(f"Общая продолжительность всех запросов = {round(duration, 3)} секунд.")
    print(f"Среднее время выполнения одного запроса = {round(duration / 5000, 3)} секунд.")


for _ in range(10):
    asyncio.run(main())
