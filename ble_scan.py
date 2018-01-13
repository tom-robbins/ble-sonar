import sys, json
from collections import defaultdict

d = defaultdict()
c = 0

for line in sys.stdin:
    try:
        c+= 1
        line = line.strip()
        if line[-3:] == ", }":
            line = line[:-3]+ "}"
        # print line
        j = json.loads(line)
        a = j['packet']['AdvA']['addr']
        if a in d.keys():
            d[a][1] = j['rssi']
        else:
            d[a] = [a, j['rssi']]
        if c % 10 == 0:
            for i in d:
                sys.stdout.write("%s\n" % str(d[i]))
            print "--------------------------"
    except:
        pass
