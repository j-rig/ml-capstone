import os
import os.path

for root, dirs, files in os.walk('crawl/l2', topdown=False):
    for name in files:
        if name == 'data.json':
            p=os.path.join(root,'data.json')
            print('removing', p)
            os.remove(p)
