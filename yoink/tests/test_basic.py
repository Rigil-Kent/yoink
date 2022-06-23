from bs4 import BeautifulSoup

import os
import unittest
from shutil import rmtree

from yoink.config import app_root, library_path, config_path, skippable_images, supported_sites, required_archive_files
from yoink.comic import Comic, download_comic_files, generate_archive, clean_up
from yoink.scraper import Scrapable



class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.test_comic = 'http://readallcomics.com/static-season-one-6-2022/'
        self.test_comic_b = 'http://readallcomics.com/captain-marvel-vs-rogue-2021-part-1/'
        self.comic = Comic(self.test_comic)
        self.remove_queue = []
        self.expected_title = 'Static Season One 6 (2022)'
        self.expected_title_b = 'Captain Marvel vs. Rogue (2021 – Part 1)'
        self.expected_category = 'Static: Season One'
        self.expected_category_b = 'Captain Marvel vs. Rogue'
        self.expected_issue_num = 6
        self.expected_vol_num = 1
        self.expected_next_url = None
        self.expected_prev_url = 'http://readallcomics.com/static-season-one-5-2022/'
        self.erroneous_comic = 'http://readallcomics.com/static-season-one-4-2021/'

        
    def tearDown(self) -> None:
        for folder in self.remove_queue:
            rmtree(folder)
        


    def test_000_comic_generates_valid_markup(self):
        self.assertTrue('!DOCTYPE html' in str(self.comic.markup))

    def test_001_comic_has_valid_title(self):
        self.assertEqual(self.expected_title, self.comic.title)

    def test_002_comic_has_valid_volume_numer(self):
        self.assertEqual(self.expected_vol_num, self.comic.volume)

    def test_003_comic_has_valid_category(self):
        self.assertEqual(self.expected_category, self.comic.category)

    def test_004_empty_comic_folder(self):
        self.assertEqual(len(os.listdir(os.path.join(library_path, 'comics'))), 0)

    def test_005_comic_folder_created_and_populated(self):
        download_comic_files(self.comic)
        self.assertTrue(os.path.exists(os.path.join(library_path, f'comics/{self.comic.title}')))
        self.assertGreater(len(os.listdir(os.path.join(library_path, f'comics/{self.comic.title}'))), 0)

    def test_006_comic_archive_generated(self):
        generate_archive(self.comic)
        self.assertTrue(os.path.exists(os.path.join(library_path, f'comics/{self.comic.title}/{self.comic.title}.cbr')))

    def test_007_folder_cleaned_after_archive_generation(self):
        clean_up(self.comic)
        self.assertLessEqual(len(os.listdir(os.path.join(library_path, f'comics/{self.comic.title}'))), 3)

    def test_008_comic_is_subclass_scrapable(self):
        self.assertTrue(issubclass(Comic, Scrapable))

    def test_009_invalid_comic_link(self):

        with self.assertRaises(ValueError) as condition:
            comic = Comic('https://viz.com')

        self.assertTrue('Unsupported' in str(condition.exception))

        self.remove_queue.append(os.path.join(library_path, f'comics/{self.comic.title}'))

    def test_010_valid_issue_number(self):
        self.assertIsInstance(self.comic.issue_number, int)
        self.assertEqual(self.comic.issue_number, self.expected_issue_num)

    def test_011_has_next_link(self):
        self.assertEqual(self.comic.next, self.expected_next_url)

    def test_012_has_prev_link(self):
        self.assertEqual(self.comic.prev, self.expected_prev_url)

    @unittest.skip("No error raised as image links have been restored")
    def test_013_broken_comic_images_raise_ref_error(self):
        with self.assertRaises(ReferenceError) as condition:
            Comic(self.erroneous_comic).archiver.download()

        self.assertTrue('images might have errored' in str(condition.exception))

    
