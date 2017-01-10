from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Element(object):

    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator


    def is_displayed(self):
        return self.driver.find_element(self.locator.by, self.locator.value).is_displayed()

    def is_enabled(self):
        return self.driver.find_element(self.locator.by, self.locator.value).is_enabled()

    def is_selected(self):
        return self.driver.find_element(self.locator.by, self.locator.value).is_selected()

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
        try:
            self.is_present(timeout)
            self.is_visible(0)
            return True
        except:
            return False

    def wait_for_present(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((self.locator.by, self.locator.value)))
        return self

    def wait_for_visible(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((self.locator.by, self.locator.value)))
        pass

    def wait_for_present_and_visible(self, timeout=10):
        self.wait_for_present(timeout)
        self.wait_for_visible(0)
        return self
