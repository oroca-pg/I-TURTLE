#!/usr/bin/env python

import os
import sys
from dust.srv import *
import rospy
import urllib2
from urllib2 import urlopen
import datetime
from xml.etree.ElementTree import parse

#get xml data from url string
def get_request_url(url):
    
    req = urllib2.Request(url)
    
    try: 
        response = urllib2.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read()
    except Exception as e:
        print(e)
        print("[%s] Error : %s" % (datetime.datetime.now(), response.getcode()))
        return None

#Handler : Request -> Handler(Sort of Function) -> Response
def dust_handler(Region):
    #print(Region) -> Auto Decoding enveloped in Request Format 
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    url += "?stationName=" + Region.Request #Access to requested data directly(Auto Encoding -> it means original string) 
    url += "&dataTerm=daily"
    url += "&pageNo=1"
    url += "&numOfRows=1"
    url += "&ServiceKey="+"cNvqEBpqfdk%2BWoU1Z6gtlXSc%2FhYi48Ay4zlMrNWzQgeuXjn9Uu8PC4bTv3WIeAZxDBiOzKcVNujJcLhTVoHGsw%3D%3D"
    url += "&ver=1.0"

    #get xml data
    data = get_request_url(url)
    
    #xml parsing
    f = open("sample.xml","wb")
    f.write(data)
    f.close()
    xml_data = parse('sample.xml')
    
    #Define xml root
    root = xml_data.getroot()
    
    #Text mining
    dataTime = root.find("body").find("items").find("item").findtext("dataTime")
    pm10Value = root.find("body").find("items").find("item").findtext("pm10Value")
    pm25Value = root.find("body").find("items").find("item").findtext("pm25Value")
    pm10Grade = root.find("body").find("items").find("item").findtext("pm10Grade")
    pm25Grade = root.find("body").find("items").find("item").findtext("pm25Grade")
    khaiValue = root.find("body").find("items").find("item").findtext("khaiValue")
    khaiGrade = root.find("body").find("items").find("item").findtext("khaiGrade")

    ###############Grade###################
    ##1:very good 2:good 3:bad 4:very bad##     

    if khaiGrade == "1" :
	Result = "Very Good"
    elif khaiGrade == "2" :
	Result = "Good"     
    elif khaiGrade == "3" :
	Result = "Bad"
    elif khaiGrade == "4" :
	Result = "Very Bad"

    print("Returning [%s]"%Region.Request)
    print("Time : %s\npm10 : %s(%sppm)\npm25 : %s(%sppm)\nTotal : %s(%s)"%(dataTime,pm10Grade,pm10Value,pm25Grade,pm25Value,khaiGrade,khaiValue))
    
    return dustResponse(Region.Request,Result)  ##Response##

#Init_Server
def dust_server():
    rospy.init_node('dust_server')
    s = rospy.Service('dust', dust, dust_handler) #Service Name, Service Type, Handler
    print "Ready to let you know how good or bad the atmosphere is"
    rospy.spin() #Make it an infinite loop


if __name__ == "__main__":
    dust_server()






