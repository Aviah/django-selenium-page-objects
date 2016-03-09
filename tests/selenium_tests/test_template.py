import os
import unittest
# edit the site_repo.settings to your site, like in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"   

from site_repo.tests.selenium_site.cases import SeleniumWebTestCaseWithData
from site_repo.tests.selenium_page_objects.helpers import custom_test_sort

class MyTest(SeleniumWebTestCaseWithData):
    
    # The case variables should be used to load data by the super class
    # Variable like initial_users = {'username':'john','password':'123456'}
        
    def test_baz(self):
        self.assertEqual('baz','baz')
        print "test baz"
        
    def test_foo(self):
        self.assertNotEqual('foo','baz')
        print "test foo"
        
        
if __name__ == '__main__':     
    from site_repo.tests.selenium_site.helpers import set_env
    set_env()
    # To customize the order the tests run (the following will run test_foo, then test_baz):
    #Ltests = ['test_foo','test_baz']
    #unittest.TestLoader.sortTestMethodsUsing = custom_test_sort(Ltests)
    unittest.main()