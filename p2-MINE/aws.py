# aws.py
# Basic location data for Amazon Web Services EC2 datacenters.
#
# Run this program like this:
#    python gcp.py
#
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Date: 9 February 2017
#
# Amazon does not seem to publish information about the actual physical
# locations of their AWS EC2 datacenters, even though they sometimes use
# suggestive titles like "US East (N. Virginia)". 
##
# Each AWS "region" contains several "availability zones", and each
# "availability zone" contains several "data centers". The data centers are
# the physical buildings that house the enormous number of computers that make
# up EC2. The actual street addresses for the data centers are not public, and
# the buildings themselves can be a little difficult to find (see [1] for
# example). Even finding the approximate city or county involves a little
# guesswork. As best I am able, I've compiled below the name of the nearest
# major city where each region's datacenters seem to be housed, and the
# geographic latitude, longitude coordinates for those locations.
#
# Some of the informabion below comes from Turnkey Linux [2]. Those folks are using
# this information as part of their project, but they don't seem to cite their
# sources for this information.
#
# [1]: https://www.theatlantic.com/technology/archive/2016/01/amazon-web-services-data-center/423147/
# [2]: https://github.com/turnkeylinux/aws-datacenters/blob/master/input/datacenters

# Availability zones have names like us-east-1a or us-east-1b. To get the
# region name, we can just remove the last letter.
def region_for_zone(z):
    lastchar = z[len(z)-1]
    if lastchar >= 'a' and lastchar <= 'z':
        return z[0:len(z)-1]
    else:
        return z

# names of all AWS regions
regions = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "ca-central-1",
    "ap-south-1", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2",
    "eu-central-1", "eu-west-1", "eu-west-2",
    "sa-east-1",
]

# official english-language title of each AWS region
region_titles = {
    "us-east-1":         "US East (N. Virginia)", 
    "us-east-2":         "US East (Ohio)", 
    "us-west-1":         "US West (N. California)", 
    "us-west-2":         "US West (Oregon)", 
    "ca-central-1":      "Canada (Central)", 
    "ap-south-1":        "Asia Pacific (Mumbai)", 
    "ap-northeast-1":    "Asia Pacific (Tokyo)", 
    "ap-northeast-2":    "Asia Pacific (Seoul)", 
    "ap-southeast-1":    "Asia Pacific (Singapore)", 
    "ap-southeast-2":    "Asia Pacific (Sydney)", 
    "eu-central-1":      "EU (Frankfurt)", 
    "eu-west-1":         "EU (Ireland)", 
    "eu-west-2":         "EU (London)", 
    "sa-east-1":         "South America (Sao Paulo)", 
}

# city where each AWS datacenter is located, approximately
region_cities = {
    "us-east-1":         "Charlottesville",
    "us-east-2":         "Columbus",
    "us-west-1":         "Palo Alto",
    "us-west-2":         "Oregon",
    "ca-central-1":      "Montreal",
    "ap-south-1":        "Mumbai",
    "ap-northeast-1":    "Tokyo",
    "ap-northeast-2":    "Seoul",
    "ap-southeast-1":    "Singapore",
    "ap-southeast-2":    "Sydney",
    "eu-central-1":      "Frankfurt",
    "eu-west-1":         "Ireland",
    "eu-west-2":         "London",
    "sa-east-1":         "Sao Paulo",
}

# (latitude, longitude) where each AWS datacenter is located, approximately
region_coords = {
    "us-east-1":       (38.13, -78.45),
    "us-east-2":       (39.96, -83.00),
    "us-west-1":       (37.44, -122.14),
    "us-west-2":       (46.15, -123.88),
    "ca-central-1":    (45.50, -73.57),
    "ap-south-1":      (19.08, 72.88),
    "ap-northeast-1":  (35.41, 139.42),
    "ap-northeast-2":  (37.57, 126.98),
    "ap-southeast-1":  (1.37, 103.80),
    "ap-southeast-2":  (-33.86, 151.20),
    "eu-central-1":    (50.1167, 8.6833),
    "eu-west-1":       (53.35, -6.26),
    "eu-west-2":       (51.51, -0.13),
    "sa-east-1":       (-23.34, -46.38),
}

def get_my_external_ip():
    import requests
    r = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
    r.raise_for_status()
    return r.text

def get_my_dns_hostname():
    import requests
    r = requests.get('http://169.254.169.254/latest/meta-data/public-hostname')
    r.raise_for_status()
    return r.text

def get_my_zone():
    import requests
    r = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone/')
    r.raise_for_status()
    return r.text

# test code
if __name__ == "__main__":
    print "There are %d Amazon Web Services regions." % (len(regions))
    print "%-16s %-26s %-36s %s, %s" % ("zone", "title", "city", "lat", "lon")
    for r in regions:
        (lat, lon) = region_coords[r]
        print "%-16s %-26s %-36s %0.2f, %0.2f" % (r, region_titles[r], region_cities[r], lat, lon)

