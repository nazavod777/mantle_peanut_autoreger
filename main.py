import asyncio
from os import mkdir
from os.path import exists
from sys import stderr

from better_proxy import Proxy
from loguru import logger

from core import start_reger

logger.remove()
logger.add(stderr, format='<white>{time:HH:mm:ss}</white>'
                          ' | <level>{level: <8}</level>'
                          ' | <cyan>{line}</cyan>'
                          ' - <white>{message}</white>')


async def main() -> None:
    tasks: list = [
        asyncio.create_task(coro=start_reger(proxy=proxies_list.pop(0)))
        for _ in range(len(proxies_list))
    ]

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    if not exists(path='result'):
        mkdir(path='result')

    with open(file='data/proxies.txt',
              mode='r',
              encoding='utf-8-sig') as file:
        proxies_list: list[str] = [Proxy.from_str(proxy=row.strip()).as_url for row in file]

    threads: int = len(proxies_list)

    logger.info(f'Successfully loaded {len(proxies_list)} Proxies (threads)')

    try:
        import uvloop

        uvloop.run(main())

    except ModuleNotFoundError:
        asyncio.run(main())
