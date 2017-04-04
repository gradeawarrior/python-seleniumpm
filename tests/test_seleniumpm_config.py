from selenium import webdriver
from seleniumpm.locator import Locator
from seleniumpm.webpage import Webpage
from seleniumpm.webelements.element import Element
import seleniumpm.config as seleniumconfig

class TestSeleniumpmConfig(object):
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

    def test_element_defaults(self):
        seleniumconfig.reset_timeouts()
        element = Element(self.driver, Locator.by_xpath("//foo"))
        assert element.page_timeout == 30, "Expecting page_timeout=30"
        assert element.element_timeout == 10, "Expecting element_timeout=10"

    def test_element_non_page_timeout_default(self):
        seleniumconfig.reset_timeouts()
        seleniumconfig.page_timeout_in_sec = 15
        element = Element(self.driver, Locator.by_xpath("//foo"))
        assert element.page_timeout == 15, "Expecting page_timeout=15"
        assert element.element_timeout == 10, "Expecting element_timeout=10"

    def test_element_non_element_timeout_default(self):
        seleniumconfig.reset_timeouts()
        seleniumconfig.element_timeout_in_sec = 20
        element = Element(self.driver, Locator.by_xpath("//foo"))
        assert element.page_timeout == 30, "Expecting page_timeout=30"
        assert element.element_timeout == 20, "Expecting element_timeout=20"

    def test_element_change_defaults_and_then_reset(self):
        seleniumconfig.reset_timeouts()
        seleniumconfig.page_timeout_in_sec = 5
        seleniumconfig.element_timeout_in_sec = 25
        element = Element(self.driver, Locator.by_xpath("//foo"))
        assert element.page_timeout == 5, "Expecting page_timeout=5"
        assert element.element_timeout == 25, "Expecting element_timeout=25"
        seleniumconfig.reset_timeouts()
        assert element.page_timeout == 30, "Expecting page_timeout=30"
        assert element.element_timeout == 10, "Expecting element_timeout=10"

    def test_page_defaults(self):
        seleniumconfig.reset_timeouts()
        page = Webpage(self.driver)
        assert page.page_timeout == 30, "Expecting page_timeout=30"
        assert page.element_timeout == 10, "Expecting element_timeout=10"

    def test_page_non_page_timeout_default(self):
        seleniumconfig.reset_timeouts()
        seleniumconfig.page_timeout_in_sec = 15
        page = Webpage(self.driver)
        assert page.page_timeout == 15, "Expecting page_timeout=15"
        assert page.element_timeout == 10, "Expecting element_timeout=10"

    def test_page_non_element_timeout_default(self):
        seleniumconfig.reset_timeouts()
        seleniumconfig.element_timeout_in_sec = 20
        page = Webpage(self.driver)
        assert page.page_timeout == 30, "Expecting page_timeout=30"
        assert page.element_timeout == 20, "Expecting element_timeout=20"

    def test_page_change_defaults_and_then_reset(self):
        seleniumconfig.reset_timeouts()
        seleniumconfig.page_timeout_in_sec = 5
        seleniumconfig.element_timeout_in_sec = 25
        page = Webpage(self.driver)
        assert page.page_timeout == 5, "Expecting page_timeout=5"
        assert page.element_timeout == 25, "Expecting element_timeout=25"
        seleniumconfig.reset_timeouts()
        assert page.page_timeout == 30, "Expecting page_timeout=30"
        assert page.element_timeout == 10, "Expecting element_timeout=10"
