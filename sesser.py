import os
import requests

r = requests.get('https://www.youtube.com/watch?v=RfLsAX9QRoA', stream=True)
with open('yt.mp4', 'wb') as f:
    for i in r.iter_content(1024):
        f.write(i)