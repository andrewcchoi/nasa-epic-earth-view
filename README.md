# nasa-epic-earth-view
Download photos of earth from nasa's epic camera
Create GIF of rotating earth

EPIC_Earth_View: download earth images with built-in limiter for requests
EPIC_Earth_View_pool: download earth images using multiprocessing pool
EPIC_Earth_View_Movie: create an MP4 video of the images

NASA API
Earth Polychromatic Imaging Camera (EPIC)
url: https://api.nasa.gov/planetary/apod?api_key=

limit = 90 connections
Image locations
Site Name	                 Archive	Collection	 Year	Month	 Day	Image Type	 File Name
https://epic.gsfc.nasa.gov	archive	natural	    2016	10	    31	 png	        epic_1b_20161031xxxx.png
https://epic.gsfc.nasa.gov	archive	natural	    2016	10	    31	 jpg	        epic_1b_20161031xxxx.jpg
https://epic.gsfc.nasa.gov	archive	natural	    2016	10	    31	 thumbs	     epic_1b_20161031xxxx.jpg
https://epic.gsfc.nasa.gov	archive	enhanced	   2016	10	    31	 png	        epic_RGB_20161031xxxx.png
https://epic.gsfc.nasa.gov	archive	enhanced	   2016	10	    31	 jpg	        epic_RGB_20161031xxxx.jpg
https://epic.gsfc.nasa.gov	archive	enhanced	   2016	10	    31	 thumbs	     epic_RGB_20161031xxxx.jpg


Examples:
https://api.nasa.gov/EPIC/api/{natural/enhanced}/images?api_key=DEMO_KEY
https://epic.gsfc.nasa.gov/api/{natural/enhanced}/images

https://api.nasa.gov/EPIC/api/{natural/enhanced}/date/2019-05-30?api_key=DEMO_KEY
https://epic.gsfc.nasa.gov/api/{natural/enhanced}/date/2015-10-31

https://api.nasa.gov/EPIC/api/{natural/enhanced}/all?api_key=DEMO_KEY
https://epic.gsfc.nasa.gov/api/{natural/enhanced}/all

https://api.nasa.gov/EPIC/archive/{natural/enhanced}/2019/05/30/png/epic_1b_20190530011359.png?api_key=DEMO_KEY
https://epic.gsfc.nasa.gov/archive/{natural/enhanced}/2015/10/31/png/epic_1b_20151031074844.png

https://epic.gsfc.nasa.gov/api/

Metadata
Image [name]
Date
Caption
centroid_coordinates
dscovr_j2000_position
lunar_j2000_position
sun_j2000_position
attitude_quaternions
coords
{
lat (Latitude)
lon (Longitude)
centroid_coordinates (Geographical coordinates that the satellite is looking at)
dscovr_j2000_position (Position of the satellite in space)
lunar_j2000_position   (Position of the moon in space)
sun_j2000_position (Position of the sun in space)
attitude_quaternions   (Satellite attitude)
}

Screen shot
 image_element = driver.find_element_by_id('chartImg')
    src = image_element.get_attribute("src")
    if src:
        driver.get(src)
        driver.save_screenshot('screen.png')

https://epic.gsfc.nasa.gov/api/images.php?available_dates
