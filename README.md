[![facialRecognitionDetection2D Homepage](https://img.shields.io/badge/facialRecognitionDetection2D-develop-orange.svg)](https://github.com/davidvelascogarcia/facialRecognitionDetection2D/tree/develop/docs) [![Latest Release](https://img.shields.io/github/tag/davidvelascogarcia/facialRecognitionDetection2D.svg?label=Latest%20Release)](https://github.com/davidvelascogarcia/facialRecognitionDetection2D/tags) [![Build Status](https://travis-ci.org/davidvelascogarcia/facialRecognitionDetection2D.svg?branch=develop)](https://travis-ci.org/davidvelascogarcia/facialRecognitionDetection2D)

# Facial Recognition: Detector 2D (PYTHON API)

- [Introduction](#introduction)
- [Trained Models](#trained-models)
- [Requirements](#requirements)
- [Additional Info](#additional-info)
- [Related projects](#related-projects)


## Introduction

`facialRecognitionDetection2D` module use `dlib` PYTHON API. The module detects faces using pre-trained models and adds facial recognition doing a facial training with user images. Also use `YARP` to send video source pre and post-procesed. Also admits `YARP` source video like input. Some [scripts](./scripts) added to create automated files of user data file images and user label name file. This module also publish detection results in `YARP` port.


## Trained Models

`facialRecognitionDetection2D` requires images of people to detect. Images should be located in [database](./database) dir. 
The process to create database files:

1. Execute [scripts/updatePeopleFiles.sh](./scripts), to create image index.
```bash
bash updatePeopleFiles.sh
```
2. Execute [script/updatePeopleData.py](./scripts), to create label index.
```python
python updatePeopleData.py
```
3. Execute [programs/facialRecognitionDetection2D.py](./programs), to start de program.
```python
python facialRecognitionDetection2D.py
```
4. Connect video source to `facialRecognitionDetection2D`.
```bash
yarp connect /videoSource /facialRecognitionDetection2D/img:i
```

NOTE:

Video results are published on `/facialRecognitionDetection2D/img:o`
Data results are published on `/facialRecognitionDetection2D/data:o`

## Requirements

`facialRecognitionDetection2D` requires:

* [Install OpenCV 3.0.0+](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-opencv.md)
* [Install YARP 2.3.XX+](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-yarp.md)
* [Install pip](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-pip.md)
* Install face_recognition:
```bash
pip2 install face_recognition
```

Tested on: `ubuntu 14.04`, `ubuntu 16.04`, `ubuntu 18.04` and `lubuntu 18.04`.


## Status

[![Build Status](https://travis-ci.org/davidvelascogarcia/facialRecognitionDetection2D.svg?branch=develop)](https://travis-ci.org/davidvelascogarcia/facialRecognitionDetection2D)

[![Issues](https://img.shields.io/github/issues/davidvelascogarcia/facialRecognitionDetection2D.svg?label=Issues)](https://github.com/davidvelascogarcia/facialRecognitionDetection2D/issues)

## Related projects

* [ageitgey: face_recognition project](https://github.com/ageitgey/face_recognition)[
* [davidvelascogarcia: Tensorflow: Detector 2D (C++ API)](https://github.com/davidvelascogarcia/tensorflowDetection2D)
