import requests
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs
import sys


def onechapter(web, output_dir):
    res = requests.get(web)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    #print(img_tags)
    parts = web.split("/")
    print(parts[4],parts[5])
    folder = f'{output_dir}\{parts[4]}\{parts[5]}'
    makedirs(folder, exist_ok=True)
    for x in range(1,len(img_tags)+1):
        if 1 <= x <= 9:
            downlink = f'https://img.imgxyzz.xyz/{parts[4]}/{parts[5]}/00{x}.jpg'
        elif x > 9:
            downlink = f'https://img.imgxyzz.xyz/{parts[4]}/{parts[5]}/0{x}.jpg'
        print(downlink)
        image_save_path = join(folder, f'0{x}.jpg')
        res = requests.get(downlink)
        with open(image_save_path, 'wb') as f:
            f.write(res.content)
    '''
    res = requests.get(web)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    image_links = [img['data-src'] for img in img_tags]
    for i, link in enumerate(image_links):
        image_save_path = join(output_dir, f'image_{i}.jpg')
        res = requests.get(link)
        with open(image_save_path, 'wb') as f:
            f.write(res.content)
    '''

def multichapters(link, dir, from_chapter, latest_chapter, *special_chapters):
    listchaps = []
    for c in range(from_chapter,latest_chapter+1):
        chapterlink = f'{link}chapter-{c}'
        listchaps.append(chapterlink)
        if special_chapters != 0:
            for x in special_chapters:
                c = c + x
                specialchapterlink = f'{link}chapter-{c}'
                c = c - x
                listchaps.append(specialchapterlink)
    for x in listchaps:
        onechapter(x, dir)

#onechapter("https://khotruyen.cc/truyen-tranh/ba-chi-chu-nha-the-owner-of-a-building/chapter-115/","\downloads")
multichapters("https://khotruyen.cc/truyen-tranh/ba-chi-chu-nha-the-owner-of-a-building/chapter-115/","\downloads",110,115,0)