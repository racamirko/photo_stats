#!/usr/bin/python3
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import os
from os import path
import numpy as np
import matplotlib.pyplot as plt

img_ext = ['jpg', 'png', 'jpeg']

def get_exif(img_filename):
    parts = {'FocalLength': 0, 'ISOSpeedRatings': 0, 'MaxApertureValue': 0}
    img = Image.open(img_filename)
    try:
        info = img._getexif()
    except AttributeError:
        return {}
    if info is None:
        return {}
    for t,v in info.items():
        decoded = TAGS.get(t,t)
        if decoded in parts.keys():
            if isinstance(v, tuple):
                parts[decoded] = float(v[0])
                if v[1] > 0:
                    parts[decoded] /= v[1]
            else:
                parts[decoded] = v
    return parts

def scan_images(folder):
    focals = np.array([])
    isos = np.array([])
    apertures = np.array([])
    for root, dirs, files in os.walk(folder):
        for ff in files:
            if ff.split('.')[-1].lower() in img_ext:
                full_ff = path.join(root,ff)
                parts = get_exif(full_ff)
                print(full_ff+" has "+str(parts))
                if len(parts) == 0:
                    continue
                focals = np.append(focals, parts['FocalLength'])
                isos = np.append(isos, parts['ISOSpeedRatings'])
                apertures = np.append(apertures, parts['MaxApertureValue'])
    return focals, isos, apertures

if __name__ == '__main__':
    focals, isos, apertures = scan_images('/home/raca/Pictures')
    plt.subplot(2,2,1)
    plt.title("Aperture distribution")
    plt.hist(apertures, bins=20)

    plt.subplot(2,2,2)
    plt.title("Focal length distribution")
    plt.hist(focals, bins=20)

    plt.subplot(2,2,3)
    plt.title("ISO distribution")
    plt.hist(isos, bins=20)

    plt.show()
