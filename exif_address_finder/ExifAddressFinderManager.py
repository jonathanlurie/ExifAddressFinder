#!/usr/bin/env python

'''
Author      : Jonathan Lurie
Email       : lurie.jo@gmail.com
Version     : 0.1
Licence     : MIT
description : The entry point to the library.
'''

import GeoToolbox
import exifread
import piexif
from IFD_KEYS_REFERENCE import *
import exifWriter
import os



class ExifAddressFinderManager:
    _geotoolbox = None


    def __init__(self):
        self._geotoolbox = GeoToolbox.GeoToolbox()


    # return a dictionnary {"lat": yy.yyy, "lon": xx.xxx}
    # or None if not found
    def _getGpsCoordinates(self, fileAddress):
        f = open(fileAddress, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f)

        # add positionning
        if('EXIF GPS GPSLatitude' in tags.keys()  and 'EXIF GPS GPSLongitude' in tags.keys()):

            # dealing with latitutes
            latValues = tags["EXIF GPS GPSLatitude"].values
            latRef = tags["EXIF GPS GPSLatitudeRef"]
            latInt = float(latValues[0].num)
            latDec = float(latValues[1].num) / float(latValues[1].den) / 60. + float(latValues[2].num) / float(latValues[2].den) / 3600.
            lat = latInt + latDec

            if(latRef.values != 'N'):
                lat = lat * (-1)

            # dealing with longitudes
            lonValues = tags["EXIF GPS GPSLongitude"].values
            lonRef = tags["EXIF GPS GPSLongitudeRef"]
            lonInt = float(lonValues[0].num)
            lonDec = float(lonValues[1].num) / float(lonValues[1].den) / 60. + float(lonValues[2].num) / float(lonValues[2].den) / 3600.
            lon = lonInt + lonDec

            if(lonRef.values != 'E'):
                lon = lon * (-1)

            return {"lat": lat, "lon": lon}

        else:
            return None


    # return the address if found
    # returns None if not retrieve
    def _retrieveAddress(self, latitude, longitude):
        address = self._geotoolbox.getAddress(latitude=latitude, longitude=longitude)

        # if the address was well retrieve
        if(address["status"]):
            return address["address"]
        else:
            return None


    # update the EXIF Decription field with the real postal address
    def _updateDescription(self, fileAddress, locationAddress, addToFormer=False):
        # reading exif
        exifDict = piexif.load(fileAddress)
        newDict = exifWriter.writeField(exifDict, DESCRIPTION_FIELD, locationAddress, addToFormer)
        exifWriter.writeExifToFile(newDict, fileAddress)


    def addAddressToImage(self, fileAddress, prefix="", suffix="", addToFormer=False):
        coordinates = self._getGpsCoordinates(fileAddress)

        if(not coordinates):
            print("\tERROR: "+ os.path.basename(fileAddress) +" is not geo tagged")
            return None

        postalAddress = self._retrieveAddress(coordinates["lat"], coordinates["lon"])

        if(not postalAddress):
            print("\tERROR: The address was impossible to retrieve")
            return None

        self._updateDescription(fileAddress, prefix + postalAddress + suffix, addToFormer)

        return 1
