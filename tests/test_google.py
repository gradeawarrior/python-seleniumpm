from selenium import webdriver

from seleniumpm.examples.google_page import GooglePage
from seleniumpm.examples.wikipedia import Wikipedia

import random


class TestGoogle():
    """
    These are proof-of-concept Selenium programs that leverage the Selenium PageModel library. All these programs
    are based around performing searches on Google.
    """

    server = 'http://localhost:4444/wd/hub'
    google_url = 'https://www.google.com'
    wikipedia_url = 'https://en.wikipedia.org/wiki/Selenium'
    capabilities = None
    driver = None
    google = None
    wikipedia = None

    def setup_class(self):

        # Capability for Firefox
        # self.capabilities = webdriver.DesiredCapabilities.FIREFOX
        # self.capabilities['marionette'] = True

        # Capability for HtmlUnit
        # TODO : There is a potential issue reported with HTMLUnit. See this bug as of January 2017 - https://sourceforge.net/p/htmlunit/bugs/1846/
        # self.capabilities = webdriver.DesiredCapabilities.HTMLUNIT
        # self.capabilities = webdriver.DesiredCapabilities.HTMLUNITWITHJS
        # self.capabilities['driverName'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0"

        # Capability for PhantomJS
        self.capabilities = webdriver.DesiredCapabilities.PHANTOMJS

        try:
            self.driver = webdriver.Remote(command_executor=self.server, desired_capabilities=self.capabilities)
            self.google = GooglePage(self.driver, url=self.google_url)
            self.wikipedia = Wikipedia(self.driver, url=self.wikipedia_url)
        except:
            if self.driver:
                self.driver.quit()

    @classmethod
    def teardown_class(self):
        if self.driver:
            self.driver.quit()

    def test_search(self):
        """This is the traditional 'HelloWorld' program you see in Selenium documentation, but implemented
        Using the Selenium PageModel library"""

        search_term = 'Cheese!'

        # And now use this to visit Google
        self.google.open().wait_for_page_load().validate()

        # Check the title of the page
        title = self.google.get_title()
        print "Page title is: {}".format(title)
        # Should see: "cheese! - Google Search"

        # Enter something to search for
        self.google.search_field.clear().type(search_term)

        # Now submit the form. WebDriver will find the form for us from the element
        self.google.search_field.submit()

        # Check the title of the page
        title = self.google.wait_for_title(search_term).get_title()
        print "Page title is: {}".format(title)
        assert search_term in title, "Expected '{}' in '{}'".format(search_term, title)
        self.google.validate()

    def test_get_result_links(self):
        """This simply verifies that we are able to grab the links from a google search
        """
        search_term = "Selenium"
        self.google.open().wait_for_page_load().validate()
        self.google.search_field.clear().type(search_term)
        self.google.search_field.submit()
        self.google.wait_for_title(search_term)
        links = self.google.get_result_links()
        assert len(links) > 5
        print "found {} links".format(len(links))
        for link in links:
            print "- '{}'".format(link.get_attribute("href"))
            # print "- '{}'".format(link.text)

    def test_search_for_10_words_from_wikipedia(self):
        """
        This test does the following:

        1) Go to Wikipedia and grab 10 random words
        2) For each word, go to google and grab the top-5 links
        """
        self.wikipedia.open().wait_for_page_load().validate()
        wikipedia_text = self.wikipedia.get_text()
        assert wikipedia_text
        word_list = wikipedia_text.split()
        random_words = []
        # Get a list of 10 random words
        while len(random_words) < 5:
            randInt = random.randint(0, len(word_list) - 1)
            word = word_list[randInt].lower()
            # Basic check to ensure that word is not already in the list
            if word in random_words:
                next
            random_words.append(word)
        # Go to Google and perform search on each word
        for search_term in random_words:
            self.google.open().wait_for_page_load().validate()
            self.google.search_field.clear().type(search_term)
            self.google.search_field.submit()
            self.google.wait_for_title(search_term)
            # Grab the first 5 urls
            links = self.google.get_result_links()
            assert len(links) >= 5
            for i, link in enumerate(links[0:5]):
                print "[{}] '{}' - {}".format(i, search_term, link.get_attribute("href"))
