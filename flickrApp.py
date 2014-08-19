__author__ = 'waynejessen'

import xml.etree.ElementTree as ET
import requests

f = open('flickr-data-SF#1.csv', 'w')

g = open('smallboxes-SF', 'w')
# api_key = 'for'

# flickr = flickrapi.FlickrAPI(api_key, format='etree')

#this is the space where I will connect to the db
# conn = psycopg2.connect(database='flickr_photos', user='wayne', password='smallbar')

#create the cursor
# cur = conn.cursor
url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=c83487f5d94759be0bcbe9a480be02c8'


#starting bounding box
#sf box -122.523763, 37.696404, -122.331622, 37.831665
#sd box -117.319930, 32.542581, -116.920422 ,32.896393
bboxlist = [[-122.523763, 37.696404, -122.331622, 37.831665]]

#initialize the smallbox list
smallboxes = []

#current box check for the total number of photos
def check_current_box(curbox):
    stringBox = str(curbox).strip("[]")
    args = {'min_take_date' : '2011-01-01',
            'bbox' : stringBox,
             'accuracy' : 16,
             'extras' : 'geo, date_taken, tags, url_sq'}
    box = requests.get(url, params = args)
    #need to parse element 'photos' in order to get
    #this will need to be debugged
    checkBox = ET.fromstring(box.content)
    total = int(checkBox[0].attrib['total'])
    nopages = int(checkBox[0].attrib['pages'])
    return {"total": total, "pages": nopages}


#function to get small enough boxes
def get_small_boxes(boundingbox):
    while len(boundingbox) > 0:
        for e in boundingbox:
            #get the current box
            currentbox = e
            #insert check_current_box here
            check = check_current_box(currentbox)
            nophotos, nopages = check['total'], check['pages']
            if nophotos >= 4000:
                print "Too many photos in the current box!"
                #find the height of the current box
                h = (abs(e[3] - e[1]) * .5)
                #find the width of the current box
                w = (abs(e[0] - e[2]) * .5)
                new_lat = e[1] + h
                new_lon = e[0] + w
                nb1 = [e[0], new_lat, new_lon, e[3]]
                bboxlist.append(nb1)
                nb2 = [new_lon, new_lat, e[2], e[3]]
                bboxlist.append(nb2)
                nb3 = [e[0], e[1], new_lon, new_lat]
                bboxlist.append(nb3)
                nb4 = [new_lon, e[1], e[2], new_lat]
                bboxlist.append(nb4)
                index = boundingbox.index(e)
                bboxlist.pop(index)
            else:
                print "This box is small enough"
                minilist = [e, nopages]
                smallboxes.append(minilist)
                get_data(e, nopages)
                index = boundingbox.index(e)
                bboxlist.pop(index)

def get_data(box, pages):
    curpage = 1
    while curpage <= pages:
        stringBox = str(box).strip("[]")
        args = {'min_take_date' : '2011-01-01',
                    'bbox' : stringBox,
                    'accuracy' : 16,
                    'extras' : 'geo, date_taken, tags, url_sq'}
        result = requests.get(url, params = args)
        curpage += 1
        for photo in result[1]:
            pid = str(photo.attrib['id'])
            line = "%s \n" %(pid)
            f.write(line)






get_small_boxes(bboxlist)


#this writes the small boxes list to a file.
for box in smallboxes:
    sbox = str(box)
    g.write(sbox + '"\n')












