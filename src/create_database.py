from utils import makeSoup

link = 'https://mangadex.org/title/19636/8-tales-of-the-zqn'
soup = makeSoup(link)
a = soup.find_all('div', class_='chapter-row d-flex row no-gutters p-2 align-items-center border-bottom odd-row')
for c in a:
    print(c)
    print('_________')