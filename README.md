Selenium-PageModel
==================

This project helps **Test Engineers** by abstracting out the implementation -- in this case Selenium -- from the actual set of **Actions** necessary to perform a single **Test Scenario**. The `Selenium-PageModel` library does this by defining a set of well defined `PageModel` constructs that **Test Engineers** can extend/implement to describe a Website. These `PageModel` constructs includes the following:

1. WebPage
2. Button
3. Checkbox
4. DropDown
6. Link
7. Table
8. TextElement
9. TextField
10. Widget

Using these constructs, you can describe a `WebPage` as having the following web-elements:

1. A Header `Widget` containing:
	* A Home `Link`
	* A Login `Link`
	* A Register `Link`
2. A form `Widget` containing:
	* A username `TextField`
	* A password `TextField`
	* A Submit `Button`
	* A potential Error message `TextElement` (in the event of a login failure)

Once a `PageModel` is defined, a _login test_ for an imaginary website may look like this:

	homePage.open();
	loginPage.waitForPageLoad().validate();
	loginPage.loginForm.userName.type("myuser");
	loginPage.loginForm.password.type("mypassword");
	loginPage.loginForm.submitButton.click();
	homePage.waitForPageLoad().isLoggedIn();

# Installation

The library can be installed via:

	pip install seleniumpm

# Usage

TODO

# Language Support

The Selenium PageModel implementation is not limited to just one language. Here are other language implementations:

* **Java** - [Java Selenium-PageModel](https://github.com/gradeawarrior/selenium-pagemodel)
* **Ruby** - In consideration depending on needs and popularity.


# Contributing to SeleniumPM
 
* Check out the latest master to make sure the feature hasn't been implemented or the bug hasn't been fixed yet.
* Check out the issue tracker to make sure someone already hasn't requested it and/or contributed it.
* Fork the project.
* Start a feature/bugfix branch.
* Commit and push until you are happy with your contribution.
* Make sure to add tests for it. This is important so I don't break it in a future version unintentionally.
* Please try not to mess with the version or history. If you want to have your own version, or is otherwise necessary, that is fine, but please isolate to its own commit so that I can cherry-pick around it.

## Testing and Releasing

### 1. Uprev the version in seleniumpm/__init__.py

You'll need to uprev the `__version__` attribute in `seleniumpm/__init__.py`:

	...
	
	__title__ = 'seleniumpm'
	__version__ = '1.0.0'
	__build__ = 0x021000
	__author__ = 'Peter Salas'
	__license__ = 'Apache 2.0'
	
	...
	
Commit and push your changes to Github!

### 2. Update HISTORY.md

You should update the Release Notes with the high-level changes contained within the release. If not ready to publish in Step 4 below, then put `UN-RELEASED` to denote that the feature is still under development has not been published to Pypi.

### 3. Upload your package to PyPI Test

Run:

	make publish.test
	
You should get no errors, and should also now be able to see your library in the test PyPI repository.

### 4. Upload to PyPI Live

Once you've successfully uploaded to PyPI Test, publish your changes to Live:

	make publish

# References

A huge shoutout to Peter Downs for his very easy-to-follow instructions for submitting a Python package to the community. See [first time with pypi](http://peterdowns.com/posts/first-time-with-pypi.html) for his instructions.

## Package Dependencies:

TODO

# Copyright

Copyright (c) 2017 Peter Salas. See LICENSE for
further details.