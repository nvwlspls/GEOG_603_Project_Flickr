__author__ = 'waynejessen'

import flickrapi


import xml.etree.ElementTree as ET

import psycopg2

import geopy

from geopy.point  import Point

api_key = 'c83487f5d94759be0bcbe9a480be02c8'

flickr = flickrapi.FlickrAPI(api_key, format='etree')

#this is the space where I will connect to the db
conn = psycopg2.connect(database='flickr_photos', user='wayne', password='smallbar')

#create the cursor
cur = conn.cursor

#starting bounding box
bboxlist = [[-122.523763, 37.696404, -122.331622, 37.831665]]

#initialize the smallbox list
smallboxes = []

#current box check
def check_current_box(currentbox):
        boxcheck = flickr.photo_search(min_upload_date=2013-01-01,
                         bbox=currentbox,
                         accuracy=16,
                         extras='geo,date_taken,tags')
        #need to parse element 'photos' in order to get
        #this will need to be debugged
        boxcheck.attrib['stat'] = 'ok'
        total = boxcheck.find('photos').attrib['total']
        nophotos = int(float(total))
        return(nophotos)



#function to get small enough boxes
def get_small_boxes(boundingbox):
    for e in boundingbox:
        #get the current box
        currentbox = str(e).strip("[]")
        #insert check_current_box here
        for e in boundingbox:
            nophotos = check_current_box(currentbox)
            if nophotos >= 4000:
                print "Too many photos in the current box!"
                #find the height of the current box
                h = (abs(e[3] - e[1])*.5)
                #find the width of the current box
                w = (abs(e[0] - e[2])*.5)
                new_lat = e[1] + h
                new_lon = e[0] + w
                nb1 = [e[0] , new_lat , new_lon, e[3]]
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
                smallboxes.append(e)
                index = boundingbox.index(e)
                bboxlist.pop(index)


def get_data(boxes):
    for e in boxes:
        #initialize page variable
        pages = 0
        curpage = 1
        while curpage <= pages:
            currentbox = str(e).strip("[]")
            search = flickr.photos_search(min_upload_date='2013-01-01',
                                bbox = currentbox,
                                accuracy=16,
                                page = curpage,
                                extras='geo,date_taken,tags',
                                perpage = 250)
            pages = search.find('photos').attrib['pages']
            print pages , " number of pages"
            total_photos = search.find('photos').attrib['total']
            print total_photos , " total photos"
    '''this is where I need to parse the xml returned from the search
       i need to get down the the 'photo' element'''





















