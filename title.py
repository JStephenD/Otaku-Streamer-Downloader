import os
title = 'Gate:_Jieitai_Kanochi_nite,_Kaku_Tatakaeri_-_Enryuu-hen'

title = title.replace('_', ' ')
title = title.replace(':', '')
title = title.replace(':', '').replace('<', '').replace('>', '').replace('?', ''). \
            replace('*', '').replace('|', '')
ep_num = 1


def download(title, ep_num):
    cwd = os.getcwd()
    if not os.path.exists(r"{}\{}".format(cwd, title)):
        os.mkdir(r"{}\{}".format(cwd, title))

    # with open(r'{}\{}\Season\s.txt'.format(cwd, title)) as f:
    #     pass
    # print(os.path.exists(r'{}\{}\Season\s.txt'.format(cwd, title)))

    filename = r"{}\{}\Season {}\{} S{:02}E{:02}.mp4".format(cwd, title, 1, title, 1, int(ep_num))
    print(filename)
    # with open(filename, 'wb') as wf:
    #     pass

    return f'DOWNLOADED {title} - {ep_num}'

download(title, ep_num)