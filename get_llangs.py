import json
import requests
import sys

with open("musicians.txt", "r") as f:
    for line in f:
        try:
            url = line.strip()
            r = requests.get(url)
            j = r.json()
            _, val = j['query']['pages'].popitem()
            print(val['langlinks'][0]['*'])
        except:
            print("didn't find", line, file=sys.stderr)
