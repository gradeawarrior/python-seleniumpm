from selenium import webdriver
from seleniumpm.webpage import Webpage
from urlparse import urlparse


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
