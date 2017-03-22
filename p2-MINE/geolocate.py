#!/usr/bin/python
#
# Author: Alex Voitik
# Date: 14 March 2017
# File: geolocate.py
#
# Contents of this file taken from the example file
# geolocate.py given on the project specification page

import sys            # for sys.argv
import aws            # for aws.region_for_zone
import gcp            # for gcp.region_for_zone
import cloud          # for cloud.region_cities, etc.

# Get the central_host name and port number from the command line
central_host = sys.argv[1]
central_port = int(sys.argv[2])

# Figure out our own host name. 
try:
    # First try AWS meta-data service to figure out our own ec2 availability zone and region.
    my_dns_name = aws.get_my_dns_hostname()
    my_ipaddr = aws.get_my_external_ip()
    my_zone = aws.get_my_zone()
    my_region = aws.region_for_zone(my_zone)
except:
    # Next try GCP meta-data service.
    my_dns_name = gcp.get_my_internal_hostname()
    my_ipaddr = gcp.get_my_external_ip()
    my_zone = gcp.get_my_zone()
    my_region = gcp.region_for_zone(my_zone)

if my_dns_name == central_host or my_ipaddr == central_host:
    # If we are the central coordinator host...
    # then call some function that implements the front end and central coordinator.
    # This code assumes there is a file named central.py containing a function 
    # named run_central_coordinator(). Alternatively, you can delete these two lines and
    # put your central coordinator code right here.
    print "Starting central coordinator at http://%s:%s/" % (central_host, central_port)
    from central import *
    run_central_coordinator(my_ipaddr, my_zone, my_region, central_host, central_port)
else:
    # Otherwise, we are one of the pinger server hosts...
    # then call some function that implements the pinger server.
    # This code assumes there is a file named pinger.py containing a function 
    # named run_pinger_server(). Alternatively, you can delete these two lines and
    # put your pinger server code right here.
    print "Starting pinger within region %s (city: %s, coordinates: %s)" % (
            my_region, cloud.region_cities[my_region], cloud.region_coords[my_region])
    from pinger import *
    run_pinger_server(my_dns_name, my_region, central_host, central_port)