"""
ImageNameFixer.py
"""

__author__ = 'Chris Campell'
__created__ = '1/14/2019'

import os
import sys
from PIL import Image
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol

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


def main():
    # Create the subdirectories used by this script if they don't already exist:
    if not os.path.exists(source_img_dir):
        os.mkdir(source_img_dir)
    if not os.path.exists(renamed_img_dir):
        os.mkdir(renamed_img_dir)
    if not os.path.exists(failed_img_dir):
        os.mkdir(failed_img_dir)

    # Traverse the source image directory. The topmost folder is the parent or 'root' folder:
    openable_images_failed_ocr = []
    unopenable_images = []

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
                print('\t[%d/%d] Running Optical Character Recognition (OCR) on image \'%s\':' % (i, num_files, fname))
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
                    continue
                # The image has been opened successfully, now try running OCR on the barcode:
                decoded_img = pyzbar.decode(img)
                if decoded_img:
                    ocr_success_images.append(os.path.join(dir_name, fname))
                    num_ocr_success += 1
                    print('\t\t%s' % decoded_img)
                else:
                    print('\t\tFailed to decode barcode.')
                    ocr_failure_images.append(os.path.join(dir_name, fname))
                    num_ocr_fails += 1
                    openable_images_failed_ocr.append(os.path.join(dir_name, fname))

if __name__ == '__main__':
    # Directories are relative to this script's location:
    root_dir = '../BarcodeReader'
    source_img_dir = 'MislabeledImages'
    renamed_img_dir = 'RenamedImages'
    failed_img_dir = 'FailedImages'

    # Ensure that the user installed the script in a directory with read and write permissions:
    if ensure_directory_is_readable_and_writeable(root_dir):
        print('INFO: Ensured script install directory exists, is readable, and is writeable.')
        main()
    else:
        print('Fatal Error: Terminating script...')
        sys.exit(-1)



