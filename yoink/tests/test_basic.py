import os
import unittest
from bs4 import BeautifulSoup
from yoink.bounty import Bounty, Downloader
from yoink.provider import Provider, ReadAllComics



class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.test_comic = 'http://readallcomics.com/static-season-one-4-2021/'
        self.item = Bounty(self.test_comic)

    def test_000_provider_generates_or_fails_correctly(self):
        # ensure valid comic link returns correct factory
        self.assertTrue(isinstance(self.item.provider, ReadAllComics))

        # ensure invalid comic link raises ValueError stating lack of support
        def busted():
            return Bounty('http://viz.com')

        with self.assertRaises(ValueError) as context:
            busted() 

            self.assertTrue('Downloads for this site are not yet supported' in context.exception)


    def test_001_provider_markup_returns_200(self):
        self.assertEqual(self.item.provider.markup.status_code, 200)


    def test_002_provider_soup_object_exists(self):
        self.assertTrue(isinstance(self.item.provider.soup, BeautifulSoup))


    def test_003_downloader_object_exists(self):
        self.assertTrue(isinstance(self.item.downloader, Downloader))

    def test_004_downloader_paths_exist(self):
        self.assertTrue(os.path.exists(self.item.downloader.root_path))
        self.assertTrue(os.path.exists(self.item.downloader.config_path))

