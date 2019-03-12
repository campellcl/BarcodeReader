# BarcodeReader
A Python implementation of ZBar (utilizing *pyzbar*) for use in renaming
herbarium specimen images with barcode content. This software is designed
to rectify incorrectly named herbarium specimen images. The software
searches through the specified folder and copies and renames images using
the barcode values in the images themselves.

## Installation Guide:
1. Clone or download this repository using either:
    1. [This very same GitHub webpage](https://github.com/ccampell/BarcodeReader)
    2. A command line interface such as [git](https://git-scm.com/),
    in which case the following command should be run:
        ```
        git clone https://github.com/ccampell/BarcodeReader.git
        ```
2. It is recommended that you create a new virtual environment before
proceeding with the installation (this is akin to doing a clean install,
 without all the hastle):
    1. For users using the Python package manager
    [PIP](https://github.com/pypa/pip), refer to the
    [PyPA documentation](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#creating-a-virtualenv).
        * On a Windows machine (with pip installed):
            ```
            py -m virtualenv env
            ```
    2. For users using the Python package manager
    [conda](https://docs.conda.io/projects/conda/en/latest/index.html)
    (bundled with the popular [Anaconda distribution](https://www.anaconda.com/distribution/)),
     refer to the [conda documentation on managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
        * On a Windows machine (with conda installed):
            ```
            conda create --name env
            ```
3. Activate your newly created virtual environment:
    1.  For users using the Python package manager [PIP](https://github.com/pypa/pip), refer to the [PyPA documentation on activating virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#activating-a-virtualenv)
        * On a Windows machine (with pip installed):
            ```
            .\env\Scripts\activate
            ```
    2. For users using the Python package manager [conda](https://docs.conda.io/projects/conda/en/latest/index.html) (bundled with the popular [Anaconda distribution](https://www.anaconda.com/distribution/)), refer to the [conda documentation on activating environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment).
        * On a Windows machine (with conda installed):
            ```
            conda activate env
            ```
4. Install Python in your new virtual environment:
    1. For users using the Python package manager [PIP](https://pypi.org/project/pip/), this is as simple as running the following command:
        * On a Windows machine (with pip installed):
            ```
            pip install python==3.6
            ```
    2. For users using the Python package manager [conda](https://docs.conda.io/projects/conda/en/latest/index.html) (bundled with the popular [Anaconda distribution](https://www.anaconda.com/distribution/)), run the following command:
        * On a Windows machine (with conda installed):
            ```
            conda install python==3.6
            ```
5. Install [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) following the [installation instructions available here](https://github.com/NaturalHistoryMuseum/pyzbar#installation) at the source repository.
    1. For users using the Python package manager [PIP](https://github.com/pypa/pip), this is as simple
    as running the following command:
        * On a Windows machine (with pip installed):
            ```
            pip install pyzbar
            ```
    2. For users using the Python package manager [conda](https://docs.conda.io/projects/conda/en/latest/index.html) (bundled with the popular [Anaconda distribution](https://www.anaconda.com/distribution/)), run the following command:
        * On a Windows machine (with conda installed):
            ```
            pip install pyzbar
            ```
        * In this case we must use *pip* inside *conda* because *pyzbar* is not available on [Anaconda Cloud](https://anaconda.org/) or [conda-forge](https://anaconda.org/conda-forge).
6. Install the
[Python Image Library (Pillow)](https://github.com/python-pillow/Pillow)
using the following
[installation guide](https://pillow.readthedocs.io/en/latest/installation.html):
    1. For users using the Python package manager
    [PIP](https://github.com/pypa/pip), this is as simple as running
    the following command:
        * On a Windows machine (with pip installed):
            ```
            pip install Pillow
            ```
    2. For users using the Python package manager [conda](https://docs.conda.io/projects/conda/en/latest/index.html) (bundled with the popular [Anaconda distribution](https://www.anaconda.com/distribution/)), run the following command:
        * On a Windows machine (with conda installed):
            ```
            pip install Pillow
            ```
            * It is recommended that pip is used within the conda virtual environment to install Pillow.

7. Run the program located at ```BarcodeReader/BarcodeReader/ImageNameFixer.py``` by navigating to the script's location and executing:
    ```
    python ImageNameFixer.py
    ```
8. You will be prompted (with the following text) to provide a path to the folder with mislabeled specimen images. Do so, then press the enter key. For example:
    ```
    Enter the file path to the folder containing mislabeled images here (you can always copy and paste it): C:\Users\chris\mislabeled_images
    ```
9. You will be prompted (with the following text) to provide a path to the folder where the automatically renamed images should be copied over to. Do so, then press the enter key. For example:
    ```
    Enter the file path to the folder where you wish automatically renamed images to be copied to: C:\Users\chris\renamed_images
    ```
    * If the folder you provide does not exist on your machine, you will be prompted to try again. If this occurs:
        1. Specify a folder that actually exists on the machine
        2. Create the folder manually (in Windows Explorer or Finder) and then try the same path again
10. For your convience the program will offer to make copies of images
that could not be automatically renamed via OCR of the specimen barcodes.
This can be useful for some workflows (for instance the folder can then
be handed to a volunteer for manual re-labeling).
If you wish for relabeled images to be copied over, enter 'y' or 'yes' and press the enter key; otherwise press 'n' or 'no' and the enter key.

11. The script will now crawl the directory you originally provided and
run OCR on all the images. If the barcode is able to be read by the OCR
software, your orginal image will be copied over and renamed to the
text encoded in the specimen image barcode. If the barcode is not able
to be read by the OCR software, the script will keep track of this. The
original file names of images which were not able to be automatically
renamed will be exported after the script finishes executing to a 'failed_images.txt' file.

## FAQ
1. This software isn't very accurate, what gives? I thought you had experience in the field of computer vision!
    1. This software was developed for an employer who (in this particular instance) was not concerned with the accuracy of the software.
    2. I have not touched the source *pyzbar* OCR code, although there are a multitude of improvements I would love to implement should my employer so desire.
    3. I hope that the *pyzbar* OCR software is good enough for your images.
    If this software is not accurate enough for your institution, feel free to experiment with the source code (within the purview of the included LICENSE.md). I will gladly accept pull requests.
2. Will this program alter my images in any way?
    1. No, your original images will be left unmodified in the source
    directory. There is no risk of corrupting your images.
3. What happens if I must terminate the program before it finishes?
    1. Simply re-run the program. Your images will be re-OCR'd.
    I have not been authorized enough time to spend on this implementation
    to include features allowing for the program to resume where it left off at
    (if previously interrupted).
4. Do you accept pull requests?
    1. Of course. I foster and encourage collaboration and open source development.
5. It's not working!
    1. That's not a question! But feel free to contact me (the maintainer of this software) at [campellcl@gmail.com](mailto:campellcl@gmail.com).


## Sources:
* This script was written by Christopher Campell, an M.S. Computer
Science student at Appalachian State University.
    * Inquries involving this software can be directed to
    [campellcl@gmail.com](mailto:campellcl@gmail.com)
* This script makes heavy use of of the Python ported version of the
 open source [Zbar software](http://zbar.sourceforge.net/) (pyzbar)
 which is available on GitHub
 [here](https://github.com/NaturalHistoryMuseum/pyzbar).

## Licensing Information:

* The Zbar software is licensed under the
[GNU LGPL 2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
for use in both commercial and open source projects.
* The Python port of this software: *pyzbar* is distributed under the
[MIT License](https://choosealicense.com/licenses/mit/).
* This repository (as a derivative work) is herebye also licensed via
the [MIT License](https://choosealicense.com/licenses/mit/)
(see the LICENSE.md file for the posted license).

