import requests
import base64
import json
import pandas as pd
import os


# GitHub repository details
owner = "hossain109"  # Replace with the GitHub username
repo = "webscrapping-automation"  # Replace with your repository name
branch = "main"  # The branch name, often 'main' or 'master'

# GitHub API URL to list files in the repository (recursively)
url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

# Send a request to the GitHub API
url_response = requests.get(url)

if url_response.status_code == 200:
    # Get the list of files in the repository
    files = url_response.json().get('tree', [])
    # Filter the files to get only the CSV files
    csv_files = [file['path'] for file in files if file['path'].endswith('.csv')and '/' not in file['path']]
else:
      print(f"Failed to fetch files from GitHub. Status code: {url_response.status_code}")

# Print the names of all CSV files found
print(csv_files)
for csv_file in csv_files:
      csv_url = f"https://raw.githubusercontent.com/hossain109/webscrapping-automation/main/{csv_file}"
      print(csv_url)
      df = pd.read_csv(csv_url)

      #name of parent category where new category will be created
      parent_cat="DevOps"

      # Get the base name (file name with extension)
      file_name_with_ext = os.path.basename(csv_url)
      # Get the file name without the extension for category name
      category_name = os.path.splitext(file_name_with_ext)[0]

      # Your WordPress credentials
      # username = 'sohrab'
      # password = '*Taspiasohrab109*'
      # credentialtriboucloud
      password="N$GvmlTV*n46Ke*Ks6SyTqDo"
      username="Samarah"

      # Prepare the headers for authentication
      credentials = f"{username}:{password}"
      token = base64.b64encode(credentials.encode())
      headers = {
      'Authorization': f'Basic {token.decode("utf-8")}',
      'Content-Type': 'application/json'
      }

      #triboucloud category
      categories_url='https://blog.tribucloud.com/wp-json/wp/v2/categories'
      #category wordpressite
      # categories_url='http://localhost/wordpress-automation/wp-json/wp/v2/categories'

      # Function to get the parent category ID by name
      def get_parent_category_id_by_name(p_category_name):
            response = requests.get(categories_url, headers=headers, params={'search': p_category_name})
            p_categories = response.json()
            if p_categories:
                  for p_category in p_categories:
                        if p_category['name'].lower() == parent_cat.lower():
                              return p_category['id']
            else:
                  print(" Parent category not found.")
                  return None

      # Function to get or create category by name
      def get_or_create_child_category(c_category_name):
            #findout parent category
            parent_id = get_parent_category_id_by_name(parent_cat)
            # Check if the category already exists
            response = requests.get(categories_url, headers=headers, params={'search': c_category_name})
            categories = response.json()
            if categories:  # If the category exists, return the ID
                  return categories[0]['id']
            
            # Otherwise, create a new category
            new_category_data = {
                  'name': category_name,
                  'parent': parent_id, #Adding parent category
                  'slug':"devops-"+category_name,
                  'description':"devops"
            }
            response = requests.post(categories_url, headers=headers, data=json.dumps(new_category_data))
            print(response)
            if response.status_code == 201:  # Successfully created category
                  new_category = response.json()
                  return new_category['id']
            else:
                  print(f"Failed to create category")
                  return None


      # Iterate over CSV data
      for index, row in df.iterrows():
            category_id = get_or_create_child_category(category_name)
            #print(category_id)
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
                  response = requests.post('https://blog.tribucloud.com/wp-json/wp/v2/posts', headers=headers, data=json.dumps(post_data))
                  #send a post resques to perso wordpress
                  # response = requests.post('http://localhost/wordpress-automation/wp-json/wp/v2/posts', headers=headers, data=json.dumps(post_data))

                  if response.status_code == 201:
                        print(f"Post created successfully for row {index}")
                  else:
                        print(f"Failed to create post for row {index}: {response.content}")
            else:
                  print("category creation failure.")