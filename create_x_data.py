import sys
import requests
import random
import json

try:
    count = int(sys.argv[1])
except ValueError:
    print "Should be integer"

for i in xrange(count):
    lat = "{0}{1}.{2}".format(random.choice(["-", ""]), random.randint(00, 99), random.randint(000000, 999999))
    lon = "{0}{1}.{2}".format(random.choice(["-", ""]), random.randint(00, 99), random.randint(000000, 999999))
    data = {"lat": lat, "lon": lon}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post("http://127.0.0.1:5000/position", data=json.dumps(data), headers=headers)
    print resp.status_code