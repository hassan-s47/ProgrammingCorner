
#importing libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

#Class for Scrapper
class Scrapper:
   #Declaring Variables
   options = webdriver.ChromeOptions()
   #Standard user agent
   user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
   #Url for website 
   url = "https://www.codesdope.com/practice/practice_cpp/"
   #Driver for scrapping
   driver = None
   def __init__(self):
      #initializing options
      self.options.headless = True
      self.options.add_argument(f'user-agent={self.user_agent}')
      self.options.add_argument("--window-size=1920,1080")
      self.options.add_argument('--ignore-certificate-errors')
      self.options.add_argument('--allow-running-insecure-content')
      self.options.add_argument("--disable-extensions")
      self.options.add_argument("--proxy-server='direct://'")
      self.options.add_argument("--proxy-bypass-list=*")
      self.options.add_argument("--start-maximized")
      self.options.add_argument('--disable-gpu')
      self.options.add_argument('--disable-dev-shm-usage')
      self.options.add_argument('--no-sandbox')
      #initializing driver with options and ChromeDriverManager and opening the headless browser
      self.driver = webdriver.Chrome (ChromeDriverManager().install(),options = self.options)



   def getquestionlist(self,topic):
      try:
         self.driver.get(self.url)
         results =  self.driver.find_elements_by_xpath("//*[@class='topic_name']")
         
         for res in results:
            if topic == res.get_attribute ("innerText"):
               topic = res


         #navigating to the topic page
         topic.click()

         results =  self.driver.find_elements_by_xpath("//*[@class='ques_title']")
         return results
      
      except:
         return None