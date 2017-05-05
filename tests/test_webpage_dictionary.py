import logging
from tests.uitestwrapper import UiTestWrapper
from seleniumpm.examples.google_page import GooglePage
from seleniumpm.examples.wikipedia import Wikipedia
from seleniumpm.examples.superwikipedia import SuperWikipedia

logging.basicConfig()
log = logging.getLogger(__name__)

class TestWebpageDictionary(UiTestWrapper):
    ##
    # TODO - These are not actually tests!
    #
    def test_google_webpage(self):
        page = GooglePage(self.driver, url="https://www.google.com/")
        log.debug("\n{}".format(page.to_json_pp()))
        log.debug(page)
        log.debug(page.to_json(simple=True))

    def test_wikipedia_webpage(self):
        page = Wikipedia(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        log.debug("\n{}".format(page.to_json_pp()))
        log.debug(page)
        log.debug(page.to_json(simple=True))

    def test_superwikipedia_webpage(self):
        page = SuperWikipedia(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        log.debug("\n{}".format(page.to_json_pp()))
        log.debug(page)
        log.debug(page.to_json(simple=True))
