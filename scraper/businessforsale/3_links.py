import os
import os.path
import json
import sys
from bs4 import BeautifulSoup
import extruct
from w3lib.html import get_base_url

base_url = 'https://us.businessesforsale.com'

linksd = {}

i = 0
for root, dirs, files in os.walk("crawl/l1", topdown=False):
    # if i > 1:
    #     break
    for name in files:
        if root.startswith('crawl/l1/us') and name == 'index.html':
            url = root.split('/')[1:]
            url[0] = base_url
            url = '/'.join(url)
            html = open(os.path.join(root, 'index.html')).read()
            # base_url= get_base_url(html, url)
            # data = extruct.extract(html, base_url=base_url)
            soup = BeautifulSoup(html, 'lxml')
            j = 0
            k=0
            # if 'json-ld' in data.keys() and len(data['json-ld']):
            #     print( data)
            #     if 'itemListElement' in data['json-ld'].keys():
            #         for li in data['json-ld']['itemListElement']:
            #             linksd[li['url']] = url
            #             k+=1
            for id in ('related-businesses', 'pagination'):
                div = soup.find('div', {'id': id})
                if div is not None:
                    for link in div.find_all('a', href=True):
                        linksd[link['href']] = url
                        j+=1
            i += 1
        print(i, j,k )

cwd=os.getcwd()
basedir=os.path.join(cwd,'crawl','l2')
if not os.path.exists(basedir):
    print('creating', basedir)
    os.makedirs(basedir)

print(len(linksd))
links=[(k,v) for k,v in linksd.items()]
with open('crawl/l2/links.json','w') as fh:
    json.dump(links,fh)
