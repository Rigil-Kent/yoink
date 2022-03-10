import imp
from bs4 import BeautifulSoup

import os
import unittest

from yoink.common import app_root, library_path, config_path, skippable_images, supported_sites, qb_client, required_comic_files, torrent_concurrent_download_limit, headers
from yoink.comic import Comic, ComicArchiver



class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.test_comic = 'http://readallcomics.com/static-season-one-4-2021/'
        self.comic = Comic(self.test_comic)
        self.archiver = ComicArchiver(self.comic)

    def test_000_comic_generates_valid_markup(self):
        self.assertTrue('!DOCTYPE html' in str(self.comic.markup))

    def test_001_comic_has_valid_title(self):
        self.assertEqual('Static Season One 4 (2021)', self.comic.title)

    def test_002_comic_has_valid_category(self):
        self.assertEqual('Static: Season One', self.comic.category)

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
        self.assertAlmostEqual(len(os.listdir(os.path.join(library_path, f'comics/{self.comic.title}'))), 3)