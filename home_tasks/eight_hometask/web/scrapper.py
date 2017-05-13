import asyncio
import aiohttp
from lxml import html
from pymongo import MongoClient
import datetime

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def responce(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'https://coinmarketcap.com/all/views/all/')
        return html


def parse(page):
    root = html.fromstring(page)

    name = []
    symbol  = []
    market_cap = []
    price = []
    supply = []
    volume  = []
    h1 = []
    h24  = []
    d7 = []
    # print( name , symbol , market_cap ,price , supply , volume , h1 , h24 , d7)
    for tr in (root.xpath('//tr')):
        name_ = (tr.xpath('td[@class = "no-wrap currency-name"]/a/text()'))
        symbol_ = (tr.xpath('td[@class = "text-left"]/text()'))
        market_cap_ = (tr.xpath('td[@class = "no-wrap market-cap text-right"]/@data-usd'))  # currency $
        price_ = (tr.xpath('td[@class = "no-wrap text-right"]/a[@class = "price"]/@data-usd'))  # currency $
        supply_ = (tr.xpath('td[@class = "no-wrap text-right"]/a/@data-supply'))
        volume_ = (tr.xpath('td[@class = "no-wrap text-right "]/a[@class = "volume"]/@data-usd'))  # currency $
        h1_ = (tr.xpath('td[contains(@class, "percent-1h")]/text()'))  # currency %
        h24_ = (tr.xpath('td[contains(@class, "percent-24h")]/text()'))  # currency %
        d7_ = (tr.xpath('td[contains(@class, "percent-7d")]/text()'))  # currency %
        try:
            name_ = name_[0]
            symbol_ = symbol_[0]

            market_cap_ = market_cap_[0]
            if '?' in market_cap_:
                market_cap_ = 0

            price_ = price_[0]
            if '?' in price_:
                price_ = 0

            if len(supply_) == 0:
                supply_ = (tr.xpath('td[@class = "no-wrap text-right"]/span/@data-supply'))


            supply_ = supply_[0]
            if 'None' in supply_:
                supply_ = 0

            volume_ = volume_[0]
            if 'None' in volume_:
                volume_ = 0

            if len(h1_) == 0:
                h1_ = 0
            else:
                h1_ = h1_[0]
                h1_ = h1_[0:(h1_.find('%'))]
            if len(h24_) == 0:
                h24_ = 0
            else:
                h24_ = h24_[0]
                h24_ = h24_[0:(h24_.find('%'))]

            if len(d7_) == 0:
                d7_ = 0
            else:
                d7_ = d7_[0]
                d7_ = d7_[0:(d7_.find('%'))]
        except:
            pass

        name.append(name_)
        symbol.append(symbol_)
        market_cap.append(market_cap_)  # currency $
        price.append(price_)  # currency $
        supply.append(supply_)
        volume.append(volume_)  # currency $
        h1.append(h1_)  # currency %
        h24.append(h24_)  # currency %
        d7.append(d7_)  # currency %

    return list(zip(name, symbol, market_cap, price, supply, volume, h1, h24, d7))

# def check_if_exists(author,topic_name):
#     result = posts.find_one({"author":author,"topic_name":topic_name})
#     if result==None:
#         return True
#     else:
#         return False

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    page = loop.run_until_complete(responce(loop))

    result = parse(page)
    result.pop(0)

    client = MongoClient('localhost', 27017)

    db = client.bitcoin

    posts = db.posts

    counter = 0

    date = datetime.datetime.now()

    for item in result:
            post = {"name" : item[0],
                    "symbol" : item[1],
                    "market_cap" : item[2],
                    "price" : item[3],
                    "supply" : item[4],
                    "volume" : item[5],
                    "h1" : item[6],
                    "h24" : item[7],
                    "d7" : item[8],
                    "date": date}
            posts.insert_one(post).inserted_id
            counter +=1

    db = client.bitcoin

    log = db.log
    log.insert_one({"date":date})

    print(counter)
    print(posts.count())
