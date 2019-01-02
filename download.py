import bs4
import os
from subprocess import call
import requests
from requests.auth import HTTPBasicAuth
import http.cookiejar #For python 2 replace http.cookiejar with cookielib


def getIframeUrl(source, part):
    cj = http.cookiejar.MozillaCookieJar('cookies.txt')
    cj.load()

    r = requests.get(source, cookies=cj)
    bs = bs4.BeautifulSoup(r.content, 'lxml')
    dest = 'https://fast.wistia.net/embed/iframe/{}'
    id = bs.find('li', {'id': 'lesson-part-' + str(part)}).a['data-id']
    return dest.format(id)


f = open('piano.txt')
lines = f.readlines()
lines = list(map(lambda l: l[:-1], lines))
f.close()

for line in lines:
    print('downloading {}'.format(line))
    folder_name = line.split('/')[4]
    try:
        os.mkdir(folder_name)
    except:
        continue

    base_link = line[:-1]
    total_videos = int(line.split('-')[-1])

    for i in range(total_videos, 0, -1):
        video_src = getIframeUrl(base_link+str(i), i)
        referer = base_link + str(i)
        destination = '~/Desktop/hdpiano/{0}/%(title)s.%(ext)s'.format(folder_name)
        print(video_src, referer, destination)
        call(['youtube-dl', video_src, '-o', destination, '--cookies', 'cookies.txt', '--referer', referer])
