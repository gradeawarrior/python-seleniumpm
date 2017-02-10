from seleniumpm.webpage import Webpage
from seleniumpm.webelements.textfield import TextField
from seleniumpm.locator import Locator
from selenium.webdriver.common.by import By

class GooglePage(Webpage):
    """
    This is an Google page that extends SeleniumPM WebPage. This class acts as a container for the different
    WebElements on the page that an engineer may want to interact with.
    """

    def __init__(self, driver, url=None):
        super(GooglePage, self).__init__(driver, url)
        self.path = ""
        self.search_field = TextField(driver, Locator(By.NAME, 'q'))

    def get_result_links(self):
        """
        Returns a list of links from a Google search.
        :return: Returns a list of links from a Google search.
        """
        links = []
        elements = self.driver.find_elements(By.XPATH, "//h3[contains(@class, 'r')]/a")
        for element in elements:
            links.append(element.get_attribute("href"))
        return links

    def wait_for_page_load(self, timeout=30):
        """
        This is an overridden method to support checks for successful page load.
        :return: self if everything is successful
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        self.search_field.wait_for_present_and_visible(timeout=timeout)
        return self

    def validate(self, timeout=10):
        """
        This is an overridden method to support validation of a Google page
        :return:
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        self.search_field.wait_for_present_and_visible(timeout=timeout)
