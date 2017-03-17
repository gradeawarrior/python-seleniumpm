from seleniumpm.webelements.element import Element
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Clickable(Element):
    def __init__(self, driver, locator):
        super(Clickable, self).__init__(driver, locator)

    def wait_for_clickable(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for clickable {}={} with timeout={}s ({})".format(self.locator.by, self.locator.value, timeout, self.__class__)
            e.msg = e.message
            raise e
        return self


    def click(self, checkVisibility=False):
        """
        This is the standard selenium click() operation

        :param checkVisibility: [True|False] This allows you to check for visibility before the click - Default: False
        """
        if checkVisibility:
            self.is_present_and_visible()
        self.get_webelement().click()

    def click_invisible(self):
        """
        This bypasses Selenium's enforcement on only allowing clicks on visible objects

        :return: self
        """
        self.driver.execute_script("arguments[0].click();", self.get_webelement())
