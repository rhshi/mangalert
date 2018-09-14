import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def makeSoup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def writeMDFollowsData(follows, fname):
    with open(os.path.join(os.path.dirname(__file__), '../data/{}.txt'.format(fname)), 'w') as f:
        f.write('\n'.join('{} {}'.format(x[0], x[1]) for x in follows))


def diffMonth(raw_date):
    d1 = datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.now()
    return (d2.year - d1.year) * 12 + d2.month - d1.month

