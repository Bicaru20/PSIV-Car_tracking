# Car Tracking with YOLO v8 and Background Subtraction

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This repository contains the code and resources for a car tracking system that combines YOLO v8 (You Only Look Once version 8) for object detection and background subtraction for more robust tracking. The project is aimed at tracking cars in various scenarios, such as surveillance, traffic management, or autonomous vehicle navigation.

## Features

- Object detection using YOLO v8 for identifying and tracking cars.
- Background subtraction to enhance the accuracy of car tracking.
- Example datasets and pre-trained YOLO weights for quick setup.
- Easy-to-use Python scripts for tracking and visualization.
- Detailed documentation and usage instructions.

## Dataset
- Recorded videos from UAB parking lot

## Step 1: Detecting Cars
In the first step of the project, we implement two distinct approaches to detect and identify cars within video streams or images. These approaches are designed to capture the presence and locations of cars using different methods.

1. YOLO v8 Object Detection:

We leverage YOLO v8 (You Only Look Once) for robust and real-time object detection. YOLO v8 is a state-of-the-art deep learning algorithm that excels at detecting and classifying objects within images or video frames. In this approach, we focus on detecting cars with high confidence scores, which indicates a high likelihood that the identified object is indeed a car. The YOLO model is trained on a wide range of object classes, making it capable of recognizing various types of vehicles, including cars. We filter the detections to retain those that are highly likely to be cars and proceed with their tracking.

2. Background Subtraction and Area Filtering:

In parallel to the YOLO-based approach, we employ background subtraction to identify moving objects in the scene. This method involves comparing each video frame to a reference background frame to isolate foreground objects. Once we have the foreground objects, we apply area filtering to retain only objects that meet specific size criteria typically indicative of a car. This approach is particularly useful when dealing with scenarios where YOLO may not perform optimally, such as crowded or challenging environments.

By combining these two approaches, we enhance the accuracy and robustness of our car tracking system, ensuring that we can effectively detect and track cars in various real-world scenarios. The subsequent steps of the project will detail how to set up and use these approaches for car tracking.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Example Datasets](#example-datasets)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.7 or higher
- OpenCV
- YOLO v8


## Setup

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/your-username/car-tracking-yolo-background.git
