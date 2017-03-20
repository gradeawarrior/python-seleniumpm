from selenium.webdriver.common.by import By
from seleniumpm.webpage import Webpage
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.textfield import TextField
from seleniumpm.locator import Locator


class GooglePage(Webpage):
    """
    This is an Google page that extends SeleniumPM WebPage. This class acts as a container for the different
    WebElements on the page that an engineer may want to interact with.
    """

    def __init__(self, driver, url=None):
        super(GooglePage, self).__init__(driver, url)
        self.search_field = TextField(driver, Locator.by_name('q'))

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
