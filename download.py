import bs4
import os
from subprocess import call
import requests
from requests.auth import HTTPBasicAuth


def getIframeUrl(source, part):
    r = requests.get(source)
    bs = bs4.BeautifulSoup(r.content, 'lxml')
    dest = 'player.vimeo.com/video/{}?api=1&player_id=vm-player&color=f47c20&badge=0&byline=0&title=0'
    id = bs.find('li', {'id': 'lesson-part-' + str(part)}).a['data-id']
    return dest.format(id)


f = open('piano.txt')
lines = f.readlines()
lines = list(map(lambda l: l[:-1], lines))
f.close()

for line in lines:
    print('downloading {}'.format(line))
    folder_name = line[27:57]
    try:
        os.mkdir(folder_name)
    except:
        continue

    base_link = line[:-1]
    total_videos = int(line[-1])

    for i in range(total_videos, 0, -1):
        video_src = getIframeUrl(base_link+str(i), i)
        referer = base_link + str(i)
        destination = '~/Desktop/hdpiano/{0}/%(title)s.%(ext)s'.format(folder_name)
        print(video_src, referer, destination)
        call(['youtube-dl', video_src, '-o', destination, '--cookies', 'cookies.txt', '--referer', referer])
