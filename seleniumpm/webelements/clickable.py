from seleniumpm.webelements.element import take_screenshot_on_element_error
from seleniumpm.webelements.element import Element
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class Clickable(Element):
    def __init__(self, driver, locator):
        super(Clickable, self).__init__(driver, locator)

    @take_screenshot_on_element_error
    def wait_for_clickable(self, timeout=None):
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for clickable {}={} with timeout={}s ({})".format(self.locator.by,
                                                                                                    self.locator.value,
                                                                                                    timeout,
                                                                                                    self.__class__)
            e.msg = e.message
            raise e
        return self

    @take_screenshot_on_element_error
    def click(self, checkVisibility=False):
        """
        This is the standard selenium click() operation

        :param checkVisibility: [True|False] This allows you to check for visibility before the click - Default: False
        """
        if checkVisibility:
            self.is_present_and_visible()
        self.get_webelement().click()

    def click_index(self, index=0, fast_click=False):
        """
        Using get_webelements(), this clicks on the nth element in the list. If index=0, then this method
        should behave exactly like click()

        :param index: (Default: 0) The index to click()
        :param fast_click: (Default: False) This removes all checks on the number of WebElements in the list. Because
                            of this, this implementation has the potential of raising an IndexError
        :raises NoSuchElementException, IndexError
        """
        if fast_click:
            self.get_webelements()[index].click()
        else:
            elements = self.get_webelements()
            if index >= len(elements):
                raise NoSuchElementException("An element at index={} was not found. Number of elements: {}".format(
                    index, len(elements)))
            elements[index].click()

    @take_screenshot_on_element_error
    def click_invisible(self):
        """
        This bypasses Selenium's enforcement on only allowing clicks on visible objects
        """
        self.driver.execute_script("arguments[0].click();", self.get_webelement())
