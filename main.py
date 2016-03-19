#!/usr/bin/env python

import argparse 
import satellite
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import glob
import os.path

def plot_data_matrix(data_matrix):
    pass


# Clean working environment (should be called before main)
def clean():
    import os
    os.system("rm -f /tmp/*.gz /tmp/*.nc")

def main():
  
	# Define parser data
    parser = argparse.ArgumentParser(description='Plotting satellite data.')
    # First arguments. Dates. TODO:SPECIFY INITIAL AND FINAL ORDER
    parser.add_argument('date', metavar='YYYY.MM.DD YYYY.MM.DD', type=str, nargs=2,\
		      help='Initial date followed by end date')
    # Specify sattelites to exclude from command line. TODO: change to flag!
    parser.add_argument('--no-ascat', dest='ascat_bool', action="store_true", \
		      default= False, help="Don't display ASCAT information")

    # Extract dates from args
    args=parser.parse_args()
    initialDate = args.date[0]
    finalDate = args.date[1]
    
    # Flow control depending on specified options
    if not args.ascat_bool:
        # Instantiate ASCAT and get datetime object
        ascat = satellite.ASCAT(initialDate, finalDate)
        ascat.get_datetime_object()
        # Download files from ASCAT servers
        ascat.download_files()
        # Get figure handler and colormap
        m, cmap = satellite.generate_figure()   
        # Process for every *.nc file in folder
        for src_name in glob.glob(os.path.join("/tmp", '*.nc')):
            base = os.path.basename(src_name)
            lat, lon, data = ascat.extract_data(src_name)
            satellite.plot_data(m, lat, lon, data, cmap)
        # Finalize plot design and show it
        plt.title('ASCAT - Sfc Wind Speed')
        plt.show()

    else:
        print "You've discarded all the satellites I know!"

if __name__ == "__main__":
    clean()
    main()  
