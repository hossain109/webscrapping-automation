import requests
import base64
import json
import pandas as pd
import os
import re

csv_url = "https://raw.githubusercontent.com/hossain109/webscrapping-automation/main/AI.csv"

df = pd.read_csv(csv_url)

# Get the base name (file name with extension)
file_name_with_ext = os.path.basename(csv_url)
# Get the file name without the extension for category name
category_name = os.path.splitext(file_name_with_ext)[0]

# Your WordPress credentials
username = 'sohrab'
password = '*Taspiasohrab109*'

# Prepare the headers for authentication
credentials = f"{username}:{password}"
token = base64.b64encode(credentials.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

categories_url = 'http://localhost/wordpress-automation/wp-json/wp/v2/categories'

# Function to get the parent category ID by name
def get_parent_category_id_by_name(category_name):
    response = requests.get(categories_url, headers=headers, params={'search': category_name})
    categories = response.json()
    
    if categories:
        return categories[0]['id']
    else:
        print(" Parent category not found.")
        return None

# Function to get or create category by name
def get_or_create_child_category(category_name):
      #findout parent category
      parent_id = get_parent_category_id_by_name("DevOps")
      # Check if the category already exists
      response = requests.get(categories_url, headers=headers, params={'search': category_name})
      categories = response.json()
      
      if categories:  # If the category exists, return the ID
            return categories[0]['id']
      
      # Otherwise, create a new category
      new_category_data = {
            'name': category_name,
            'parent': parent_id, #Adding parent category
            'slug':"devops"+category_name,
           'description':"devops"
           }
      response = requests.post(categories_url, headers=headers, data=json.dumps(new_category_data))
      
      if response.status_code == 201:  # Successfully created category
            new_category = response.json()
            return new_category['id']
      else:
            print(f"Failed to create category")
            return None


# Iterate over CSV data
for index, row in df.iterrows():
      category_id = get_or_create_child_category(category_name)
      #category id exist or not
      if category_id:
            # Data for creating a post in WordPress
            post_data = {
                  'title': row['Title'],  # Column name from CSV
                  'content': row['Content'],  # Another column
                  'categories': [category_id],  # Adding the category ID to the post
                  'status': 'draft'  # Set to 'draft' if you don't want to publish immediately
            }

            # Send a POST request to WordPress
            response = requests.post('http://localhost/wordpress-automation/wp-json/wp/v2/posts', headers=headers, data=json.dumps(post_data))

            if response.status_code == 201:
                  print(f"Post created successfully for row {index}")
            else:
                  print(f"Failed to create post for row {index}: {response.content}")
      else:
           print("category creation failure.")