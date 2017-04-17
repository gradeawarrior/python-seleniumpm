import pytest

from tests.uitestwrapper import UiTestWrapper

from seleniumpm.webelements.element import Element
from seleniumpm.locator import Locator
from selenium.webdriver.common.by import By

class TestElement(UiTestWrapper):
    def test_instantiate_element(self):
        xpath = "//foo"
        element = Element(self.driver, Locator(By.XPATH, xpath))
        assert element != None

    def test_two_elements_are_equal(self):
        xpath = "//foo"
        element1 = Element(self.driver, Locator(By.XPATH, xpath))
        element2 = Element(self.driver, Locator(By.XPATH, xpath))
        assert element1 == element2
        assert not (element1 != element2)

    def test_two_elements_are_not_equal_by_by(self):
        xpath = "//foo"
        element1 = Element(self.driver, Locator(By.XPATH, xpath))
        element2 = Element(self.driver, Locator(By.CLASS_NAME, xpath))
        assert element1 != element2
        assert not (element1 == element2)

    def test_two_elements_are_not_equal_by_value(self):
        xpath = "//foo"
        xpath2 = "//foo/bar"
        element1 = Element(self.driver, Locator(By.XPATH, xpath))
        element2 = Element(self.driver, Locator(By.XPATH, xpath2))
        assert element1 != element2
        assert not (element1 == element2)

    test_number_data = [
        ("1", 1),
        ("1.0", 1.0),
        ("  1", 1),
        ("   1     ", 1),
        ("  1.0", 1.0),
        ("   1.0     ", 1.0),
        ("-1", -1),
        ("-1.0", -1.0),
        ("  -1", -1),
        ("   -1     ", -1),
        ("  -1.0", -1.0),
        ("   -1.0     ", -1.0),
        ("1mbps", 1),
        ("1.0mbps", 1.0),
        ("0.3556 percent", 0.3556),
        ("There is 1.0 number here", 1.0),
        ("-1mbps", -1),
        ("-1.0mbps", -1.0),
        ("-0.3556 percent", -0.3556),
        ("There is -1.0 number here", -1.0),
        ("There-are-several-dashes but one number: 1.0", 1.0),
        ("There is 1.0 number here but many dots.", 1.0),
        ("there are two numbers: 1 and 1.0", 1),
        ("there-are-several-numbers.and.dots: 123, 4, 4.0, 5.6.7", 123),
        ("there-are-several-numbers.and.dots: 123.456, 4, 4.0, 5.6.7", 123.456),
        ("there-are-several-numbers.and.dots: -123.456, 4, 4.0, 5.6.7", -123.456),
        ("", None),
        ("   ", None),
        (" 1.2.3  ", 1.2),          # The behavior is that it will assume the first part as valid
        (" -1.2.3  ", -1.2),        # The behavior is that it will assume the first part as valid
        (" 1.2.3.4.5  ", 1.2),      # The behavior is that it will assume the first part as valid
        (" -1.2.3.4.5  ", -1.2),    # The behavior is that it will assume the first part as valid
        (" foo  ", None),
        (" 10,11,12,13,14   ", 10),
        (" 10.0,11.0,12.0,13.0,14.0   ", 10.0),
    ]

    test_number_with_index_data = [
        (" 1.2.3  ", 1,  3.0),          # The behavior is that it will assume the first part as valid
        (" -1.2.3  ", 1, 3.0),          # The behavior is that it will assume the first part as valid
        (" 1.2.3.4.5  ", 1, 3.4),       # The behavior is that it will assume the first part as valid
        (" -1.2.3.4.5  ", 1, 3.4),      # The behavior is that it will assume the first part as valid
        (" 10,11,12,13,14   ", 2, 12),
        (" 10.0,11.0,12.0,13.0,14.0   ", 3, 13.0),
        (" 10.0,11.0,12.0,-13.0,14.0   ", 3, -13.0),
    ]

    @pytest.mark.parametrize("string,expected", test_number_data)
    def test_get_number(self, string, expected):
        xpath = "//foo"
        element = Element(self.driver, Locator(By.XPATH, xpath))

        actual = element.get_number(string)
        assert actual == expected, "Expecting '{}' to convert to {} - actual: {}".format(string, expected, actual)

    @pytest.mark.parametrize("string,index, expected", test_number_with_index_data)
    def test_get_number_by_index(self, string, index, expected):
        xpath = "//foo"
        element = Element(self.driver, Locator(By.XPATH, xpath))

        actual = element.get_number(string, result_index=index)
        assert actual == expected, "Expecting '{}' to convert to {} - actual: {}".format(string, expected, actual)
