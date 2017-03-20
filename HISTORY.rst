Release History
===============

FUTURE (UN-RELEASED)
--------------------

**New Features:**

**Fixed:**

- Moving upload of wheel to use to twine instead of setup.py. See the following link for why: https://packaging.python.org/distributing/#wheels

2.7.1 (2017-03-20)
------------------

**New Features:**

**Fixed:**

- Fixed HISTORY.rst and README.rst files that are malformed sometime after 2.5.1 release
- Hopefully fixing other issues with 2.7.0 not being installable

2.7.0 (2017-03-20) - BROKEN
---------------------------

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
