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
        xpath = "//table"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        assert table != None

    def test_two_table_are_equal(self):
        xpath = "//table"
        table1 = Table(self.driver, Locator(By.XPATH, xpath))
        table2 = Table(self.driver, Locator(By.XPATH, xpath))
        assert table1 == table2
        assert not (table1 != table2)

    def test_two_table_are_not_equal_by_value(self):
        xpath = "//table"
        xpath2 = "//table/bar"
        table1 = Table(self.driver, Locator(By.XPATH, xpath))
        table2 = Table(self.driver, Locator(By.XPATH, xpath2))
        assert table1 != table2
        assert not (table1 == table2)

    def test_get_locator(self):
        xpath = "//table"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        # Get 2nd row 4th column
        assert table.get_locator(1, 3) == Locator(By.XPATH, "{}{}".format(xpath, "/tbody/tr[1]/td[3]"))
        # Get 1st row 2nd column
        assert table.get_locator(0, 1) == Locator(By.XPATH, "{}{}".format(xpath, "/tbody/tr[0]/td[1]"))
        # Get 30th row 5th column
        assert table.get_locator(29, 4) == Locator(By.XPATH, "{}{}".format(xpath, "/tbody/tr[29]/td[4]"))


    def test_get_rows(self):
        xpath = "//table"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        rows = table.get_rows()
        assert isinstance(rows, list)
        assert len(rows) == 0

    def test_count_rows(self):
        xpath = "//table"
        table = Table(self.driver, Locator(By.XPATH, xpath))
        count = table.count_rows()
        assert count == 0

    def test_error_if_specify_table_with_non_xpath_locator(self):
        xpath = "//table"
        try:
            Table(self.driver, Locator(By.CLASS_NAME, xpath))
            assert False, "Expected there to be an AttributeError"
        except AttributeError:
            pass
