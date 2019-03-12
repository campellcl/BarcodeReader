"""
ImageNameFixer.py
"""

__author__ = 'Chris Campell'
__created__ = '1/14/2019'
__updated__ = '2/17/2019'

import os
import sys
import shutil
from PIL import Image
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
# import matplotlib.pyplot as plt
# import numpy as np

# Valid image types that this program will attempt to read barcodes from
# NOTE: Extensions are case insensitive, if 'jpg' is in this list then both: 'MyFile.jpg' and 'MyFile.JPG' will be valid
VALID_EXTENSIONS = ['jpg', 'jpeg', 'png']


def _directory_exists_and_is_readable_and_writeable(dir):
    """
    _directory_exists_and_is_readable_and_writeable: Ensures that the directory:
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
                print('INFO: Ensured directory: \'%s\' exists, is readable, and is writeable.' % dir)
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
    what the pearl version of the script does via ImageMagick's geometry argument.
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


def _get_mislabeled_image_dir_from_user():
    while True:
        mislabeled_img_dir = input('Enter the file path to the folder containing mislabeled images here (you can always '
                                   'copy and paste it): ')
        if _directory_exists_and_is_readable_and_writeable(mislabeled_img_dir):
            break
        else:
            print('Try again.')
    return mislabeled_img_dir


def _get_failed_image_dir_from_user():
    while True:
        failed_img_dir = input('Enter the file path to the folder where you wish mislabeled images (which could not be '
                               'automatically re-named) to be copied to: ')
        if _directory_exists_and_is_readable_and_writeable(failed_img_dir):
            break
        else:
            print('Try again.')
    return failed_img_dir


def _get_renamed_image_dir_from_user():
    while True:
        renamed_img_dir = input('Enter the file path to the folder where you wish automatically renamed images to be '
                                'copied to: ')
        if _directory_exists_and_is_readable_and_writeable(renamed_img_dir):
            break
        else:
            print('Try again.')
    return renamed_img_dir


def _get_wants_failed_images_copied_from_user():
    wants_failed_images_copied = None
    while wants_failed_images_copied is None:
        wants_failed_images_copied_verbatim = input('Do you wish for mislabeled images that are not able to be '
                                                    'automatically re-named to be copied over to a separate folder? '
                                                    'Enter {(y)es, (n)o}: ')
        if wants_failed_images_copied_verbatim.lower() == 'yes' or wants_failed_images_copied_verbatim.lower() == 'y':
            wants_failed_images_copied = True
        elif wants_failed_images_copied_verbatim.lower() == 'no' or wants_failed_images_copied_verbatim.lower() == 'n':
            wants_failed_images_copied = False
        else:
            print('Failed to interpret user entered response: \'%s\'. Please enter either \'yes\' (\'y\') or \'no\' '
                  '(\'n\'). Try again!' % wants_failed_images_copied_verbatim)
    return wants_failed_images_copied


def _ocr_and_rename_all_images_in_dir(mislabeled_img_dir, renamed_img_dir, failed_img_dir=None):
    openable_images = []
    unopenable_images = []
    ocr_success_images = []
    ocr_failure_images = []
    # num_ocr_successes = 0
    # num_ocr_failures = 0
    num_openable_files = 0

    for dir_name, sub_dir_list, file_list in os.walk(mislabeled_img_dir):
        print('INFO: Walking directory: \'%s\'' % dir_name)
        num_files_in_dir = len(file_list)
        num_ocr_failures_in_dir = 0
        num_ocr_successes_in_dir = 0
        for i, fname in enumerate(file_list):
            # Ensure that the image extension is in the list of programmer specified valid extension file types:
            if os.path.basename(fname).lower().split('.')[1] in VALID_EXTENSIONS:
                print('\t[%d/%d] Running Optical Character Recognition (OCR) on image \'%s\':' % (i+1, num_files_in_dir, fname))
                # Attempt to open the image using PIL:
                try:
                    img = Image.open(os.path.join(dir_name, fname))
                    # img = Image.open(os.path.join(dir_name, fname)).convert('RGB')
                    openable_images.append(os.path.join(dir_name, fname))
                    num_openable_files += 1
                    if os.path.getsize(os.path.join(dir_name, fname)) == 0:
                        print('\t\tWARNING: Image \'%s\' is of size 0 bytes.' % fname)
                except Exception as err:
                    print('\t\tERROR: Failed to open image \'%s\'. Proceeding without this image.' % fname)
                    unopenable_images.append(os.path.join(dir_name, fname))
                    if failed_img_dir is not None:
                        # Copy image to failed_image_dir:
                        shutil.copy(os.path.join(dir_name, fname), os.path.join(failed_img_dir, fname))
                    continue
                # The image has been opened successfully, now try running OCR on the barcode:
                decoded_img = pyzbar.decode(img)
                if decoded_img:
                    # OCR worked
                    ocr_success_images.append(os.path.join(dir_name, fname))
                    num_ocr_successes_in_dir += 1
                    print('\t\t%s' % decoded_img)
                    # Get the new image name from the barcode:
                    new_img_name = decoded_img[0][0].decode()
                    # Get the old image extension:
                    source_img_ext = os.path.splitext(img.filename)[1]
                    # Copy and rename the image:
                    shutil.copy(
                        src=os.path.join(dir_name, fname),
                        dst=os.path.join(renamed_img_dir, new_img_name + source_img_ext)
                    )
                else:
                    # OCR failed
                    print('\t\tFailed to OCR and decode barcode.')
                    num_ocr_failures_in_dir += 1
                    ocr_failure_images.append(os.path.join(dir_name, fname))
        ocr_success_rate_in_dir = ((num_ocr_successes_in_dir * 100)/num_files_in_dir)
        print('INFO: Directory OCR Stats: \n\tOCR Success Rate: %.2f%%\n\tNumber of renamed images: %d\n\tNumber of '
              'remaining mislabeled images: %d'
              % (ocr_success_rate_in_dir, num_ocr_successes_in_dir, num_ocr_failures_in_dir))
    print('INFO: No more sub-directories identified. Global OCR and renaming finished. Dumping list of failed OCR '
          'images to: \'%s\'' % '/BarcodeReader/failed_images.txt')
    with open('failed_images.txt', 'w') as fp:
        for image_name in ocr_failure_images:
            fp.write(os.path.basename(image_name) + '\n')
    print('INFO: Script finished. Failed to OCR the images listed in the \'failed_images.txt\' file. Exiting...')
    exit(0)


def main():
    mislabeled_img_dir = _get_mislabeled_image_dir_from_user()
    renamed_img_dir = _get_renamed_image_dir_from_user()
    user_wants_failed_images_copied = _get_wants_failed_images_copied_from_user()
    if user_wants_failed_images_copied:
        failed_img_dir = _get_failed_image_dir_from_user()
    else:
        failed_img_dir = None
    _ocr_and_rename_all_images_in_dir(
        mislabeled_img_dir=mislabeled_img_dir,
        renamed_img_dir=renamed_img_dir,
        failed_img_dir=failed_img_dir
    )


if __name__ == '__main__':
    main()
