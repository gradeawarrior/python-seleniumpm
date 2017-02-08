from seleniumpm.locator import Locator
from selenium.webdriver.common.by import By


class TestLocator:
    def test_new_locator(self):
        """
        Ensure that a locator can be created
        :return:
        """
        xpath = "//div/foobar"
        locator = Locator(By.XPATH, xpath)
        assert locator != None
        assert locator.by == By.XPATH
        assert locator.value == xpath

    def test_two_locators_are_the_same(self):
        """
        Make sure equivalence check between two locators that are the same
        :return:
        """
        xpath = "//div/foobar"
        locator1 = Locator(By.XPATH, xpath)
        locator2 = Locator(By.XPATH, xpath)
        assert locator1 == locator2
        assert not (locator1 != locator2)

    def test_two_locators_can_be_modified_independently(self):
        """
        Make sure two locators can be created and modified independent of one another
        :return:
        """
        xpath = "//div/foobar"
        locator1 = Locator(By.XPATH, xpath)
        locator2 = Locator(By.XPATH, xpath)
        assert locator1 == locator2
        assert not (locator1 != locator2)

        # Change locator2 value
        locator2.value += "/test"
        assert locator1.by == By.XPATH
        assert locator1.value == xpath
        assert locator2.by == By.XPATH
        assert locator2.value == "{}/{}".format(xpath, "test")
        assert locator1 != locator2

    def test_two_locators_are_the_not_same_by_value(self):
        """
        Make sure equivalence check between two locators with the same By but different value
        :return:
        """
        xpath1 = "//div/foobar"
        xpath2 = "//div/foobar/what"
        locator1 = Locator(By.XPATH, xpath1)
        locator2 = Locator(By.XPATH, xpath2)
        assert locator1 != locator2
        assert not (locator1 == locator2)

    def test_two_locators_are_the_not_same_by_by(self):
        """
        Make sure equivalence check between two locators with the same value but different By
        :return:
        """
        xpath = "//div/foobar"
        locator1 = Locator(By.XPATH, xpath)
        locator2 = Locator(By.CLASS_NAME, xpath)
        assert locator1 != locator2
        assert not (locator1 == locator2)

    def test_locator_reference(self):
        """
        Tests that changes to a reference copy of Locator get reflected between two locator references
        :return:
        """
        xpath = "//div/foobar"
        locator1 = Locator(By.XPATH, xpath)
        locator2 = locator1
        assert locator1 == locator2

        # Change locator2 value
        locator2.value += "/test"
        assert locator1.by == By.XPATH
        assert locator1.value != xpath
        assert locator1.value == "{}/{}".format(xpath, "test")
        assert locator2.by == By.XPATH
        assert locator2.value == "{}/{}".format(xpath, "test")
        assert locator1 == locator2

    def test_locator_copy(self):
        """
        Tests that we can make a copy of the Locator object and make changes without affecting the other
        :return:
        """
        xpath = "//div/foobar"
        locator1 = Locator(By.XPATH, xpath)
        locator2 = locator1.copy()
        assert locator1 == locator2

        # Change locator2 value
        locator2.value += "/test"
        assert locator1.by == By.XPATH
        assert locator1.value == xpath
        assert locator2.by == By.XPATH
        assert locator2.value == "{}/{}".format(xpath, "test")
        assert locator1 != locator2

    def test_locator_append(self):
        """
        Tests that locator.append(str) successfully modifies the locator.value
        :return:
        """
        xpath = "//div/foobar"
        locator = Locator(By.XPATH, xpath)
        assert locator != None
        assert locator.by == By.XPATH
        assert locator.value == xpath
        locator.append("/helloworld")
        assert locator.value == "{}{}".format(xpath, "/helloworld")
