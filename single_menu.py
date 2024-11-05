from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

# # Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')  # Ignore SSL issues (if needed)
chrome_options.add_argument('--start-maximized')

# Set the path to your ChromeDriver
chrome_path = r"C:\webscrapping-automation\chromedriver.exe"

# Create a Service object
service = Service(chrome_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

translator = GoogleTranslator(source='auto', target='fr')

# Open the webpage
nav_url = "https://devops.com/category/blogs/ai/"
driver.get(nav_url)

# data clean and convert into string
def clean_and_convert_to_string(data):
    # Initialize an empty list to store valid HTML strings
    html_parts = []

    # Iterate through each item in the data
    for item in data:
        # Since the items are sets, extract the string from the set
        # Here, we assume each set contains exactly one string item
        # Convert the set to a list and get the first element
        string_item = list(item)[0] if isinstance(item, set) and len(item) == 1 else item
        
        # Check if the extracted item is a string
        if isinstance(string_item, str):
            # Append to the list of HTML parts
            html_parts.append(string_item)

    # Join all parts into a single HTML string
    return ''.join(html_parts)

try:
    # Wait for the overlay to appear and remove it if found
    overlay = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sgpb-popup-overlay"))
    )
    if overlay:
        driver.execute_script("arguments[0].remove();", overlay)
    print("Popup removed successfully.")
except TimeoutException:
    print("No popup to close or issue closing it.")

count=0
while True:
    try:
        if count<0:
            # Locate and click the "Show More" button
            link = driver.find_element(By.LINK_TEXT, 'Show More')
            link.click()
        
            # Optional: Sleep to allow page content to load
            time.sleep(2)
        else:
            # Simulate NoSuchElementException after count >= 2
            raise NoSuchElementException("Count exceeded 2, simulating NoSuchElementException.")
        count=count+1

    except NoSuchElementException:
        # Collect
        print("Collecting page resources before exiting...")

        # Collect page source just before the exception is thrown
        html_source = driver.page_source
        p_soup = bs(html_source, 'html.parser')
        p_conts = p_soup.findAll("div",{"class":"pt-cv-ifield"})
        # open each article read and insert data into list
        #declaration array
        all_articles=[]
        for p_cont in p_conts:
                #search link of title
                title_link_tag=p_cont.find('a', href=True)
                title_url = title_link_tag.get("href")
                print(title_url)
                #collect content from article
                response_content=rq.get(title_url)
                if response_content.status_code==200:
                    a_soup=bs(response_content.text,"html.parser")

                    content = a_soup.find('div',{"class":"entry-content"})
                    # Initialize lists for storing data
                    article = []
                    element=""
                    main_header_value=a_soup.find("h1",{"class":"entry-title"}).text
                    main_header=translator.translate(main_header_value)
                    # Loop through the elements and append headers and article correctly
                    for elem in content.find_all(['h3','h4','li','ol','blockquote', 'p','img']):
                        if elem.name in ['h3']:
                            element = elem.text.strip()  # Store the latest header
                            #translate in french
                            if element:
                                    element=translator.translate(element)
                                    element="<h3>"+element+"</h3>"
                            else: current_header=''
                        elif elem.name == 'p':
                            element = elem.text.strip()
                            #translate in french
                            if element:
                                    element=translator.translate(element)
                                    element="<p>"+element+"</p>"
                            else: element=''
                        elif elem.name == 'h4':
                            element = elem.text.strip()
                            #translate in french
                            if element:
                                    element=translator.translate(element)
                                    element="<h4>"+element+"</h4>"
                            else: element=''

                        elif elem.name == 'li':
                            element = elem.text.strip()
                            #translate in french
                            if element:
                                    element=translator.translate(element)
                                    element="<li>"+element+"</li>"
                            else: element=''
                        
                        elif elem.name == 'ol':
                            element = elem.text.strip()
                            #translate in french
                            if element:
                                    element=translator.translate(element)
                                    element="<ol>"+element+"</ol>"
                            else: element=''
                        
                        elif elem.name == 'blockquote':
                            element = elem.text.strip()
                            #translate in french
                            if element:
                                    element=translator.translate(element)
                                    element="<blockquote>"+element+"</blockquote>"
                            else: element=''
                        # elif elem.name == 'svg':
                        #     #take image source
                        #     element = elem
                        #     print(elem)
                                 

                        article.append({element})
                        element=''

                resulting_html_string = clean_and_convert_to_string(article)
                # put all articles in list
                all_articles.append({"Title":main_header,"Content":resulting_html_string})
        
        #data convert into csv
        display_articles = pd.DataFrame(all_articles,columns = ['Title', 'Content'])
        display_articles.to_csv('AI.csv',encoding='utf-8',index=False)
        print("finished")
        
        break  # Exit the loop