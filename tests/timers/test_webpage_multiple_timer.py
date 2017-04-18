import time
import tests.pages.testingwebpages as testingwebpages
from tests.uitestwrapper import UiTestWrapper


class TestWebpageMultipleTimer(UiTestWrapper):
    def timer_assertions(self, page_start_time, page_end_time, duration):
        assert hasattr(self.driver, "page_start_time")
        assert hasattr(self.driver, "page_end_time")
        assert hasattr(self.driver, "page_duration_time")
        assert isinstance(page_start_time, float), "Expecting returned page_start_time to be a float"
        assert isinstance(page_end_time, float), "Expecting returned page_end_time to be a float"
        assert isinstance(duration, float), "Expecting returned duration to be a float"
        assert isinstance(self.driver.page_start_time, float), "Expecting page_start_time to be a float"
        assert isinstance(self.driver.page_end_time, float), "Expecting page_end_time to be a float"
        assert isinstance(self.driver.page_duration_time, float), "Expecting page_duration_time to be a float"
        assert str(self.driver.page_start_time) == str(page_start_time), "Expecting the page_start_time = {} - actual: {}".format(
            page_start_time, self.driver.page_start_time)
        assert str(self.driver.page_end_time) == str(page_end_time), "Expecting page_end_time actual: {} - expected: {}".format(
            self.driver.page_end_time, page_end_time)
        actual_duration = self.driver.page_end_time - self.driver.page_start_time
        assert str(actual_duration) == str(duration), "Expecting duration actual: {} - expected: {}".format(
            actual_duration, duration)

    def teardown_method(self, test_method):
        if hasattr(self.driver, "page_start_time"):
            delattr(self.driver, "page_start_time")
        if hasattr(self.driver, "page_end_time"):
            delattr(self.driver, "page_end_time")
        if hasattr(self.driver, "page_duration_time"):
            delattr(self.driver, "page_duration_time")

    def test_start_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        assert hasattr(self.driver, "page_start_time")
        assert self.driver.page_start_time == page_start_time, "Expecting the page_start_time = {} - actual: {}".format(
            page_start_time, self.driver.page_start_time)

    def test_get_split_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        split_time = page.get_split_time(type="page")
        assert split_time == 0, "Expecting the split time to be 0 if I haven't started a timer"

    def test_get_split_after_reset_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        assert hasattr(self.driver, "page_start_time")
        assert self.driver.page_start_time == page_start_time, "Expecting the page_start_time = {} - actual: {}".format(
            page_start_time, self.driver.page_start_time)
        page.reset_timer(type="page")
        split_time = page.get_split_time(type="page")
        assert split_time == 0, "Expecting the split time to be 0 if I haven't started a timer"

    def test_start_stop_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        time.sleep(0.5)
        page_end_time = page.stop_timer(type="page")
        duration = page.get_duration(type="page")
        self.timer_assertions(page_start_time, page_end_time, duration)

    def test_start_stop_multiple_times_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        time.sleep(0.5)
        page.stop_timer(type="page")
        time.sleep(0.5)
        page_end_time = page.stop_timer(type="page")
        duration = page.get_duration(type="page")
        self.timer_assertions(page_start_time, page_end_time, duration)

    def test_start_stop_duration_multiple_times_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        time.sleep(0.5)
        page_end_time = page.stop_timer(type="page")
        time.sleep(0.5)
        page.get_duration(type="page")
        time.sleep(0.5)
        page.get_duration(type="page")
        duration = page.get_duration(type="page")
        self.timer_assertions(page_start_time, page_end_time, duration)

    def test_start_get_duration_multiple_times_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        time.sleep(0.5)
        duration = page.get_duration(type="page")
        page_end_time = self.driver.page_end_time
        time.sleep(0.5)
        actual_duration = page.get_duration(type="page")
        assert str(actual_duration) == str(duration), "Expecting duration to be the same - actual: {} - expected: {}".format(
            actual_duration, duration)
        time.sleep(0.5)
        actual_duration = page.get_duration(type="page")
        assert str(actual_duration) == str(duration), "Expecting duration to be the same - actual: {} - expected: {}".format(
            actual_duration, duration)
        self.timer_assertions(page_start_time, page_end_time, duration)

    def test_start_stop_split_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page_start_time = page.start_timer(type="page")
        time.sleep(0.5)
        split_time = page.get_split_time(type="page")
        assert split_time > 0
        assert not hasattr(self.driver, "page_end_time") or self.driver.page_end_time == 0
        time.sleep(0.5)
        split_time = page.get_split_time(type="page")
        assert not hasattr(self.driver, "page_end_time") or self.driver.page_end_time == 0
        assert split_time > 0
        time.sleep(0.5)
        page_end_time = page.stop_timer(type="page")
        duration = page.get_duration(type="page")
        assert duration > split_time
        self.timer_assertions(page_start_time, page_end_time, duration)
