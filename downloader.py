import re
import requests
import os
import sys
import time
import concurrent.futures
from bs4 import BeautifulSoup
from collections import defaultdict

requests.packages.urllib3.disable_warnings()

do_progress = False
start = time.time()
percentages = defaultdict(int)
if len(sys.argv) != 1:
    if '-progress' in sys.argv:
        do_progress = True

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
    global start
    cwd = os.getcwd()
    if not os.path.exists(r"{}\{}".format(cwd, title)):
        try:
            os.mkdir(r"{}\{}".format(cwd, title))
        except:
            pass

    vid_stream = sess.get(src, stream=True, verify=False)
    total_size = vid_stream.headers.get('content-length')
    total_size = int(total_size)
    downloaded = 0
    try:
        filename = ''
        if '.' in ep_num:
            filename = r"{}\{}\{} ep{:02}.mp4".format(cwd, title, title, float(ep_num))
        else:
            filename = r"{}\{}\{} ep{:02}.mp4".format(cwd, title, title, int(ep_num))
        # print(filename)
        with open(filename, 'wb') as wf:
            if not do_progress: print(f'downloading {title} - {ep_num}')
            for chunk in vid_stream.iter_content(chunk_size=8192):
                if chunk:
                    wf.write(chunk)

                    if do_progress:
                        downloaded += len(chunk)
                        percentages[int(ep_num)] = int(100 * downloaded / total_size)
                        
                        if time.time() - start >= 5:
                            start = time.time()
                            sys.stdout.write('\033[{}A'.format(len(hrefs)))
                            sys.stdout.flush()
                            for i in range(1, len(hrefs)+1):
                                if percentages[i] == 0:
                                    sys.stdout.write('\n')
                                else:
                                    sys.stdout.write('\r[{:>3}%] << ep {}{}\n'.format(percentages[i], i,' '*100))
                                sys.stdout.flush()
    except Exception as e:
        return f'ERROR on {title} - {ep_num} error message: {e}'

    return f'DOWNLOADED {title} - {ep_num}'


print(f'Progress bar = {do_progress}')
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

        if do_progress:
            sys.stdout.write('{:<50}\n'.format("waiting for download"))
            sys.stdout.flush()
    # sys.stdout.flush()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(download, sess, s['src'], s['title'], s['ep_num']) for s in srcs]

        for f in concurrent.futures.as_completed(results):
            if not do_progress:
                print(f.result())