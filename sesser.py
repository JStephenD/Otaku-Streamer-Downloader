import os
import requests
from bs4 import BeautifulSoup

payload = {
    'username': os.environ['username'],
    'password': os.environ['password']
} 

print('----')
with requests.Session() as sess:
    sess_get = sess.get('https://beta.otaku-streamers.com/')
    logged_in = sess.post('https://beta.otaku-streamers.com/login', data=payload)

    ep_page = sess.get('https://beta.otaku-streamers.com/watch/4481/episode1-Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri')
    ep_soup = BeautifulSoup(ep_page.content, 'html.parser')
    
    # print(ep_soup.find('div', class_='video-container'))
    print(ep_soup.find('source', type='video/mp4'))
    # with open('x.html', 'w') as wf:
    #     wf.write(ep_page.text)