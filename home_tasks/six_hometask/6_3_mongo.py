import pymongo
import pprint
from pymongo import MongoClient

import asyncio
import aiohttp
from lxml import html
import re
import sys

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def runn(pages):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    for item in pages:
        task = asyncio.ensure_future(fetch(item, session))
        tasks.append(task)
    return await asyncio.gather(*tasks)
        # you now have all response bodies in this variable


def parsing(responses):
    list = []
    list_of_topics= []
    author = []
    for item in responses:
        # print(item)
        root = html.fromstring(item)

        list_of_topics.extend(root.xpath('//div[@class="list-inner"]/a/text()'))

        list.extend(root.xpath('//a[@class="topictitle"]/@href'))

        author.extend(root.xpath('//dd[@class="author"]/a/text()'))

    new_list = []
    for item in list:
        str = 'http://forum.overclockers.ua/'
        item = item[2:]
        new_list.append(str + item)

    return new_list, list_of_topics, author


def find_money(posts):
    price = []
    currency = []
    for post in posts:
        post = str(post)
        patter = re.compile('(\d*)[\s]?(грн|\$|usd|dollars|долларов|гривен|гривень|ГРН|USD|Гривен|Гривень)')
        result = patter.findall(post)
        if result == []:
            price.append(0)
            currency.append('грн')
        else:
            price.append(result[0][0])
            currency.append(result[0][1])
    return price,currency


if __name__ == '__main__':
    url = "http://forum.overclockers.ua/viewforum.php?f=26&start={}"
    try:
        pages_count = int(input('Pages count:'))
    except:
        sys.exit()

    url_pages = []
    for i in range(pages_count):
        url_pages.append(url.format(i*40))

    with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()
        # Polychaem spisok tem
        result = loop.run_until_complete(runn(url_pages))

        # Polychaem ssulki
        urls, topic_names, author = parsing(result)

        #poluchaem text topikov
        bodies = loop.run_until_complete(runn(urls))

    post_text = []
    for item in bodies:
        post = html.fromstring(item)
        post_text.append((post.xpath('//div[@class="content"]')[0].xpath('descendant-or-self::text()')))

    price , currency = find_money(post_text)

def check_if_exists(author,topic_name):
    result = posts.find_one({"author":author,"topic_name":topic_name})
    if result==None:
        return True
    else:
        return False
# for i in range(0,len(urls)):
#     print(urls[i],topic_names[i],author[i],post_text[i],price[i],currency[i])

    # '''
    # Sozdaem Bazu
    # '''

client = MongoClient('localhost', 27017)

db = client.new_base

collection = db.new_collection

posts = db.posts


for i in range(0,len(urls)):
    if check_if_exists(author[i],topic_names[i]):
        post = {"topic_name":topic_names[i],
                "author":author[i],
                "url":urls[i],
                "post_text":post_text[i],
                "price":price[i],
                "currency":currency[i]}
        posts.insert_one(post).inserted_id

print(posts.count())

