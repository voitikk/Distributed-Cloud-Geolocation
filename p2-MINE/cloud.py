# cloud.py
# Basic location data demo for both AWS and GCP datacenters.
#
# Run this program like this:
#    python cloud.py
#
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Date: 9 February 2017
#

import aws
import gcp

# names of all AWS and GCP regions
regions = aws.regions + gcp.regions

# official english-language title of each AWS or GCP region
region_titles = aws.region_titles.copy()
region_titles.update(gcp.region_titles)

# city where each AWS or GCP datacenter is located, approximately
region_cities = aws.region_cities.copy()
region_cities.update(gcp.region_cities)

# (latitude, longitude) where each AWS or GCP datacenter is located, approximately
region_coords = aws.region_coords.copy()
region_coords.update(gcp.region_coords)

# test code
if __name__ == "__main__":
    print "There are %d AWS and GCP cloud regions." % (len(regions))
    for r in regions:
        print r
        print "  title:", region_titles[r]
        print "  city:", region_cities[r]
        (lat, lon) = region_coords[r]
        print "  latitude:", lat
        print "  latitude:", lon

