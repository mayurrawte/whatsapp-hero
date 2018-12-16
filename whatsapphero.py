import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import os

class WhatsappHeroCore():
    def scan_qr(self):
        wait_for_scan = True
        while wait_for_scan:
            #check every two second
            time.sleep(2)
            try:
                qr = self.driver.find_element_by_xpath('//img[@alt="Scan me!"]')
                self.driver.save_screenshot("scan_me.png")
            except NoSuchElementException:
                wait_for_scan = False
                # ready to go
        return True
    def get_element_by_xpath(self, xpath = '/'):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            return element
        except NoSuchElementException:
            return False
    def get_elements_by_xpath(self, xpath= '/'):
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            if elements and len(elements):
                return elements
            return []
        except Exception as e:
            print(e)
            return []
    
    def is_logged_in(self):
        if self.get_element_by_xpath('//img[@alt="Scan me!"]'):
            return False
        time.sleep(5)
        return True

    def wait_for_element_by_xpath(self, xpath = '/'):
        delay = 3
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False



class WhatsappHero(WhatsappHeroCore):

    def __init__(self,browser='chrome', browser_path='/tmp/chromeheadless', username='person1', headless=False):
        self.browser = browser
        self.browser_path = browser_path
        profiledir=os.path.join(".","chrome_cache")
        if not os.path.exists(profiledir):
            os.makedirs(profiledir)
        if browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("user-data-dir=%s" % profiledir)
            if headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('start-maximized') 
                # chrome_options.add_argument('disable-infobars')
                chrome_options.add_argument("--disable-extensions")
            self.driver = webdriver.Chrome(options=chrome_options)

        ## read class names from helper file
        try:
            self.config = json.loads(open('config.json', 'r+').read())
        except Exception as e:
            print(e)
            print('invalid helper json')

    '''
    Get Class Names defined in helper file
    '''
    def get_class_name(self, key):
        return self.config['class_names'].get(key, '')

    '''
    login using qr code scan
    will wait while you scan the code
    you can scan the code from the qr.png file
    '''
    def login(self):
        self.driver.get('https://web.whatsapp.com')
        time.sleep(2)
        if not self.is_logged_in():
            self.scan_qr()
        return self.wait_for_element_by_xpath('//*[@id="side"]')

    '''
        get most recent received message
    '''
    def get_latest_message(self):
        most_recent_contact = self.get_element_by_xpath('//*[@class="_2wP_Y"]')
        recent_contact = most_recent_contact.find_element_by_xpath('//span[@dir="auto"]').text
        recent_message = most_recent_contact.find_element_by_xpath('//*[@class="_itDl"]').text
        return recent_contact + ' sent ' + recent_message

    '''
        get element of all the unread message list
    '''
    def get_unread_message_contact_list(self):
        xpath = '//*[@class="' + self.get_class_name('left_area_unread_message_icon') + '"]/../../../../..'
        unseen_contacts = self.get_elements_by_xpath(xpath)
        return unseen_contacts

    '''
        ?
    '''
    def get_all_messages_of_contact(self):
        pass
        # xpath = '//*[@class="' + self.get_class_name('chat_area_all_messages') + '"]'

    '''
        NOTE - Before calling this function make sure you already have a contact chat area open
        get all the unread messages of the user 
    '''
    def get_unread_messages_of_contact(self):
        messages = []
        # xpath = '//*[@class="' + self.get_class_name('chat_area') + '"]/div[@class="'+self.get_class_name('chat_message')+'"]'
        xpath = '//*[@class="' + self.get_class_name('chat_area') + '"]//span[contains(concat(" ", @class, " "), " selectable-text ")]'
        print(self.get_elements_by_xpath(xpath))
        unseen_messages_elements = self.get_elements_by_xpath(xpath)
        for message_element in unseen_messages_elements:
            if message_element.get_attribute('class') == self.get_class_name('chat_area_unread_message_box'):
                break
            # text = message_element.find_element_by_xpath('//*[@class="'+self.get_class_name('chat_message')+'"]')
            messages.append(message_element.text)
        return messages

    def get_all_chat_contact_list(self):
        xpath = '//*[@class="' + self.get_class_name('left_area_all_chat_contacts') + '"]/div'
        all_chat_contacts = self.get_elements_by_xpath(xpath)
        return all_chat_contacts
    
    '''
       NOTE - Before calling this function make sure you already have a contact chat area open
       reply to a contact  
    '''
    def reply_to_contact(self, message):
        xpath = '//div[text()="Type a message"]/../div[2]'
        chat_text_area = self.get_element_by_xpath(xpath)
        chat_text_area.send_keys(message)
        send_button = self.get_element_by_xpath('//*[@class="_35EW6"]')
        if send_button:
            send_button.click()
