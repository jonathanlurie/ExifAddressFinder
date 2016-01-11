#!/usr/bin/env python

'''
Author      : Jonathan Lurie
Email       : lurie.jo@gmail.com
Version     : 0.1
Licence     : MIT
description :
              Doc for exif fields: http://piexif.readthedocs.org/en/latest/
'''


from mapbox import Geocoder

import codecs
import sys
import MAPBOX_TOKEN


class GeoToolbox:
    _geocoder = None

    #constructor
    def __init__(self):
        self._geocoder = Geocoder(access_token = MAPBOX_TOKEN.MAPBOX_ACCESS_TOKEN)


    # get the address from lat and lon
    def getAddress(self, latitude, longitude):
        fullAnswer = {"status": False, "code" : None, "address": None}

        response = self._geocoder.reverse(lon = longitude, lat = latitude)

        fullAnswer["code"] = response.status_code

        if(response.status_code == 200):
            fullAnswer["status"] = True


            for f in response.geojson()['features']:
                fullAnswer["address"] = u'{place_name}'.format(**f)
                break


        return fullAnswer


def TEST01_GeoToolbox():
    gtb = GeoToolbox()
    print gtb.getAddress(latitude=33.280491, longitude=-116.433201)
    print gtb.getAddress(latitude=43.599107, longitude=1.452454)

#if __name__ == '__main__':
#    TEST01_GeoToolbox()
