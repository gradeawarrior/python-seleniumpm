from seleniumpm.webelements.button import Button
from seleniumpm.locator import Locator
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestButton(object):

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

    def test_instantiate_button(self):
        xpath = "//foo"
        button = Button(self.driver, Locator(By.XPATH, xpath))
        assert button != None

    def test_two_buttons_are_equal(self):
        xpath = "//foo"
        button1 = Button(self.driver, Locator(By.XPATH, xpath))
        button2 = Button(self.driver, Locator(By.XPATH, xpath))
        assert button1 == button2
        assert not (button1 != button2)

    def test_two_buttons_are_not_equal_by_by(self):
        xpath = "//foo"
        button1 = Button(self.driver, Locator(By.XPATH, xpath))
        button2 = Button(self.driver, Locator(By.CLASS_NAME, xpath))
        assert button1 != button2
        assert not (button1 == button2)

    def test_two_buttons_are_not_equal_by_value(self):
        xpath = "//foo"
        xpath2 = "//foo/bar"
        button1 = Button(self.driver, Locator(By.XPATH, xpath))
        button2 = Button(self.driver, Locator(By.XPATH, xpath2))
        assert button1 != button2
        assert not (button1 == button2)
