__author__ = 'waynejessen'

import flickrapi as flickr

import xml.etree.ElementTree as ET

import psycopg2

import geopy

from geopy.point  import Point

#this is the space where I will connect to the db
#dbconnect....


'''I am using this file to try the .walk method that comes with the flickrapi
helper I have been using.  This will walk through each result from the search
that I am using.  However, I have been having some problems with duplicate
records being returned.  I will nedd to work in some error variables to count
errors and ensure that I do not enter duplicate records into the db.
'''

walker = flickr.walk(min_upload_date='2013-01-01',
                             bbox='-122.523763, 37.696404, -122.331622, 37.83166',
                             accuracy=16,
                             extras='geo,date_taken,tags')

total = walker.find('photos').attrib['total']
print total , " total photos for bbox"

for photo in walker:
    for photo in walker:
	pid = photo.get('id')
	owner = photo.get('owner')
	try:
		title = photo.get('title')
	except UnicodeEncodeError:
		title = "UnicodeEncodeError"
	lat = photo.get('latitude')
	lon = photo.get('longitude')
	placeid = photo.get('place_id')
	woeid = photo.get('woeid')
	try:
		tag = photo.get('tags')
	except UnicodeEncodeError:
		tag = ("Unicode Error")
	date_taken = photo.get('datetaken')
	xy  = geopy.Point(lat,lon)
	#lat,lon,alt = xy
	#print xy , "second"
	#print xy
	try:
		cur.execute("INSERT INTO photos VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (pid, owner, title, lat, lon, placeid, woeid, tag, date_taken, xy))
	except (psycopg2.IntegrityError, psycopg2.DataError):
		errors = errors + 1
	conn.commit()
	print errors
	#count = count + 1

