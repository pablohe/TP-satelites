# Date time manipulation libraries
import datetime
from datetime import timedelta, date

# Links extraction libraries
import urllib
import lxml.html
import re

# Data-handling and plotting routines libraries
from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl

# Get lists of dates between two given days
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

# Get handler for figure and setup colormap
def generate_figure():
    # Initiate figure
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
        llcrnrlon=0,urcrnrlon=360,lat_ts=20,resolution='c')
    # Draw coastlines, etc.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.drawparallels(np.arange(-60.,60.,15.))
    m.drawmeridians(np.arange(0.,360.,60.))

    # Configure colormap
    cmap = plt.cm.jet
    cmap.set_under((0,0,0,0)) 
    
    return m, cmap
    
# Plot data (Satellite independent)
def plot_data(fig_handler, x, y, data, cmap):
    # Latitude and longitudes projection
    x,y = fig_handler(y,x)
    
    # Plot
    cs = fig_handler.pcolor(x,y,data,cmap=cmap, vmin=0,\
        vmax=30)
    
    # Configure colorbar
    cb = fig_handler.colorbar(cs,"right", size="5%", pad='2%')
    cb.set_label('m/s')
    cb.set_ticks([0, 10, 20, 30, 40])        

        
# Abstract satellite class
class Satellite(object):
    # Constructor
    def __init__(self, initial_time, final_time):
        self.initial_time = initial_time
        self.final_time = final_time

# ASCAT subclass
class ASCAT(Satellite):
    # Constructor
    def __init__(self,initial_time, final_time):
        Satellite.__init__(self,initial_time, final_time)
    
    # Convert string to datetime object
    def get_datetime_object(self):
        # Expected format for input
        formt = '%Y.%m.%d'
        
        # Creates datetime object
        self.initial_time = datetime.datetime.strptime(self.initial_time, formt)
        self.final_time = datetime.datetime.strptime(self.final_time, formt)

    # Download all files for certain day
    def download_files(self):
        root_URL = 'http://podaac-opendap.jpl.nasa.gov/opendap/allData/ascat/preview/L2/metop_b/25km/'
        for day in daterange(self.initial_time,self.final_time):
            URL = root_URL + str(day.year) + '/' + str(day.timetuple().tm_yday) + '/'
            print "Downloading data for day {}".format(day.date())
            self.get_netCDF(URL)

    # Extract list of gz files (wouldn't be necessary if FTP was possible)
    def get_links (self,url):
        # Opens index html page
        connection = urllib.urlopen(url)
        # Get DOM information for index html page
        dom =  lxml.html.fromstring(connection.read())
        files = []
        # Iterate through links in the webpage
        for link in dom.xpath('//a/@href'):
            # If it doesn't have opendap (garbage links)
            if (not re.search("opendap", link)):
                # Get only files which end in .gz
                if (re.search("gz$", link)):
                    files.append(link)
        return files

    # Downloads NetCDF4 files for ASCAT (geniuses at NASA erroneusly append .gz -.-)
    def get_netCDF(self,url):
        # Get links
        files = self.get_links(url)
        # Counter for error message
        i=1
        # Download files to directory
        for item in files:
            fullurl = url+item
            dest = "/tmp/" + item[:-3]
            print "    Downloading file {}".format(i)
            urllib.urlretrieve(fullurl, dest)       
            i = i + 1

    # Extract data for ASCAT satellites
    def extract_data (self, path_to_file):
        # Opens file
        f=Dataset(path_to_file,"r")

        # Extract lat, long, time and wind speed
        latitudes=f.variables["lat"][:,:]
        longitudes=f.variables["lon"][:,:]
        wind_speed = f.variables["wind_speed"]        
        velviento = f.variables["wind_speed"][:,:]
        
        # Replace missing values for NaNs
        faltante=wind_speed._FillValue
        velviento.data[velviento.data == faltante] = np.nan
        velviento.data[velviento.data == 0] = np.nan

        # Return values of interest
        return latitudes, longitudes, velviento.data



"""    
class OTROSAT(object):
    
    def __init__(self...):
        pass
    def make_URL(self,initial_date,final_date...):
        
        
        pass
    def make_data_matrix(self,...):
        pass
    
"""
