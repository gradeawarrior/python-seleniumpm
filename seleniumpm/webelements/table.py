import re
from selenium.webdriver.common.by import By
from seleniumpm.webelements.element import Element
from seleniumpm.locator import Locator


class Table(Element):
    """
    Searching and enumerating over a Table rows and columns can be complicated. This class aims at simplifying common
    tasks that can be extended to fit your application.
    """

    def __init__(self, driver, locator):
        if locator.by != By.XPATH:
            raise AttributeError("Tables only support XPATH locators")
        super(Table, self).__init__(driver, locator)

    def get_row_index(self, column_index, pattern, regex_flag=0):
        """
        Retrieves the row_index that a given 'pattern' is found. The use case is: I want to find which row that contains
        ID '12345'.
        :param column_index: The column number (starting at 0) that you want to search
        :param pattern: The pattern you want to search (e.g. "Foobar")
        :param regex_flag: These are the re flags (e.g. re.IGNORECASE) - Default: 0
        :return: The row index that contains the pattern, otherwise returns -1 if not found
        """
        elements = self.driver.find_elements(By.XPATH, "{}{}".format(
            self.locator.value, "/tbody/tr/td[{}]".format(column_index)))
        row_index = 0
        for field in elements:
            if re.search(pattern=pattern, string=field.get_text(), flags=regex_flag):
                return row_index
            row_index += 1
        return -1

    def get_column_names(self):
        """
        Retrieves a list of column names. The column name indexes will correspond to the column_index for the value on
        every row.

        NOTE: The column names assume that the table specified them under '//thead/tr/th'. If your table was not defined
        in this manner, then this operation will return an empty list
        :return:
        """
        elements = self.driver.find_elements(By.XPATH, "{}{}".format(self.locator.value, "/thead/tr/th"))
        column_names = []
        for header in elements:
            column_names.append(header.get_text())
        return column_names

    def get_element(self, row_index, column_index):
        """
        Returns a WebDriver Element reference to the specified row + column
        :param row_index: The row number (starting at 0)
        :param column_index: The column number (starting at 0)
        :return:
        :raises NoSuchElementError: if the element doesn't exist
        """
        return self.driver.find_element(By.XPATH, "{}{}".format(
            self.locator.value, "/tbody/tr[{}]/td[{}]".format(row_index, column_index)))

    def get_locator(self, row_index, column_index):
        """
        Returns a Locator object to the specified row + column
        :param row_index: The row number (starting at 0)
        :param column_index: The column number (starting at 0)
        :return:
        """
        return Locator(By.XPATH, "{}{}".format(
            self.locator.value, "/tbody/tr[{}]/td[{}]".format(row_index, column_index)))

    def get_rows(self):
        """
        Returns a list of WebDriver Elements for each row in the table
        :return:
        """
        return self.driver.find_elements(By.XPATH, "{}{}".format(self.locator.value, "/tbody/tr"))

    def count_rows(self):
        """
        Returns a count of the number of rows in the table
        :return:
        """
        return len(self.get_rows())
