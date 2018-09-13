import os
import requests
from bs4 import BeautifulSoup


def makeSoup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def writeFollowsData(follows):
    with open(os.path.join(os.path.dirname(__file__), '../data/follows.txt'), 'w') as f:
        f.write('\n'.join('{} {}'.format(x[0], x[1]) for x in follows))

