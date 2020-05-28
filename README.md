# Yolo to Kitti Converter (YoloToKitti)

This repository holds the YoloToKitti. A simple code to convert Yolo detection files to Kitti files.
- Yolo format: (int_label, x_center, y_center, width, height) - float values relative to width and height of image, it can be equal from (0.0 to 1.0].
- Kitti format: (str_label, x1, y1, x2, y2) - "real" bounding box values.

# Contents
* [Usage Guide](#usage-guide)
  * [Prerequisites](#prerequisites)
  * [Code & Data Preparation](#code--data-preparation)
    * [Get the code](#get-the-code)
    * [Usage](#usage)
* [Other Info](#other-info)
  * [Contact](#contact)

----
# Usage Guide

## Prerequisites
[[back to top](#yolo-to-kitti-converter-yolotokitti)]

The main dependency to run the code is

- [OpenCV][opencv]

The codebase is written in Python 3.6. We recommend the [Anaconda][anaconda] Python distribution.

## Code & Data Preparation

### Get the code
[[back to top](#yolo-to-kitti-converter-yolotokitti)]

Use git to clone this repository
```
git clone --recursive https://github.com/carloscaetano/YoloToKitti
```

### Usage
[[back to top](#yolo-to-kitti-converter-yolotokitti)]

To convert the Yolo format detection files to Kitti format, run the YolloToKitti.py. It has two arguments:
- [--input, -i] Directory containing the Yolo detection files (.txt)
- [--output, -o] Directory to save the converted Kitti detection files (.txt)

#### Example
To convert the Yolo detection files, at the example directory ./yoloV4_detections/ and save the converted Kitti detection files to the folder ./files_converted, you can run
```
python YolloToKitti.py --input ./yoloV4_detections --output ./files_converted
```
or
```
python YolloToKitti.py -i ./yoloV4_detections -o ./files_converted
```

# Other Info
[[back to top](#yolo-to-kitti-converter-yolotokitti))]

## Contact
For any question, please contact
```
Carlos Caetano: carlos.caetano@dcc.ufmg.br
```

[opencv]:https://opencv.org/
[anaconda]:https://www.continuum.io/downloads