import asyncio
import requests as req
from aiohttp import ClientSession
from lxml import html
import re
import sqlite3
import psycopg2

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run(r):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i*40), session))
            tasks.append(task)
        return await asyncio.gather(*tasks)
        # you now have all response bodies in this variable

async def runn(pages):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for item in pages:
            task = asyncio.ensure_future(fetch(item, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)
        # you now have all response bodies in this variable

def parsing(responses):
    list = []

    for item in responses:
        # print(item)
        root = html.fromstring(item)
        list_of_topics.extend(root.xpath('//div[@class="list-inner"]/a/text()'))
        # list.append(root.xpath('//div[@class="list-inner"]/a/text()'))
        # print(root.xpath('//a[@class="topictitle"]/@href'))
        list.extend(root.xpath('//a[@class="topictitle"]/@href'))
        # list.append(root.xpath('//a[@class="topictitle"]/@href'))
        author.extend(root.xpath('//dd[@class="author"]/a/text()'))
        # list.append(root.xpath('//dd[@class="author"]/a/text()'))
    new_list = []
    for item in list:
        str = 'http://forum.overclockers.ua/'
        item = item[2:]
        new_list.append(str + item)

    return new_list

def find_money(posts):
    price = []
    currency = []
    for post in posts:
        post = str(post)
        patter = re.compile('(\d*)[ ]?(грн)')
        result = patter.findall(post)
        if result == []:
            price.append(0)
            currency.append('грн')
        else:
            price.append(result[0][0])
            currency.append(result[0][1])
    return price,currency

url = "http://forum.overclockers.ua/viewforum.php?f=26&start={}"




loop = asyncio.get_event_loop()

# Polychaem spisok tem
result = loop.run_until_complete(run(1))

# Polychaem ssulki
list_of_topics = []
author = []
pages = parsing(result)
print(len(author))
print(len(pages))
print(len(list_of_topics))


bodies = loop.run_until_complete(runn(pages))

posts = []
for item in bodies:
    post = html.fromstring(item)
    posts.append((post.xpath('//div[@class="content"]')[0].xpath('descendant-or-self::text()')))
print(len(posts))

p , c = find_money(posts)
print(len(p))
print(len(c))

# '''
# Sozdaem Bazu
# '''

conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='9348'")
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS posts(
       id SERIAL PRIMARY KEY,
       author TEXT NOT NULL,
       url TEXT NOT NULL,
       topics TEXT NOT NULL,
       post_text TEXT NOT NULL,
       price TEXT NOT NULL,
       currency TEXT NOT NULL
    );
    ''')

for i in range (1,len(author)):
    cur.execute('''INSERT INTO posts(id, author, url, topics, post_text, price, currency)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);''',(i,author[i-1],pages[i-1],list_of_topics[i-1],posts[i-1],p[i-1],c[i-1]))



conn.commit()
conn.close()

# body = html.fromstring(bodies[21])
# print(body.xpath('//div[@class="content"]')[0].xpath('descendant-or-self::text()'))

