from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from textblob import TextBlob
import pandas as pd

from datetime import datetime
import time

#BBC Constants
NEWS_PAGES=1
MAX_NEWS_PER_PAGE=8

#CNBC Constants
CNBC_MAX_NEWS=3
DATE_FORMAT="%b %d %Y %I:%M %p %Z"


def get_news_analysis(source, topic, data):
  service = Service(executable_path='resources\\chromedriver-win64\\chromedriver.exe')
  options = webdriver.ChromeOptions()
  driver = webdriver.Chrome(service=service, options=options)
  wait = WebDriverWait(driver, 20)

  if source=='BBC':
    driver.get('https://www.bbc.com/news')

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Search BBC"]'))).click()
    search_bar=driver.find_element(By.CSS_SELECTOR, '[data-testid="search-input-field"]')
    search_bar.send_keys(topic)
    search_bar.send_keys(Keys.RETURN)

    for page in range(NEWS_PAGES):
      for new_index in range(MAX_NEWS_PER_PAGE):
        news_data=[]

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="card-headline"]')))
        news_cards=driver.find_elements(By.CSS_SELECTOR, '[data-testid="card-headline"]')
        news_cards[new_index].click()

        try:
          new_header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-component="headline-block"]')))
          new_header_text=new_header.text

          new_date=driver.find_element(By.XPATH, '//time')

          new_content=driver.find_elements(By.CSS_SELECTOR, '[data-component="text-block"]')
          new_content_text=''

          for new_paragraph in new_content:
            new_content_text+=new_paragraph.text

          analysis = TextBlob(new_header_text+' '+new_content_text)

          news_data.append(pd.to_datetime(new_date.text))
          news_data.append(analysis.sentiment.polarity)
          news_data.append(analysis.sentiment.subjectivity)
          data.append(news_data)

        except:
          print(f"Attempt {new_index+1}: Element not visible yet. Retrying...")
        driver.back()
        
      next_button=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="pagination-next-button"]')))
      next_button.click()
  
  if source=='Yahoo':
    driver.get('https://finance.yahoo.com/')

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="ybar_mod_searchbox_s"] input'))).click()
    search_bar=driver.find_element(By.CSS_SELECTOR, '[name="ybar_mod_searchbox_s"] input')
    search_bar.send_keys(topic)
    driver.find_element(By.CSS_SELECTOR, 'button[id="ybar-search"]').click()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[title="News"]'))).click()
    time.sleep(50)

  if source=='CNBC':
    driver.get('https://www.cnbc.com/search/')

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[id="query"]')))
    search_bar=driver.find_element(By.CSS_SELECTOR, 'input[id="query"]')
    search_bar.send_keys(topic)
    search_bar.send_keys(Keys.RETURN)
    
    for new_index in range(CNBC_MAX_NEWS):
      news_data=[]

      wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="Card-title"]')))
      news_cards=driver.find_elements(By.CSS_SELECTOR, '[class="Card-title"]')
      news_cards[new_index].click()

      new_header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1[class="ArticleHeader-headline"]')))
      new_header_text=new_header.text

      new_date=driver.find_element(By.CSS_SELECTOR, 'time[data-testid="published-timestamp"]').text
      parsed_date = new_date.split(',')[1]
      parsed_date = datetime.strptime(parsed_date,DATE_FORMAT)

      new_content=driver.find_elements(By.CSS_SELECTOR, 'div[class="group"] p')
      new_content_text=''

      for new_paragraph in new_content:
        new_content_text+=new_paragraph.text

      analysis = TextBlob(new_header_text+' '+new_content_text)
      print(new_content_text)
      print('________________')

      news_data.append(pd.to_datetime(parsed_date))
      news_data.append(analysis.sentiment.polarity)
      news_data.append(analysis.sentiment.subjectivity)
      data.append(news_data)

      driver.back()
      time.sleep(5)
    

  
