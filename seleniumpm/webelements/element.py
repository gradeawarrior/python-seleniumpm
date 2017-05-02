from functools import wraps
import base64
import os
import re
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import seleniumpm.config as seleniumconfig
from seleniumpm.locator import Locator

# Regular expression to find numbers (both int and float) in a string
number_re = r'([\-]*\d+\.\d+|[\-]*\d+)'

def take_screenshot_on_element_error(func):
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
                filename = "element_error_%s_%s" % (func.func_name, time.strftime('%Y_%m_%d-%H_%M_%S'))
                page = Element(funcObj.driver, Locator.by_xpath("//placeholder"))
                page.take_screenshot(screenshot_name=filename)
                import sys
                exc_class, exc, tb = sys.exc_info()
                new_exc = exc_class("\n%s\nScreenshot file: %s.png" % (exc or exc_class, filename))
                raise new_exc.__class__, new_exc, tb
            raise e
        return func_response

    return newFunc

class Element(object):

    def __init__(self, driver, locator):
        if not seleniumconfig.disable_check_for_selenium_webdriver and not isinstance(driver, WebDriver):
            raise AttributeError("driver was not an expected RemoteWebdriver type!")
        if not isinstance(locator, Locator) and locator is not None:
            raise AttributeError("locator was not an expected seleniumpm.Locator type!")
        self.driver = driver
        self.locator = locator

        # These attributes controls Webpage and Widget validation checks
        self.check_visible = True
        self.do_not_check = False

    def mark_invisible(self):
        self.check_visible = False
        return self

    def mark_visible(self):
        self.check_visible = True
        return self

    def mark_do_not_check(self):
        self.do_not_check = True
        return self

    def mark_check(self):
        self.do_not_check = False
        return self

    @take_screenshot_on_element_error
    def get_webelement(self):
        """
        This method basically does a driver.find_element(by, value) call

        :return: A Selenium WebElement
        """
        if self.locator is None:
            raise AttributeError("locator was not specified!")
        return self.driver.find_element(self.locator.by, self.locator.value)

    @take_screenshot_on_element_error
    def get_webelements(self):
        """
        This method basically does a driver.find_elements(by, value) call

        :return: A list of Selenium WebElements
        """
        if self.locator is None:
            raise AttributeError("locator was not specified!")
        return self.driver.find_elements(self.locator.by, self.locator.value)

    @take_screenshot_on_element_error
    def wait_for_webelements(self, expected_min_length=None, timeout=10, polling=0.5):
        """
        This method does a driver.find_elements(by, value) call, but has an optional expected_min_length
        parameter. This is useful for checking lists after a save has been performed. If no expected_min_length is
        specified, then this method behaves the same as get_webelements()

        :param expected_min_length: (Default: None) If specified, then poll and check to see if the returned
                                    WebElements is at least the minimum length.
        :param timeout: (Default: 10s) This controls the threshold for how long to check if expected_min_length
                        is specified.
        :param polling: (Default: 0.5s or 500ms) This controls how often to check
        :return: A list of Selenium WebElements. If by the expected_min_length is not met by the timeout period, then
                 the last retrieved list is returned.
        """
        if self.locator is None:
            raise AttributeError("locator was not specified!")
        current_time = time.time()
        end_time = (current_time + (timeout * 1000)) \
            if (expected_min_length is not None and timeout is not None and timeout > 0) else current_time
        return_elements = []
        while current_time <= end_time:
            return_elements = self.get_webelements()
            if expected_min_length is not None and len(return_elements) >= expected_min_length:
                return return_elements
            time.sleep(polling)
            current_time = time.time()
        return return_elements

    def get_action_chains(self):
        return ActionChains(self.driver)

    @take_screenshot_on_element_error
    def get_text(self):
        """
        This method does a driver.find_elements(by, value).txt call.

        :return: A string
        """
        return self.get_webelement().text

    @take_screenshot_on_element_error
    def wait_for_text(self, expected_txt=None, timeout=10, polling=0.5):
        """
        This method does a driver.find_elements(by, value).txt call, but has an optional expected_txt parameter.

        :param expected_txt: (Default: None) If specified, then poll and check to see if the returned
                             WebElement contains the expected txt
        :param timeout: (Default: 10s) This controls the threshold for how long to check if expected_txt
                        is specified.
        :param polling: (Default: 0.5s or 500ms) This controls how often to check
        :return: A string. If by the expected_txt is not met by the timeout period, then the last retrieved text
                 is returned.
        """
        current_time = time.time()
        end_time = (current_time + (timeout * 1000)) \
            if (expected_txt is not None and timeout is not None and timeout > 0) else current_time
        result_txt = None
        while current_time <= end_time:
            result_txt = self.get_text()
            if expected_txt is not None and expected_txt == result_txt:
                return result_txt
            time.sleep(polling)
            current_time = time.time()
        return result_txt

    @take_screenshot_on_element_error
    def get_texts(self):
        """
        This method does a driver.find_elements(by, value).txt call

        :return: A list of strings
        """
        result_txts = []
        elements = self.get_webelements()
        for element in elements:
            result_txts.append(element.text)
        return result_txts

    @take_screenshot_on_element_error
    def wait_for_texts(self, expected_txt=None, timeout=10, polling=0.5):
        """
        This method does a driver.find_elements(by, value).txt call, but has an optional expected_txt parameter. This
        is useful for checking lists after a save has been performed. If no expected_min_length is specified, then
        this method behaves the same as get_texts()

        :param expected_txt: (Default: None) If specified, then poll and check to see if the returned
                                    list contains the expected txt
        :param timeout: (Default: 10s) This controls the threshold for how long to check if expected_txt
                        is specified.
        :param polling: (Default: 0.5s or 500ms) This controls how often to check
        :return: A list of strings. If by the expected_txt is not met by the timeout period, then
                 the last retrieved list is returned.
        """
        current_time = time.time()
        end_time = (current_time + (timeout * 1000)) \
            if (expected_txt is not None and timeout is not None and timeout > 0) else current_time
        result_txts = []
        while current_time <= end_time:
            result_txts = self.get_texts()
            if expected_txt is not None and expected_txt in result_txts:
                return result_txts
            time.sleep(polling)
            current_time = time.time()
        return result_txts

    def get_index_of_text(self, text, operator="=="):
        """
        This method returns the index where the given text is found. This method of course is assuming your
        locator is a reference to a list, and performs a get_webelements() to retrieve all WebElements.

        :param text: The text to search for
        :param operator: (Default: '==') This value can either be '==' or '~='. The first is an exact match, while
                         The second is a search within the text.
        :return: The index where the text was found, otherwise, -1
        """
        for index, element in enumerate(self.get_texts()):
            if operator == "==" and element.text == text:
                return index
            elif operator == "~=" and re.search(text, element.text):
                return index
        return -1

    @take_screenshot_on_element_error
    def get_number(self, string=None, result_index=0):
        """
        This simplifies getting a number from an element

        :param string: (Optional) Default: None - This is a string that we want to extract a number from. By default
                        this is implicitly doing an element.text operation to retrieve the string.
        :param result_index: (Optional) Default: 0 - By default, converts and returns the first matching set. This can
                                be changed to return the n'th matching set
        :return: A number that can be (i) an int, (ii) a float, or (iii) None if neither.
        """
        string = self.get_text() if string == None else string
        try:
            return self.get_int(string, result_index)
        except ValueError:
            try:
                return self.get_float(string, result_index)
            except ValueError:
                return None

    def get_numbers(self):
        """
        This simplifies getting a list of numbers from a set of web elements

        :return: A list of numbers where each item can be (i) an int, (ii) a float, or (iii) None if neither.
        """
        web_elements = self.get_webelements()
        results = []
        for web_element in web_elements:
            results.append(self.get_number(web_element.text))
        return results

    @take_screenshot_on_element_error
    def get_int(self, string=None, result_index=0):
        """
        This simplifies getting an integer from an element

        :param string: (Optional) Default: None - This is a string that we want to extract a number from. By default
                        this is implicitly doing an element.text operation to retrieve the string.
        :param result_index: (Optional) Default: 0 - By default, converts and returns the first matching set. This can
                                be changed to return the n'th matching set
        :return: an integer value
        :raises ValueError: if the element text is not an integer
        """
        string = self.get_text() if string == None else string
        results = map(int, re.findall(number_re, string))
        return results[result_index] if len(results) > 0 else None

    @take_screenshot_on_element_error
    def get_float(self, string=None, result_index=0):
        """
        This simplifies getting an float from an element

        :param string: (Optional) Default: None - This is a string that we want to extract a number from. By default
                        this is implicitly doing an element.text operation to retrieve the string.
        :param result_index: (Optional) Default: 0 - By default, converts and returns the first matching set. This can
                                be changed to return the n'th matching set
        :return: an float value
        :raises ValueError: if the element text is not an float
        """
        string = self.get_text() if string == None else string
        results = map(float, re.findall(number_re, string))
        return results[result_index] if len(results) > 0 else None

    @take_screenshot_on_element_error
    def get_attribute(self, name):
        """
        Performs a Webelement.get_attribute() and thus returns back a string

        :param name: This is the attribute that you want to retrieve (e.g. class or href) the value of
        :return: string
        """
        return self.get_webelement().get_attribute(name)

    def get_attribute_contains(self, name, value):
        """
        Returns True|False depending on whether or not the specified value is in the results. This is implemented
        specifically for matching css classes, and thus the attribute values **MUST** be space-delimited

        :param name: The attribute name to retrieve
        :param value: A specific attribute value that you want to match
        :return: True|False if the attribute value is in the list
        """
        attribute = self.get_attribute(name)
        attributes = attribute.split()
        return True if value in attributes else False

    def get_attribute_is(self, name, value):
        """
        Returns True|False depending on whether or not the specified value matches the returned attribute value

        :param name: The attribute name to retrieve
        :param value: A specific attribute value that you want to match
        :return: True|False if the attribute value is an exact match
        """
        return True if self.get_attribute(name) == value else False

    @take_screenshot_on_element_error
    def is_displayed(self):
        return self.get_webelement().is_displayed()

    @take_screenshot_on_element_error
    def is_enabled(self):
        return self.get_webelement().is_enabled()

    @take_screenshot_on_element_error
    def is_selected(self):
        return self.get_webelement().is_selected()

    @take_screenshot_on_element_error
    def is_present(self, timeout=None):
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            self.wait_for_present(timeout)
            return True
        except:
            return False

    @take_screenshot_on_element_error
    def is_visible(self, timeout=None):
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            self.wait_for_visible(timeout)
            return True
        except:
            return False

    @take_screenshot_on_element_error
    def is_present_and_visible(self, timeout=None, present_timeout=None, visible_timeout=None):
        present_timeout = present_timeout if present_timeout is not None else self.element_timeout
        visible_timeout = visible_timeout if visible_timeout is not None else self.element_timeout
        return self.is_present(timeout if timeout is not None else present_timeout) and \
               self.is_visible(timeout if timeout is not None else visible_timeout)

    @take_screenshot_on_element_error
    def set_focus(self):
        return self.scroll_into_view()

    @take_screenshot_on_element_error
    def scroll_into_view(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.get_webelement())
        return self

    @take_screenshot_on_element_error
    def move_to_element(self):
        return self.get_action_chains().move_to_element(self.get_webelement()).build().perform()

    @take_screenshot_on_element_error
    def hover_over(self):
        self.move_to_element()

    @take_screenshot_on_element_error
    def get_html(self):
        """
        Retrieves the inner-html of an element

        :return: str representing the inner-html of an element
        """
        return self.get_webelement().get_attribute("innerHTML").encode("utf-8")

    @take_screenshot_on_element_error
    def wait_for_selected(self, timeout=None):
        if self.locator is None:
            raise AttributeError("locator was not specified!")
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_selected((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for selected {}={} with timeout={}s ({})".format(self.locator.by, self.locator.value, timeout, self.__class__)
            e.msg = e.message
            raise e
        return self

    @take_screenshot_on_element_error
    def wait_for_present(self, timeout=None):
        if self.locator is None:
            raise AttributeError("locator was not specified!")
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for present {}={} with timeout={}s ({})".format(self.locator.by, self.locator.value, timeout, self.__class__)
            e.msg = e.message
            raise e
        return self

    @take_screenshot_on_element_error
    def wait_for_visible(self, timeout=None):
        if self.locator is None:
            raise AttributeError("locator was not specified!")
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((self.locator.by, self.locator.value)))
        except TimeoutException as e:
            e.message = "TimeoutException waiting for visible {}={} with timeout={}s ({})".format(self.locator.by, self.locator.value, timeout, self.__class__)
            e.msg = e.message
            raise e
        return self

    @take_screenshot_on_element_error
    def wait_for_present_and_visible(self, timeout=None, present_timeout=None, visible_timeout=None):
        present_timeout = present_timeout if present_timeout is not None else self.element_timeout
        visible_timeout = visible_timeout if visible_timeout is not None else self.element_timeout
        self.wait_for_present(timeout if timeout is not None else present_timeout)
        self.wait_for_visible(timeout if timeout is not None else visible_timeout)
        return self

    def take_screenshot(self, screenshot_dir=None, screenshot_name=None, debug_logger_object=None):
        """
        Allows you to take a screenshot of the current page.

        :param screenshot_dir: (Default: './screenshots') The directory path for the screenshots
        :param screenshot_name: (Default: "screenshot_%s" % time.strftime('%Y_%m_%d-%H_%M_%S')) The file name excluding
                                the type
        :param debug_logger_object: (Default: None) Ability to reference your own debugger object. I am assuming there
                                    is a debug(msg) method, in which this method will write to.
        :return: screenshot_name
        """
        screenshot_name = "screenshot_%s" % time.strftime(
            '%Y_%m_%d-%H_%M_%S') if screenshot_name is None else screenshot_name
        screenshot_dir = seleniumconfig.screenshot_dir if screenshot_dir is None else screenshot_dir
        debug_logger_object = seleniumconfig.debug_logger_object if debug_logger_object is None else debug_logger_object
        filename = "%s/%s.png" % (screenshot_dir, screenshot_name)

        # Ensure that path exists, otherwise create it
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        # Debugging information
        if debug_logger_object is not None:
            debug_logger_object.debug("Saving ScreenShot at %s" % filename)
        else:
            print "[DEBUG] Saving Screenshot at %s" % filename

        base64_data = self.driver.get_screenshot_as_base64()
        screenshot_data = base64.decodestring(base64_data)
        screenshot_file = open(filename, "w")
        screenshot_file.write(screenshot_data)
        screenshot_file.close()

        return screenshot_name
        return self

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def dict(self):
        """
        This returns a dictionary representation of a Element

        :return: a dict representation of a Element
        """
        return {
            'type': self.__class__.__name__,
            'package': self.__module__,
            'locator': self.locator.dict(),
            'check_visible': self.check_visible,
            'do_not_check': self.do_not_check
        }

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

    def start_timer(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This method
        will "start" the timer and set driver.start_time = time.time().

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g. 'page' or
                        'element') then all timer attributes will be prefixed with '<type>_'
                        (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The start time
        """
        attr = "start_time" if type is None else "{}_start_time".format(type)
        setattr(self.driver, attr, time.time())
        return getattr(self.driver, attr)

    def stop_timer(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This method
        will "stop" the timer and set driver.end_time = time.time().

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g. 'page' or
                        'element') then all timer attributes will be prefixed with '<type>_'
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
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This method
        will return a duration between driver.start_time and now. If a timer was not started, then return 0.

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g. 'page' or
                        'element') then all timer attributes will be prefixed with '<type>_'
                        (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The duration between driver.start_time and time.time(). Otherwise, 0
        """
        attr = "start_time" if type is None else "{}_start_time".format(type)
        if not hasattr(self.driver, attr) or getattr(self.driver, attr) == 0:
            return 0
        return time.time() - getattr(self.driver, attr)

    def get_duration(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This method
        will return a duration between driver.start_time and now. This method will also call stop_timer(). If a timer
        was already stopped, then do not call stop_timer() again; instead return the previous duration. If a timer was
        not started, then return 0.

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g. 'page' or
                        'element') then all timer attributes will be prefixed with '<type>_'
                        (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: The duration between driver.start_time and driver.end_time. Otherwise, 0
        """
        start_attr = "start_time" if type is None else "{}_start_time".format(type)
        end_attr = "end_time" if type is None else "{}_end_time".format(type)
        duration_attr = "duration_time" if type is None else "{}_duration_time".format(type)
        if not hasattr(self.driver, start_attr):
            return 0
        if not hasattr(self.driver, end_attr):
            self.stop_timer(type=type)
        if getattr(self.driver, end_attr) < getattr(self.driver, start_attr):
            self.stop_timer(type=type)
        return getattr(self.driver, duration_attr)

    def reset_timer(self, type=None):
        """
        This method is part of the stop-watch set of capabilities for PageObjects and elements. This method
        will set driver.start_time = 0, driver.end_time = 0, and driver.duration_time = 0

        :param type: (Default: None) This is used for capturing different timers. If not None (e.g. 'page' or
                        'element') then all timer attributes will be prefixed with '<type>_'
                        (e.g. driver.page_start_time, page_end_time, and page_duration_time)
        :return: self
        """
        start_attr = "start_time" if type is None else "{}_start_time".format(type)
        end_attr = "end_time" if type is None else "{}_end_time".format(type)
        duration_attr = "duration_time" if type is None else "{}_duration_time".format(type)
        setattr(self.driver, start_attr, 0)
        setattr(self.driver, end_attr, 0)
        setattr(self.driver, duration_attr, 0)
        return self
