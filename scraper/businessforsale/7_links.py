import os
import os.path
import json
import sys
from bs4 import BeautifulSoup
import extruct
from w3lib.html import get_base_url
from multiprocessing import Process, Queue, cpu_count, Event
import time
from queue import Empty
# import threading
# import queue

# base_url = 'https://us.businessesforsale.com'

# linksd = {}
#
# i = 0
# j=0
# k=0
# for crawls in ("crawl/l2/us","crawl/l3/us"):
#     for root, dirs, files in os.walk(crawls, topdown=False):
#         # if i > 1:
#         #     break
#         for name in files:
#             if name == 'index.html':
#                 url = root.split('/')[1:]
#                 url[0] = base_url
#                 url = '/'.join(url)
#                 html = open(os.path.join(root, 'index.html')).read()
#                 base_url= get_base_url(html, url)
#                 data = extruct.extract(html, base_url=base_url)
#                 # soup = BeautifulSoup(html, 'lxml')
#                 #print(soup)
#                 j=0
#                 k=0
#                 if 'json-ld' in data.keys():
#                     for jld in data['json-ld']:
#                         #print( data)
#                         if 'itemListElement' in jld.keys():
#                             for li in jld['itemListElement']:
#                                 linksd[li['url']] = url
#                                 k+=1
#                 #print(url)
#                 # for id in ( 'pagination',):
#                 #     div = soup.find('div', {'class': id})
#                 #     #print(div)
#                 #     if div is not None:
#                 #         for link in div.find_all('a', href=True):
#                 #             linksd[link['href']] = url
#                 #             j+=1
#                 i += 1
#                 print(i, j,k )
#
# def get_paths(wq):
#     for crawls in ("crawl/l2/us","crawl/l3/us"):
#         for root, dirs, files in os.walk(crawls, topdown=False):
#             for name in files:
#                 if name == 'index.html':
#                     wq.put(root)
#

def proc_paths(wq,lq):
    base_url = 'https://us.businessesforsale.com'
    pid=os.getpid()
    try:
        root= wq.get(timeout=10.0)
        while root:
            url = root.split('/')[1:]
            url[0] = base_url
            url = '/'.join(url)
            html = open(os.path.join(root, 'index.html')).read()
            base_url_= get_base_url(html, url)
            data = extruct.extract(html, base_url=base_url_)
            if 'json-ld' in data.keys():
                for jld in data['json-ld']:
                    if 'itemListElement' in jld.keys():
                        for li in jld['itemListElement']:
                            print(pid,li['url'])
                            lq.put((li['url'],url))
            root= wq.get(timeout=10.0)
    except Empty:
        pass

def proc_links(lq):
    cwd=os.getcwd()
    basedir=os.path.join(cwd,'crawl','l4')
    if not os.path.exists(basedir):
        print('creating', basedir)
        os.makedirs(basedir)

    links=[]
    with open('crawl/l4/links.q.txt','w') as fh:
        try:
            link=lq.get(timeout=10.0)
            while link:
                links.append(link)
                fh.write(f'{link[0]}\t{link[1]}\n')
                fh.flush()
                link=lq.get(timeout=10.0)
        except Empty:
            pass

    print(len(links))
    with open('crawl/l4/links.q.json','w') as fh:
        json.dump(links,fh)

def crawl_paths(wq):
    for crawls in ("crawl/l2/us","crawl/l3/us"):
        for root, dirs, files in os.walk(crawls, topdown=False):
            for name in files:
                if name == 'index.html':
                    wq.put(root)

if __name__ == '__main__':
    wq=Queue()
    lq=Queue()

    print('crawling...')
    p=Process(target=crawl_paths, args=(wq,))
    p.start()

    for i in range(cpu_count()):
        print(i, 'processing...')
        p=Process(target=proc_paths, args=(wq,lq))
        p.start()

    print('collecting...')
    p=Process(target=proc_links, args=(lq,))
    p.start()
    p.join()
