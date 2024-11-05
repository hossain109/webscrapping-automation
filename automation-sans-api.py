from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Set the path to your ChromeDriver
chrome_path = "C:/Scrapping/chromedriver.exe"

# Create a Service object
service = Service(chrome_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Open the webpage
driver.get("https://blog.tribucloud.com/ssl-aes256")
# driver.get('http://localhost/wordpress-automation/wp-login.php')


# Step 1: Read the CSV file
datas = pd.read_csv("AI.csv")
# Get the base name (file name with extension)
file_name_with_ext = os.path.basename("AI.csv")
# Get the file name without the extension for category name
file_name = os.path.splitext(file_name_with_ext)[0]


# define function for login wordpress
password="N$GvmlTV*n46Ke*Ks6SyTqDo"
username="Samarah"
# password="*Taspiasohrab109*"
# username="sohrab"


#define a function for wordpress article content
def clean_for_wordpress(content):
    # Remove unnecessary characters like {}, '' and double quotes surrounding the tags
    cleaned_content = re.sub(r'[{}\[\]""\'\']', '', content)

    # Remove commas
    cleaned_content = cleaned_content.replace(',', '')
    # Optional: Strip any excess whitespace
    cleaned_content = cleaned_content.strip()
    
    return cleaned_content

def login():
    usernamebox = driver.find_element(by=By.ID,value="user_login")
    usernamebox.send_keys(username)
    passwordbox = driver.find_element(by=By.ID,value="user_pass")
    passwordbox.send_keys(password)
    #click on login button
    button_login = driver.find_element(by=By.ID, value="wp-submit")
    button_login.click()

#create category
def category():
    #click on Artilces
    menu_articles= driver.find_element(By.LINK_TEXT, 'Articles')
    menu_articles.click()
    #click on Categories
    menu_category= driver.find_element(By.LINK_TEXT,'Catégories')
    menu_category.click()
    #add category
    category_name=driver.find_element(by=By.ID,value="tag-name")
    category_name.send_keys(file_name)
    slug_name=driver.find_element(by=By.ID,value='tag-slug')
    slug_name.send_keys('devops'+'-'+file_name)
    parent_category=driver.find_element(by=By.ID,value='parent')
    parent_category.send_keys("DevOps")
    tag_description=driver.find_element(by=By.ID,value='tag-description')
    #add button
    button_category=driver.find_element(by=By.ID,value='submit')
    button_category.click()

# define function automation wordpress article
def do_action():
    #click on Artilces
    menu_articles= driver.find_element(By.LINK_TEXT, 'Articles')
    menu_articles.click()
    #add a article
    add_article = driver.find_element(by=By.CLASS_NAME,value="page-title-action")
    add_article.click()
    #click for list block
    wp_button_list = driver.find_element(by=By.CLASS_NAME,value='editor-document-tools__inserter-toggle')
    wp_button_list.click()

    #scroll click for html block
    wp_button_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.editor-block-list-item-html')))
    wp_button_button.click()
    #send title
    wp_title = driver.find_element(by=By.CLASS_NAME,value='wp-block-post-title')
    wp_title.send_keys(title)
    #send content
    wp_content = driver.find_element(by=By.CLASS_NAME,value='block-editor-plain-text')
    wp_content.send_keys(content)

    # Find the button by its aria-label
    regle_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Réglages"]')

    # Get the class attribute of the button
    button_class = regle_button.get_attribute('class')
    # Check if the class 'is-pressed' is present
    if 'is-pressed' not in button_class:
        regle_button.click()
    
    button_article=driver.find_element(By.ID,'tabs-0-edit-post/document')
    button_article.click()
    #scroll click on categorie 
   # Wait until the 'Catégories' element is located
    categories_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Catégories')]")))
    
    #check button already open or not
    aria_expanded=categories_button.get_attribute('aria-expanded')
    if aria_expanded=="false":
        categories_button.click()
 
    #Checked category in wordpress
    label_elements = driver.find_elements(By.CLASS_NAME, 'components-checkbox-control__label')
    for label_element in label_elements:
        if label_element.text==file_name:
            checkbox_id = label_element.get_attribute("for")
            if checkbox_id:
                checkbox = driver.find_element(By.ID, checkbox_id)
                if not checkbox.is_selected():
                    checkbox.click()
            else: print("No associated checkbox")
    time.sleep(5)
    #save into draft
    wp_save = driver.find_element(by=By.CLASS_NAME,value='editor-post-save-draft')
    wp_save.click()
    wp_les_article = driver.find_element(by=By.CLASS_NAME,value='edit-post-fullscreen-mode-close')
    wp_les_article.click()
#check csv data exist
if len(datas)!=None:
    for index in range(0,len(datas)):
        title = datas["Title"][index]
        #clean data with function
        cleaned_content = clean_for_wordpress(datas["Content"][index])
        content=cleaned_content

        try:
            displayname = driver.find_element(by=By.CLASS_NAME,value="display-name")
            if(displayname.text==username):
                    print("Login sucessful")
                    #automation wordpress when you are login
                    do_action()
                    #time.sleep(10)
            else: 
                print("not match")
                login()
                if(displayname.text==username):
                    do_action()

                    # time.sleep(10)
        except:
            #first time login
            login()
            displayname = driver.find_element(by=By.CLASS_NAME,value="display-name")
            if(displayname.text==username):

                #create category
                category()
                #call method automation wordpress when login successful
                do_action()
            else: print("login error")
else : print("No data")


      
