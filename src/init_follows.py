from .utils import makeSoup, writeFollowsData


def initializeFollows():
    page_num = 1
    follows = []
    while True:
        link = 'https://mangadex.org/list/4680/0/2/{}/'.format(page_num)
        soup = makeSoup(link)
        contents = soup.find_all('a')

        page = []
        for content in contents:
            try:
                title = content.text.strip()
                link = content['href']
                if title and link.startswith('/title/'):
                    tup = (title, link)
                    page.append(tup)
            except:
                print('Page {} done'.format(page_num))
    
        if len(page) == 0:
            break
    
        follows.extend(page)
        page_num += 1  
    
    writeFollowsData(follows)