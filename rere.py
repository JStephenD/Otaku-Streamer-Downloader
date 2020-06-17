import re


title_pattern = re.compile(r'(episode)(\d+)-([a-zA-Z0-9:_]*)')
x = re.search(title_pattern, "https://beta.otaku-streamers.com/watch/4481/episode12-Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri")
print(x.groups())
episode_number, title = x.group(2,3)