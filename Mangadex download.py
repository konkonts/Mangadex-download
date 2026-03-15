#download mangadex

import requests, os, re

manga_id = input('input manga id: ')
url = ('https://api.mangadex.org/manga/' + manga_id)

response = requests.get(url)
try:
    response.raise_for_status()
except Exception as exc:
    print(f'There was a problem: {exc}')
    exit()

title = response.json()["data"]["attributes"]["title"]
title = list(title.values())[0]
title = re.sub(r'[\\/*?:"<>|]', "", title)

print ('Manga:', title)

download_path = input('download path: ')

os.makedirs(os.path.join(download_path, title), exist_ok=True)

chapter_url = f'https://api.mangadex.org/chapter?manga={manga_id}&limit=100'
chapter_response = requests.get(chapter_url)
try:
    response.raise_for_status()
except Exception as exc:
    print(f'There was a problem: {exc}')
    exit()

language_scan = list({
    c['attributes'].get('translatedLanguage')
    for c in chapter_response.json()['data']
    if c['attributes'].get('translatedLanguage')
})
print('Available languages:')
for lang in language_scan:
    print('-', lang)

language = input('input language: ')
chapters = [c for c in chapter_response.json()['data'] if c['attributes'].get('translatedLanguage') == language]

for chapter in chapters:

    chapter_id = chapter['id']

    chapter_num = chapter['attributes']['chapter']

    if chapter_num is None:
        chapter_num = 'unknown'

    print('Download chapter', chapter_num)


    at_home = f'https://api.mangadex.org/at-home/server/{chapter_id}'

    server = requests.get(at_home).json()

    base = server['baseUrl']
    hash = server['chapter']['hash']
    pages = server['chapter']['data']

    chapter_folder = f'{download_path}/{title}/chapter_{chapter_num}'
    os.makedirs(chapter_folder, exist_ok=True)

    for i, page in enumerate(pages):

        img_url = f'{base}/data/{hash}/{page}'

        img = requests.get(img_url)

        with open(f'{chapter_folder}/page{i+1}.jpg', 'wb') as f:
            f.write(img.content)

print('Download selesai')
print('File save in: ', os.path.abspath(title))









