import subprocess
import sys
import os
import time
import webbrowser

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
        import webbrowser
        from bs4 import BeautifulSoup
        return True
    except ImportError:
        return False


clear_screen()

if not check_dependencies():
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
            print(f"\x1b[1;92mShare successful for post ID {post_id} - {success_counter[0] + 1}\x1b[0m")
        else:
            print(f'Error during sharing. Response: {response}')
    except Exception as e:
        print(f"Error sharing: {e}")


def auto_share_on_facebook_post():
  user_email = input("\n\x1b[1;97mEnter your Facebook Email: \x1b[0m")
  user_password = input("\x1b[1;97mEnter your Facebook Password: \x1b[0m")
  user_cookies = get_user_cookie(user_email, user_password)

  if not user_cookies:
      print("\x1b[1;91mInvalid email or password.\x1b[0m")
      input()
      return

  post_url_to_share = input("\x1b[1;97mEnter the Facebook Post URL to Share: \x1b[0m")

  post_id = is_post_id(post_url_to_share)
  if not post_id:
      print("\x1b[1;91mInvalid post URL.\x1b[0m")
      input()
      return

  share_delay = int(input("\x1b[1;97mEnter the Share Delay in seconds: \x1b[0m"))
  total_shares = int(input("\x1b[1;97mStop the Tool after how many Shares: \x1b[0m"))

  facebook_token = get_facebook_token(user_cookies)
  if not facebook_token:
      print("\x1b[1;91mError: Cookie is undefined. Press Enter to start again.\x1b[0m")
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

  print(f'\n\x1b[1;92mSUCCESS: Shares Completed ({success_counter[0]}) | Press [Enter] to run again\x1b[0m')
 


          
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
                    url = input('\n\x1b[1;97mEnter the post URL: \x1b[0m')
                    user_url = extract_user_url(url)

                    if not user_url:
                        print("\x1b[1;91mInvalid post URL.\x1b[0m")
                        return

                    token = input('\x1b[1;97mEnter the access token: \x1b[0m')
                    reaction_type = input('\x1b[1;97mEnter the reaction type (e.g., LIKE, LOVE, HAHA, WOW, SAD, ANGRY): \x1b[0m')
                    delay_seconds = float(input('\x1b[1;97mEnter the delay between requests (in seconds): \x1b[0m'))

                    comment_text = "<>"
                    comment = comment_text.replace('<>', '\n')

                    post_id = is_post_id(url)
                    user_id = None  

                    if not post_id:
                        print("\x1b[1;91mUnable to fetch post ID from the URL.\x1b[0m")
                        return

                    print("\x1b[1;97mPlease wait...\x1b[0m")
                    time.sleep(5) 
                    user_id = is_post_id(user_url)

                    if not user_id:
                        print("\x1b[1;91mUnable to fetch user ID from the URL.\x1b[0m")
                        return

                    post_url = f'{user_id}_{post_id}'
                    pages_data = get_facebook_pages(token)

                    if pages_data:
                        print("\x1b[1;97mAvailable Pages:\x1b[0m")
                        for i, page in enumerate(pages_data):
                          print(f"\x1b[1;92m[{i + 1}]. \x1b[1;97m{page['name']}\x1b[0m")

                        continue_react = input("\x1b[1;97mDo you want to continue reacting? (yes/no): \x1b[0m")

                        if continue_react.lower() == 'yes':
                            limit = int(input('\x1b[1;97m[•] Enter the limit for reactions: \x1b[0m'))
                            i = 0
                            while i < limit:
                                page = pages_data[i % len(pages_data)]

                                try:
                                    response = requests.post(f'https://graph.facebook.com/{post_url}/reactions?type={reaction_type}&access_token={page["accessToken"]}')
                                    response.raise_for_status()
                                    print(f"\x1b[1;92mSUCCESS: Given {reaction_type} reaction to {post_url} on behalf of {page['name']}\x1b[0m")

                                except requests.RequestException as e:
                                    print(f"\x1b[1;91mError making request: {e}\x1b[0m")
                                    print(f"\x1b[1;91mERROR: Failed to give {reaction_type} reaction to {post_url} on behalf of {page['name']}\x1b[0m")

                                i += 1
                                time.sleep(delay_seconds)



       

def display_page_info(page):
            print(f"\n\x1b[1;92mPage information:\x1b[0m")
            print(f"Name: \x1b[1;97m{page['name']}\x1b[0m")
            print(f"Token: \x1b[1;97m{page['accessToken']}\x1b[0m")

