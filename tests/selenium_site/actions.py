from site_repo.tests.selenium_page_objects.actions import SeleniumWebActionBase

from . import public_pages
from . import login_pages

class ExampleAction(SeleniumWebActionBase):
    """ define "actions" that repeat in many tests.
    Typical action: sign-in, sign-up, add item, change user settings, 
    add item, delete item etc"""
    
    def action_foo(self,baz,bar):
        """Action class should have one action method, starts with action_
        the action__ should return a browser"""
    
        # do something
        return self.browser
        
