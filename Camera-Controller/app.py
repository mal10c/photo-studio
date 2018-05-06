import logging
import os
import gphoto2 as gp
from flask import Flask
from shutil import copyfile

app = Flask(__name__)

def take_photo():

    log = ""

    # Get the directory containing this script
    photoDir = "/tmp"

    # Create capture directory
    photoDirName = "photos"
    photoDir = os.path.join(photoDir, photoDirName)
    if not os.path.exists(photoDir):
        log += "Creating photo directory" + "\n"
        os.makedirs(photoDir)
    
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    log += 'Capturing image' + "\n"
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    log += 'Camera file path: {0}/{1}'.format(file_path.folder, file_path.name) + "\n"
    photoFile = os.path.join(photoDir, file_path.name)
    log += 'Copying image to' + photoFile + "\n"
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, photoFile))
    gp.check_result(gp.gp_camera_exit(camera))

    newPath = os.path.dirname(os.path.realpath(__file__))
    newPath = os.path.join(newPath, "photos")

    log += "Copying to: " + newPath + "\n"

    if not os.path.exists(newPath):
        log += "Creating final photo directory" + "\n"
        os.makedirs(newPath)

    newPath = os.path.join(newPath, file_path.name)

    copyfile(photoFile, newPath)

    return photoFile, photoDir, log

@app.route('/')
def hello():
    photoFile, photoDir, log = take_photo()
    return '<b>Hello from the camera controller!\n{}\n\n{}'.format(photoDir, log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
