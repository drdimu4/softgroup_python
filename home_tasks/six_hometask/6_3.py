import asyncio
import aiohttp
from lxml import html
import re
import psycopg2
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
        patter = re.compile('(\d*)[\s]?(грн|\$|usd|dollars|долларов|гривен|гривень|ГРН|USD|Гривен|Гривень)')
        result = patter.findall(post)
        if result == []:
            price.append(0)
            currency.append('грн')
        else:
            price.append(result[0][0])
            currency.append(result[0][1])
    return price,currency

def check_if_exists(cursor, author, topic_title):
    cursor.execute('''SELECT author FROM posts WHERE topics = (%s) AND author = (%s)''',
                               (topic_title, author))
    result = cursor.fetchone()

    if result:
        return True
    return False

if __name__ == '__main__':
    url = "http://forum.overclockers.ua/viewforum.php?f=26&start={}"
    try:
        pages_count = int(input('Pages count:'))
    except:
        sys.exit()

    url_pages = []
    for i in range(pages_count):
        url_pages.append(url.format(i*40))

    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession() as session:
        # Polychaem spisok tem
        result = loop.run_until_complete(runn(url_pages))

        # Polychaem ssulki
        list_of_topics = []
        author = []
        pages = parsing(result)

        #poluchaem text topikov
        bodies = loop.run_until_complete(runn(pages))

    posts = []
    for item in bodies:
        post = html.fromstring(item)
        posts.append((post.xpath('//div[@class="content"]')[0].xpath('descendant-or-self::text()')))

    p , c = find_money(posts)

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

    ins_count = 0
    for i in range (1, len(author)):
        topic_author = author[i-1]
        topic_title = list_of_topics[i-1]

        if not check_if_exists(cur, topic_author, topic_title):
            cur.execute('''INSERT INTO posts(author, url, topics, post_text, price, currency)
                            VALUES (%s,%s,%s,%s,%s,%s);''',(topic_author, pages[i-1],topic_title,posts[i-1],p[i-1],c[i-1]))
            ins_count += 1

    conn.commit()
    print('Rows inserted: {}'.format(ins_count))
    conn.close()
