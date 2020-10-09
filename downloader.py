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
max_workers = 8
start = time.time()
percentages = defaultdict(int)
downloaded = defaultdict(lambda : [0, 0])
dl_from = None
dl_to = None
for arg in sys.argv:
    if arg == '-progress':
        do_progress = True
    if arg == '-4':
        max_workers = 4
    if 'from' in arg:
        dl_from = int(arg.split('=')[1])
    if 'to' in arg:
        dl_to = int(arg.split('=')[1])
    

url = input('enter base url: \n')
season_num = int(input('enter season number: \n'))
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
episodes = soup.find('ul', class_='os-album-list')
links = episodes.find_all('a')
hrefs = list(set([l['href'] for l in links]))
ep_nums = []

title_pattern = re.compile(r'(\d+)/episode(\d+)-(.*)')

payload = {
    'username': os.environ['username'],
    'password': os.environ['password']
} 

def download(sess, src, title, ep_num):
    global start, ep_nums
    ep_num = int(ep_num)
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
    try:
        filename = ''
        if '.' in str(ep_num):
            filename = r"{}\{}\Season {}\{} S{:02}E{:02}.mp4".format(cwd, title, season_num, title, season_num, float(ep_num))
        else:
            filename = r"{}\{}\Season {}\{} S{:02}E{:02}.mp4".format(cwd, title, season_num, title, season_num, int(ep_num))
        # print(os.path.exists(filename))
        with open(filename, 'wb') as wf:
            if not do_progress: print(f'downloading {title} - {ep_num}')
            for chunk in vid_stream.iter_content(chunk_size=1024):            
                if chunk:
                    wf.write(chunk)

                    if do_progress:
                        downloaded[ep_num][0] += len(chunk)
                        if downloaded[ep_num][0] == 0: percentages[ep_num] = 0
                        else: percentages[ep_num] = int(100 * downloaded[ep_num][0] / total_size)
                        end = time.time()

                        if end - start >= 5:
                            _start = start
                            start = time.time()
                            sys.stdout.write('\033[{}A'.format(len(ep_nums)))
                            sys.stdout.flush()
                            for i in ep_nums:
                                if percentages[i] == 0:
                                    print('\rwaiting for download')
                                else:
                                    curr_downloaded, prev_downloaded = downloaded[i]
                                    downloaded[i][1] = curr_downloaded
                                    kbps = ((curr_downloaded - prev_downloaded) / (end - _start)) / 1000
                                    sys.stdout.write('\r[{:>3}%] {:06.2f} kBps << ep {}\n'.format(
                                        percentages[i], kbps, i)
                                    )
                                sys.stdout.flush()
    except Exception as e:
        return f'ERROR on {title} - {ep_num} error message: {e}'

    return f'DOWNLOADED {title} - {ep_num}'


print(f'Progress bar = {do_progress}')
with requests.Session() as sess:
    sess_get = sess.get('https://beta.otaku-streamers.com/')
    logged_in = sess.post('https://beta.otaku-streamers.com/login', data=payload)

    srcs = []
    dl_range = None
    if dl_from:
        if dl_to:
            dl_range = [i for i in range(dl_from, dl_to+1)]
        else: 
            dl_range = dl_from

    def helper(href):
        x = re.search(title_pattern, href)
        anime_id, ep_num, title = x.group(1, 2, 3)

        if type(dl_range) == int:
            if int(ep_num) < dl_range: return
        if type(dl_range) == list:
            if int(ep_num) not in dl_range: return

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
        ep_nums.append(int(ep_num))

        if do_progress:
            sys.stdout.write('{}\n'.format("waiting for download"))
            sys.stdout.flush()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(helper, href) for href in hrefs]
    
    ep_nums.sort()

    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = [executor.submit(download, sess, s['src'], s['title'], s['ep_num']) for s in srcs]

        for f in concurrent.futures.as_completed(results):            
            res = f.result()
            errors.append(res)
            if not do_progress:
                print(res)
    
    sys.stdout.write('\033[{}A'.format(len(hrefs)))
    sys.stdout.flush()
    for i in range(1, len(hrefs)+1):
        if percentages[i] == 0:
            print('\rwaiting for download')
        else:
            sys.stdout.write('\r[{:>3}%] << ep {}{}\n'.format(percentages[i], i,' '*15))
        sys.stdout.flush()
    print('\nCOMPLETED DOWNLOADS')

    for i in errors:
        print(i)