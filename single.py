import re
import requests
import os
import sys
import time
import urllib.parse
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
    

url = urllib.parse.unquote(input('enter single episode url: \n'))
season_num = int(input('enter season number: \n'))

title_pattern = re.compile(r'(\d+)/episode(\d+)-(.*)')

payload = {
    'username': os.environ['username'],
    'password': os.environ['password']
} 

def download(sess, src, title, ep_num):
    global start
    cwd = os.getcwd()
    if not os.path.exists(r"{}\{}".format(cwd, title)):
        try: os.mkdir(r"{}\{}".format(cwd, title))
        except: pass
    if not os.path.exists(r"{}\{}\Season {}".format(cwd, title, season_num)):
        try: os.mkdir(r"{}\{}\Season {}".format(cwd, title, season_num))
        except: pass

    vid_stream = sess.get(src, stream=True, verify=False)
    total_size = vid_stream.headers.get('content-length')
    total_size = int(total_size)
    downloaded = 0

    try:
        filename = ''
        if '.' in str(ep_num):
            filename = r"{}\{}\Season {}\{} S{:02}E{:02}.mp4".format(cwd, title, season_num, title, season_num, float(ep_num))
        else:
            filename = r"{}\{}\Season {}\{} S{:02}E{:02}.mp4".format(cwd, title, season_num, title, season_num, int(ep_num))
        # print(os.path.exists(filename))
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
                            sys.stdout.write('\033[{}A'.format(1))
                            sys.stdout.flush()
                            sys.stdout.write('\r[{:>3}%] << ep {}{}\n'.format(percentages[ep_num], ep_num,' '*20))
                            sys.stdout.flush()
    except Exception as e:
        return f'ERROR on {title} - {ep_num} error message: {e}'

    return f'DOWNLOADED {title} - {ep_num}'

with requests.Session() as sess:
    sess_get = sess.get('https://beta.otaku-streamers.com/')
    logged_in = sess.post('https://beta.otaku-streamers.com/login', data=payload)

    _, ep_num, title = re.search(title_pattern, url).groups()
    title = title.replace('_', ' ')
    title = title.replace(':', '').replace('<', '').replace('>', '').replace('?', ''). \
        replace('*', '').replace('|', '')

    if do_progress:
        sys.stdout.write('{}\n'.format("waiting for download"))
        sys.stdout.flush()

    ep_page = sess.get(url)
    ep_soup = BeautifulSoup(ep_page.content, 'html.parser')

    src = ep_soup.find('source', type='video/mp4')['src']
    result = download(sess, src, title, int(ep_num))

    sys.stdout.write('\033[{}A'.format(1))
    sys.stdout.flush()
    sys.stdout.write('\r[{:>3}%] << ep {}{}'.format(percentages[int(ep_num)], ep_num,' '*20))
    sys.stdout.flush()

    print(f'\n{result}')