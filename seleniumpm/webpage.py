from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import seleniumpm.config as seleniumconfig

from seleniumpm.iframe import IFrame
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.panel import Panel

from urlparse import urlparse
import re
import sys

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
            def __init__(self, driver, url=None):
                super(Google, self).__init__(driver, url)
                self.path = ""
                self.search_field = TextField(driver, Locator.by_name('q'))

    In the constructor, you do the following:

        1) Call the parent class's constructor
        2) You define 'path' attribute (default is "", so it didn't need to be specified in this example)
        3) You add a set of WebElements to your Webpage
    """

    def __init__(self, driver, url=None):
        if not isinstance(driver, WebDriver):
            raise AttributeError("driver was not an expected RemoteWebdriver type!")
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

    def refresh(self):
        """Does a page refresh
        """
        self.driver.refresh()

    def reload(self):
        """Does a page refresh
        """
        self.refresh()

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

    def get_current_url(self):
        """Returns the current page url
        """
        return self.driver.current_url

    @property
    def current_url(self):
        """Returns the current page url
        """
        return self.get_current_url()

    @property
    def page_timeout(self):
        return self.get_page_timeout()

    @property
    def element_timeout(self):
        return self.get_element_timeout()

    def get_page_timeout(self):
        return seleniumconfig.page_timeout_in_sec

    def get_element_timeout(self):
        return seleniumconfig.element_timeout_in_sec

    def wait_for_title(self, title, timeout=None):
        """This could be used similar to a wait_for_page_load() if the page title can uniquely identify
        different pages or states of the page. Google Search works like this.

        :param title: The title to search for (case sensitive)
        :param timeout: The number of seconds to wait - Default: 10s
        :raises TimeoutException: if the title does not appear within timeout period
        """
        timeout = timeout if timeout is not None else self.element_timeout
        WebDriverWait(driver=self.driver, timeout=timeout).until(EC.title_contains(title))
        return self

    def wait_for_page_load(self, timeout=None, force_check_visibility=False):
        """
        This method "waits for page load" by checking that all expected objects are both present and visible on the
        page. This is similar to validate() operation except that sometimes certain pages take a long time to load.
        Typically the threshold is 30sec, but this is configurable.

        :param timeout: (Default: 30s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :return: self if everything is successful
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        timeout = timeout if timeout is not None else self.page_timeout
        self.validate(timeout=timeout, force_check_visibility=force_check_visibility)
        return self

    def validate(self, timeout=None, force_check_visibility=False):
        """
        The intention of validate is to make sure that an already loaded webpage contains these elements.

        :param timeout: (Default: 10s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        timeout = timeout if timeout is not None else self.element_timeout
        for element in self.get_element_attr():
            # Continue if the element has marked itself do_not_check=True
            if element.do_not_check:
                continue
            # Check for presence and visibility
            if force_check_visibility or element.check_visible:
                # Print to stderr a WARNING message when force_check_visibility=True and element has been marked 'invisible'
                if force_check_visibility and not element.check_visible:
                    sys.stderr.write(
                        "[WARNING] element {}={} ({}) was marked as 'invisible' but force_check_visibility=True".format(
                            element.locator.by, element.locator.value, self.__class__))
                if isinstance(element, IFrame):
                    element.validate(timeout=timeout, force_check_visibility=force_check_visibility)
                else:
                    element.wait_for_present_and_visible(timeout)
            else:
                element.wait_for_present(timeout)
        return self

    def is_page(self, timeout=None, force_check_visibility=False):
        """
        This is like validate() operation except that it returns a boolean True/False. The idea is to
        ask whether or not you are on a page; this is an implementation of that idea. There are of course
        other ways of checking whether you are on the right page or not (e.g. checking the page title).

        :param timeout: (Default: 30s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :return: True if validate() does not throw an exception; False otherwise
        """
        timeout = timeout if timeout is not None else self.page_timeout
        try:
            self.validate(timeout=timeout, force_check_visibility=force_check_visibility)
            return True
        except:
            return False

    def get_element_attr(self, type=Element, override_check_visible=False, override_do_not_check=False,
                         expand_iframe_elements=False, result_type=list):
        """
        Retrieves a list of WebElements on a Webpage. Optionally, you can pass in a different type (e.g. Button,
        Link, TextElement) to return only those types associated with a Webpage object.

        :param type: one of the seleniumpm.webelement types (Default: seleniumpm.webelements.Element)
        :param override_check_visible: (Default: False) This overrides check for visibility. By default, widgets that are
                                        invisible, means that we assume its elements are also invisible
        :param override_do_not_check: (Default: False) This overrides check for do_not_check. By default, widgets that are
                                        marked as do_not_check, means that we assume its elements are not accessible
        :param expand_iframe_elements: (Default: False) Elements within an iFrame must be kept together in order to execute validate()
        :param result_type: (Default: list) This value can either be (list|dict). By default, we simply want a list of
                            available elements on the page. However, the dictionary version is implemented for the ability
                            to retrieve every element and sub-element on a Webpage directly from the page level
        :return: This is a list or dict of attributes of base type seleniumpm.webelements.Element
        """
        if result_type != list and result_type != dict:
            raise AttributeError(
                "result_type can either be 'list' (default) or 'dict', but was '{}'".format(result_type))
        elements = [] if result_type == list else {}
        temp_widgets = {}
        for attr in dir(self):
            element = getattr(self, attr)
            # Ensure that it is of type Element
            if isinstance(element, Element):
                # If it is a widget, then recursively drill down and get its Elements
                if isinstance(element, Widget):
                    # Check if widget is a type of iFrame and also check for visibility
                    if (element.check_visible or override_check_visible) and \
                            (not element.do_not_check or override_do_not_check) and \
                            not isinstance(element, IFrame) or \
                            ((isinstance(element, IFrame) and expand_iframe_elements)):
                        if result_type == dict:
                            temp_widgets[attr] = []
                            for key, value in element.get_element_attr(type=type,
                                                                       override_check_visible=override_check_visible,
                                                                       override_do_not_check=override_do_not_check,
                                                                       expand_iframe_elements=expand_iframe_elements,
                                                                       result_type=result_type,
                                                                       attr_name=attr).items():
                                temp_widgets[attr].append({'key': key, 'value': value})
                        else:
                            for welement in element.get_element_attr(type=type):
                                elements.append(welement)
                    # Add the widget but not its sub-elements if invisible
                    else:
                        if result_type == dict:
                            elements[attr] = element
                        else:
                            elements.append(element)
                # Add the element if it matches the expected type (not a Widget)
                if type not in (Widget, Panel, IFrame) and isinstance(element, type) and not isinstance(element,
                                                                                                        Widget):
                    if result_type == dict:
                        elements[attr] = element
                    else:
                        elements.append(element)

        # Give non-widgets priority, hence why there is a separate loop for widgets and their elements
        for attr, values in temp_widgets.items():
            for element in values:
                if element['key'] not in elements:
                    elements[element['key']] = element['value']
                else:
                    elements["{}_{}".format(attr, element['key'])] = element['value']

        # Ensure that there is only 1 iframe defined on page at this time
        count_iframes = 0
        # TODO - apparently list(elements.values()) is how this should be implemented if using Python 3
        list_elements = elements.values() if result_type == dict else elements
        for element in list_elements:
            if isinstance(element, IFrame) and not element.do_not_check:
                count_iframes += 1
            if count_iframes > 1 and not expand_iframe_elements:
                raise AttributeError(
                    "There was more than 1 IFrame found on this page. This is currently not supported. "
                    "If necessary, please mark at least 1 of them using 'mark_do_not_check()'")

        return elements

    def get_all_elements_on_page(self):
        """
        Retrieves all the webelements that have been defined on the page. This includes all sub-elements found on
        widgets, panels, and iframes.

        :return: A dict of all the elements
        """
        return self.get_element_attr(override_check_visible=True,
                                     override_do_not_check=True,
                                     expand_iframe_elements=True,
                                     result_type=dict)

    def __getattr__(self, name):
        """
        Overridden method so that we can also be able to directly access all webelements defined at lower level
        webelements (a.k.a. widgets, panels, and iframes)

        :param name: The name of the attribute or webelement that we expect to exist on the Webpage
        :return: The attribute value if found
        :raises AttributeError: If the attribute with given name doesn't exist
        """
        # Need to escape a potential infinite recursion for the following names
        if name in ('__members__', '__methods__'):
            return
        # Checking if the element is defined in the sub-widgets, panels, or iframes
        all_elements = self.get_all_elements_on_page()
        if name in all_elements:
            return all_elements[name]
        else:
            raise AttributeError(
                "'{}' webpage and its widgets has no attribute '{}'. The following are valid webelements on the page:\n  - {}".format(
                    self.__class__.__name__, name, "\n  - ".join(all_elements.keys())))
