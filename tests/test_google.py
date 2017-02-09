from selenium import webdriver

from seleniumpm.examples.google_page import GooglePage


class TestGoogle():
    server = 'http://localhost:4444/wd/hub'
    google_url = 'https://www.google.com'
    capabilities = None
    browser = None
    google_page = None

    def setup_class(self):

        # # Capability for Firefox
        # self.capabilities = webdriver.DesiredCapabilities.FIREFOX
        # self.capabilities['marionette'] = True

        # Capability for HtmlUnit
        # TODO : There is a potential issue reported with HTMLUnit. See this bug as of January 2017 - https://sourceforge.net/p/htmlunit/bugs/1846/
        # self.capabilities = webdriver.DesiredCapabilities.HTMLUNIT
        # self.capabilities = webdriver.DesiredCapabilities.HTMLUNITWITHJS
        # self.capabilities['browserName'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0"

        # Capability for PhantomJS
        self.capabilities = webdriver.DesiredCapabilities.PHANTOMJS

        try:
            self.browser = webdriver.Remote(command_executor=self.server, desired_capabilities=self.capabilities)
            self.google_page = GooglePage(self.browser, url=self.google_url)
        except:
            if self.browser:
                self.browser.quit()

    @classmethod
    def teardown_class(self):
        if self.browser:
            self.browser.quit()

    def test_search(self):

        search_term = 'Cheese!'

        # And now use this to visit Google
        self.google_page.open().wait_for_page_load().validate()

        # Check the title of the page
        title = self.google_page.get_title()
        print "Page title is: {}".format(title)
        # Should see: "cheese! - Google Search"

        # Enter something to search for
        self.google_page.search_field.type(search_term)

        # Now submit the form. WebDriver will find the form for us from the element
        self.google_page.search_field.submit()

        # Check the title of the page
        title = self.google_page.wait_for_title(search_term).get_title()
        print "Page title is: {}".format(title)
        assert search_term in title, "Expected '{}' in '{}'".format(search_term, title)
        self.google_page.validate()
