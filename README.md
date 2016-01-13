# ExifAddressFinder

**ExifAddressFinder** adds the postal address in the EXIF Description tag of your geo-tagged pictures.

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

## Usage

```shell
ExifAddressFinder --help
```

If the file ExifAddressFinder is not executable, you need to chmod it:

```shell
chmod u+x ExifAddressFinder
```

### Adding the EXIF Description tag
The default behavior of **ExifAddressFinder** is to add the address to the *already-existing* EXIF description. If there is no description, the tag will be created.

**For 1 image:**  

```shell
ExifAddressFinder -files /aFolder/image1.jpg
```

**For multiple images:**  

```shell
ExifAddressFinder -files /aFolder/image1.jpg /aFolder/image2.jpg /aFolder/image3.jpg
```

### Prefix and suffix

These are **optional**.

It's more than possible you want to format this raw address with some text, or maybe with HTML markups if you are sure you will use the description tag for the web.

```shell
ExifAddressFinder -prefix "(Hello, I am a prefix) " -suffix " (hello, I am a suffix)" -files /aFolder/image1.jpg
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
ExifAddressFinder -replace -files /aFolder/image1.jpg
```

## Dependencies
- **Exifread**, for easy EXIF reading ([Pypi](https://pypi.python.org/pypi/ExifRead) or [Github](https://github.com/ianare/exif-py))
- **Piexif**, for EXIF writing in pure Python ([Pypi](https://pypi.python.org/pypi/piexif/1.0.2) or [Github](https://github.com/hMatoba/Piexif))
- **Mapbox**, for reverse geocoding ([Pypi](https://pypi.python.org/pypi/mapbox/0.6.0) or [Github](https://github.com/mapbox/mapbox-sdk-py))

*Note:* Exifread is way easier to use and does not require to know the EXIF tag ID (or any other related black magic), unfortunately it is just for reading. Piexif is trickier to use but allows reading **and** writing, which is pretty cool for a pure Python package.  
For this reason the next time I will work on **ExifAddressFinder**, I will try to get rid of Exifread to use only Piexif.

For those who want to know more about EXIF tags and black magic, [here](http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf) is the spec sheet I used.
