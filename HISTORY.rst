Release History
===============

FUTURE (UN-RELEASED)
--------------------

**New Features:**

- Added highlight() feature to all Element types
- Support defining locators as tuples
- Adding utility for scanning a path and generating json output of all the PageObject structures in the project
- Added get_webelement_by_text() to Element types

**Fixed:**

- Moving upload of wheel to use twine instead of setup.py. See the following link for why: https://packaging.python.org/distributing/#wheels
- Fixed issue with validating a Widget with locator = None on a Webpage

2.13.0 (2017-05-18)
-------------------

**New Features:**

- Removed snapshot feature

**Fixed:**

2.12.2 (2017-05-09)
-------------------

**New Features:**

- Implementing a *wait_for_page_load* (Default: False) on Webpage *open()*, *refresh()*, and *reload()* operations

**Fixed:**

- Webpage.refresh() and Webpage.reload() did not return self

2.12.1 (2017-05-08)
-------------------

**New Features:**

**Fixed:**

- Turning off snapshot feature during is_page() and is_widget_loaded() operations. These operations often time trigger TimeoutException but it should not trigger a snapshot to be taken.

2.12.0 (2017-05-07)
-------------------

**New Features:**

- Implementing to_json() and to_json_pp() for Element, Widget, Locator, and Webpage types
- Adding additional wait_for_widget_load() timer to calculate load time of a widget
- Adding more logging across seleniumpm. Most are WARNING levels, so this will need to be set accordingly
- Implemented a is_widget_loaded() for all Widget types. This also includes both Panel and IFrame types
- Added ability to enumerate over all elements defined on a webpage and/or widget, and then return all elements that failed their checks for presence and visibility. The ability is built directly into *wait_for_page_load()*, *validate()*, and *wait_for_widget_load()*. This check is controlled via parameter and global selenium config *failfast_check_element* (Default: True). This is set to True by default for old behavior of throwing exception on the first element that is not present/visible. Setting this to False will enable this feature and will check each element before raising the expected TimeoutException with a message containing all the elements that failed. *NOTE: Depending on the timeout, this could potentially be a compounded amount of time before the method returns, hence why this feature is disabled by default.*

**Fixed:**

- Element.dict() had an issue if the locator was None
- Widget.validate() force_check_visibility was accidentally set to True when expected to be False. This ended up causing unexpected conditions in a test where some elements were marked as invisible, but validate() was still checking for visibility

2.11.8 (2017-05-05)
-------------------

**New Features:**

- For validate() and wait_for_page_load() operations, adding the meta-data for the Class and attribute name of the element that is being checked. This is so that if there is a TimeoutException, we can also report where we can find this element to fix in the code
- Add Logger for better debugging capability for testing purposes.

**Fixed:**

2.11.7 (2017-05-02)
-------------------

**New Features:**

**Fixed:**

- Moving click_index() from Clickable to Element type.

2.11.6 (2017-05-02)
-------------------

**New Features:**

**Fixed:**

- Adding Clickable.click_index() and Element.get_index_of_text() to indirectly address StaleElementReferenceException. Unfortunately, the problem may still arise and some experts say that StaleElementReferenceException is by design and should generally be "fixed" on a case-by-case basis and should not be fixed in a wrapper framework like seleniumpm nor will it be addressed in the Selenium core library.

2.11.5 (2017-05-01)
-------------------

**New Features:**

- Adding the following 'wait_for' methods to Element: wait_for_webelements(), wait_for_text(), and wait_for_texts()

**Fixed:**

- Element.wait_for_present_and_visible() did not have a return self
- Adding mark_check() and mark_visible() to complement the existing mark_do_not_check() and mark_invisible()

2.11.4 (2017-04-26)
-------------------

**New Features:**

- Adding unselect() to Checkbox and select() to both RadioButton and Checkbox types.
- Adding a new Label type. Right now, this is effectively the same as a TextElement or an Element

**Fixed:**

2.11.3 (2017-04-20)
-------------------

**New Features:**

**Fixed:**

- Fixing a missed-case configuring *disable_check_for_selenium_webdriver* (Default: False) on a Webpage

2.11.2 (2017-04-20)
-------------------

**New Features:**

- Adding new config *disable_check_for_selenium_webdriver* (Default: False) which now makes is possible to disable this check on an Element. Apparently, there are situations where a developer may pass in a non-webdriver object that overrides __getattr__() to returns driver.__getattribute__(item)

**Fixed:**

2.11.1 (2017-04-18)
-------------------

**New Features:**

- Adding a check_myself flag (Default: True) on a Widget/Panel/IFrame type. This is to support certain scenarios where a developer may want to validate the collection of elements found in an Widget/Panel/IFrame, but not actually validate itself. Again, this is because Widget/Panel/IFrame is of type Element and thus has a locator.

