import asyncio
import aiohttp
from lxml import html
import xlsxwriter

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
            price_ = price_[0]
            if len(supply_) == 0:
                supply_ = (tr.xpath('td[@class = "no-wrap text-right"]/span/@data-supply'))
            supply_ = supply_[0]
            volume_ = volume_[0]
            if len(h1_) == 0:
                h1_ = '?'
            else:
                h1_ = h1_[0]

            if len(h24_) == 0:
                h24_ = '?'
            else:
                h24_ = h24_[0]

            if len(d7_) == 0:
                d7_ = '?'
            else:
                d7_ = d7_[0]
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


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    page = loop.run_until_complete(responce(loop))

    result = parse(page)
    result.pop(0)
    print(result)

    workbook = xlsxwriter.Workbook('Result.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for name, symbol, market_cap, price, supply, volume, h1, h24, d7 in result:

        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, symbol)
        worksheet.write(row, col + 2, market_cap)
        worksheet.write(row, col + 3, price)
        worksheet.write(row, col + 4, supply)
        worksheet.write(row, col + 5, volume)
        worksheet.write(row, col + 6, h1)
        worksheet.write(row, col + 7, h24)
        worksheet.write(row, col + 8, d7)
        row += 1

    workbook.close()
