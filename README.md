# ExifAddressFinder

The project **ExifAddressFinder** contains a executable named `find_address`. It adds the postal address in the EXIF Description tag of your geo-tagged pictures.

Coded on OSX, supposed to work on other UNIX platforms and possibly on Windows if the right dependencies are installed.

## Case example
A photo taken with a smartphone (GPS tagging activated) contains GPS informations like that:  
```
latitude : 32.7483333  
longitude: -117.123333
```

Then, the value written into the EXIF Description tag will be:
```
Thrifty, 3255 University Ave, San Diego, California 92104, United States
```
(The photo was taken on the pavement just in front of a Thrifty gas station)

So far, it works only for jpg images. It could also work for Tiff, but this was not tested.

## Installation

Download the [master](https://github.com/jonathanlurie/ExifAddressFinder/archive/master.zip), unzip-it somewhere and run:

```
cd ExifAddressFinder
python setup.py install
```

This will install the dependances and make `find_address`available to use in a terminal.

## Token
*Optional*  

This projects uses [Mapbox](http://mapbox.com) reverse-geocoding API to find an address from GPS coordinates. This API needs a *token*, which is hard-coded in the file `exif_address_finder/MAPBOX_TOKEN.py` and it should work quite well.  
If you plan to use `find_address` quite often, please considere getting your own token [here](https://www.mapbox.com/studio/account/tokens) to prevent any usage restriction.

## Usage

```shell
find_address --help
```


### Adding the EXIF Description tag
The default behavior of `find_address` is to add the address to the *already-existing* EXIF description. If there is no description, the tag will be created.

**For 1 image:**  

```shell
find_address -files /aFolder/image1.jpg
```

**For multiple images:**  

```shell
find_address -files /aFolder/image1.jpg /aFolder/image2.jpg /aFolder/image3.jpg
```

### Prefix and suffix

These are **optional**.

It's more than possible you want to format this raw address with some text, or maybe with HTML markups if you are sure you will use the description tag for the web.

```shell
find_address -prefix "(Hello, I am a prefix) " -suffix " (hello, I am a suffix)" -files /aFolder/image1.jpg
```

If we come back to our *Example Case*, the description tag will be:  
```
(Hello, I am a prefix) Thrifty, 3255 University Ave, San Diego, California 92104, United States (hello, I am a suffix)
```

Note the blank spaces at the end of the prefix and at the beginning of the suffix.  
If the image already had an EXIF description, you might want to use a *-prefix* containing just a white space to be sure the address is not stuck to the former description.

### Replacing an existing description

This is **optional**.

Case: you already have a description in your EXIF tag but you want to erase it, so that the EXIF tag contains only the address. Use the **-replace** option:  

```shell
find_address -replace -files /aFolder/image1.jpg
```

## Dependencies

Note: the following dependencies should be automatically downloaded/resolved during the installation process.

- **Exifread**, for easy EXIF reading ([Pypi](https://pypi.python.org/pypi/ExifRead) or [Github](https://github.com/ianare/exif-py))
- **Piexif**, for EXIF writing in pure Python ([Pypi](https://pypi.python.org/pypi/piexif/1.0.2) or [Github](https://github.com/hMatoba/Piexif))
- **Mapbox**, for reverse geocoding ([Pypi](https://pypi.python.org/pypi/mapbox/0.6.0) or [Github](https://github.com/mapbox/mapbox-sdk-py))

Exifread is way easier to use and does not require to know the EXIF tag ID (or any other related black magic), unfortunately it is just for reading. Piexif is trickier to use but allows reading **and** writing, which is pretty cool for a pure Python package.  
For this reason the next time I will work on **ExifAddressFinder**, I will try to get rid of Exifread to use only Piexif.

For those who want to know more about EXIF tags and black magic, [here](http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf) is the spec sheet I used.
