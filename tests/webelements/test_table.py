from seleniumpm.webelements.table import Table
from seleniumpm.locator import Locator
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTable(object):
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

    def test_instantiate_table(self):
        xpath = "//foo"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        assert table != None

    def test_two_table_are_equal(self):
        xpath = "//foo"
        table1 = Table(self.driver, Locator(By.XPATH, xpath))
        table2 = Table(self.driver, Locator(By.XPATH, xpath))
        assert table1 == table2
        assert not (table1 != table2)

    def test_two_table_are_not_equal_by_value(self):
        xpath = "//foo"
        xpath2 = "//foo/bar"
        table1 = Table(self.driver, Locator(By.XPATH, xpath))
        table2 = Table(self.driver, Locator(By.XPATH, xpath2))
        assert table1 != table2
        assert not (table1 == table2)


    def test_get_rows_with_xpath_locator(self):
        xpath = "//foo"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        rows = table.get_rows()
        assert len(rows) == 0

    def test_error_if_specify_table_with_non_xpath_locator(self):
        xpath = "//foo"
        try:
            Table(self.driver, Locator(By.CLASS_NAME, xpath))
            assert False, "Expected there to be an AttributeError"
        except AttributeError:
            pass

    def test_count_rows_with_xpath_locator(self):
        xpath = "//foo"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        count = table.count_rows()
        assert count == 0
