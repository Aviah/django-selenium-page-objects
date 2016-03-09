from site_repo.tests.selenium_page_objects.selenium_cases import SeleniumWebTestCaseBase
from site_repo.tests.load_data import helpers


class SeleniumWebTestCaseWithData(SeleniumWebTestCaseBase):
    """subclass and customize the base selenium test case"""
    
    # defince case class variables
    # variables could be initial_users = None
   
    
    @classmethod
    def setUpTestData(cls):
        """site specific data loading functions
        use class variables to load data and config settings
        So the test set variables, and the class loads the data"""     
        
        # data loading, something like helpers.add_users(self.initial_users)
        pass
        
    @classmethod
    def setUpClass(cls):
        super(SeleniumWebTestCaseWithData,cls).setUpClass()
        cls.setUpTestData()
        
        
        
        
        
        
        
        
    
    