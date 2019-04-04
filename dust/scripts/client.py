#!/usr/bin/env python

import sys
import rospy
from dust.srv import *

def dust_client(req):
    rospy.wait_for_service('dust') #Wait for server
    try:
        dust_handler = rospy.ServiceProxy('dust', dust) #handler(Name, Type) : Requesting handler, Proxy
        resp = dust_handler(req) #Return = dustResponse / resp.Region : jongro-gu, resp.Result : Good
	print("Region : %s"%resp.Region)
        return resp.Result 
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "put [string1]"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        req = str(sys.argv[1])
    else:
        print usage()
        sys.exit(1)
    print("%s requested"%(req))
    print("Status %s"%dust_client(req))
