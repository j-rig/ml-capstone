
import os
import random
import requests
import os.path
import json
import time
import sys

ua_raw=open('ua.txt').read().strip().split('\n')
ua= [ s for s in ua_raw if s[0]!='#']
random.shuffle(ua)
print('loaded user agents:', len(ua))

# links_raw=open('crawl/l4/links.q.txt').readlines()
links=json.load(open('crawl/l4/links.q.json'))
# links=[ l for l in links_raw[1] if l.endswith('aspx')]
print(len(links))
# print(links_raw[:5])
# #links_raw=links_raw.split('\n')
# links=[ l for l in links_raw]
# links=[]
# with open('crawl/l4/links.q.txt') as fh:
#     line= fh.readline()
#     while len(line):
#         print(line)
#         # links.append(line.split())
#         line= fh.readline()
random.shuffle(links)

# print(links[:5])
# print(links[0])
# sys.exit(0)
print('loaded links to crawl:', len(links))

def get_url(url, referer):
    #print(url, referer)
    headers={'User-Agent':random.choice(ua),
        'Referer': referer}
    return requests.get(url,headers=headers,timeout=10)

print('')
cwd=os.getcwd()

basedir=os.path.join(cwd,'crawl','l4')
if not os.path.exists(basedir):
    print('creating', basedir)
    os.makedirs(basedir)

log=open(os.path.join(basedir,f'crawl.{os.getpid()}.log.txt'),'a')

i=0
c200=0
cn200=0
skipped=0
while len(links):
    link,referer=links.pop()
    datadir=os.path.join(basedir,os.path.join(*link.split('/')[3:]))
    datafile=os.path.join(datadir,'index.html')
    if not os.path.exists(datadir):
        print('creating', datadir)
        os.makedirs(datadir)
    if not os.path.exists(datafile):
        print(i,'getting', link)
        try:
            result=get_url(link, referer)
            if result.status_code==200:
                open(datafile,'w').write(result.text)
                c200+=1
            else:
                cn200+=1
            msg=f"{i},{time.time()},{result.status_code},{len(result.text)},{link}"
            log.write(msg+'\n')
            print(msg)
        except:
            cn200+=1
            msg=f'{i},{time.time()},exception,{link}'
            log.write(msg+'\n')
            print(msg)
            time.sleep(random.randrange(1,30))
        if not i % 107:
            time.sleep(random.randrange(1,7))
        # else:
        #     # time.sleep(random.randrange(1,2))
        #     pass
    else:
        skipped+=1
        print(i,'skipping',link)
    i+=1
    if c200 and i > skipped and float(cn200)/float(c200) > 0.2:
        log.write(f"{time.time()},200:{c200},Not200:{cn200},quitting...\n")
        break
