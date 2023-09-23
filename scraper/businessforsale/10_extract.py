import os
import os.path
import json

i=0
j=0
with open('businessesforsale.search.lines.json','w') as fh:
    for crawls in ("crawl/l2/us","crawl/l3/us"):
        for root, dirs, files in os.walk(crawls, topdown=False):
            for name in files:
                if name == 'data.json':
                    dp=os.path.join(root,'data.json')
                    data=json.load(open(dp))
                    for d in data:
                        fh.write(json.dumps(d))
                        fh.write('\n')
                        i+=1
                    print(i,j)

with open('businessesforsale.detail.lines.json','w') as fh:
    for crawls in ("crawl/l1/us","crawl/l4/us"):
        for root, dirs, files in os.walk(crawls, topdown=False):
            for name in files:
                if name == 'data.json':
                    dp=os.path.join(root,'data.json')
                    data=json.load(open(dp))
                    if len(data):
                        fh.write(json.dumps(data))
                        fh.write('\n')
                        j+=1
                    print(i,j)
