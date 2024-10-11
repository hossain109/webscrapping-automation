import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from googletrans import Translator
from deep_translator import GoogleTranslator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


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

my_url = 'https://devops.com'

response = rq.get(my_url)
p_soup = bs(response.text,"html.parser")
#findout all menus
menus = p_soup.findAll("li",{"class":"menu-item"})
#cretae translator object
#translator = Translator()
translator = GoogleTranslator(source='auto', target='fr')

#findout title and article for each menu item
for menu in menus:
      href_tag=menu.find('a', href=True)
      nav_url=href_tag.get("href")
      response_nav = rq.get(nav_url)
      # Check url: if the response status is 200 (OK)
      if response.status_code == 200:
            p_soup = bs(response_nav.text,"html.parser")
            #findout all articles
            p_conts = p_soup.findAll("div",{"class":"pt-cv-ifield"})
            #find out heading for file name
            text_menu=menu.find('span').text.replace('/', '-')
            #declaration array
            all_articles=[]

            # open each article read and insert data into list
            for p_cont in p_conts:
                  #search link of title
                  title_link_tag=p_cont.find('a', href=True)
                  title_url = title_link_tag.get("href")
                  #collect content from article
                  response_content=rq.get(title_url)
                  if response.status_code==200:
                        a_soup=bs(response_content.text,"html.parser")

                        content = a_soup.find('div',{"class":"entry-content"})
                        # Initialize lists for storing data
                        article = []
                        element=""
                        main_header_value=a_soup.find("h1",{"class":"entry-title"}).text
                        main_header=translator.translate(main_header_value)
                        main_header = main_header
                        # Loop through the elements and append headers and paragraphs correctly
                        for elem in content.find_all(['h3','h4','li','ol','blockquote', 'p']):
                              if elem.name in ['h3']:
                                    element = elem.text.strip()  # Store the latest header
                                    #translate in french
                                    if element:
                                          element=translator.translate(element)
                                          element="<h3>"+element+"</h3>"
                                    else: element=''
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

                              article.append({element})
                              element=''
                              
                  resulting_html_string = clean_and_convert_to_string(article)
                  # put all articles in list
                  all_articles.append({"Title":main_header,"Content":resulting_html_string})
            
            #data convert into csv
            display_articles = pd.DataFrame(all_articles,columns = ['Title', 'Content'])
            display_articles.to_csv(f'{text_menu}.csv',encoding='utf-8',index=False)
      # Continue processing, e.g., parse the content
      else:
            print("Request failed ! page not exist")