from ..selenium_page_objects.pages import WebPageBase
from . import forms

class PublicPage(WebPageBase):
    """Base class for all pages for public pages
    Typical methods will be sign-in, about-us etc"""
        
    def __init__(self,*args,**kwargs):
        
        super(PublicPage,self).__init__(*args,**kwargs)
        
    def sign_in(self,username,password):
        """this sign-in method will be available to all public pages""" 
    
        # sign-in actions
        return self.browser    


class HomePage(PublicPage):
    
    def __init__(self,*args,**kwargs):
        self.page_id = 'home_page'
        url = '/'
        super(HomePage,self).__init__(url=url,*args,**kwargs)
        
        #if page has a form, add it
        # self.form = forms.ExampleForm(browser=self.browser)
        return
    
class AboutUsPage(PublicPage):
    
    def __init__(self,*args,**kwargs):
        self.page_id = 'about_us'
        super(AboutUsPage,self).__init__(url=url,*args,**kwargs)
        
        #if page has a form, add it
        # self.form = forms.ExampleForm(browser=self.browser)
        return
        
    
    
    