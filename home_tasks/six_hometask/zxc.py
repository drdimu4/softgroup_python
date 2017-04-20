import asyncio
import requests as req
from aiohttp import ClientSession
from lxml import html
async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def run(r):
    url = "http://forum.overclockers.ua/viewforum.php?f=26&start={}"
    tasks = []
    list = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i*40), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable

        for item in responses:
            # print(item)
            root = html.fromstring(item)
            # print(root.xpath('//div[@class="list-inner"]/a/text()'))
            # list.append(root.xpath('//div[@class="list-inner"]/a/text()'))
            # print(root.xpath('//a[@class="topictitle"]/@href'))
            list.extend(root.xpath('//a[@class="topictitle"]/@href'))
            # list.append(root.xpath('//a[@class="topictitle"]/@href'))
            # print(root.xpath('//dd[@class="author"]/a/text()'))
            # list.append(root.xpath('//dd[@class="author"]/a/text()'))
    print(list)
    new_list = []
    for item in list:
        str = 'http://forum.overclockers.ua/'
        item = item[2:]
        new_list.append(str + item)
    print(new_list)

    list_of_posts = []

    for item in new_list:
        res = req.get(item)
        root = html.fromstring(res.text)
        # list_of_posts.append(root.xpath('div[@class="content"]/text()'))
        print(root.xpath('//div[@class="content"]')[0].xpath('descendant-or-self::text()'))


def print_responses(result):
    print(result)

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(5))
loop.run_until_complete(future)