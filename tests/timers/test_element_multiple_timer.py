import time
from tests.uitestwrapper import UiTestWrapper
from seleniumpm.webelements.element import Element


class TestElementMultipleTimer(UiTestWrapper):
    def timer_assertions(self, element_start_time, element_end_time, duration):
        assert hasattr(self.driver, "element_start_time")
        assert hasattr(self.driver, "element_end_time")
        assert hasattr(self.driver, "element_duration_time")
        assert isinstance(element_start_time, float), "Expecting returned element_start_time to be a float"
        assert isinstance(element_end_time, float), "Expecting returned element_end_time to be a float"
        assert isinstance(duration, float), "Expecting returned duration to be a float"
        assert isinstance(self.driver.element_start_time, float), "Expecting element_start_time to be a float"
        assert isinstance(self.driver.element_end_time, float), "Expecting element_end_time to be a float"
        assert isinstance(self.driver.element_duration_time, float), "Expecting element_duration_time to be a float"
        assert str(self.driver.element_start_time) == str(element_start_time), "Expecting the element_start_time = {} - actual: {}".format(
            element_start_time, self.driver.element_start_time)
        assert str(self.driver.element_end_time) == str(element_end_time), "Expecting element_end_time actual: {} - expected: {}".format(
            self.driver.element_end_time, element_end_time)
        actual_duration = self.driver.element_end_time - self.driver.element_start_time
        assert str(actual_duration) == str(duration), "Expecting duration actual: {} - expected: {}".format(
            actual_duration, duration)

    def teardown_method(self, test_method):
        if hasattr(self.driver, "element_start_time"):
            delattr(self.driver, "element_start_time")
        if hasattr(self.driver, "element_end_time"):
            delattr(self.driver, "element_end_time")
        if hasattr(self.driver, "element_duration_time"):
            delattr(self.driver, "element_duration_time")

    def test_element_start_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        assert hasattr(self.driver, "element_start_time")
        assert self.driver.element_start_time == element_start_time, "Expecting the element_start_time = {} - actual: {}".format(
            element_start_time, self.driver.element_start_time)

    def test_get_split_timer(self):
        element = Element(self.driver, None)
        split_time = element.get_split_time(type="element")
        assert split_time == 0, "Expecting the split time to be 0 if I haven't started a timer"

    def test_get_split_after_reset_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        assert hasattr(self.driver, "element_start_time")
        assert self.driver.element_start_time == element_start_time, "Expecting the element_start_time = {} - actual: {}".format(
            element_start_time, self.driver.element_start_time)
        element.reset_timer(type="element")
        split_time = element.get_split_time(type="element")
        assert split_time == 0, "Expecting the split time to be 0 if I haven't started a timer"

    def test_start_stop_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        time.sleep(0.5)
        element_end_time = element.stop_timer(type="element")
        duration = element.get_duration(type="element")
        self.timer_assertions(element_start_time, element_end_time, duration)

    def test_start_stop_multiple_times_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        time.sleep(0.5)
        element.stop_timer(type="element")
        time.sleep(0.5)
        element_end_time = element.stop_timer(type="element")
        duration = element.get_duration(type="element")
        self.timer_assertions(element_start_time, element_end_time, duration)

    def test_start_stop_duration_multiple_times_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        time.sleep(0.5)
        element_end_time = element.stop_timer(type="element")
        time.sleep(0.5)
        element.get_duration(type="element")
        time.sleep(0.5)
        element.get_duration(type="element")
        duration = element.get_duration(type="element")
        self.timer_assertions(element_start_time, element_end_time, duration)

    def test_start_get_duration_multiple_times_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        time.sleep(0.5)
        duration = element.get_duration(type="element")
        element_end_time = self.driver.element_end_time
        time.sleep(0.5)
        actual_duration = element.get_duration(type="element")
        assert str(actual_duration) == str(duration), "Expecting duration to be the same - actual: {} - expected: {}".format(
            actual_duration, duration)
        time.sleep(0.5)
        actual_duration = element.get_duration(type="element")
        assert str(actual_duration) == str(duration), "Expecting duration to be the same - actual: {} - expected: {}".format(
            actual_duration, duration)
        self.timer_assertions(element_start_time, element_end_time, duration)

    def test_start_stop_split_timer(self):
        element = Element(self.driver, None)
        element_start_time = element.start_timer(type="element")
        time.sleep(0.5)
        split_time = element.get_split_time(type="element")
        assert split_time > 0
        assert not hasattr(self.driver, "element_end_time") or self.driver.element_end_time == 0
        time.sleep(0.5)
        split_time = element.get_split_time(type="element")
        assert not hasattr(self.driver, "element_end_time") or self.driver.element_end_time == 0
        assert split_time > 0
        time.sleep(0.5)
        element_end_time = element.stop_timer(type="element")
        duration = element.get_duration(type="element")
        assert duration > split_time
        self.timer_assertions(element_start_time, element_end_time, duration)
