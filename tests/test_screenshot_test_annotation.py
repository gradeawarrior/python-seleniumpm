import os
import time
import pytest

from tests.uitestwrapper import UiTestWrapper

import seleniumpm.config as seleniumconfig
from seleniumpm.locator import Locator
from seleniumpm.examples.google_page import GooglePage
from seleniumpm.webelements.element import Element
from seleniumpm.annotations import take_screenshot_on_test_error

class TestScreenshotTestAnnotation(UiTestWrapper):
    @staticmethod
    def create_screenshot_dir(screenshot_dir=seleniumconfig.screenshot_dir):
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

    @staticmethod
    def count_files(path):
        """
        Counts the number of files given a directory path

        :param path: Some path
        :return: A count of all file types (excluding directories)
        """
        num_files = len([f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))])
        return num_files

    @classmethod
    def setup_class(self):
        super(TestScreenshotTestAnnotation, self).setup_class()
        self.create_screenshot_dir()
        self.num_files_before = self.count_files(seleniumconfig.screenshot_dir)

    @pytest.mark.xfail()
    @take_screenshot_on_test_error
    def test_xfailed_wait_for_page_load(self):
        self.num_files_before = self.count_files(seleniumconfig.screenshot_dir)
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        page.wait_for_page_load(timeout=5)

    def test_failed_validation(self):
        time.sleep(3)
        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == (self.num_files_before + 2), "Expecting there to be the 2-more screenshots taken"

