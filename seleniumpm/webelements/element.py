from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from seleniumpm.locator import Locator


class Element(object):
    def __init__(self, driver, locator):
        if not isinstance(driver, WebDriver):
            raise AttributeError("driver was not an expected RemoteWebdriver type!")
        if not isinstance(locator, Locator):
            raise AttributeError("locator was not an expected seleniumpm.Locator type!")
        self.driver = driver
        self.locator = locator

    def get_webelement(self):
        return self.driver.find_element(self.locator.by, self.locator.value)

    def get_webelements(self):
        return self.driver.find_elements(self.locator.by, self.locator.value)

    def get_action_chains(self):
        return ActionChains(self.driver)

    def get_text(self):
        return self.get_webelement().text

    def get_attribute(self, name):
        self.get_webelement().get_attribute(name)

    def is_displayed(self):
        return self.get_webelement().is_displayed()

    def is_enabled(self):
        return self.get_webelement().is_enabled()

    def is_selected(self):
        return self.get_webelement().is_selected()

    def is_present(self, timeout=10):
        try:
            self.wait_for_present(timeout)
            return True
        except:
            return False

    def is_visible(self, timeout=10):
        try:
            self.wait_for_visible(timeout)
            return True
        except:
            return False

    def is_present_and_visible(self, timeout=10):
        return self.is_present(timeout) and self.is_visible(0)

    def set_focus(self):
        return self.scroll_into_view()

    def scroll_into_view(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.get_webelement())
        return self

    def move_to_element(self):
        return self.get_action_chains().move_to_element(self.get_webelement())

    def wait_for_present(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for present {}={} ({})".format(self.locator.by, self.locator.value, self.__class__)
            e.msg = e.message
            raise e
        return self

    def wait_for_visible(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for visibile {}={} ({})".format(self.locator.by, self.locator.value, self.__class__)
            e.msg = e.message
            raise e
        return self

    def wait_for_present_and_visible(self, timeout=10):
        self.wait_for_present(timeout)
        self.wait_for_visible(0)
        return self

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
