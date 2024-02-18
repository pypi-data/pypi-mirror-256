import requests
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs
import sys

#https://stackoverflow.com/questions/14587728/what-does-this-error-in-beautiful-soup-means

def onechapter(web,output_dir):
    res = requests.get(web)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.findAll('img',{"data-src":True})
    image_links = [img['data-src'] for img in img_tags]
    #['https:', '', 'evvdsfgefdszihfdx.hentaivn.lat', 'HGHrrFSDweqZSfd', 'lgbdfexijzbxsdrl', '2024', '01', '12', '1705045067-0.png?imgmax=1200']
    #https://i3.hhentai.net/images/5/6/7/8
    parts = web.split("/")
    print(parts[2],parts[3])
    folder = f'{output_dir}\{parts[2]}\{parts[3]}'
    makedirs(folder, exist_ok=True)
    for x in image_links:
        l = x.split("/")
        name = l[8].replace("?imgmax=1200","")
        link = f'https://i3.hhentai.net/images/{l[5]}/{l[6]}/{l[7]}/{l[8]}'
        image_save_path = join(folder, name)
        print(image_save_path)
        res = requests.get(link)
        with open(image_save_path, 'wb') as f:
            f.write(res.content)
 

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

onechapter("https://hentaivn.lat/36055-67235-xem-truyen-goblin-kara-hajimeru-sekai-seifuku-chap-1.html","\downloads")
#multichapters("https://khotruyen.cc/truyen-tranh/ba-chi-chu-nha-the-owner-of-a-building/chapter-115/","\downloads",110,115,0)