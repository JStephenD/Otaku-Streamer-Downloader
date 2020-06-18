import re
import requests
import os
import concurrent.futures
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

url = input('enter base url: \n')
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
episodes = soup.find('ul', class_='os-album-list')
links = episodes.find_all('a')
hrefs = list(set([l['href'] for l in links]))

title_pattern = re.compile(r'(\d+)/episode(\d+)-(.*)')  

payload = {
    'username': os.environ['username'],
    'password': os.environ['password']
} 

def download(sess, src, title, ep_num):
    cwd = os.getcwd()
    if not os.path.exists(r"{}\{}".format(cwd, title)):
        try:
            os.mkdir(r"{}\{}".format(cwd, title))
        except:
            pass

    vid_stream = sess.get(src, stream=True, verify=False)
    filename = r"{}\{}\{} ep{:02}.mp4".format(cwd, title, title, ep_num)
    # print(filename)
    with open(filename, 'wb') as wf:
        for chunk in vid_stream.iter_content(chunk_size=8192):
            if chunk:
                wf.write(chunk)

    return f'DOWNLOADED {title} - {ep_num}'


print('----')
with requests.Session() as sess:
    sess_get = sess.get('https://beta.otaku-streamers.com/')
    logged_in = sess.post('https://beta.otaku-streamers.com/login', data=payload)

    srcs = []

    for href in hrefs:
        x = re.search(title_pattern, href)
        anime_id, ep_num, title = x.group(1, 2, 3)
        title = title.replace('_', ' ')
        title = title.replace(':', '').replace('<', '').replace('>', '').replace('?', ''). \
            replace('*', '').replace('|', '')

        ep_page = sess.get(href)
        ep_soup = BeautifulSoup(ep_page.content, 'html.parser')

        src = ep_soup.find('source', type='video/mp4')['src']
        srcs.append({
            'src': src,
            'title': title,
            'ep_num': ep_num
        })

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(download, sess, s['src'], s['title'], s['ep_num']) for s in srcs]

        for f in concurrent.futures.as_completed(results):
            print(f.result())