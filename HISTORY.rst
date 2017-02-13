Release History
===============


2.5.0 (UN-RELEASED)
-------------------

**New Features:**

**Fixed:**

- Fixing issue with uploading to wheel
- Simplifying README for more of a project overview. More details should be located on the wiki

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
