__author__ = 'waynejessen'

import flickrapi

f = open('flickr-data-SD#2.csv', 'w')

g = open('smallboxes-SD', 'w')

api_key = 'c83487f5d94759be0bcbe9a480be02c8'

flickr = flickrapi.FlickrAPI(api_key, format='etree')

#this is the space where I will connect to the db
# conn = psycopg2.connect(database='flickr_photos', user='wayne', password='smallbar')

#create the cursor
# cur = conn.cursor

#starting bounding box
#sf box -122.523763, 37.696404, -122.331622, 37.831665
#sd box -117.319930, 32.542581, -116.920422 ,32.896393
bboxlist = [[-117.319930, 32.542581, -116.920422 ,32.896393]]

#initialize the smallbox list
smallboxes = []

#current box check for the total number of photos
def check_current_box(curbox):
    boxcheck = flickr.photos_search(min_taken_date='2011-01-01',
                                    bbox= '%s, %s, %s, %s'%(curbox[0], curbox[1], curbox[2], curbox[3]),
                                    accuracy='16',)
    #need to parse element 'photos' in order to get
    #this will need to be debugged
    boxcheck.attrib['stat'] = 'ok'
    total = boxcheck.find('photos').attrib['total']
    nophotos = int(float(total))
    pages = boxcheck.find('photos').attrib['pages']
    nopages = int(float(pages))
    return {"total": nophotos, "pages": nopages}


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
        result = flickr.photos_search(min_taken_date='2011-01-01',
                                        bbox= '%s, %s, %s, %s'%(box[0], box[1], box[2], box[3]),
                                        accuracy='16',
                                        page = '%s'% curpage,
                                        extras = 'geo, date_taken, tags')
        curpage += 1
        for photo in result.iter('photo'):
            pid = photo.get('id')     #pid = photoid, this gets the XML element labled id from the method above
            pids = str(pid)        #changes the data type of pid into a string
            f.write('"' + pids + '"' + ';')       #writes the string and a semi-colon to the file 'f'
            owner = photo.get('owner')
            owners = str(owner)
            f.write('"' + owners + '";')
            try:                        #any unicode errors in the title will have Unicodeerror as their title.
                title = photo.get('title')
                titles = str(title)
                f.write('"' + titles + '";')
            except UnicodeEncodeError:
                f.write('"UnicodeEncodeError";')
            lat = photo.get('latitude')
            lats = str(lat)
            f.write('"' + lats + '";')
            lon = photo.get('longitude')
            lons = str(lon)
            f.write('"' + lons + '";')
            placeid = photo.get('place_id')
            placeids = str(placeid)
            f.write('"' + placeids + '";')
            woeid = photo.get('woeid')
            woeids = str(woeid)
            f.write('"' + woeids + '";')
            try:                #same as above but with tags
                tag = photo.get('tags')
                tags = str(tag)
                f.write('"' + tags + '";')
            except UnicodeEncodeError:
                f.write('"UnicodeEncodeError";')
            date_taken = photo.get('datetaken')
            date_takens = str(date_taken)
            f.write('"' + date_takens + '"\n')   # the \n moves it down to the next line to start the next photo.



get_small_boxes(bboxlist)


#this writes the small boxes list to a file.
for box in smallboxes:
    sbox = str(box)
    g.write(sbox + '"\n')












