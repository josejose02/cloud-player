# Wowza Cloud & Engine REST API v1
#   for Josestrem 2018
#   ------------------
# v0.1 of the python file
#   ------------------

import json
import requests
import xml.etree.ElementTree as ET #For the XML responses
import math

class josestreamCloud(object):
    def __init__(self):
        self.code = ""
        self.cloudKey = "r53CQvVmt8GbZYT79ZHzDfMSnpP2NVDEbaXlkqCQjdafpZj5olJ7wlXaiptZ3546"
        self.cloudAuth = "zoSCRpC3NZQDddZo7oRK8LGiYvICQfAxgi3eeyHiQrQ57o9e13MFyrEhcgKV3359"
        self.headers = {"wsc-api-key": self.cloudKey,"wsc-access-key": self.cloudAuth,"Content-Type": "application/json"}
        self.partURL = "https://api.cloud.wowza.com/api/"
        self.version = "v1"
        self.url = self.partURL + self.version

    def responseStatus(self, res):
        if res.status_code == 200:
            #print("Success")
            return True
        else:
            print("Error! - Request")
            print(res.content)
            return False

    def setData(self, identifier): #NOT USEFULL NOW :)
        response = requests.get(self.url+"/stream_targets/"+identifier, headers=self.headers)
        #??????????????????????????????

        self.code = "" #GET user stream cloud code (Wowza Cloud) --> something like this --> user.object.get(code)

    def newTarget(self, name):
        data = { "stream_target": { "name": name, "provider": "akamai_cupertino", "type": "WowzaStreamTarget" }}
        data = json.dumps(data)
        response = requests.post(self.url+"/stream_targets/", headers=self.headers, data=data)
        self.responseStatus(response)
        if True:
            response = response.json()
            base = response["stream_target"]
            identifier = base["id"]
            streamCode =  base["stream_name"]
            hls = base["hls_playback_url"]
            connectionCode = base["connection_code"]
            print("ID:{} Stream Name:{} | hls url:{} | Connection Code: {}").format( identifier,streamCode,hls,connectionCode)


    def getTarget(self, identifier):
        response = requests.get(self.url+"/stream_targets/"+identifier, headers=self.headers)
        self.responseStatus(response)
        response = response.json()
        base = response['stream_target'] #Base
        streamCode = base['stream_name']
        hls = base['hls_playback_url']
        https = base['use_https']
        data = {'stream_target':base, 'stream_name':streamCode, 'hls_playback':hls}
        return data


     #GeoBlocking --> Requiere sales to active (per change)...so jxc-ni5-mwp

    def getToken(self, identifier):
        response = requests.get(self.url+"/stream_targets/"+identifier+"/token_auth", headers=self.headers)
        self.responseStatus(response)
        response = response.json()
        return response['token_auth']['trusted_shared_secret']

    def createGeoBlock(self, code, ok):
        if ok == false:
            allow = ""
        response = requests.post(self.url+"/stream_targets/"+code+"/geoblock", headers=self.headers, data=data)
    #to -- sales, bla bla bla....

    def delTarget(self, identifier):
        response = request.delete(self.url+"/stream_targets/"+identifier+"/properties/????", headers=self.headers) # To see what the ??? is about !!!
        response2 = requests.get(self.url+"/stream_targets/"+identifier, headers=self.headers)
        if response2.status_code == 410:
            print("Success! - Target Deleted")


    #####       Usage Data      #####
    def getAnalytics(self, code):
        response = requests.get(self.url+"/usage/viewer_data/stream_targets/"+code, headers=self.headers)
        #Check
        self.responseStatus(response)
        #Parse
        response = response.json()
        countryList = response["stream_target"]["country_list"]
        i = 0
        while i < len(countryList):
            #i = o - 1
            code = countryList[i]
            base = response["stream_target"]["countries"][i][code]
            countryName = base["name"]
            percentageViewersC = base["percentage_viewers"]
            percentageViewingT = base["percentage_viewing_time"]
            averageTimeViewing = base["seconds_avg_viewing_time"]
            totalTimeViewing = base["seconds_total_viewing_time"]
            uniqueViews = base["total_unique_viewers"]
            print(("{} {} |Viewers: {}% (Time {}%, Average {}min, Total {}min) |Unique Viewers: {}").format(code, countryName, percentageViewersC, percentageViewingT, math.ceil(averageTimeViewing), math.ceil(totalTimeViewing), uniqueViews))
            i += 1

    def getnetworkUsage(self):
        response = requests.get(self.url+"/usage/network/stream_targets", headers=self.headers)
        #Check
        self.responseStatus(response)
        #Parse
        response = response.json()
        i = 0
        totalUsed = response["total"]["bytes_used"]
        totalBilled = response["total"]["bytes_billed"]
        targets = response["stream_source"]
        print(("Total used: {} | Total billed:{}").format(totalUsed, totalBilled))
        while i < len(targets):
            base = response["stream_targets"][i]
            billed = base["bytes_billed"]
            used = base["bytes_used"]
            deleted = base["deleted"]
            identifier = base["id"]
            name = base["name"]
            print(("{} {} (Deleted: {}) Used:{} | Billed:{}").format(identifier,name,deleted,used,billed))
