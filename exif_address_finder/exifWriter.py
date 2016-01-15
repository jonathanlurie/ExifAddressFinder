#!/usr/bin/env python

'''
Author      : Jonathan Lurie
Email       : lurie.jo@gmail.com
Version     : 0.1
Licence     : MIT
description : Wraps piexif to write data to the EXIF tags.
              IFD_KEYS_REFERENCE contains tag codes
'''
import piexif
from IFD_KEYS_REFERENCE import *


# returns the value of a field.
# None if field does not exist
def readValue(exifDict, field):
    fieldValue = None

    if(field[0] in exifDict):
        if(field[1] in exifDict[field[0]]):
            fieldValue = exifDict[field[0]][field[1]]

    return fieldValue


# write to dictionnary.
# addToFormer allows to concatenate the new value with the old (string only)
def writeField(exifDict, field, value, addToFormer = False):
    if(addToFormer):
        # check if there was a value already
        formerValue = readValue(exifDict, field)
        if(formerValue):
            value = str(formerValue) + value

    if(field[0] in exifDict):
        exifDict[field[0]][field[1]] = value
    else:
        exifDict[field[0]] = {field[1] : value}

    return exifDict


# write dictionnary to file
def writeExifToFile(exifDict, fileAddress):
    exifBytes = piexif.dump(exifDict)
    piexif.insert(exifBytes, fileAddress)
