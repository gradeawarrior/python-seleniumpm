from tests.uitestwrapper import UiTestWrapper
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from seleniumpm.locator import Locator
from seleniumpm.examples.google_page import GooglePage
from seleniumpm.webelements.element import Element
import seleniumpm.config as seleniumconfig

import logging
import os
import time

logging.basicConfig()
log = logging.getLogger()

class TestScreenshot(UiTestWrapper):
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
        super(TestScreenshot, self).setup_class()
        self.create_screenshot_dir()
        log.setLevel(logging.ERROR)

    @classmethod
    def teardown_class(self):
        log.setLevel(logging.WARNING)

    def test_take_explicit_webpage_screenshot(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        file = page.take_screenshot()
        filepath = "{}/{}.png".format(seleniumconfig.screenshot_dir, file)
        assert os.path.exists(filepath), "Expecting that a screenshot was taken and saved here: {}".format(filepath)

    def test_take_multiple_webpage_screenshots_with_same_name(self):
        """
        The expectation is that they overwrite each other
        """
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)
        time.sleep(1)
        file1 = page.take_screenshot()
        time.sleep(2)
        file2 = page.take_screenshot(screenshot_name=file1)
        file3 = page.take_screenshot(screenshot_name=file1)
        filepath = "{}/{}.png".format(seleniumconfig.screenshot_dir, file1)
        time.sleep(3)
        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert file1 == file2 and file2 == file3, "I'm expecting the files to the same if taken really fast - file1: {} - file2: {} - file3: {}".format(
            file1, file2, file3)
        assert os.path.exists(filepath), "Expecting that a screenshot was taken and saved here: {}".format(filepath)
        assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_webpage_screenshot_enabled_validate(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.invalid_element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)
        try:
            page.validate(timeout=5)
        except TimeoutException:
            num_files_after = self.count_files(seleniumconfig.screenshot_dir)
            assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_webpage_screenshot_enabled_wait_for_page_load(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.invalid_element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)
        try:
            page.wait_for_page_load(timeout=5)
        except TimeoutException:
            num_files_after = self.count_files(seleniumconfig.screenshot_dir)
            assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_webpage_screenshot_disabled(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.invalid_element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        # Disable taking screenshot globally
        seleniumconfig.screenshot_enabled = False

        try:
            page.wait_for_page_load(timeout=5)
        except TimeoutException:
            num_files_after = self.count_files(seleniumconfig.screenshot_dir)
            assert num_files_after == num_files_before, "Expecting there to be the same number of screenshots taken"
        finally:
            seleniumconfig.screenshot_enabled = True

    def test_take_explicit_element_screenshot(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        file = page.element.take_screenshot()
        filepath = "{}/{}.png".format(seleniumconfig.screenshot_dir, file)
        assert os.path.exists(filepath), "Expecting that a screenshot was taken and saved here: {}".format(filepath)

    def test_take_multiple_element_screenshots_with_same_name(self):
        """
        The expectation is that they overwrite each other
        """
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)
        time.sleep(1)
        file1 = page.element.take_screenshot()
        time.sleep(2)
        file2 = page.element.take_screenshot(screenshot_name=file1)
        file3 = page.element.take_screenshot(screenshot_name=file1)
        filepath = "{}/{}.png".format(seleniumconfig.screenshot_dir, file1)
        time.sleep(3)
        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert file1 == file2 and file2 == file3, "I'm expecting the files to the same if taken really fast - file1: {} - file2: {} - file3: {}".format(
            file1, file2, file3)
        assert os.path.exists(filepath), "Expecting that a screenshot was taken and saved here: {}".format(filepath)
        assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_element_screenshot_enabled_get_web_element(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        try:
            page.element.get_webelement()
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_element_screenshot_disabled(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        # Disable taking screenshot globally
        seleniumconfig.screenshot_enabled = False

        try:
            page.element.get_webelement()
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass
        finally:
            seleniumconfig.screenshot_enabled = True

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == num_files_before, "Expecting there to be the same number of screenshots taken"

    def test_take_implicit_element_screenshot_enabled_wait_for_present(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        try:
            page.element.wait_for_present(timeout=1)
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_element_screenshot_enabled_wait_for_present_and_visible(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        try:
            page.element.wait_for_present_and_visible(timeout=1)
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == (num_files_before + 1), "Expecting there to be 1-more screenshot taken"

    def test_take_implicit_element_screenshot_enabled_is_present(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        try:
            page.element.is_present(timeout=1)
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == num_files_before, "Expecting there to be the same number of screenshots taken"

    def test_take_implicit_element_screenshot_enabled_is_visible(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        try:
            page.element.is_visible(timeout=1)
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == num_files_before, "Expecting there to be the same number of screenshots taken"

    def test_take_implicit_element_screenshot_enabled_is_present_and_visible(self):
        page = GooglePage(driver=self.driver, url="http://www.google.com")
        page.open().wait_for_page_load()
        page.element = Element(self.driver, Locator.by_xpath("//foo"))
        num_files_before = self.count_files(seleniumconfig.screenshot_dir)

        try:
            page.element.is_present_and_visible(timeout=1)
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        num_files_after = self.count_files(seleniumconfig.screenshot_dir)
        assert num_files_after == num_files_before, "Expecting there to be the same number of screenshots taken"
