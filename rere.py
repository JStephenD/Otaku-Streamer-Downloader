import re
import sys

dl_from = None
dl_to = None
for arg in sys.argv:
    if arg == "-progress":
        do_progress = True
    if arg == "-4":
        max_workers = 4
    if "from" in arg:
        dl_from = int(arg.split("=")[1])
    if "to" in arg:
        dl_to = int(arg.split("=")[1])

dl_range = None
if dl_from:
    if dl_to:
        dl_range = [i for i in range(dl_from, dl_to + 1)]
    else:
        dl_range = dl_from

print(dl_range)
ep_num = "3"

if type(dl_range) == int:
    if int(ep_num) < dl_range:
        print("not within from range")
if type(dl_range) == list:
    if int(ep_num) not in dl_range:
        print("not within from and to range")

title_pattern = re.compile(r"(episode)(\d+)-([a-zA-Z0-9:_]*)")
x = re.search(
    title_pattern,
    "https://beta.otaku-streamers.com/watch/4481/episode12-Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri",
)
print(x.groups())
episode_number, title = x.group(2, 3)
