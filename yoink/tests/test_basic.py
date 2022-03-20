from bs4 import BeautifulSoup

import os
import unittest
from shutil import rmtree

from yoink.common import app_root, library_path, config_path, skippable_images, supported_sites, required_comic_files
from yoink.comic import Comic, ComicArchiver
from yoink.scraper import Scrapable



class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.test_comic = 'http://readallcomics.com/static-season-one-4-2021/'
        self.test_comic_b = 'http://readallcomics.com/captain-marvel-vs-rogue-2021-part-1/'
        self.comic = Comic(self.test_comic_b)
        self.archiver = ComicArchiver(self.comic)
        self.remove_queue = []
        self.expected_title = 'Static Season One 4 (2021)'
        self.expected_title_b = 'Captain Marvel vs. Rogue (2021 – Part 1)'
        self.expected_category = 'Static: Season One'
        self.expected_category_b = 'Captain Marvel vs. Rogue'
        self.expected_issue_num = 1

        
    def tearDown(self) -> None:
        for folder in self.remove_queue:
            rmtree(folder)
        


    def test_000_comic_generates_valid_markup(self):
        self.assertTrue('!DOCTYPE html' in str(self.comic.markup))

    def test_001_comic_has_valid_title(self):
        self.assertEqual(self.expected_title_b, self.comic.title)

    def test_002_comic_has_valid_category(self):
        self.assertEqual(self.expected_category_b, self.comic.category)

    def test_003_empty_comic_folder(self):
        self.assertEqual(len(os.listdir(os.path.join(library_path, 'comics'))), 0)

    def test_004_comic_folder_created_and_populated(self):
        self.archiver.download()
        self.assertTrue(os.path.exists(os.path.join(library_path, f'comics/{self.comic.title}')))
        self.assertGreater(len(os.listdir(os.path.join(library_path, f'comics/{self.comic.title}'))), 0)

    def test_005_comic_archive_generated(self):
        self.archiver.generate_archive()
        self.assertTrue(os.path.exists(os.path.join(library_path, f'comics/{self.comic.title}/{self.comic.title}.cbr')))

    def test_006_folder_cleaned_after_archive_generation(self):
        self.archiver.cleanup_worktree()
        self.assertLessEqual(len(os.listdir(os.path.join(library_path, f'comics/{self.comic.title}'))), 3)

    def test_007_comic_instance_has_archiver(self):
        self.assertIsInstance(self.comic.archiver, ComicArchiver)

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
    