**Fixed:**

2.11.0 (2017-04-18)
-------------------

**New Features:**

- Adding a get_html() capability to return back either an entire page or the inner-html of a specific element. This is implemented on a Webpage, an IFrame, and Element types.
- Adding a wait_for_iframe_load() to IFrame type
- Added stop-watch capabilities (e.g. start, stop, split) to a Webpage and Element types. In addition, a basic page load timer has been implemented. Basically, every wait_for_page_load() and wait_for_iframe_load() will calculate a duration time automatically.
- Removed requirement that a Widget/Panel/IFrame type must define a Locator. This is to support situations where a developer doesn't want to validate the location of the Widget, but instead just wants to validate the objects that are within a Widget. This is similar to a Webpage validation.

**Fixed:**

- Fixed scenario for __getattr__ where a developer could decorate a method with @property, and thus could execute code that results in an Error/Exception.
- Added try/finally block to the validate() operation on an IFrame. This is to handle the situation when a sub-webpage (a.k.a. an iFrame) fails a validation; in this situation, we want to make sure that we allow going back to the top-level-webpage in the event of a Error.

2.10.0 (2017-04-07)
-------------------

**New Features:**

- Added a get_attribute_contains() and a get_attribute_is() on Element type. The intention is to implement an all-in-one solution for both retrieving an attribute and validating whether something contains or is something. This operation is useful for dynamic elements that use css classes for changing the state of a page (e.g. <div class='svgOverviewView-status-icon fa fa-exclamation-triangle svg-status-warning'>); One could define a generic reference to this element, and then use get_attribute_contains() to check if it now contains 'fa-exclamation-triangle' css class.
- Implementation of seleniumpm.config module. This module can be imported via *import seleniumpm.config as seleniumconfig*; and variables can be changed like so: *seleniumconfig.page_timeout_in_sec = 60*
- Added a global *element_timeout_in_ms* and *page_timeout_in_ms* to seleniumpm.config module. Defaults are still 10s for element timeout and 30s for page timeout.
- Added a global *debug_logging_function* to selenium.config module
- Added a refresh() operation on a Webpage (a.k.a. a page refresh). This of course is simply a driver.refresh() operation on an opened page.
- Added a get_current_url() operation on a Webpage
- Added get_number(), get_numbers(), get_int(), and get_float() to an Element. This is so that you can quickly and easily get numbers from element(s) text that represent numbers
- Added an "access element" abstraction layer so that you can retrieve any element defined any levels deep (e.g. A button defined within a Panel that is under an IFrame). The idea is simple: If I want to click a button 2-levels-deep, this can be done either by (1) page.iframe.panel1.login_button.click(), or (2) directly from the top-level page as if it was a local attribute via page.login_button.click()
- Added take_screenshot() feature to both a Webpage and Element types.
- Added a take_screenshot_on_test_error annotation for annotating tests. The screenshot capability for a test is controlled by *seleniumpm.config.test_screenshot_enabled* and is set to True by default.
- Added pretty-print way of visualizing all attributes and methods for a Webpage. This is useful for documentation as well as for debugging

**Fixed:**

- Fixing issue with get_attribute() on Element. This method did not have an expected return statement

2.9.1 (2017-03-27)
------------------

**New Features:**

**Fixed:**

- Fixing missing implementation to do proper validation of an IFrame that is embedded on a Webpage

2.9.0 (2017-03-27)
------------------

**New Features:**

- Implement a get_texts() which returns back all the text (in a List) given a locator. This is available for all Element types
- Implement hover_over() capability to Element

**Fixed:**

- Fixed several critical issues related to get_element_attr(), validate(), and wait_for_page_load() operations on both a Webpage and Widget types
- Add more unittests for IFrame
- Fix wait_for_present_and_visible() timeout for the check for visibility. There are scenarios in which an element may be present, but not immediately visible

2.8.0 (2017-03-24)
------------------

**New Features:**

- Adding click() operations to a Widget. This is to support the fact that sometimes an entire section of a page can be "clickable"
- Adding new IFrame type

**Fixed:**

- Fixing issue with get_element_attr() method on both a Widget and a Webpage. The problem was that if you marked Widget type as do_not_check, then it should respect both the Widget and all of its embedded elements. The issue was that it would respect that the Widget was marked as do_not_check, but would still enumerate over all of its sub-elements.
- Fixing another issue with get_element_attr() method on both a Widget and a Webpage. The problem was related to Widget's that are marked "invisible". Similar to do_not_check, sub-elements should not be checked if the top-level Widget is already "invisible".

2.7.2 (2017-03-20)
------------------

**New Features:**

**Fixed:**

