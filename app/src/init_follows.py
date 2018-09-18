import time

from .utils import diffMonth, makeSoup, writeMDFollowsData


def gatherFollows():
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
    
    return follows


def determineComplete(manga):
    link = 'https://mangadex.org{}'.format(manga[1])
    soup = makeSoup(link)
    alerts = soup.find_all('div', class_='alert alert-info mt-3 text-center')
    if alerts:
        return True
    manga_info = soup.find_all('div', class_='row m-0 py-1 px-0 border-top')
    for info in manga_info:
        text = info.text.strip()
        if text.startswith('Pub. status:') and text.endswith('Completed'):
            page = 1
            while True:
                chaplink = 'https://mangadex.org{}/{}'.format(manga[1], page)
                chapsoup = makeSoup(chaplink)
                chaps_info = soup.find_all('div', class_='col ')
                chaps_iter = iter(chaps_info)
                while True:
                    try:
                        chapter = next(chaps_iter)
                        date_info = chapter.find('div', class_='col-2 col-lg-1 ml-1 text-right text-truncate order-lg-8 ')
                        image = chapter.find('img')
                        if date_info and image and image['title'] == 'English':
                            raw_date = date_info['title'][:-4]
                            diff = diffMonth(raw_date)
                            if diff > 6:
                                return True
                            else:
                                return False
                        else:
                            continue
                    except StopIteration:
                        break

                time.sleep(1)
                
                page += 1

        elif text.startswith('Pub. status:') and text.endswith('Ongoing'):
            return False

        else:
            continue


def initializeFollows():
    all_follows = gatherFollows()
    ongoing = []
    complete = []
    for manga in all_follows:
        if not determineComplete(manga):
            ongoing.append(manga)
            print(manga[0], ': ongoing')
        else:
            complete.append(manga)
            print(manga[0], ': completed')
        time.sleep(1)

    writeMDFollowsData(ongoing, 'ongoing')
    writeMDFollowsData(complete, 'completed')                                    