from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import seleniumpm.config as seleniumconfig

from seleniumpm.iframe import IFrame
from seleniumpm.locator import Locator
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.panel import Panel

from functools import wraps
from urlparse import urlparse
import base64
import inspect
import json
import logging
import os
import re
import sys
import time
import types

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def take_screenshot_on_webpage_error(func):
    """
    This is an annotation for automatic screenshot ability for Webpage functions. It leverages
    "higher-order" operations available through functools library; and as the function implies,
    allows for automatic taking of a screenshot when there is an error/exception thrown.
    """

    @wraps(func)
    def newFunc(*args, **kwargs):
        try:
            # Disable Screenshot
            current_screenshot_enabled = seleniumconfig.screenshot_enabled
            if current_screenshot_enabled:
                seleniumconfig.screenshot_enabled = False
            try:
                func_response = func(*args, **kwargs)
            finally:
                # Reset screenshot
                seleniumconfig.screenshot_enabled = current_screenshot_enabled
        except Exception as e:
            if seleniumconfig.screenshot_enabled:
                funcObj = args[0]
                filename = "page_error_%s_%s" % (func.func_name, time.strftime('%Y_%m_%d-%H_%M_%S'))
                page = Webpage(funcObj.driver)
                page.take_screenshot(screenshot_name=filename)
                import sys
                exc_class, exc, tb = sys.exc_info()
                new_exc = exc_class("\n%s\nScreenshot file: %s.png" % (exc or exc_class, filename))
                raise new_exc.__class__, new_exc, tb
            raise e
        return func_response

    return newFunc


