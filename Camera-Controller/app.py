import logging
import os
import gphoto2 as gp
from flask import Flask, request, redirect
from shutil import copyfile
import logging
from PIL import Image
import json
import io

app = Flask(__name__)

def take_photo(token, ct, p):

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
        format='%(levelname)s: %(name)s: %(message)s', level=logging.INFO)
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

    newPath = "/photos"
    fileName = token + "__" + str(ct) + "_" + file_path.name
    newDir = os.path.join(newPath, token)
    if not os.path.exists(newDir):
        logging.info("Creating directory for photos at: " + newDir)
        os.mkdir(newDir)
    else:
        logging.warning("Photo directory already exists: " + newDir)

    newPath = os.path.join(newDir, fileName)
    fileNameWithLogo = token + "__" + str(ct) + "_LOGO_" + file_path.name
    newPathWithLogo = os.path.join(newDir, fileNameWithLogo)
    copyfile(photoFile, newPath)

    place_logo_on_photo("/logo/logo-with-shadow.png", newPath, newPathWithLogo, p)

    return newDir

def place_logo_on_photo(logo, inPhoto, outPhoto, percent):

    mimage = Image.open(inPhoto)
    limage = Image.open(logo)

    # resize logo
    wsize = int(min(mimage.size[0], mimage.size[1]) * percent)    
    wpercent = (wsize / float(limage.size[0]))
    hsize = int((float(limage.size[1]) * float(wpercent)))

    simage = limage.resize((wsize, hsize))
    mbox = mimage.getbbox()
    sbox = simage.getbbox()

    # right bottom corner
    box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
    mimage.paste(simage, box, simage)
    mimage.save(outPhoto)

@app.route('/<path:path>')
def catch_all(path):
    if path == "takePhoto":
        token = request.args.get("token")
        ct = request.args.get("ct")
        p = request.args.get("p")
        email = request.args.get("email")
        fname = request.args.get("fname")
        lname = request.args.get("lname")
        logging.info("TAKING PICTURE!")
        newPath = take_photo(token, ct, float(p))

        # Create json file in directory containing images
        data = {
            "email": email,
            "fname": fname,
            "lname": lname,
            "path": newPath
        }

        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str

        jsonFile = os.path.join(newPath, "data.json")
        with io.open(jsonFile, 'w', encoding='utf8') as dataFile:
            str_ = json.dumps(data,
                indent=4,
                sort_keys=True,
                separators=(',', ': '),
                ensure_ascii=False)
            dataFile.write(to_unicode(str_))

        return '{}'.format(newPath)
    
    return "No token given"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", debug=True)
