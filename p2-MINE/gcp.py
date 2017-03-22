# gcp.py
# Basic location data for Google Cloud Platform GCE datacenters.
#
# Run this program like this:
#    python gcp.py
#
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Date: 9 February 2017
#
# Google is a bit more public about the actual physical locations of their GCP
# GCE datacenters than Amazon, but the location data below is still only an
# approximation.
##
# Each GCP "region" contains several "availability zones", and each
# "availability zone" contains several "data centers". The data centers are
# the physical buildings that house the enormous number of computers that make
# up GCE.

# Availability zones have names like us-east1-a or us-east1-b. To get the
# region name, we can just remove the last letter and the dash .
def region_for_zone(z):
    lastchar = z[len(z)-1]
    penultimatechar = z[len(z)-2]
    if lastchar >= 'a' and lastchar <= 'z' and penultimatechar == '-':
        return z[0:len(z)-2]
    else:
        return z

# names of all GCP regions
regions = [
    "us-west1", "us-central1", "us-east1", 
    "europe-west1",
    "asia-east1", "asia-northeast1",
]

# official english-language title of each GCP region
region_titles = {
    "us-west1":          "Western US (Oregon)",
    "us-central1":       "Central US (Iowa)",
    "us-east1":          "Eastern US (S. Carolina)",
    "europe-west1":      "Western Europe (Belgium)",
    "asia-east1":        "Eastern Asia-Pacific (Taiwan)",
    "asia-northeast1":   "Northeastern Asia-Pacific (Japan)",
}

# city where each GCP datacenter is located, approximately
region_cities = {
    "us-west1":          "The Dalles",
    "us-central1":       "Council Bluffs",
    "us-east1":          "Berkeley County",
    "europe-west1":      "St. Ghislain",
    "asia-east1":        "Changhua County",
    "asia-northeast1":   "Tokyo",
}

# (latitude, longitude) where each GCP datacenter is located, approximately
region_coords = {
    "us-west1":          (45.594565, -121.178682),
    "us-central1":       (41.261944, -95.860833),
    "us-east1":          (33.126062, -80.008775),
    "europe-west1":      (50.449109, 3.818376),
    "asia-east1":        (24.051796, 120.516135),
    "asia-northeast1":   (35.689488, 139.691706),
}

metadata_flavor = {'Metadata-Flavor' : 'Google'}

def get_my_internal_hostname():
    import requests
    r = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/name', headers = metadata_flavor)
    r.raise_for_status()
    return r.text

def get_my_external_ip():
    import requests
    r = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip', headers = metadata_flavor)
    r.raise_for_status()
    return r.text

def get_my_zone():
    import requests
    r = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/zone', headers = metadata_flavor)
    r.raise_for_status()
    return r.text.split('/')[-1]

# test code
if __name__ == "__main__":
    print "There are %d Google Cloud Platform regions." % (len(regions))
    print "%-16s %-26s %-36s %s, %s" % ("zone", "title", "city", "lat", "lon")
    for r in regions:
        (lat, lon) = region_coords[r]
        print "%-16s %-26s %-36s %0.2f, %0.2f" % (r, region_titles[r], region_cities[r], lat, lon)

