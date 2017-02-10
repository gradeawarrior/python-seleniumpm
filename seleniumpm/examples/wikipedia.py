from seleniumpm.locator import Locator
from seleniumpm.webpage import Webpage
from seleniumpm.webelements.textelement import TextElement
from selenium.webdriver.common.by import By

class Wikipedia(Webpage):
    """
    This is a basic Wikipedia page. For the constructor, the URL path will be used as the Webpage path
    """

    def __init__(self, driver, url):
        super(Wikipedia, self).__init__(driver, url)
        self.path = self.url.path
        self.headingText = TextElement(driver, Locator(By.ID, "firstHeading"))
        self.bodyText = TextElement(driver, Locator(By.ID, "bodyContent"))
        self.bodyTexts = TextElement(driver, Locator(By.XPATH, "//div[@id='bodyContent']/div/p"))

    def get_text(self):
        """Retrieves all the words in the body
        """
        txt = ""
        paragraphs = self.bodyTexts.get_webelements()
        for paragraph in paragraphs:
            txt += " {}".format(paragraph.text.encode('ascii', 'ignore'))
        return txt

    def wait_for_page_load(self, timeout=30):
        self.headingText.wait_for_present_and_visible(timeout=timeout)
        self.bodyText.wait_for_present_and_visible(timeout=timeout)
        return self

    def validate(self):
        self.headingText.wait_for_present_and_visible()
        self.bodyText.wait_for_present_and_visible()
