import collections

from .utils import makeSoup


def getUpdates():
    link = 'https://mangadex.org/updates/'
    soup = makeSoup(link)
    table = soup.find('table', class_='table table-striped table-sm')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = collections.OrderedDict()
    for row in rows:
        eles = row.find_all('td')
        for ele in eles:
            contents = ele.find('a')
            try:
                title = contents.text.strip()
                link = contents['href']
                if link.startswith('/title'):
                    if title not in data:
                        data[title] = {}
                        data[title]['mlink'] = link
                        data[title]['chlinks'] = []
                        data[title]['language'] = None
                    else:
                        pass
                elif link.startswith('/chapter'):
                    last_key = next(reversed(data))
                    data[last_key]['chlinks'].append(link)
            except:
                pass
            images = ele.find('img', class_='rounded align-text-bottom d-inline-block flag')
            if images:
                last_key = next(reversed(data))
                if not data[last_key]['language']:
                    data[last_key]['language'] = images['title']

    updates = dict(data)
    for key in list(updates.keys()):
        if updates[key]['language'] != 'English':
            del updates[key]

    return updates
