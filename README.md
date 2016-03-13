# Django-Selenium Page Objects

**Framework to test django sites with Selenium, by app context & the page-objects design pattern**

*Note: It's easier to grasp the idea in real code, so after this README, please look at a full page objects testing code for a real website in the [django-website](https://github.com/Aviah/django-website)*

[Overview](#overview)    
[How To](#how-to)    
[Components](#components)    
[Writing Tests](#writing-tests)    
[Install](#install)    
[Browser](#browser)    
[Actions](#actions)    
[Page id](#page-id)    
[Settings](#settings)    
[Wrapper](#wrapper)    
[Best Paractices](#best-practices)    
[Automation is Not Everything](#automation-is-not-everyting)    



## Overview

When you test a website with Selenium, the Selenium's web driver provides access to the HTML attributes of the pages and the site. So using Selenium, you can test that the expected HTML elements on the page are similar to what you expect this page to be.

A better approach is to write the tests not against HTML, but with the actual web application context. Instead of writing tests that check a "div" or a "button", you write a test that deals with the application objects: contacts, items, expenses, products, songs etc. The real application objects.

To achieve this context testing, you have to write another layer of objects, that maps the generic HTML selenium elements to the actual website context elements.     
A **page object** is an object that maps to a real page. The page objects attributes will map to the actual actions the user can run on this page. So each page objects represents a specifc application page.    
A "contacts page" object could look something like this:


	class MyContactsPage(BasePage):
	
		def follow(self,contact):
			...
						
		def unfollow(self,contact):
			...
						
		def notify_contact(self,contact):
			...
		
A "contact" is also a context object, and not an HTML element. It's not the "div" element  with the contact details, but a python object of a "contact". This context object is mapped with Selenium to an HTML element. This "contact" object might have properties like name, email, ormethods like "send_message_to".

Once you write this mapping layer between Selenium and the application context, then writing tests is not only easier, but better it reflects the application. Such test could run lines like:

		contacts = MyContactsPage()
		john = contacts.contacts_list[0]
		contacts.unfollow(john)
		
		
This code is also much easier to maintain, and if you ever tried to adjust a decent Selenium tests suite to the ever changing HTML, frameworks and style, you will appreciate it. And if you didn't, consider yourself lucky.

**To summarize:**

1. **Selenium identifies the HTML elements**
2. **An abstraction layer maps these HTML elements to page objects and application objects, according to the application context**
3. **Write Selenium tests against the application objects layer.**




## How To

This repository contains all the layers you need to write tests in the page objects pattern:

####selenium_page_objects
The base classes that map application context objects like pages, contacts, products, etc to Selenium generic HTML elements

###selenium_site
Where you write your specific site context objects, using the selenium_page_objects base classes. In a way, this layer maps the objects, attributes and methods to the actual GUI

###selenium_test
Here you write test cases, with common unittest. You use the selenium_site objects to write a test that map to the application context, and when possible using page objects and page methods that have similar name to the actual website pages and user actions.


## Components

The **selenium_site** contains several modules to work with:

**login_pages.py**    
Define a base class of LoginPage with all the methods that are shared between pages that user logs in to use. From this base LoginPage, subclass and define specific app pages. Login pages could be user settings, dashboard, my contacts, etc.

A LoginPage could look something like:

		class UserSettingsPage(LoginPage):
		
			def change_email(self,new_email):
				...
				
			def change_password(self,new_password):
				...

The LoginPage is a subclass of selenium_page_objects >> WebPageBase
				

**public_pages.py**    
Define a base class of PublicPage, with all the methods that shared between public, without authentication, pages. From this PublicPage, subclass and define specific app pages. Public pages could be home page, about us page, etc.

A PublicPage could look something like:

	class HomePage(PublicPage):
	
		def join_email_list(self,email):
			...
			
		def privacy_policy(self):
			...
			
The PublicPage is a subclass of selenium_page_objects >> WebPageBase			

**forms.py**    
Application forms, like sign-in form, sign-up form etc. When you define a page object (PublicPage or LoginPage), set the page form property to this form:

	from forms import SignInForm
	
	class HomePage(PublicPage):
		def __init__(self,*args,**kwargs):
			self.form = SignInForm(…)
			
A form is a subclass of selenium_page_objects >> WebFormById, or WebFormByClass
Both are a subclass of selenium_page_objects >> WebFormBase

When you define a form, it will automatically find the form by the element (id or class), and map all the text input field. It also has additional useful methods to clear the fields, change the fields values with a dictionary, and submit.

**elements.py**    
Define application context element like contact, expense, product, item, etc. An element should have application context methods like approve, delete, update, follow, etc.

When you define a list view page, it will typically have a list of elements: a MyContacts page will have a list of "Contacts" elements.

The element should subclass selenium_page_objects >> WebElementById, or WebElementByClass, or WebElementByXPath.    
All these base elements are subclass of WebElementHtmlBase.



**actions.py**    
Actions are handy if you want to bundle several steps into one call that you use in many tests. 

A Typical candidate is a "sign-in" action. The action will:

1.  Open the home page
2.  Show the sign-in form
3.  Enter values to the sign-in form
4.  Do something with the first page the user should see after login.
		
An action should subclass selenium_page_objects >> SeleniumWebActionBase, and have one method that starts with action:

	class SignInAction(SeleniumWebActionBase):
	
		def action_sign_in(username,password):
			...
			
**test_case.py**    
A SeleniumWebTestCaseWithData test case, subclass of SeleniumWebTestCaseBase. Define the data loading you need for your tests. The way to do it is via class variables (like initial_users or initial_products), and then methods to load the data from this variables in setUpTestData.

The idea is that in the tests, you subclass SeleniumWebTestCaseWithData, and then just have to define these variables to load the correct data for the tests.

Here the context is the specific data loader.

## Writing Tests

A test is a common unittest, that runs the some application flow. 

Say that we want to test that the user 'John' approves a friend's request from 'Tom'.
The test runs in a unittest case, so self is the TestCase:



	def test_approve_request(self):
	
		home = HomePage(self.browser)
		self.browser = home.sign_in(username='john',password='abcdef')
		dashboard = DashboardPage(browser=self.browser)
		dashboard.show_requests()
		new_request = dashboard.requests[0] # the dashboard.requests is a list of FriendRequest objects
		new_request.approve()
		my_frirends = MyFriendsPage(browser=dashboard.my_friends())
		my_friends.sort_friends(recent=True)
		new_friend = my_friends.friends[0] # the MyFriends.friends is a list of Friend objects
		self.assertEqual('tom',new_friend.name)
		home = HomePage(browser=dashboard.logout())

Since we have the page objects layer, we can write tests that reflects the actual user actions.
This test uses 3 pages objects:

* HomePage
* DashboardPage
* MyFriendsPage

Each page object has unique methods that map to the actions the user can take on this page.

The test also uses two application elements:

* FriendRequest 
* FriendObject

Here, the test uses the `FriendRequest` object's `approve` method. It can of course have other methods like `delete`, or a property like `request_date`.

## Install

1. To install Selenium:

		$ sudo pip install -U selenium
		
2. The default driver is Firefox, so you need Firefox installed. For Chrome (or Chromium) you will need to download additional Selenium-Chrome driver and set the CHROME_DRIVER settings. See [Settings](#settings).

2. If you don't have a `tests` directory in your project, add one.
2. In the `tests` directory, add the three page-objects directories from the repo: 

		tests/
			selenium_page_objects
			selenium_site
			selenium_test
	
3. The `selnium_page_objects` directory contains the base objects: pages, elements, forms, and helpers.
4. Subclass these base objects to the `selenium_site` directory, where you write the classes and the code for your site **specific** context. The specific pages, elements and forms. The selenium_site directory contains a few examples.
5. Finally, write and run the tests, based on `selenium_tests/test_template.py`. Copy the test template and write your tests (not via subclassing, but a simple copy of the file).
6. You may need to change the imports in the files to match your project and `PYTHONPATH`. Since tests are often run as scripts, and not as packages, try not to use relative imports.
7. To change defaults, add and adjust settings, see [Settings](#settings)

## Browser

The browser is the Selenium driver instance of a browser. The test case subclasses SeleniumWebTestCaseWithData, or SeleniumWebTestCaseBase, which opens a new driver instance available to the test with **self.browser**.

When the page object initiated, you have to provide a browser instance, so that the page __init__ method gets the page.

**Every method should return a browser**, so you run lines like:

	my_friends = MyFriendsPage(browser=dashboard.my_friends())
	
What happens here?

1. Previously defined, there is a "dashboard" page object, for the site "dashboard" page.
2. The tests calls the "my_friends" method of the dashboard page object (which could be a link or a buttor on the page)
2. This method moves the browser to the "my friends" page. It returns the browser instance.
3. The tests instansiate a MyFriendsPage page object with the browser instance, that now points to a "my friends" page

In a similar way, site elements are also initated with a browser:

	class Contact(elements_base.WebElementByID):
		...
		
	john = Contact(browser=self.browser,element_id='current_contact'):
	
This will create a "Contact" element object that maps to the HTML element with id="current_contact".    
This contact element may have methods like:

	john.follow()
	john.send_mesaage('foo')
	
All page objects, element objects and form objects have a "browser" attribute, so it's OK to test:

	john = Contact(browser=my_contacts_page.browser)
					

**To summarize: every page and element method should return a browser instance, and every page and element should initiated with `(browser=...)`**

## Actions

When many tests share the same repeating steps, it's easier to define an "action", a series of steps that the test can run in one call.

To continue with the above test example of a new friend request, the same test could be written with actions:

	def test_approve_request(self):
	
		sign_in = SignInAction(browser=self.browser)
		dashboard_page = sign_in.run(username='john',password='abcdef')
		approve_first = ApproveFirstRequestAction(browser=dashboard.browser)
		self.browser = approve_first.run()
		
		my_friends = MyFriendsPage(browser=self.browser)
		my_friends.sort_friends(recent=True)
		new_friend = my_friends.friends[0]
		self.assertEqual('tom',new_friend.name)
		home = HomePage(browser=dashboard.logout())

	
The more steps, pages and elements are involved, the more an action becomes useful.


## Page id

An optional but recommended test that each page object runs is that it instanciate the correct application page. A page_id is a hidden HTML attribute that the page object init tries to find when `CHECK_PAGE_ID = True` (see [Settings](settings.py)).

To add `page_id`, add the following snippet to the base template. It should run when the page is ready. If you use jQuery, put it in the `$(function(){})` script:

	$('body').append('<span id="page_id" page_id="{% block page_id %}base{% endblock page_id %}" style="display:none;"></span>');
	
Then in each template that extends the base template:

	{% block page_id %} my_contacts_page {% endblock page_id %}
	
And in the page object class:

	class MyContactsPage(LoginPage):	
		page_id = 'my_contacts_page'	
		def __init__(self,*args,**kwargs):
			...
			
When the test instanciate a MyContactsPage:

	my_contacts = MyContactsPage(browser=self.browser)
	
The page object will check that the page `self.browser` points to a page with the correct `page_id`. The test will fail if it's not. This is a very easy way to make sure that the application navigation works as expected, and to find out errors before the test tries to run some further code on the wrong page.    



## Settings

To changes the default page object selenium testing, add a dictionary named `SELENIUM` to the main site `settings.py` file.

These are the dictionary keys and defaults:

	SELENIUM = {
	    'EXCLUDE_FIELDS': ['csrfmiddlewaretoken'],
	    'CHROME_DRIVER': '/home/username/lib/chromedriver',# download the correct version https://sites.google.com/a/chromium.org/chromedriver/downloads
	    'WEBDRIVER_USE_BROWSER':'Firefox', # 'Firefox', etc
	    'SELENIUM_TIMEOUT_WEBDRIVER':2, # implicit wait, the default used when init the driver
	    'SELENIUM_TIMEOUT_PAGE_LOAD':2, # implict wait, the default for page id
	    'WAIT_FOR_ELEMENT_TIMEOUT':3, # implicit wait for element the wrapper
	    'DESIRED_CAPABILITIES': "",
	    'HOST': '127.0.0.1:8000', # to use the site host settings.ALLOWED_HOSTS[0]
	    'USE_HTTPS': False,
	    'CHECK_PAGE_ID': True
	}


**EXCLUDE_FIELDS**    
When you subclass a form with `WebFormById` or `WebFormByClass`, it automatically grabs all the text user input fields. These fields are then cleared with `clear`, or edited. If a text input field should be ignored by the test form manipulation code, add it to the `EXCLUDE_FIELDS`. The default is `['csrfmiddlewaretoken']`, which is used by django for CSRF and is not useful for any user input or user interaction.

**CHROME_DRIVER**    
Running selenium tests with Chrome (or Chromium), require a separate driver that matches the specific Chrome version on your machine.
Download the correct driver file from https://www.youtube.com/watch?v=9ox603IYU7U, and set this key to the path

**WEBDRIVER_USE_BROWSER**   
The browser that Selenium runs. The default is Firefox, which does not need any other driver after you install selenium.

**SELENIUM_TIMEOUT_WEBDRIVER**    
Wait in seconds for an element, before TimeOut exception when the element is not found. Increase for slow loading websites.

**SELENIUM_TIMEOUT_PAGE_LOAD**   
Wait in seconds for the `page_id` HTML element, which tells the test that the page is ready (see [Page id](#page-id)

**WAIT_FOR_ELEMENT_TIMEOUT**    
Implict wait for an HTML element in the Selenium wrapper methods. Useful when a specific element  takes more time to load. See [Wrapper](#wrapper).

**DESIRED_CAPABILITIES**   
Optional Selenium configs

**HOST**   
The website hosts. Use `127.0.0.1:8000` for the django development server, or  `www.example.com` for a remote site (e.g. `www.mystaging.com`).

**USE_HTTPS**    
If you test over HTTPS, set to True

**CHECK_PAGE_ID**    
Sets behaviour of page objects. By default, when instanciated, a page object will look for a "page id" element with the correct values. However, this will require to add "page id" to all templates and pages. If you don't use page id, set to False (not recomended). See [Page id]()


# Wrapper

The WebPageBase and WebElementBase classes have a "wrapper", you can use with self.wrapper. This is an instance of SeleniumWrapper, defined in the selenium_page_objects/wrapper.py module. From the elemnt, this wrapper is also available to forms.

The SeleniumWrapper is a simple wrapper to Selenium main find element methods, with optional wait arguments when finding a specific elemnt. When possible use this wrapper.

Instead of:

		def add_item(self):
		  	self.browser.find_elements_by_id("add_item).click()
         	return self.browser
        
Use:
        
		def add_item(self):
        	self.wrapper.get_html_element_by_id("add_item").click()
        	return self.browser
        	
The second add_item does not call the driver native find function, but the wrapper function.

This is useful, first because you can easily define additional waits for specific elements that require more time to load:

	def add_item(self):
        self.wrapper.get_html_element_by_id("add_item",wait=True).click()
        return self.browser
        
Another reaon to use the wrapper is that you will need it. As the application and the test suites evolve, you often need tweaks and waits, and with a wrapper you will have one place to do that, saving the need to find and adjust all the find element lines in your test suite.

    
		

## Best Paractices

### Use page id
Testing with page id may seem a hustle at first, to add page id to all templates, but it quickly pays of. You know that the application takes the user to where it should, and you don't waiste time on exceptions because of the wrong page.

### Instanciate a Page Object by Application Flow
You can instanciate a page with:

1.  Instanciate page with url, something like:
		
		user_settings = UserSettingsPage(url="/account/settings")

2. Instanciate page with a browser instance. Assume the test is on the "dashboard" page, could be:

		user_settings = UserSettingsPage(browser=dashboard.menu('settings))
		
		
You should use the option that matches the real user interaction. If users land in the user settings page with the menu, then the second option is better. But if users get to a page with a url, then the test should reflect it.

The home page is usually reached with a url:

	home_page = HomePage(url="/")
	
And you can even add this url to the page object __init__:

	class HomePage(PublicPage):
    
   	def __init__(self,*args,**kwargs):
   		self.page_id = 'home_page'
   		url = '/'
   		super(HomePage,self).__init__(url=url,*args,**kwargs)
   		self.form = forms.HomePageSignInForm(browser=self.browser)
   		return
   		
   		
### Waits
Many Selenium otherwise unexplained errors are solved with a simple wait. This is especially true for dynamic elements, like pop ups, hiding and showing elements, a lot of javascript when the page loads, or just slow pages.
 
You can adjust the time Selenium waits, in seconds, as follows:

Usage | Settings
-| -
The entire driver session |SELENIUM_TIMEOUT_WEBDRIVER
Wait until page loads to "ready" state | SELENIUM_TIMEOUT_PAGE_LOAD
Wait for a specific element | WAIT_FOR_ELEMENT_TIMEOUT, and use the wrapper calls with wait=True

### Website Main Menu
Add the main menu that is common to all the application pages in one base page class, and subclass to other page objects:
 
	class LoginPage(WebPageBase):
    	"""login required """
    
    	def init(self,*args,**kwargs):
    		...
    		
    	def add_item(self):
    		...
    		
    	def settings(self):
    		...
    		
    	def logout(self):
    		…
    		
    		
Or:

	class LoginPage(WebPageBase):
    	"""login required """
    
    	def init(self,*args,**kwargs):
    		...
    		
    	def menu(self,menu_select):
    		
    		if menu_select == 'add_item':
    			...
    			
    		
  
When you subclass LoginPage, the main menu is available to all pages.


### List View Pages

To repesent a list of items in a page, use **xpath**. In most web application every item has an id, or a uuid, so it's hard to know beforehand what this id will be when the test runs.    
Xpath is a convinient way to loop through the list by the item by **position**, regardless the id.

Map every item to an element object, with context methods like `edit`, `delete`, `update`, `approve` etc.

Coding against a "table of expesnes" page may look like this:


	class Expense(elements_base.WebElementByXPath):
		...
		
	class ExpensesPage(LoginPage):
	
		def __init__(self,*args,**kwargs):
			...
					
		@property
		def expenses(self):
			return self._expenses
    
    	@expenses.setter
    	def expenses(self,expenses_count):
        self._expenses = []
        for m in range(1,expenses_count+1):
        	expense = Expense(browser=self.browser,xpath="//*[@id="expenses_table"]/tbody/tr[%s]"%m
        	self._expenses.append(expense)
        	
        	
Then in the test, an expenses page with 5 expenses:

	exp_page = ExpensesPage(browser=self.browser)
	exp_page.expenses = 5
	
You can even add the expenses to the `__init__` method, so instanciating is:

	exp_page = ExpensesPage(browser=self.browser,expenses=5)
	
Do something with the 2nd expense:

	exp_page.expenses[1].approve()
	
	
### Context	
Page objects testing is better understood with real code, so after this README please review the [django-website](https://github.com/Aviah/django-website), a complete website with page objects testing: pages, elements, forms and data
	

## Automation is Not Everyting
Finally, automation is important, and efficiant, but it can't replace the look and feel of a manual testing, of real work with the application. Only with manual testing you can find things that are not easily understood, confusing, unclear.

It's even useful once in while to run the Selenium tests with a real browser, and just watch the app runs, make sure that it makes sense to a human.

Only with actual usage of the web application you suddenly spot bugs and errors that the best test suite and 100% coverage can not find - but the user will.

          	
