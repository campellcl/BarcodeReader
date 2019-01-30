"""
ImageNameFixer.py
"""

__author__ = 'Chris Campell'
__created__ = '1/14/2019'

import os
import sys
import shutil
from PIL import Image
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
import matplotlib.pyplot as plt
import numpy as np

# Valid image types that this program will attempt to read barcodes from
# NOTE: Extensions are case insensitive, if 'jpg' is in this list then both: 'MyFile.jpg' and 'MyFile.JPG' will be valid
VALID_EXTENSIONS = ['jpg', 'jpeg', 'png']


def ensure_directory_is_readable_and_writeable(dir):
    """
    ensure_directory_is_readable_and_writeable: Ensures that the directory:
        1) Exists
        2) Has been granted read permissions by the OS
        3) Has been granted write permissions by the OS
    :param dir: <str> The directory to ensure the above for.
    :return: <bool> True if the directory exists, is readable, and writeable; False otherwise.
    """
    # Ensure the directory exists:
    if os.path.exists(dir):
        # Ensure the directory has read access:
        if os.access(dir, os.R_OK):
            # Ensure the directory has write access:
            if os.access(dir, os.W_OK):
                return True
            else:
                print('Error: This script does not have OS permission to write to the provided directory: \'%s\'' % dir)
                return False
        else:
            print('Error: This script does not have OS permission to read from the provided directory: \'%s\'' % dir)
            return False
    else:
        print('Error: This script could not find the provided directory: \'%s\' on your machine.' % dir)
        return False


def resize_image(img, new_width):
    """
    resize_image: Resizes the provided image to the specified width while preserving aspect ratio. This appears to be
    what the pearl version of the script does via ImageMagick geometry argument.
    :url :
    :param new_width:
    :return:
    """
    img_clone = img.copy()
    maximum_width, maximum_height = img.size
    resize_dims = new_width, maximum_height
    try:
        img_clone.thumbnail(resize_dims, Image.ANTIALIAS)
        # img_clone.thumbnail(resize_dims)
    except Exception as err:
        print('Could not create thumbnail for image: %s. Stack trace: %s' % (img, err))
        return None
    return img_clone


def main():
    # Create the subdirectories used by this script if they don't already exist:
    if not os.path.exists(source_img_dir):
        os.mkdir(source_img_dir)
    if not os.path.exists(renamed_img_dir):
        os.mkdir(renamed_img_dir)
    if not os.path.exists(failed_img_dir):
        os.mkdir(failed_img_dir)

    # Traverse the source image directory. The topmost folder is the parent or 'root' folder:
    for dir_name, sub_dir_list, file_list in os.walk(source_img_dir):
        # Skip the parent directory:
        if dir_name == root_dir:
            continue

        print('Walking directory : %s' % dir_name)
        num_files = len(file_list)
        openable_images = []
        unopenable_images = []
        ocr_success_images = []
        ocr_failure_images = []
        num_ocr_success = 0
        num_ocr_fails = 0
        num_openable_files = 0

        for i, fname in enumerate(file_list):
            # Ensure that the image extension is in the list of programmer specified valid extension file types:
            if os.path.basename(fname).lower().split('.')[1] in VALID_EXTENSIONS:
                print('\t[%d/%d] Running Optical Character Recognition (OCR) on image \'%s\':' % (i+1, num_files, fname))
                # Attempt to open the image using PIL:
                try:
                    img = Image.open(os.path.join(dir_name, fname))
                    openable_images.append(os.path.join(dir_name, fname))
                    num_openable_files += 1
                    if os.path.getsize(os.path.join(dir_name, fname)) == 0:
                        print('\t\tWARNING: Image \'%s\' is of size 0 bytes.' % fname)
                except Exception as err:
                    print('\t\tERROR: Failed to open image \'%s\'. Proceeding without this image.' % fname)
                    unopenable_images.append(os.path.join(dir_name, fname))
                    # Copy image to failed_image_dir:
                    shutil.copy(os.path.join(dir_name, fname), os.path.join(failed_img_dir, fname))
                    continue
                # The image has been opened successfully, now try running OCR on the barcode:
                decoded_img = pyzbar.decode(img)
                if decoded_img:
                    # OCR worked
                    ocr_success_images.append(os.path.join(dir_name, fname))
                    num_ocr_success += 1
                    print('\t\t%s' % decoded_img)
                    # Get the new image name from the barcode:
                    new_img_name = decoded_img[0][0].decode()
                    # Get the old image extension:
                    source_img_ext = os.path.splitext(img.filename)[1]
                    # Copy and rename the image:
                    shutil.copy(src=os.path.join(dir_name, fname), dst=os.path.join(renamed_img_dir, new_img_name + source_img_ext))
                else:
                    # OCR failed
                    print('\t\tFailed to decode barcode. Attempting to resize and OCR...')
                    # plt.imshow(np.array(img))
                    # plt.show()
                    # plt.clf()
                    # See: http://www.imagemagick.org/script/command-line-processing.php#geometry for magic number 3000x
                    resized_img = resize_image(img, new_width=3000)
                    # plt.imshow(np.array(resized_img))
                    # plt.show()
                    print('\t\t\tImage down-sampled to new aspect ratio: %s. Attempting to OCR...' % (resized_img.size,))
                    decoded_img = pyzbar.decode(resized_img)
                    if decoded_img:
                        # OCR Success:
                        ocr_success_images.append(os.path.join(dir_name, fname))
                        num_ocr_success += 1
                        print('\t\t\t%s' % decoded_img)
                        # Get the new image name from the barcode:
                        new_img_name = decoded_img[0][0].decode()
                        # Get the old image extension:
                        source_img_ext = os.path.splitext(img.filename)[1]
                        # Copy and rename the image:
                        shutil.copy(src=os.path.join(dir_name, fname), dst=os.path.join(renamed_img_dir, new_img_name + source_img_ext))
                    else:
                        # OCR Failure
                        print('\t\t\tOCR failed on the resized image. Copying image: \'%s\' to the failed image '
                              'directory: \'%s\'.' % (fname, failed_img_dir))
                        ocr_failure_images.append(os.path.join(dir_name, fname))
                        num_ocr_fails += 1
                        # Copy image to failed_image_dir:
                        shutil.copy(os.path.join(dir_name, fname), os.path.join(failed_img_dir, fname))

        # Dump list of failed OCR images to root directory:
        with open('failed_images.txt', 'w') as fp:
            for image_name in ocr_failure_images:
                fp.write(os.path.basename(image_name) + '\n')
        print('Script finished. Failed to OCR the images listed in the \'failed_images.txt\' file. Exiting...')
        exit(0)


if __name__ == '__main__':
    # Directories are relative to this script's location:
    root_dir = '../BarcodeReader'
    source_img_dir = 'MislabeledImages'
    renamed_img_dir = 'RenamedImages'
    failed_img_dir = 'FailedImages'

    # Ensure that the user installed the script in a directory with read and write permissions:
    if ensure_directory_is_readable_and_writeable(root_dir):
        print('INFO: Ensured script install directory exists, is readable, and is writeable.')
        if not os.path.isdir(source_img_dir):
            os.mkdir(source_img_dir)
            print('INFO: Created directory \'%s\' for you. Please place all mislabeled images in this folder, '
                  'and run the script again.' % source_img_dir)
            exit(0)
        main()
    else:
        print('Fatal Error: Terminating script...')
        sys.exit(-1)
