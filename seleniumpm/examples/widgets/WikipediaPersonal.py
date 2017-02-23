from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.link import Link
from seleniumpm.locator import Locator
from selenium.webdriver.common.by import By

class WikipediaPersonal(Widget):
    """
    This is an example way of sub-organizing elements on a page. In this examp,e, we're grouping a set of
    links located near the top-right of the Wikipedia page.
    """

    def __init__(self, driver, locator):
        super(WikipediaPersonal, self).__init__(driver, locator)
        self.talk_link = Link(driver, Locator(By.XPATH, "//li[@id='pt-anontalk']/a"))
        self.contributions_link = Link(driver, Locator(By.XPATH, "//li[@id='pt-anoncontribs']/a"))
        self.createaccount_link = Link(driver, Locator(By.XPATH, "//li[@id='pt-createaccount']/a"))
        self.login_link = Link(driver, Locator(By.XPATH, "//li[@id='pt-login']/a"))
