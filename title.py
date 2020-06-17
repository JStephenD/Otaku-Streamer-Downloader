import os
title = 'Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri'

title = title.replace('_', ' ')
title = title.replace(':', '')
ep_num = 1

filename = r"{}\{} - {}.mp4".format(os.getcwd(), title, ep_num)
print (filename)
with open(filename, 'wb') as wf:
    pass