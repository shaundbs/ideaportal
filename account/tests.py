from django.test import TestCase
import faker
from selenium import webdriver
import time
import random
from faker import Faker

fakegen = Faker()

class FunctionalTestCase(TestCase):

    def generate_username():
        return faker.first_name

    def setUp(self):
        self.browser = webdriver.Firefox()

    password_list=['Mark_dkjdjkdkj', 'Amber_Mark_dkjdjkdkj', 'Todd_Mark_dkjdjkdkj', 'Anita_Mark_dkjdjkdkj',
     'Sandy_Mark_dkjdjkdkj', 'Goober_Mark_dkjdjkdkj', 'Ralph_dkjdjkdkj', 'Jake_dkjdjkdkj', 'Phillip_dkjdjkdkj', 'Shaun_dkjdjkdkj']

    def password_gen(self):
        return random.choice(self.password_list)

    

    # def test_there_is_homepage(self):
    #     self.browser.get('http://localhost:8000')
    #     self.assertIn('Sign In', self.browser.page_source)
    #     time.sleep(5)

    def test_registration(self):

        # Create account
        self.browser.get('http://localhost:8000')    
        createAccountBut = self.browser.find_element_by_xpath("//a[contains(text(), 'Click to create an account')]")
        createAccountBut.click()
        time.sleep(1.5)
        registerBut = self.browser.find_element_by_xpath("//span[contains(text(), 'Register with us')]")
        registerBut.click()
        time.sleep(1.5)
        usernameBox = self.browser.find_element_by_xpath("//input[@id='id_username']")
        gen_username = str(random.randrange(0,5000))
        usernameBox.send_keys('Random_user' + gen_username)
        time.sleep(1.5)
        emailBox = self.browser.find_element_by_xpath("//input[@id='id_email']")
        emailBox.send_keys('random' + str(random.randrange(0,5000)) + '@nhs.net')
        password1 = self.browser.find_element_by_xpath("//input[@id='id_password1']")
        password1.send_keys("Persona_123")
        password2 = self.browser.find_element_by_xpath("//input[@id='id_password2']")
        password2.send_keys("Persona_123")
        time.sleep(1.5)
        continueBut = self.browser.find_element_by_xpath("//button[@class='nhsuk-button']")
        continueBut.click()


        time.sleep(1.5)
        continueBut2 = self.browser.find_element_by_xpath("//button[contains(text(), 'Continue')]")
        chosenAge = self.browser.find_element_by_xpath("//input[@value='21-30']")
        chosenAge.click()
        continueBut2.click()

        time.sleep(1.5)
        continueBut3 = self.browser.find_element_by_xpath("//button[@id='submit-button']")
        chosenJob = self.browser.find_element_by_xpath("//input[@value='Yes']")
        chosenJob.click()
        continueBut3.click()

        time.sleep(1.5)
        chosenInterest1 = self.browser.find_element_by_xpath("//input[@value='culture']")
        chosenInterest2 = self.browser.find_element_by_xpath("//input[@value='leadership']")
        continueBut4 = self.browser.find_element_by_xpath("//button[@class='nhsuk-button']")

        chosenInterest1.click()
        chosenInterest2.click()
        continueBut4.click()

        time.sleep(1.5)
        logBackInBut = self.browser.find_element_by_xpath("//button[contains(text(), 'Login')]")
        logBackInBut.click()

        time.sleep(5)

        portalUsername = self.browser.find_element_by_xpath("//input[@name='username']")
        portalUsername.send_keys('Random_user' + gen_username)

        time.sleep(1.5)
        portalPassword = self.browser.find_element_by_xpath("//input[@name='password']")
        portalPassword.send_keys('Persona_123')

        portalLogin = self.browser.find_element_by_xpath("//input[@name='Login']")
        portalLogin.click()
        time.sleep(10)
        if self.browser.find_element_by_xpath("//header[@class='nhsuk-header']"):
            print('ELEMENT LOCATED - Login Successful')
        else:
            print('ERROR - element not located')
        
        














        
        
    def tearDown(self):
        self.browser.quit()


# class UnitTestCase(TestCase):

    # def test_home_homepage_template(self):
    #     response = self.client.get('/')
    #     self.assertTemplateUsed(response, 'authentication/home.html')

    # def test_registration_template(self):
    #     response = self.client.get('/register/')
    #     self.assertTemplateUsed(response, 'userauth/register.html')

    # def test_sign_in_template(self):
    #     response = self.client.get('/sign_in/')
    #     self.assertTemplateUsed(response, 'userauth/sign_in.html')

    # def test_hash_form(self):
    #     form = UserauthForm(data={'text':'hello'})
    #     self.assertTrue(form.is_valid())