class Webpage(object):
    """
    The Webpage class is intended to be the parent class for all Webpages. In principle, a Webpage
    is simply a construct that allows us to organize a set of WebElements on any given page;
    therefore, this class and other Selenium PageModel entities follows this paradigm.

    The first step to do is to write your own class that extends Webpage:

        class Google(Webpage):
            def __init__(self, driver, url=None):
                super(Google, self).__init__(driver, url)
                self.path = ""
                self.search_field = TextField(driver, Locator.by_name('q'))

    In the constructor, you do the following:

        1) Call the parent class's constructor
        2) You define 'path' attribute (default is "", so it didn't need to be specified in this
           example)
        3) You add a set of WebElements to your Webpage
    """

    def __init__(self, driver, url=None):
        if not seleniumconfig.disable_check_for_selenium_webdriver and not isinstance(driver,
                                                                                      WebDriver):
            raise AttributeError("driver was not an expected RemoteWebdriver type!")
        self.driver = driver
        self.path = ""
        self.log = logging.getLogger(__name__)

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

        :param url: (Default: None) The url to open, but it is recommended that this be specified in
                    constructor
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

    def dict(self, simple=False):
        """
        This returns a dictionary representation of the Webpage

        :param simple: (Default: False) If set to True, this will return a simple representation of a Webpage containing
                        only the list of 'methods' and a list of 'accessible_elements'
        :return: a dict representation of a Webpage
        """
        dictionary = {
            'type': "{}.{}".format(self.__module__, self.__class__.__name__),
        }
        if not simple:
            dictionary['url'] = self.url.geturl()
            dictionary['path'] = self.path
            elements = self.get_element_attr_local()
            dictionary['elements'] = {}
            for key, element in elements.iteritems():
                dictionary['elements'][key] = element.dict()
        methods = self.get_methods_local()
        dictionary['methods'] = methods.keys() if simple else methods
        dictionary['accessible_elements'] = self.get_all_elements_on_page().keys()
        return dictionary

    def to_json(self, simple=False):
        """Returns a json string
        """
        return json.dumps(self.dict(simple=simple))

    def to_json_pp(self, simple=False):
        """Returns a pretty-print json string
        """
        return json.dumps(self.dict(simple=simple), indent=4)

    def start_timer(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This
        method will "start" the timer and set driver.start_time = time.time().

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g.
                     'page' or 'element') then all timer attributes will be prefixed with '<type>_'
                     (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The start time
        """
        attr = "start_time" if type is None else "{}_start_time".format(type)
        setattr(self.driver, attr, time.time())
        return getattr(self.driver, attr)

    def stop_timer(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements.
        This method will "stop" the timer and set driver.end_time = time.time().

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g.
                     'page' or 'element') then all timer attributes will be prefixed with '<type>_'
                     (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The end time
        """
        start_attr = "start_time" if type is None else "{}_start_time".format(type)
        end_attr = "end_time" if type is None else "{}_end_time".format(type)
        duration_attr = "duration_time" if type is None else "{}_duration_time".format(type)

        # Return None if haven't started a timer
        if not hasattr(self.driver, start_attr) or getattr(self.driver, start_attr) == 0:
            return None

        setattr(self.driver, end_attr, time.time())
        start_time = getattr(self.driver, start_attr)
        end_time = getattr(self.driver, end_attr)
        setattr(self.driver, duration_attr, end_time - start_time)
        return end_time

    def get_split_time(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This
        method will return a duration between driver.start_time and now. If a timer was not started,
        then return 0.

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g.
                     'page' or 'element') then all timer attributes will be prefixed with '<type>_'
                     (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The duration between driver.start_time and time.time(). Otherwise, 0
        """
        attr = "start_time" if type is None else "{}_start_time".format(type)
        if not hasattr(self.driver, attr) or getattr(self.driver, attr) == 0:
            return 0
        return time.time() - getattr(self.driver, attr)

    def get_duration(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements.
        This method will return a duration between driver.start_time and now. This method will also
        call stop_timer(). If a timer was already stopped, then do not call stop_timer() again;
        instead return the previous duration. If a timer was not started, then return 0.

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g.
                     'page' or 'element') then all timer attributes will be prefixed with '<type>_'
                     (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The duration between driver.start_time and driver.end_time. Otherwise, 0
        """
        start_attr = "start_time" if type is None else "{}_start_time".format(type)
        end_attr = "end_time" if type is None else "{}_end_time".format(type)
        duration_attr = "duration_time" if type is None else "{}_duration_time".format(type)
        if not hasattr(self.driver, start_attr) or getattr(self.driver, start_attr) == 0:
            return 0
        if not hasattr(self.driver, end_attr):
            self.stop_timer(type=type)
        if getattr(self.driver, end_attr) < getattr(self.driver, start_attr):
            self.stop_timer(type=type)
        return getattr(self.driver, duration_attr)

    def reset_timer(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This
        method will set driver.start_time = 0, driver.end_time = 0, and driver.duration_time = 0

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g.
                        'page' or 'element') then all timer attributes will be prefixed with
                        '<type>_' (e.g. driver.page_start_time, page_end_time, and
                        page_duration_time)
        :return: self
        """
        start_attr = "start_time" if type is None else "{}_start_time".format(type)
        end_attr = "end_time" if type is None else "{}_end_time".format(type)
        duration_attr = "duration_time" if type is None else "{}_duration_time".format(type)
        setattr(self.driver, start_attr, 0)
        setattr(self.driver, end_attr, 0)
        setattr(self.driver, duration_attr, 0)
        return self

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

    @take_screenshot_on_webpage_error
    def get_html(self):
        """
        Retrieves the html of the entire webpage

        :return: a str of the entire page html
        """
        return Element(self.driver, Locator.by_xpath("//html")).get_html()

    @take_screenshot_on_webpage_error
    def wait_for_title(self, title, timeout=None):
        """
        This could be used similarly to a wait_for_page_load() if the page title can uniquely
        identify different pages or states of the page. Google Search works like this.

        :param title: The title to search for (case sensitive)
        :param timeout: The number of seconds to wait - Default: 10s
        :raises TimeoutException: if the title does not appear within timeout period
        """
        timeout = timeout if timeout is not None else self.element_timeout
        WebDriverWait(driver=self.driver, timeout=timeout).until(EC.title_contains(title))
        return self

    @take_screenshot_on_webpage_error
    def wait_for_page_load(self, timeout=None, force_check_visibility=False):
        """
        This method "waits for page load" by checking that all expected objects are both present
        and visible on the page. This is similar to validate() operation except that sometimes
        certain pages take a long time to load. Typically the threshold is 30sec, but this is
        configurable.

        :param timeout: (Default: 30s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible
                                       (but present) on load. The default is to respect this setting
                                       and only check for presence. Setting this to 'True' means you
                                       want to check for both present and visible.
        :return: self if everything is successful
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        timeout = timeout if timeout is not None else self.page_timeout
        self.start_timer(type="page_load")
        self.validate(timeout=timeout, force_check_visibility=force_check_visibility)
        self.stop_timer(type="page_load")
        self.log.debug("Page load for {} took {}sec".format(self.__class__.__name__,
                                                            self.get_duration("page_load")))
        return self

    @take_screenshot_on_webpage_error
    def validate(self, timeout=None, force_check_visibility=False, failfast_check_element=None):
        """
        The intention of validate is to make sure that an already loaded webpage contains these
        elements.

        :param timeout: (Default: 10s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible
                                       (but present) on load. The default is to respect this setting
                                       and only check for presence. Setting this to 'True' means you
                                       want to check for both present and visible.
        :param failfast_check_element: (Default: True) If set to False, then if there is a
                                       TimeoutException on a WebElement, then it will cache the
                                       exception message, check all other elements, and then
                                       re-raise the TimeoutException with a combined list of all
                                       WebElements that failed their check. This is useful for
                                       debugging your Webpage/Widget and all its elements.
                                       However, it does have the Selenium side-effect that the
                                       time it takes for the method to return could be compounded
                                       because of the timeout on each failure.
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        timeout = timeout if timeout is not None else self.element_timeout
        failfast_check_element = failfast_check_element \
            if failfast_check_element is not None else seleniumconfig.failfast_check_element
        error_msgs = []
        for element in self.get_element_attr():
            # Continue if the element has marked itself do_not_check=True
            if element.do_not_check:
                continue
            # Check for presence and visibility
            if force_check_visibility or element.check_visible:
                # Print to stderr a WARNING message when force_check_visibility=True and element
                # has been marked 'invisible'
                if force_check_visibility and not element.check_visible:
                    self.log.warn("element {}={} ({}) was marked as 'invisible' "
                                  "but force_check_visibility=True".format(element.locator.by,
                                                                           element.locator.value,
                                                                           self.__class__))
                try:
                    if isinstance(element, IFrame):
                        element.validate(timeout=timeout,
                                         force_check_visibility=force_check_visibility)
                    else:
                        element.wait_for_present_and_visible(timeout)
                except TimeoutException as ex:
                    self.log.debug(ex.msg)
                    if failfast_check_element:
                        raise ex
                    self.log.debug("Continuing check on other elements")
                    error_msgs.append(ex.msg)
            else:
                try:
                    element.wait_for_present(timeout)
                except TimeoutException as ex:
                    self.log.debug(ex.msg)
                    if failfast_check_element:
                        raise ex
                    self.log.debug("Continuing check on other elements")
                    error_msgs.append(ex.msg)
        if len(error_msgs) > 0:
            raise TimeoutException("- \n".join(error_msgs))
        return self

    def is_page(self, timeout=None, force_check_visibility=False):
        """
        This is like validate() operation except that it returns a boolean True/False. The idea is
        to ask whether or not you are on a page; this is an implementation of that idea. There are
        of course other ways of checking whether you are on the right page or not (e.g. checking the
        page title).

        :param timeout: (Default: 30s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible
                                       (but present) on load. The default is to respect this setting
                                       and only check for presence. Setting this to 'True' means you
                                       want to check for both present and visible.
        :return: True if validate() does not throw an exception; False otherwise
        """
        timeout = timeout if timeout is not None else self.page_timeout
        try:
            self.validate(timeout=timeout,
                          force_check_visibility=force_check_visibility,
                          failfast_check_element=True)
            return True
        except:
            return False

    def take_screenshot(self, screenshot_dir=None, screenshot_name=None, debug_logger_object=None):
        """
        Allows you to take a screenshot of the current page.

        :param screenshot_dir: (Default: './screenshots') The directory path for the screenshots
        :param screenshot_name: (Default: "screenshot_%s" % time.strftime('%Y_%m_%d-%H_%M_%S')) The
                                file name excluding the type
        :param debug_logger_object: (Default: None) Ability to reference your own debugger object.
                                    I am assuming there is a debug(msg) method, in which this method
                                    will write to.
        :return: screenshot_name
        """
        screenshot_name = "screenshot_%s" % time.strftime(
            '%Y_%m_%d-%H_%M_%S') if screenshot_name is None else screenshot_name
        screenshot_dir = seleniumconfig.screenshot_dir if screenshot_dir is None else screenshot_dir
        debug_logger_object = seleniumconfig.debug_logger_object \
            if debug_logger_object is None else debug_logger_object
        filename = "%s/%s.png" % (screenshot_dir, screenshot_name)

        # Ensure that path exists, otherwise create it
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        # Debugging information
        if debug_logger_object is not None:
            debug_logger_object.debug("Saving ScreenShot at %s" % filename)
        else:
            self.log.warning("Saving Screenshot at %s" % filename)

        base64_data = self.driver.get_screenshot_as_base64()
        screenshot_data = base64.decodestring(base64_data)
        screenshot_file = open(filename, "w")
        screenshot_file.write(screenshot_data)
        screenshot_file.close()

        return screenshot_name

    def get_element_attr(self, type=Element, override_check_visible=False,
                         override_do_not_check=False, expand_iframe_elements=False,
                         result_type=list):
        """
        Retrieves a list of WebElements on a Webpage. Optionally, you can pass in a different type
        (e.g. Button, Link, TextElement) to return only those types associated with a Webpage
        object.

        :param type: (Default: seleniumpm.webelements.Element) one of the seleniumpm.webelement
                     types
        :param override_check_visible: (Default: False) This overrides check for visibility. By
                                        default, widgets that are invisible, means that we assume
                                        its elements are also invisible
        :param override_do_not_check: (Default: False) This overrides check for do_not_check. By
                                        default, widgets that are marked as do_not_check, means that
                                        we assume its elements are not accessible
        :param expand_iframe_elements: (Default: False) Elements within an iFrame must be kept
                                        together in order to execute validate()
        :param result_type: (Default: list) This value can either be (list|dict). By default, we
                            simply want a list of available elements on the page. However, the
                            dictionary version is implemented for the ability to retrieve every
                            element and sub-element on a Webpage directly from the page level
        :return: This is a list or dict of attributes of base type seleniumpm.webelements.Element
        """
        if result_type != list and result_type != dict:
            raise AttributeError(
                "result_type can either be 'list' (default) or "
                "'dict', but was '{}'".format(result_type))
        elements = [] if result_type == list else {}
        temp_widgets = {}
        for attr in dir(self):
            # This is to catch potential exceptions thrown in situations where a developer
            # decorates a method with @property and the method raises an error
            try:
                element = getattr(self, attr, None)
            except:
                element = None
            # Ensure that it is of type Element
            if isinstance(element, Element):
                # Set some Webpage meta-data in the element
                element.attr_name = attr
                element.attr_class_name = self.__class__.__name__
                # If it is a widget, then recursively drill down and get its Elements
                if isinstance(element, Widget):
                    # Check if widget is a type of iFrame and also check for visibility
                    if (element.check_visible or override_check_visible) and \
                            (not element.do_not_check or override_do_not_check) and \
                            not isinstance(element, IFrame) or \
                            ((isinstance(element, IFrame) and expand_iframe_elements)):
                        if result_type == dict:
                            temp_widgets[attr] = []
                            for key, value in element \
                                    .get_element_attr(type=type,
                                                      override_check_visible=override_check_visible,
                                                      override_do_not_check=override_do_not_check,
                                                      expand_iframe_elements=expand_iframe_elements,
                                                      result_type=result_type,
                                                      check_myself=True,
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
                if type not in (Widget, Panel, IFrame) \
                        and isinstance(element, type) \
                        and not isinstance(element, Widget):
                    if result_type == dict:
                        elements[attr] = element
                    else:
                        elements.append(element)

        # Give non-widgets priority, hence why there is a separate loop for widgets and their
        # elements
        for attr, values in temp_widgets.items():
            for element in values:
                if element['key'] not in elements:
                    elements[element['key']] = element['value']
                else:
                    elements["{}_{}".format(attr, element['key'])] = element['value']

        # Ensure that there is only 1 iframe defined on page at this time
        count_iframes = 0
        # TODO - apparently list(elements.values()) is how this should be implemented if using
        # TODO - Python 3
        list_elements = elements.values() if result_type == dict else elements
        for element in list_elements:
            if isinstance(element, IFrame) and not element.do_not_check:
                count_iframes += 1
            if count_iframes > 1 and not expand_iframe_elements:
                raise AttributeError("There was more than 1 IFrame found on this page. "
                                     "This is currently not supported. If necessary, "
                                     "please mark at least 1 of them using 'mark_do_not_check()'")

        return elements

    def get_element_attr_local(self):
        """
        This is a much simpler implement of get_element_attr() in that it only returns back the
        locally defined Elements, and not any elements defined in sub-Widgets and sub-Panels.

        :return: A dict of Element types
        """
        elements = {}
        for attr in dir(self):
            element = getattr(self, attr)
            if isinstance(element, Element) and attr in self.__dict__.keys():
                elements[attr] = element
        return elements

    def get_methods_local(self):
        """
        Returns only the local methods defined for this class

        :return: a dict containing method names (keys) and a list of parameters for the method
                 (values)
        """
        results = {}
        for attr in dir(self):
            method = getattr(self, attr)
            if type(method) == types.MethodType and \
                            method.__name__ not in ('__init__') and \
                            method.__func__ in method.im_class.__dict__.values():
                args = inspect.getargspec(method)[0][1:]
                results[method.__name__] = args
        return results

    def get_all_elements_on_page(self):
        """
        Retrieves all the webelements that have been defined on the page. This includes all
        sub-elements found on widgets, panels, and iframes.

        :return: A dict of all the elements
        """
        return self.get_element_attr(override_check_visible=True,
                                     override_do_not_check=True,
                                     expand_iframe_elements=True,
                                     result_type=dict)

    def __getattr__(self, name):
        """
        Overridden method so that we can also be able to directly access all webelements defined at
        lower level webelements (a.k.a. widgets, panels, and iframes)

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
            raise AttributeError("'{}' webpage and its widgets has no attribute '{}'. "
                                 "The following are valid webelements on the page:\n  - {}".format(
                self.__class__.__name__, name, "\n  - ".join(all_elements.keys())))
