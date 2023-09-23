import os
import os.path
import extruct
from w3lib.html import get_base_url
import sys
import pprint
import json

linksd={}

base_url='https://www.bizbuysell.com'

ii=0
for root, dirs, files in os.walk("crawl/l1", topdown=False):
    for name in files:
        # print(ii, root)
        if name =='index.html':
            url=root.split('/')
            url[0]=base_url
            url_='/'.join(url)
            txt=open(os.path.join(root, name)).read()
            base_url_ = get_base_url(txt, url_)
            data = extruct.extract(txt, base_url=base_url_)
            jj=0
            for i in data['json-ld']:
                if 'about' in i.keys():
                    for j in i['about']:
                        if 'item' in j.keys():
                            k=j['item']
                            if 'productId' in k.keys() and 'url' in k.keys():
                                url=k['url'].split('/')[1:-1]
                                if url[-1]==k['productId']:
                                    url=[base_url,]+url
                                    url='/'.join(url)
                                    linksd[url]=url_
                                    jj+=1
        print(ii,jj,root)
    ii+=1
    # if ii > 100:
    #     break

cwd=os.getcwd()
basedir=os.path.join(cwd,'crawl','l2')
if not os.path.exists(basedir):
    print('creating', basedir)
    os.makedirs(basedir)

print(len(linksd))
links=[(k,v) for k,v in linksd.items()]
with open('crawl/l2/links.l2.json','w') as fh:
    json.dump(links,fh)
