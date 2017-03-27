from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumpm.locator import Locator
from seleniumpm.webpage import Webpage
from seleniumpm.examples.wikipedia import Wikipedia
from seleniumpm.examples.superwikipedia import SuperWikipedia
from seleniumpm.examples.google_page import GooglePage
from seleniumpm.webelements.button import Button
from seleniumpm.webelements.link import Link
from seleniumpm.webelements.textelement import TextElement
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.panel import Panel
from seleniumpm.iframe import IFrame
from urlparse import urlparse
import tests.pages.testingwebpages as testingwebpages
import pytest


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
        assert isinstance(page, testingwebpages.ZeroValidatedElementsPage), \
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
            page.open().wait_for_page_load(timeout=0)
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

    @pytest.mark.skip("Need to find a hidden element on a page to test this out on")
    def test_hidden_element_validation(self):
        pass

    @staticmethod
    def calculate_meta(elements):
        initial = {'total': 0,
                   'visible': 0,
                   'invisible': 0,
                   'do-not-check': 0,
                   'types': {'iframe': 0,
                             'panel': 0,
                             'widget': 0,
                             'element': 0}}
        for element in elements:
            initial['total'] += 1
            if element.do_not_check:
                initial['do-not-check'] += 1
            elif element.check_visible:
                initial['visible'] += 1
            else:
                initial['invisible'] += 1
            if isinstance(element, IFrame):
                initial['types']['iframe'] += 1
            elif isinstance(element, Panel):
                initial['types']['panel'] += 1
            elif isinstance(element, Widget):
                initial['types']['widget'] += 1
            elif isinstance(element, Element):
                initial['types']['element'] += 1
        return initial

    def test_complex_page(self):
        page = testingwebpages.MyComplexPage(self.driver)
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 3, "Expecting there to be 3 elements in this test complex page"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['visible'] == 1, "Expecting there to be 1 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_page_with_widget(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page.visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 7, "Expecting there to be 7 elements in this test complex page"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['visible'] == 3, "Expecting there to be 3 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_page_with_invisible_widget(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page.visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget")).mark_invisible()
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 4, "Expecting there to be 4 elements in this test complex page"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['visible'] == 1, "Expecting there to be 1 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_page_with_do_not_check_widget(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page.visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget")).mark_do_not_check()
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 4, "Expecting there to be 4 elements in this test complex page"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['visible'] == 1, "Expecting there to be 1 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_page_with_widget_panel(self):
        page = testingwebpages.MyComplexPage(self.driver)
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.visible_panel = testingwebpages.MyComplexPanel(self.driver, Locator.by_xpath("//panel"))
        page.visible_widget = visible_widget
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 11, "Expecting there to be 11 elements in this test complex page"
        assert meta_data['types']['element'] == 9, "Expecting there to be 9 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['types']['panel'] == 1, "Expecting there to be 1 Panel types"
        assert meta_data['visible'] == 5, "Expecting there to be 5 visible"
        assert meta_data['invisible'] == 3, "Expecting there to be 3 invisible"
        assert meta_data['do-not-check'] == 3, "Expecting there to be 3 do-not-check"

    def test_complex_page_with_widget_hidden_panel(self):
        page = testingwebpages.MyComplexPage(self.driver)
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.invisible_panel = testingwebpages.MyComplexPanel(self.driver, Locator.by_xpath("//panel")).mark_invisible()
        page.visible_widget = visible_widget
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 8, "Expecting there to be 8 elements in this test complex page"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['types']['panel'] == 1, "Expecting there to be 1 Panel types"
        assert meta_data['visible'] == 3, "Expecting there to be 3 visible"
        assert meta_data['invisible'] == 3, "Expecting there to be 3 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_page_with_widget_do_not_check_panel(self):
        page = testingwebpages.MyComplexPage(self.driver)
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.do_not_check_panel = testingwebpages.MyComplexPanel(self.driver, Locator.by_xpath("//panel")).mark_do_not_check()
        page.visible_widget = visible_widget
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 8, "Expecting there to be 8 elements in this test complex page"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['types']['panel'] == 1, "Expecting there to be 1 Panel types"
        assert meta_data['visible'] == 3, "Expecting there to be 3 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 3, "Expecting there to be 3 do-not-check"

    def test_complex_page_with_iframe(self):
        page = testingwebpages.MyComplexPage(self.driver)
        page.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 4, "Expecting there to be 4 elements in this test complex page"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['types']['iframe'] == 1, "Expecting there to be 1 IFrame types"
        assert meta_data['visible'] == 2, "Expecting there to be 2 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_page_with_widget_iframe(self):
        page = testingwebpages.MyComplexPage(self.driver)
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        page.visible_widget = visible_widget
        elements = page.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 8, "Expecting there to be 8 elements in this test complex page"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['types']['iframe'] == 1, "Expecting there to be 1 IFrame types"
        assert meta_data['visible'] == 4, "Expecting there to be 4 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_page_with_multiple_iframes(self):
        page = testingwebpages.MyComplexPage(self.driver)
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe1"))
        page.visible_widget = visible_widget
        page.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe2"))
        try:
            page.get_element_attr()
            assert False, "Expecting to throw an AttributeError because 2 iframes were defined on a page"
        except AttributeError:
            pass

