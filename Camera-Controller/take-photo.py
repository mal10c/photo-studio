#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2015-17  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# libgphoto2:
#   http://www.gphoto.org/proj/libgphoto2/support.php
# Install OpenCV:
#   sudo apt-get install libopencv-dev python-opencv
#   pip install -U numpy
#   If you get numpy errors, make sure PYTHONPATH is set properly in ~/.bashrc to:
#   /usr/local/lib/python3.6/dist-packages
# Install face recognition:
#   sudo pip install dlib
#   sudo pip3 install face_recognition
# Install blink detection:
#   sudo pip install --upgrade imutils
#   sudo pip install scipy
# CORBA:
#   sudo apt-get install omniorb
#   sudo apt-get install omniorb-idl
#   sudo apt-get install omniorb-nameserver
#   sudo apt-get install omnievents
#   sudo apt-get install python-omniorb
#   sudo apt-get install omniidl-python
#   sudo apt-get install virtualenv
#   
# Interesting link:
#   http://www.orocos.org/wiki/rtt/simple-examples/omniorbpy-python-binding-omniorb
from __future__ import print_function

import logging
import os
import subprocess
import sys
import argparse
import gphoto2 as gp
import cv2
from PIL import Image
import face_recognition

from imutils import face_utils
import numpy as np
import imutils
import dlib

parser = argparse.ArgumentParser(description='Takes photo for St. Joseph Fun Days')
parser.add_argument('email', help='E-mail address that will receive photo')
args = parser.parse_args()

def take_photo():

    # Get the directory containing this script
    photoDir = os.path.dirname(os.path.realpath(__file__))

    # Create capture directory
    photoDirName = "photos"
    photoDir = os.path.join(photoDir, photoDirName)
    if not os.path.exists(photoDir):
        print("Creating photo directory")
        os.makedirs(photoDir)
    
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    photoFile = os.path.join(photoDir, file_path.name)
    print('Copying image to', photoFile)
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, photoFile))
    #subprocess.call(['xdg-open', photoFile])
    gp.check_result(gp.gp_camera_exit(camera))

    return photoFile

def find_face_characteristics(photo):
 
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
 
    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(photo)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # detect faces in the grayscale image
    rects = detector(gray, 1)


    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
     
        # loop over the face parts individually
        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            # clone the original image so we can draw on it, then
            # display the name of the face part on the image
            clone = image.copy()
            cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 255), 2)
     
            # loop over the subset of facial landmarks, drawing the
            # specific face part
            for (x, y) in shape[i:j]:
                cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

            # extract the ROI of the face region as a separate image
            (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
            roi = image[y:y + h, x:x + w]
            roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)
     
            # show the particular face part
            #cv2.imshow("ROI", roi)
            #cv2.imshow("Image", clone)
            #cv2.waitKey(0)
     
        # visualize all facial landmarks with a transparent overlay
        output = face_utils.visualize_facial_landmarks(image, shape)
        cv2.imshow("Image", output)
        cv2.waitKey(0)


def find_faces_in_photo(photo):

    print("Looking for faces in: " + photo)
    image = face_recognition.load_image_file(photo)
    face_locations = face_recognition.face_locations(image)
    
    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()

def place_logo_on_photo(logo, inPhoto, outPhoto):

    mimage = Image.open(inPhoto)
    limage = Image.open(logo)

    # resize logo
    wsize = int(min(mimage.size[0], mimage.size[1]) * 0.25)
    wpercent = (wsize / float(limage.size[0]))
    hsize = int((float(limage.size[1]) * float(wpercent)))

    simage = limage.resize((wsize, hsize))
    mbox = mimage.getbbox()
    sbox = simage.getbbox()

    # right bottom corner
    box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
    mimage.paste(simage, box, simage)
    mimage.save(outPhoto)

def main():

    photo = take_photo()
    #find_faces_in_photo(photo)
    #find_face_characteristics(photo)
    
    place_logo_on_photo("logo-with-shadow.png", photo, "photos/out.jpg")
    #place_logo_on_photo("logo-with-shadow.png", "photos/eric.jpg", "photos/eric-out.jpg")

if __name__ == "__main__":
    sys.exit(main())
