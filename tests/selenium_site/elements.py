from site_repo.tests.selenium_page_objects import elements_base,exceptions

class ExempleElement(object):
    """Define elements in the context of the site
    A typical element will be contact, expense, item, etc.
    The element method should reflect site context, like change_name, add amount"""
    
    
    def __init__(self,element_by_xpath):
        """exemple: get the element with xpath
        can use by_id, class etc"""
        assert isinstance(element_by_xpath, elements_base.WebElementByXPath)
        self.element = element_by_xpath.element
        self.browser = element_by_xpath.browser
        self.xpath = element_by_xpath.element_xpath
       
    @property 
    def text(self):        
        return self.element.text
    
    def change(self):        
       # do something with element
        return self.browser
