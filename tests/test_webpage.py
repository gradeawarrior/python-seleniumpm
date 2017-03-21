from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumpm.webpage import Webpage
from seleniumpm.examples.wikipedia import Wikipedia
from seleniumpm.examples.superwikipedia import SuperWikipedia
from seleniumpm.examples.google_page import GooglePage
from seleniumpm.webelements.button import Button
from seleniumpm.webelements.link import Link
from seleniumpm.webelements.textelement import TextElement
from seleniumpm.webelements.widget import Widget
from urlparse import urlparse
import tests.pages.testingwebpages as testingwebpages
from pytest import skip


class TestWebPage(object):
    driver = None

    @classmethod
    def setup_class(self):
        server = 'http://localhost:4444/wd/hub'
        capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        self.driver = webdriver.Remote(command_executor=server, desired_capabilities=capabilities)

    @classmethod
    def teardown_class(self):
        if self.driver:
            self.driver.quit()

    def test_create_webpage_with_string_http_url(self):
        url = "http://www.example.com"
        page = Webpage(self.driver, url=url)
        assert page != None
        assert page.url != None
        assert isinstance(page.url, tuple)
        assert page.url.scheme == "http"
        assert page.url.hostname == "www.example.com"

    def test_create_webpage_with_string_https_url(self):
        url = "https://www.example.com"
        page = Webpage(self.driver, url=url)
        assert page != None
        assert page.url != None
        assert isinstance(page.url, tuple)
        assert page.url.scheme == "https"
        assert page.url.hostname == "www.example.com"

    def test_create_webpage_with_parsed_http_url(self):
        url = urlparse("http://www.example.com")
        page = Webpage(self.driver, url=url)
        assert page != None
        assert page.url != None
        assert isinstance(page.url, tuple)
        assert page.url.scheme == "http"
        assert page.url.hostname == "www.example.com"

    def test_create_webpage_with_parsed_https_url(self):
        url = urlparse("https://www.example.com")
        page = Webpage(self.driver, url=url)
        assert page != None
        assert page.url != None
        assert isinstance(page.url, tuple)
        assert page.url.scheme == "https"
        assert page.url.hostname == "www.example.com"

    def test_create_webpage_with_invalid_urls(self):
        urls = ['foo', 'foobar.com', 'www.foobar.com', 'htps://www.foobar.com']
        for url in urls:
            try:
                Webpage(self.driver, url=url)
                assert False, "Expecting an AttributeError for the following invalid url: '{}'".format(url)
            except AttributeError:
                pass

    def test_webpage_with_no_defined_elements(self):
        elements = Webpage(self.driver).get_element_attr()
        assert len(elements) == 0

    def assert_elements(self, elements, expected_count):
        assert len(elements) == expected_count
        for element in elements:
            assert isinstance(element.driver, WebDriver)

    def test_webpage_with_multiple_elements(self):
        google = GooglePage(self.driver, "http://www.google.com")
        wikipedia = Wikipedia(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        elements = google.get_element_attr()
        self.assert_elements(elements, expected_count=1)
        elements = wikipedia.get_element_attr()
        self.assert_elements(elements, expected_count=4)
        elements = wikipedia.get_element_attr(type=Button)
        self.assert_elements(elements, expected_count=0)
        elements = wikipedia.get_element_attr(type=TextElement)
        self.assert_elements(elements, expected_count=3)

    def test_extended_webpage_with_multiple_elements(self):
        wikipedia = SuperWikipedia(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        elements = wikipedia.get_element_attr()
        self.assert_elements(elements, expected_count=10)
        elements = wikipedia.get_element_attr(type=Widget)
        self.assert_elements(elements, expected_count=1)
        elements = wikipedia.get_element_attr(type=Button)
        self.assert_elements(elements, expected_count=0)
        elements = wikipedia.get_element_attr(type=Link)
        self.assert_elements(elements, expected_count=5)
        elements = wikipedia.get_element_attr(type=TextElement)
        self.assert_elements(elements, expected_count=3)

    def test_validate_returns_self(self):
        page = testingwebpages.ZeroValidatedElementsPage(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        page = page.open().validate()
        assert page != None, "validate returns an object"
        assert isinstance(page, Webpage), "Ensure returned page is of type Webpage"
        assert isinstance(page, testingwebpages.ZeroValidatedElementsPage),\
            "Ensure returned page is of type ZeroValidatedElementPage"

    def test_wait_for_page_load_returns_self(self):
        page = testingwebpages.ZeroValidatedElementsPage(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        page = page.open().wait_for_page_load()
        assert page != None, "validate returns an object"
        assert isinstance(page, Webpage), "Ensure returned page is of type Webpage"
        assert isinstance(page, testingwebpages.ZeroValidatedElementsPage), \
            "Ensure returned page is of type ZeroValidatedElementPage"

    def test_zero_validated_webpage(self):
        page = testingwebpages.ZeroValidatedElementsPage(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        elements = page.get_element_attr()
        self.assert_elements(elements, expected_count=3)
        for element in elements:
            assert element.do_not_check == True
            assert element.check_visible == True
        # Since there all elements are marked as 'do not check', I expect these operations to succeed
        page.open().wait_for_page_load().validate()

    def test_hidden_elements_on_webpage(self):
        page = testingwebpages.HiddenElementsPage(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        elements = page.get_element_attr()
        self.assert_elements(elements, expected_count=3)
        for element in elements:
            assert element.do_not_check == False
            assert element.check_visible == False

        # TODO : This is simply testing testing that TimeoutException is happening on a non-existent element. The real
        # TODO : work is to actually define an element that is present but is not visible on a Webpage
        try:
            page.open().wait_for_page_load()
            assert False, "Expecting there to be a TimeoutException thrown"
        except TimeoutException:
            pass

    def test_marking_elements_as_do_not_check(self):
        page = testingwebpages.HiddenElementsPage(self.driver, "https://en.wikipedia.org/wiki/Selenium")
        elements = page.get_element_attr()
        # Manually mark all elements as 'do not check'
        for element in elements:
            element.mark_do_not_check()
            assert element.do_not_check == True
            assert element.check_visible == False
        page.open().wait_for_page_load().validate()

    @skip("Need to find a hidden element on a page to test this out on")
    def test_hidden_element_validation(self):
        pass
