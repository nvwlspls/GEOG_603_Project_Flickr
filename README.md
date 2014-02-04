GEOG_603_Project_Flickr
=======================
This project is desgined to get geo data about flickr photos for a given area.  Large cities can have hundreds of thousands of flickr photos that are geotagged within their city limits.  Flickr limits the amount of photos that can be returned for one query to 4,000 photos.  This app will take one large bounding box and break it down into smaller and smaller boxes until the number of results is under 4,000.  Once the box is small enough another request is made to the server and the results are parsed and written to a csv file.

