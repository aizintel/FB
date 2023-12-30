import subprocess
import sys
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def install_dependencies():
    dependencies = ['requests', 'beautifulsoup4']
    installed_count = 0

    for dep in dependencies:
        sys.stdout.write(f"\rInstalling {dep}... ({installed_count}/{len(dependencies)})")
        sys.stdout.flush()

        try:
            subprocess.run(['pip', 'install', dep], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            installed_count += 1
        except subprocess.CalledProcessError as e:
            print(f"\nError installing {dep}: {e.stderr.decode('utf-8')}")

    sys.stdout.write("\n")

def check_dependencies():
    try:
        import requests
        from bs4 import BeautifulSoup
        return True
    except ImportError:
        return False


clear_screen()

if check_dependencies():
    print("Dependencies are already installed.")
else:
    print("Dependencies not found. Installing...")
    time.sleep(2) 
    clear_screen()


    install_dependencies()


import time
import random
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import threading
import re


def get_user_cookie(user_email, user_password):
  url = 'https://n.facebook.com'
  xurl = url + '/login.php'
  user_agent = "Mozilla/5.0 (Linux; Android 4.1.2; GT-I8552 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
  req = requests.Session()
  req.headers.update({
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en_US',
      'cache-control': 'max-age=0',
      'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': "Windows",
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': user_agent
  })
  with req.get(url) as response_body:
      inspect = bs(response_body.text, 'html.parser')
      lsd_key = inspect.find('input', {'name': 'lsd'})['value']
      jazoest_key = inspect.find('input', {'name': 'jazoest'})['value']
      m_ts_key = inspect.find('input', {'name': 'm_ts'})['value']
      li_key = inspect.find('input', {'name': 'li'})['value']
      try_number_key = inspect.find('input', {'name': 'try_number'})['value']
      unrecognized_tries_key = inspect.find('input', {'name': 'unrecognized_tries'})['value']
      bi_xrwh_key = inspect.find('input', {'name': 'bi_xrwh'})['value']
      data = {
          'lsd': lsd_key, 'jazoest': jazoest_key,
          'm_ts': m_ts_key, 'li': li_key,
          'try_number': try_number_key,
          'unrecognized_tries': unrecognized_tries_key,
          'bi_xrwh': bi_xrwh_key, 'email': user_email,
          'pass': user_password, 'login': "submit"
      }
      response_body2 = req.post(xurl, data=data, allow_redirects=True, timeout=300)
      cookie = str(req.cookies.get_dict())[1:-1].replace("'", "").replace(",", ";").replace(":", "=")

      if 'c_user' in cookie:
          return (cookie) 
      else:
          return None
        
def get_facebook_token(cookie):
  headers = {
      'authority': 'business.facebook.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
      'cache-control': 'max-age=0',
      'cookie': cookie,
      'referer': 'https://www.facebook.com/',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
  }
  try:
      home_business = requests.get('https://business.facebook.com/content_management', headers=headers).text
      token = home_business.split('EAAG')[1].split('","')[0]
      return f'{cookie}|EAAG{token}'
  except Exception as e:
      return None


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_post_id(url):
    response = requests.post('https://id.traodoisub.com/api.php', data={'link': url})
    post_id_link = response.json().get('id')
    print(response.json())
    return post_id_link 

def is_cookie_alive(cookie):
    headers = {
        'authority': 'business.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'referer': 'https://www.facebook.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }
    try:
        response = requests.get('https://business.facebook.com/content_management', headers=headers)
        return response.ok
    except Exception as e:
        print(f"Error checking if the cookie is alive")
        return False



def perform_share(token_data, post_id, success_counter):
    cookie, token = token_data.split('|')
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'connection': 'keep-alive',
        'content-length': '0',
        'cookie': cookie,
        'host': 'graph.facebook.com'
    }
    try:
        response = requests.post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{post_id}&published=0&access_token={token}', headers=headers).json()
        if 'id' in response:
            success_counter[0] += 1
            print(f'Share successful for post ID {post_id} - {success_counter[0]}')
        else:
            print(f'Error during sharing. Response: {response}')
    except Exception as e:
        print(f"Error sharing: {e}")


def auto_share_on_facebook_post():
    user_email = input("Enter your Facebook Email: ")
    user_password = input("Enter your Facebook Password: ")
    user_cookies = get_user_cookie(user_email, user_password)

    if not user_cookies:
        print("Invalid email or password.")
        input()
        return

    post_url_to_share = input("Enter the Facebook Post URL to Share: ")

    post_id = is_post_id(post_url_to_share)
    if not post_id:
        print("Invalid post URL.")
        input()
        return

    share_delay = int(input("Enter the Share Delay in seconds: "))
    total_shares = int(input("Stop the Tool after how many Shares: "))

    facebook_token = get_facebook_token(user_cookies)
    if not facebook_token:
        print("Error: Cookie is undefined. Press Enter to start again.")
        input()
        return

    all_tokens = [facebook_token]

    share_count = 0
    success_counter = [0]

    while share_count < total_shares:
        for token_data in all_tokens:
            share_count += 1
            threading.Thread(target=perform_share, args=(token_data, post_id, success_counter)).start()
            time.sleep(share_delay)

    print(f'\nSUCCESS: Shares Completed ({success_counter[0]}) | Press [Enter] to run again')
 


          
def get_facebook_pages(user_access_token):
    url = 'https://graph.facebook.com/v18.0/me/accounts'
    headers = {
        'Authorization': f'Bearer {user_access_token}',
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None

    data = response.json()
    pages_data = [{'accessToken': page['access_token'], 'name': page['name']} for page in data['data']]

    return pages_data

def extract_user_url(post_url):
  pattern = r"(https://www\.facebook\.com/[^/]+)"
  match = re.search(pattern, post_url)
  if match:
      return match.group(1)
  else:
      return None
    


def auto_react_to_facebook_post():
        url = input('[•] Enter the post URL: ')
        user_url = extract_user_url(url)

        if not user_url:
            print("Invalid post URL.")
            return

        token = input('[•] Enter the access token: ')
        reaction_type = input('[•] Enter the reaction type (e.g., LIKE, LOVE, HAHA, WOW, SAD, ANGRY): ')
        delay_seconds = float(input('[•] Enter the delay between requests (in seconds): '))

        comment_text = "<>"
        comment = comment_text.replace('<>', '\n')

        post_id = is_post_id(url)
        user_id = None  

        if not post_id:
            print("Unable to fetch post ID from the URL.")
            return

        print("Please wait...")
        time.sleep(5) 
        user_id = is_post_id(user_url)

        if not user_id:
            print("Unable to fetch user ID from the URL.")
            return

        post_url = f'{user_id}_{post_id}'
        pages_data = get_facebook_pages(token)

        if pages_data:
            print("Available Pages:")
            for i, page in enumerate(pages_data):
                print(f"{i + 1}. {page['name']}")

            continue_react = input("Do you want to continue reacting? (yes/no): ")

            if continue_react.lower() == 'yes':
                limit = int(input('[•] Enter the limit for reactions: '))
                i = 0
                while i < limit:
                    page = pages_data[i % len(pages_data)]

                    try:
                        response = requests.post(f'https://graph.facebook.com/{post_url}/reactions?type={reaction_type}&access_token={page["accessToken"]}')
                        response.raise_for_status()
                        print(f"SUCCESS: Given {reaction_type} reaction to {post_url} on behalf of {page['name']}")

                    except requests.RequestException as e:
                        print(f"Error making request: {e}")
                        print(f"ERROR: Failed to give {reaction_type} reaction to {post_url} on behalf of {page['name']}")

                    i += 1
                    time.sleep(delay_seconds)



def display_page_info(page):
  print(f"\nPage information:")
  print(f"Name: {page['name']}")
  print(f"Token: {page['accessToken']}")

def auto_comment_on_facebook_post():
  user_access_token = input('[•] Enter Facebook Access Token: ')
  post_id = input('[•] Enter Post URL: ')
  comment_text = input('[•] Enter Comment: ')
  delay_seconds = float(input('[•] Enter Delay between requests (in seconds): '))

  comment = comment_text.replace('<>', '\n')
  pages_data = get_facebook_pages(user_access_token)

  post_url = is_post_id(post_id)

  if not post_url:
     print(f"Invalid post URL.")
     return

  if pages_data:
      print("Available Pages:")
      for i, page in enumerate(pages_data):
          print(f"{i + 1}. {page['name']}")

      continue_comment = input("Do you want to continue commenting? (yes/no): ")

      if continue_comment.lower() == 'yes':
          limit = int(input('[•] Enter the limit for comment: '))
          i = 0
          while i < limit:
              page = pages_data[i % len(pages_data)]
              display_page_info(page)
              print(f"\n[•] Processing {i + 1}")
              try:
                  response = requests.post(f'https://graph.facebook.com/{post_url}/comments', params={'message': comment, 'access_token': page['accessToken']})

                  if response.status_code == 200:
                    print(f'Successfully commented on post: {post_id} (Page: {page["name"]})')
                  else:
                    print(f'Failed to post comment on post: {post_id} (Page: {page["name"]})')
                    print(f'Error message: {response.text}')

              except Exception as e:
                  print(f"An error occurred: {str(e)}")

              i += 1
              time.sleep(delay_seconds)

          print("\n[•] Finished! Commented on all available pages.")

if __name__ == "__main__":
      try:
       
              while True:
                  print("\nChoose operation:")
                  print("1. Auto React on Facebook Post (page)")
                  print("2. Auto Comment on Facebook Post (page)")
                  print("3. Auto Share on Facebook Post (user)")
                  print("4. Exit")

                  operation_choice = input("Enter your operation choice: ")

                  if operation_choice == '1':
                      auto_react_to_facebook_post()
                  elif operation_choice == '2':
                      auto_comment_on_facebook_post()
                  elif operation_choice == '3':
                      auto_share_on_facebook_post()
                  elif operation_choice == '4':
                      sys.exit()
                  else:
                      print("Invalid choice. Please choose again.")
      except KeyboardInterrupt:
          print("\n[×] Input canceled. Exiting")
