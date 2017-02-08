from seleniumpm.webpage import Webpage
from seleniumpm.webelements.textfield import TextField
from seleniumpm.locator import Locator
from selenium.webdriver.common.by import By

class GooglePage(Webpage):

    def __init__(self, driver, url=None):
        super(GooglePage, self).__init__(driver, url)
        self.search_field = TextField(driver, Locator(By.NAME, 'q'))

    def validate(self):
        self.search_field.wait_for_present_and_visible()
