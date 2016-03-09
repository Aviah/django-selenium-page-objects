from ..selenium_page_objects import forms_base,forms_html

class ExampleForm(forms_base.WebFormById):
    """define forms by site context: sign-in form, sign-up form, edit item form, etc
    use WebFormById or WebFormByClass"""
    
    def __init__(self,*args,**kwargs):
        """call super with the form element_id arg""" 
              
        element_id = "form_element_id"
        super(ExampleForm,self).__init__(element_id=element_id,*args,**kwargs)
        
    def save(self):
        """this method should be named by site context: save, update etc"""
        self.submit()
        return self.browser
        
        
        
        
        
        


    
    