__author__ = 'waynejessen'
count = 0
practicelist = [21, 85, 52, 53, 99]

print len(practicelist) ," length"

for e in practicelist[:]:
    index = practicelist.index(e)
    print index , " index"
    practicelist.pop(index)
    print practicelist
    count = count + 1

print  count