- Both Webpage and Widget validate() methods should return self
- Fixing force_check_visibility parameter in Webpage.wait_for_page_load(). The default was set to True instead of False

2.7.1 (2017-03-20)
------------------

**New Features:**

**Fixed:**

- Fixed HISTORY.rst and README.rst files that are malformed sometime after 2.5.1 release
- Hopefully fixing other issues with 2.7.0 not being installable

2.7.0 (2017-03-20)
------------------

**New Features:**

- Adding a new ability to mark an Element type as 'invisible' so that validations on a Widget or Webpage can be done simply on presence
- Adding a new ability to mark an Element type as 'do not check' so that you could potentially define an Element that you simply don't validate using the default validation() operation defined on a Widget or a Webpage. This feature should be used sparingly as there are better design patterns to handle **most** cases that you may think that you need to avoid validating the presence of specific Element types.

**Fixed:**

2.6.0 (2017-03-17)
------------------

**New Features:**

- Adding get_tuple() to Locator object. This is to make passing between SeleniumPM and the Selenium libraries eaiser
- Adding simpler way of defining Locators. Locators can now be created via Locator.by_xpath(path) or Locator.by_css_selector(path). The following types are supported:
   * by_xpath(path)
   * by_css_selector(path)
   * by_name(path)
   * by_class_name(path)
   * by_id(path)
   * by_link_text(path)
   * by_partial_link_text(path)
   * by_tag_name(path)
- Adding wait_for_selected() to Element
- Adding wait_for_clickable() and click_invisible() to Clickable
- Adding send_keys_delayed() and type_delayed() to TextField
- Adding new Panel type that simply extends Widget. Conceptually they're exactly the same, but Panel appears to be a more generally acceptable term for a section of a page

**Fixed:**
- Simplifying README for more of a project overview. Details should be located on the wiki

2.5.2 (2017-03-07)
------------------

**New Features:**

**Fixed:**

- Fixing issue with setup.py throwing error missing HISTORY.rst from package data

2.5.1 (2017-03-07) - BROKEN
---------------------------

**New Features:**

**Fixed:**

- Fixing issue with set_focus() or scroll_into_view(). They were apparently not included in 2.5.0 release

2.5.0 (2017-03-07) - BROKEN
---------------------------

**New Features:**

- Addition of RadioButton type
- Addition of Dropdown type
- Addition of Image type
- Add new method get_element_attr() to Webpage and Widget type. This will give developers access to all define
  Element attributes on a Webpage or within a Widget. This method all supports retrieving a specific Element type
  (e.g. Button, Link, Checkbox)
- Changing default wait_for_page_load() and validate() methods to use the above mentioned get_element_attr(). This can
  still be overridden, and does not affect previous implementations.
- Adding new seleniumpm.examples.widgets package
- Element class now implements a get_action_chains() method to return back an ActionChains type.
- Element class now implements a set_focus() or scroll_into_view() functionality, for those pesky webelements that are
  need to be visible, but are corrently scrolled off page somehow.

**Fixed:**

- Adding type-checking to constructor of the Element, Widget, and Webpage types. These classes will now throw an
  AttributeError if not passed in a legitimate RemoteWebdriver, URL, or Locator type as parameters.

2.4.2 (2017-02-13)
------------------

**New Features:**

**Fixed:**

- Fixing issue appending two .rst files together to generate the long_description
- Using setuptools for setup.py.

2.4.1 (2017-02-13)
------------------

**New Features:**

**Fixed:**

- Using disutils.core instead of setuptools for setup.py. Hoping this fixes pretty-print of rst files on PyPi

2.4.0 (2017-02-13)
------------------

**New Features:**

- Better support for Table type and interacting with them on a page. This includes support for 'search' operations and
  enumerating over rows and columns
- Additional methods to Locator object to assist in managing them
- implemented get_webelement() and get_webelements() for all Elements. This will return the Selenium WebElement
  object(s).
- Implementation of object equality for all Selenium Page Model classes
- UnitTests are now using PhantomJS (Headless) target
- Removal of requestest dependency to keep the project simple

**Fixed:**

- The Widget type was missing in 2.3.0 release
- Expanding of the UnitTest coverage to ensure libraries are working correctly
- Fixing issue with get_text() in Python Selenium. Apparently, this call in Python (versus Java) is simply called 'text'
- Conversion of README and HISTORY files to rst. This is so that they are rendered correctly on PyPi server

2.3.0 (2017-02-06)
------------------

**New Features:**

- Provides a full implementation of the current Java v2.3 of Selenium PageModel

2.0.0 (2017-01-10)
------------------

**New Features:**

- First release of seleniumpm for the world
- Contains minimum proof-of-concept for testing search on Google
