import asyncio
import random
import aiohttp
from time import perf_counter

lock = asyncio.Lock()


def get_senders() -> list[dict[str, str]]:
    """Сгенериует список из 100 словарей"""

    SENDERS = ("Джеймс Гослинг", "Деннис Ритчи", "Бьёрн Страуструп", "Гвидо ван Россум", "Брендан Эйх",
               "Ларри Уолл", "Расмус Лердорф", "Юкихиро Мацумото", "Джон Маккарти", "Никлаус Вирт")

    with open("./text.txt", encoding="utf-8") as text:
        result: list[str] = list(map(str.strip, text.readlines()))

    return [dict(name=random.choice(SENDERS), text=random.choice(result)) for _ in range(100)]


async def send_large_data(data_to_send: dict[str, str]):
    async with lock:
        async with aiohttp.ClientSession() as session:
            port = random.choice((7000, 8000))
            await session.post(url=f"http://127.0.0.1:{port}/api/v1/", json=data_to_send)


async def start_coroutine():
    await asyncio.gather(*[send_large_data(sender) for sender in get_senders()])


async def main():
    start_time = perf_counter()
    for _ in range(50):
        await start_coroutine()
    duration = round(perf_counter() - start_time, 3)

    print(f"Вcего прошло времени {duration=}")
    print(f"Среднее время выполнения одного запроса {round(duration / 5000, 3)}")


asyncio.run(main())
