from scrapper import *
import unittest


class FixturesTest(unittest.TestCase):
    def setUp(self):
        # loop = asyncio.get_event_loop()
        # page = loop.run_until_complete(responce(loop))
        #
        # result = parse(page)

        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        self.compare_result = ['Bitcoin', 'BTC', 1000.0, 100.0, 100.0, 99.0, 1.0, 2.0, 3.0]

        with open('test_table.html', 'r') as file:
            self.content = file.read()

    def test_response(self):
        page = self.event_loop.run_until_complete(responce(self.event_loop))
        self.assertIsInstance(page, str, 'html doc')

    def test_parse(self):
        result = parse(self.content)
        self.assertEqual(result, list(self.compare_result), 'Scraper failed to properly scrap test_table.html')

    def test_database(self):
        counter, posts_count = database(parse(self.content))
        self.assertLess(counter,1000,'wdsfghj')
        self.assertGreater(posts_count,1000,'wdsfghj')

    def tearDown(self):
        self.event_loop.close()
