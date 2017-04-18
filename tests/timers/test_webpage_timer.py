import time
import tests.pages.testingwebpages as testingwebpages
from tests.uitestwrapper import UiTestWrapper


class TestWebpageTimer(UiTestWrapper):
    def timer_assertions(self, start_time, end_time, duration):
        assert hasattr(self.driver, "start_time")
        assert hasattr(self.driver, "end_time")
        assert hasattr(self.driver, "duration_time")
        assert isinstance(start_time, float), "Expecting returned start_time to be a float"
        assert isinstance(end_time, float), "Expecting returned end_time to be a float"
        assert isinstance(duration, float), "Expecting returned duration to be a float"
        assert isinstance(self.driver.start_time, float), "Expecting start_time to be a float"
        assert isinstance(self.driver.end_time, float), "Expecting end_time to be a float"
        assert isinstance(self.driver.duration_time, float), "Expecting duration_time to be a float"
        assert str(self.driver.start_time) == str(start_time), "Expecting the start_time = {} - actual: {}".format(
            start_time, self.driver.start_time)
        assert str(self.driver.end_time) == str(end_time), "Expecting end_time actual: {} - expected: {}".format(
            self.driver.end_time, end_time)
        actual_duration = self.driver.end_time - self.driver.start_time
        assert str(actual_duration) == str(duration), "Expecting duration actual: {} - expected: {}".format(
            actual_duration, duration)

    def teardown_method(self, test_method):
        if hasattr(self.driver, "start_time"):
            delattr(self.driver, "start_time")
        if hasattr(self.driver, "end_time"):
            delattr(self.driver, "end_time")
        if hasattr(self.driver, "duration_time"):
            delattr(self.driver, "duration_time")

    def test_start_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        assert hasattr(self.driver, "start_time")
        assert self.driver.start_time == start_time, "Expecting the start_time = {} - actual: {}".format(
            start_time, self.driver.start_time)

    def test_get_split_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        split_time = page.get_split_time()
        assert split_time == 0, "Expecting the split time to be 0 if I haven't started a timer"

    def test_get_split_after_reset_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        assert hasattr(self.driver, "start_time")
        assert self.driver.start_time == start_time, "Expecting the start_time = {} - actual: {}".format(
            start_time, self.driver.start_time)
        page.reset_timer()
        split_time = page.get_split_time()
        assert split_time == 0, "Expecting the split time to be 0 if I haven't started a timer"

    def test_start_stop_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        time.sleep(0.5)
        end_time = page.stop_timer()
        duration = page.get_duration()
        self.timer_assertions(start_time, end_time, duration)

    def test_start_stop_multiple_times_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        time.sleep(0.5)
        page.stop_timer()
        time.sleep(0.5)
        end_time = page.stop_timer()
        duration = page.get_duration()
        self.timer_assertions(start_time, end_time, duration)

    def test_start_stop_duration_multiple_times_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        time.sleep(0.5)
        end_time = page.stop_timer()
        time.sleep(0.5)
        page.get_duration()
        time.sleep(0.5)
        page.get_duration()
        duration = page.get_duration()
        self.timer_assertions(start_time, end_time, duration)

    def test_start_get_duration_multiple_times_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        time.sleep(0.5)
        duration = page.get_duration()
        end_time = self.driver.end_time
        time.sleep(0.5)
        actual_duration = page.get_duration()
        assert str(actual_duration) == str(duration), "Expecting duration to be the same - actual: {} - expected: {}".format(
            actual_duration, duration)
        time.sleep(0.5)
        actual_duration = page.get_duration()
        assert str(actual_duration) == str(duration), "Expecting duration to be the same - actual: {} - expected: {}".format(
            actual_duration, duration)
        self.timer_assertions(start_time, end_time, duration)

    def test_start_stop_split_timer(self):
        page = testingwebpages.MyComplexPage(self.driver)
        start_time = page.start_timer()
        time.sleep(0.5)
        split_time = page.get_split_time()
        assert split_time > 0
        assert not hasattr(self.driver, "end_time") or self.driver.end_time == 0
        time.sleep(0.5)
        split_time = page.get_split_time()
        assert not hasattr(self.driver, "end_time") or self.driver.end_time == 0
        assert split_time > 0
        time.sleep(0.5)
        end_time = page.stop_timer()
        duration = page.get_duration()
        assert duration > split_time
        self.timer_assertions(start_time, end_time, duration)
