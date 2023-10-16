import re
import sys

doc = open(sys.argv[1]).read()
doc_out = re.sub(
    'src="static/(.*)"', r""" src="{{ url_for('static', filename='\1') }}" """, doc
)

sys.stdout.write(doc_out)

sys.stdout.flush()
