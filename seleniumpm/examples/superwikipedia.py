from seleniumpm.examples.wikipedia import Wikipedia
from seleniumpm.examples.widgets.WikipediaPersonal import WikipediaPersonal
from seleniumpm.webelements.link import Link
from seleniumpm.locator import Locator
from selenium.webdriver.common.by import By


class SuperWikipedia(Wikipedia):
    """
    This is simply an example of how you could extend Webpage classes. One use-case of this could be that your
    website has a HomepageUnauthenticated and a HomepageAuthenticated; in essence, you could implement
    2 classes that represent the base Homepage class in (1) an authenticated state, and (2) an unauthenticated
    state.
    """

    def __init__(self, driver, url):
        super(SuperWikipedia, self).__init__(driver, url)
        self.mainpage_link = Link(driver, Locator(By.XPATH, "//li[@id='n-mainpage-description']/a"))
        self.personal_widget = WikipediaPersonal(driver, Locator(By.XPATH, "//div[@id='p-personal']"))
