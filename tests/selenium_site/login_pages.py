from ..selenium_page_objects.pages import WebPageBase
from ..selenium_page_objects import elements_base
from ..selenium_page_objects.helpers import element_exists
from . import elements
from . import forms

class LoginPage(WebPageBase):
    """Base class for all pages for login, authenticated pages
    Typical methods will be the web application main menu"""
        
    def __init__(self,*args,**kwargs):                
        super(LoginPage,self).__init__(*args,**kwargs)
        
    def logout(self):        
        # run the logout click
        return self.browser
    
        
class ExampleApplicationPage(LoginPage):
    """each application page should have it's own class
    where the class methods reflect the actions the user can do in this page"""
    
    # the test checks that the page in the browser is the actual page the test expects
    page_id = "example_page_name" 
    
    def __init__(self,*args,**kwargs):
        super(ExampleApplicationPage,self).__init__(*args,**kwargs)
        
        # if the page has a form, add the form and init it
        # self.form = forms.ExampleForm(browser=self.browser)
        
    def foo(self):
        """do something that the user can do on this page
        must return a browser"""
        return self.browser
       
    @property
    def bar(self):
        """return some page property
        typical properties are 'can edit', 'can update', 'status' etc
        a property doesn't have to return a browser"""
        
        return is_bar
    