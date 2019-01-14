# BarcodeReader
A Python implementation of ZBar (utilizing *pyzbar*) for use in renaming
herbarium specimen images with barcode content. This software is designed
to rectify incorrectly named herbarium specimen images. The software
searches through the specified folder and copies and renames images using
the barcode values in the images themselves.

## Installation Guide:
1. Clone or download this repository using the GitHub webpage or
command line interface.
2. Install pyzbar following the instructions available
[here](https://github.com/NaturalHistoryMuseum/pyzbar) at the source
repository.
    1. For users using the Python package manager [PIP](https://github.com/pypa/pip), this is as simple
    as running the following command:
    ```
    pip install pyzbar
    ```
    2. Other users should refer to the
    [pyzbar installation instructions](https://github.com/NaturalHistoryMuseum/pyzbar).
3. Install the
[Python Image Library (PIL)](https://github.com/python-pillow/Pillow)
using the following
[installation guide](https://pillow.readthedocs.io/en/latest/installation.html).
    1. For users using the Python package manager
    [PIP](https://github.com/pypa/pip), this is as simple as running
    the following command:
    ```
    pip install Pillow
    ```
4. Extract the downloaded zip file. You should see a folder labeled
`BarcodeReader` which contains:
    * A folder named `MislabeledImages`
    * The script: `ImageNameFixer.py`
5. Copy all mislabeled herbarium specimen images to the `BarcodeReader/MislabeledImages/` directory.
6. Run the script: `ImageNameFixer.py`. This can be done from the command line by invoking:
    ```
    python ImageNameFixer.py
    ```
7. Sit back and relax, the script will rename as many images as possible
using the contents of the images barcode. Your existing images **will not be
modified**, so there is no fear of data loss.
    * Images which were re-named successfully
will be copied to a newly created directory: `BarcodeReader/RenamedImages/`
    * Images which were unable to be automatically re-named will be copied to a newly
    created directory: `BarcodeReader/FailedImages/`
    * Your original images will be left un-modified in the
    `BarcodeReader/MislabeledImages/` directory.

<!-- ## Useage Guide: -->
<!-- 1. After downloading the repository -->
<!-- 1. Copy all mislabeled herbarium specimen images to -->


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

