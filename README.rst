Selenium-PageModel
==================

This project helps **Test Engineers** by abstracting out the implementation -- in this case Selenium -- from the actual set of **Actions** necessary to perform a single **Test Scenario**. The Selenium-PageModel_ library does this by defining a set of well defined *PageModel* constructs that **Test Engineers** can extend/implement to describe a Website. These *PageModel* constructs includes the following:

1. WebPage
2. Button
3. Checkbox
4. Dropdown
5. Link
6. Table
7. TextElement
8. TextField
9. Widget

Using these constructs, you can describe a *WebPage* as having the following web-elements:

1. A Header *Widget* containing:
    * A Home *Link*
    * A Login *Link*
    * A Register *Link*
2. A form *Widget* containing:
    * A username *TextField*
    * A password *TextField*
    * A Submit *Button*
    * A potential Error message *TextElement* (in the event of a login failure)

Once a *PageModel* is defined, a *login test* for an imaginary website may look like this::

    homePage.open();
    loginPage.waitForPageLoad().validate();
    loginPage.loginForm.userName.type("myuser");
    loginPage.loginForm.password.type("mypassword");
    loginPage.loginForm.submitButton.click();
    homePage.waitForPageLoad().isLoggedIn();

Please see the project's Homepage for more information: Selenium-PageModel_

Installation
------------

The library can be installed via::

    pip install seleniumpm

Or if you want to install from src::

    pip install git+https://github.com/gradeawarrior/python-seleniumpm.git

Usage
-----

Here is the ever so popular Google example using *seleniumpm*::

    from selenium import webdriver
    from seleniumpm.examples.google_page import GooglePage

    """
    Setup for Remote execution against a local standalone-selenium-server
    and using the PhantomJS driver. This can be changed of course to using
    the driver of your choice (e.g. Chrome or Firefox)
    """
    driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.PHANTOMJS)

    # Instantiate Google Page
    google = GooglePage(driver, url="https://www.google.com")

    # Open + wait for page load + validate Google
    google.open().wait_for_page_load().validate()

    # Print the page title
    print google.get_title()

    # Search for 'Cheese!'
    search_str = "Cheese!"
    google.search_field.type(search_str)
    google.search_field.submit()

    # Ensure that the page is refreshed from your search
    print google.wait_for_title(search_str).get_title()

Creating your PageObject's
++++++++++++++++++++++++++

The GooglePage used in the above example looks like the following::

    from selenium.webdriver.common.by import By
    from seleniumpm.webpage import Webpage
    from seleniumpm.webelements.textfield import TextField
    from seleniumpm.locator import Locator

    class GooglePage(Webpage):
        def __init__(self, driver, url=None):
            super(GooglePage, self).__init__(driver, url)
            self.search_field = TextField(driver, Locator.by_name('q'))

        def get_result_links(self):
            links = []
            elements = self.driver.find_elements(By.XPATH, "//h3[contains(@class, 'r')]/a")
            for element in elements:
                links.append(element.get_attribute("href"))
            return links

You should notice that most of the operations except for get_result_links() are not visible on the GooglePage class. That is because the basic behaviors are either part of the Webpage or the TextField (aka an Element) type.

For more information about writing your PageObject's in SeleniumPM, please direct your attention to Creating-your-PageObject-with-SeleniumPM_

Language Support
----------------

The Selenium PageModel implementation is not limited to just one language. Here are other language implementations:

* **Java** - Java-SeleniumPM_
* **Ruby** - In consideration depending on needs and popularity.


Contributing to SeleniumPM
--------------------------
 
* Check out the latest master to make sure the feature hasn't been implemented or the bug hasn't been fixed yet.
* Check out the issue tracker to make sure someone already hasn't requested it and/or contributed it.
* Fork the project.
* Start a feature/bugfix branch.
* Commit and push until you are happy with your contribution.
* Make sure to add tests for it. This is important so I don't break it in a future version unintentionally.
* Please try not to mess with the version or history. If you want to have your own version, or is otherwise necessary, that is fine, but please isolate to its own commit so that I can cherry-pick around it.

References
----------

A huge shoutout to Peter Downs for his very easy-to-follow instructions for submitting a Python package to the community. See `first time with pypi <http://peterdowns.com/posts/first-time-with-pypi.html>`_ for his instructions.

Also see the following:

- selenium-server-runner_ - If you're running on a Mac, this project helps you setup and run the *standalone-selenium-server* on your laptop
- Java-SeleniumPM_ - The Java version of SeleniumPM_
- requestests_ - An API testing library

.. _Selenium-PageModel: https://github.com/gradeawarrior/python-seleniumpm
.. _Creating-your-PageObject-with-SeleniumPM: https://github.com/gradeawarrior/python-seleniumpm/wiki/Page-Object-Model
.. _SeleniumPM: https://github.com/gradeawarrior/python-seleniumpm
.. _Java-SeleniumPM: https://github.com/gradeawarrior/selenium-pagemodel
.. _selenium-server-runner: https://github.com/gradeawarrior/selenium-server-runner
.. _requestests: https://github.com/gradeawarrior/requestests

Package Dependencies:
---------------------

*seleniumpm* installs the following upstream packages as of the latest release:

- `selenium~=2.53.6 <https://pypi.python.org/pypi/selenium/2.53.6>`_

Copyright
---------

Copyright (c) 2017 Peter Salas. See LICENSE for
further details.