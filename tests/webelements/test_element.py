from seleniumpm.webelements.element import Element
from seleniumpm.locator import Locator
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestElement(object):

    driver = None

    @classmethod
    def setup_class(self):
        server = 'http://localhost:4444/wd/hub'
        capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        self.driver = webdriver.Remote(command_executor=server, desired_capabilities=capabilities)

    @classmethod
    def teardown_class(self):
        if self.driver:
            self.driver.quit()

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
