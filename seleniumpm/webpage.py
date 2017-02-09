from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urlparse import urlparse
import re

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Webpage(object):
    """
    The Webpage class is intended to be the parent class for all Webpages. In principle, a Webpage is simply a
    construct that allows us to organize a set of WebElements on any given page; therefore, this class and other
    Selenium PageModel entities follows this paradigm.

    The first step to do is to write your own class that extends Webpage:

        class Google(Webpage):
            def __init__(self, driver, locator):
                super(Google, self).__init__(driver, locator)
                self.path = ""
                self.search_field = TextField(driver, Locator(By.NAME, 'q'))

            def wait_for_page_load(self, timeout=30):
                self.search_field.wait_for_present_and_visible(timeout=timeout)
                return self

            def validate(self, timeout=10):
                self.search_field.wait_for_present_and_visible(timeout=timeout)

    In the constructor, you do the following:

        1) Call the parent class's constructor
        2) You define 'path' attribute (default is "", so it didn't need to be specified in this example)
        3) You add a set of WebElements to your Webpage

    There are two additional methods that you should override from the parent:

        1) wait_for_page_load() - This is used for defining a set of WebElements that can be checked to determine if the
                                  Webpage was successfully loaded
        2) validate() - This is used for quick validation of a set of WebElements on a page (e.g.
                        registration_page.validate())
    """

    def __init__(self, driver, url=None):
        self.driver = driver
        self.path = ""
        # Check if a valid url
        if url and not url_regex.search(url.geturl() if isinstance(url, tuple) else url):
            raise AttributeError("Invalid url: '{}'".format(url))
        # Check if  url is None or has already been parsed
        if url == None or isinstance(url, tuple):
            self.url = url
        # Check if url is defined but has not been parsed
        elif url and not isinstance(url, tuple):
            self.url = urlparse(url)

    def open(self, url=None):
        """
        This method has two forms of operation:

        1) It will open whatever url that is passed into method
        2) It will use the url specified when the WebPage object was specified (Recommended)

        The latter method is the recommended approach.
        :param url: The url to open, but it is recommended that this be specified in constructor - Default: None
        :return:
        """
        if url:
            self.driver.get(url)
        elif self.url:
            url = "{}://{}:{}{}".format(
                self.url.scheme,
                self.url.hostname,
                self.url.port if self.url.port else (80 if self.url.scheme == "http" else 443),
                self.path)
            self.driver.get(url)
        else:
            raise AttributeError("Url is not defined!")
        return self

    def close(self):
        """Closes the browser
        """
        self.driver.close()

    def quit(self):
        """Quits the Selenium session
        """
        self.driver.quit()

    def get_title(self):
        """Returns the title of the WebPage
        """
        return self.driver.title

    def wait_for_title(self, title, timeout=10):
        """This could be used similar to a wait_for_page_load() if the page title can uniquely identify
        different pages or states of the page. Google Search works like this.
        :param title: The title to search for (case sensitive)
        :param timeout: The number of seconds to wait - Default: 10
        :raises TimeoutException: if the title does not appear within timeout period
        """
        WebDriverWait(driver=self.driver, timeout=timeout).until(EC.title_contains(title))
        return self

    def wait_for_page_load(self):
        """
        This method "waits for page load" by checking that all expected objects are both present and visible on the
        page. This is similar to validate() operation except that sometimes certain pages take a long time to load.
        Typically the threshold is 30sec, but this is configurable.
        :return: self if everything is successful
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        raise NotImplementedError

    def validate(self):
        """
        The intention of validate is to make sure that an already loaded webpage contains these elements.
        :return:
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        raise NotImplementedError