def auto_comment_on_facebook_post():
            user_access_token = input('\n\x1b[1;97mEnter Facebook Access Token: \x1b[0m')
            post_id = input('\x1b[1;97mEnter Post URL: \x1b[0m')
            comment_text = input('\x1b[1;97mEnter Comment: \x1b[0m')
            delay_seconds = float(input('\x1b[1;97mEnter Delay between requests (in seconds): \x1b[0m'))

            comment = comment_text.replace('<>', '\n')
            pages_data = get_facebook_pages(user_access_token)

            post_url = is_post_id(post_id)

            if not post_url:
                print(f"\x1b[1;91mInvalid post URL.\x1b[0m")
                return

            if pages_data:
                print("\x1b[1;97mAvailable Pages:\x1b[0m")
                for i, page in enumerate(pages_data):
                    print(f"\x1b[1;92m[{i + 1}]. \x1b[1;97m{page['name']}\x1b[0m")

                continue_comment = input("\x1b[1;97mDo you want to continue commenting? (yes/no): \x1b[0m")

                if continue_comment.lower() == 'yes':
                    limit = int(input('\x1b[1;97m[•] Enter the limit for comment: \x1b[0m'))
                    i = 0
                    while i < limit:
                        page = pages_data[i % len(pages_data)]
                        display_page_info(page)
                        print(f"\n\x1b[1;97m[•] Processing {i + 1}\x1b[0m")
                        try:
                            response = requests.post(f'https://graph.facebook.com/{post_url}/comments', params={'message': comment, 'access_token': page['accessToken']})

                            if response.status_code == 200:
                                print(f'\x1b[1;92mSuccessfully commented on post: {post_id} (Page: {page["name"]})\x1b[0m')
                            else:
                                print(f'\x1b[1;91mFailed to post comment on post: {post_id} (Page: {page["name"]})\x1b[0m')
                                print(f'\x1b[1;91mError message: {response.text}\x1b[0m')

                        except Exception as e:
                            print(f"\x1b[1;91mAn error occurred: {str(e)}\x1b[0m")

                        i += 1
                        time.sleep(delay_seconds)

                    print("\n\x1b[1;97m[•] Finished! Commented on all available pages.\x1b[0m")

def auto_follow_facebook_user():
  token = input('\n\x1b[1;97mEnter the access token: \x1b[0m')
  user_url = input('\x1b[1;97mEnter the profile URL of the user you want to follow: \x1b[0m')

  user_id = is_post_id(user_url)
  if not user_id:
      print("\x1b[1;91mInvalid user URL.\x1b[0m")
      return

  delay_seconds = float(input('\x1b[1;97mEnter the delay between requests (in seconds): \x1b[0m'))

  pages_data = get_facebook_pages(token)

  if pages_data:
      print("\x1b[1;97mAvailable Pages:\x1b[0m")
      for i, page in enumerate(pages_data):
          print(f"\x1b[1;92m[{i + 1}]. \x1b[1;97m{page['name']}\x1b[0m")

      continue_follow = input("\x1b[1;97mDo you want to continue follow? (yes/no): \x1b[0m")

      if continue_follow.lower() == 'yes':
          limit = int(input('[•] Enter the limit for follows: '))
          i = 0
          while i < limit:
              page = pages_data[i % len(pages_data)]

              try:
                  url = f'https://graph.facebook.com/v18.0/{user_id}/subscribers'
                  headers = {'Authorization': f'Bearer {page["accessToken"]}'}

                  response = requests.post(url, headers=headers, json={})
                  response.raise_for_status()
                  print(f"\x1b[1;92mSUCCESS: Followed user {user_id} on behalf of {page['name']}\x1b[0m")

              except requests.RequestException as e:
                  print(f"\x1b[1;91mError making request: {e}\x1b[0m")
                  print(f"\x1b[1;91mERROR: Failed to follow user {user_id} on behalf of {page['name']}\x1b[0m")

              i += 1
              time.sleep(delay_seconds)




    

if __name__ == "__main__":
      try:
       
              while True:
                print('\n\x1b[1;92m                █████╗ ██╗███████╗           \x1b[0m')
                print('\x1b[1;92m               ██╔══██╗██║╚══███╔╝          \x1b[0m')
                print('\x1b[1;92m               ███████║██║  ███╔╝           \x1b[0m')
                print('\x1b[1;92m               ██╔══██║██║ ███╔╝            \x1b[0m')
                print('\x1b[1;92m               ██║  ██║██║███████╗          \x1b[0m')
                print('\x1b[1;92m               ╚═╝  ╚═╝╚═╝╚══════╝          \x1b[0m')
                print('\n\x1b[1;92m' + '-' * 50 + '\x1b[0m')
                print('\n\x1b[1;92mOwner     :\x1b[0m \x1b[1;97mAiz\x1b[0m ')
                print('\x1b[1;92mFacebook  :\x1b[0m \x1b[1;97mfacebook.com/intel.aiz\x1b[0m ')
                print('\x1b[1;92mTool Type :\x1b[0m \x1b[1;97mFacebook Manager\x1b[0m ')
                print('\x1b[1;92mVersion   :\x1b[0m \x1b[1;97m1.0\x1b[0m ')
                print('\n\x1b[1;92m' + '-' * 50 + '\x1b[0m')
                print('\n\x1b[1;92m[01]\x1b[0m \x1b[1;97mAuto React on Facebook Post (page)\x1b[0m')
                print('\x1b[1;92m[02]\x1b[0m \x1b[1;97mAuto Comment on Facebook Post (page)\x1b[0m')
                print('\x1b[1;92m[03]\x1b[0m \x1b[1;97mAuto Share on Facebook Post (user)\x1b[0m')
                print('\x1b[1;92m[04]\x1b[0m \x1b[1;97mAuto Follow Facebook Account (page)\x1b[0m')
                print('\x1b[1;92m[05]\x1b[0m \x1b[1;97mExit\x1b[0m')

                operation_choice = input("\n\x1b[1mEnter your operation choice: \x1b[0m")

                if operation_choice == '1':
                      auto_react_to_facebook_post()
                elif operation_choice == '2':
                      auto_comment_on_facebook_post()
                elif operation_choice == '3':
                      auto_share_on_facebook_post()
                elif operation_choice == '4':
                     auto_follow_facebook_user()
                elif operation_choice == '5':
                      sys.exit()
                else:
                      print("\x1b[1;97mInvalid choice. Please choose again.\x1b[0m")

      except KeyboardInterrupt:
        print("\x1b[1;91m\n[×] Input canceled. Exiting\x1b[0m")

