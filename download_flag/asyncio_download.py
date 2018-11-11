import asyncio
import aiohttp
from download_flag.configs import BASE_URL
from base_download import save_flag, show, main
from utils import timer

@asyncio.coroutine
def get_flag(cc):
    url = BASE_URL.format(country=cc)
    print(url)
    res = yield from aiohttp.ClientSession().get(url)
    image = yield from res.read()
    return image


@asyncio.coroutine
def download_one(cc):
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, '{}.gif'.format(cc))
    return cc

@timer
def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(future=wait_coro)
    loop.close()
    return len(res)


if __name__ == '__main__':
    main(download_many)