from functools import wraps
import time

import seleniumpm.config as seleniumconfig
from seleniumpm.webpage import Webpage

def take_screenshot_on_test_error(func):
    @wraps(func)
    def newFunc(*args, **kwargs):
        try:
            func_response = func(*args, **kwargs)
        except Exception as e:
            if seleniumconfig.test_screenshot_enabled:
                funcObj = args[0]
                filename = "test_error_%s_%s" % (func.func_name, time.strftime('%Y_%m_%d-%H_%M_%S'))
                page = Webpage(funcObj.driver)
                page.take_screenshot(screenshot_name=filename)
                import sys
                exc_class, exc, tb = sys.exc_info()
                new_exc = exc_class("\n%s\nScreenshot file: %s.png" % (exc or exc_class, filename))
                raise new_exc.__class__, new_exc, tb
            raise e
        return func_response

    return newFunc
