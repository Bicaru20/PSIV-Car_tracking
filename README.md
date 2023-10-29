
# Car Tracking with YOLO v8 and Background Subtraction

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This repository contains the code and resources for a car tracking system that combines YOLO v8 (You Only Look Once version 8) for object detection and background subtraction for more robust tracking. The project is aimed at tracking cars in various scenarios, such as surveillance, traffic management, or autonomous vehicle navigation.

## Table of Contents

- [Features](#features)
- [Step 1: Detecting Cars](#step-1-detecting-cars)
- [Step 2: Tracking Cars](#step-2-tracking-cars)
- [Step 3: Visualizing Car Tracking](#step-3-visualizing-car-tracking)
- [Requirements](#requirements)
- [Setup](#setup)
- [Dataset](#dataset)
- [Contributing](#contributing)


## Features

- Object detection using YOLO v8 for identifying and tracking cars.
- Background subtraction to enhance the accuracy of car tracking.
- Example datasets and pre-trained YOLO weights for quick setup.
- Easy-to-use Python scripts for tracking and visualization.
- Detailed documentation and usage instructions.


## Step 1: Detecting Cars

In the first step of the project, we implement two distinct approaches to detect and identify cars within video streams or images. These approaches are designed to capture the presence and locations of cars using different methods.

1. YOLO v8 Object Detection:

We leverage YOLO v8 (You Only Look Once) for robust and real-time object detection. YOLO v8 is a state-of-the-art deep learning algorithm that excels at detecting and classifying objects within images or video frames. In this approach, we focus on detecting cars with high confidence scores, which indicates a high likelihood that the identified object is indeed a car. The YOLO model is trained on a wide range of object classes, making it capable of recognizing various types of vehicles, including cars. We filter the detections to retain those that are highly likely to be cars and proceed with their tracking.

2. Background Subtraction and Area Filtering:

In parallel to the YOLO-based approach, we employ background subtraction to identify moving objects in the scene. This method involves comparing each video frame to a reference background frame to isolate foreground objects. Once we have the foreground objects, we apply area filtering to retain only objects that meet specific size criteria typically indicative of a car. This approach is particularly useful when dealing with scenarios where YOLO may not perform optimally, such as crowded or challenging environments.

By combining these two approaches, we enhance the accuracy and robustness of our car tracking system, ensuring that we can effectively detect and track cars in various real-world scenarios. The subsequent steps of the project will detail how to set up and use these approaches for car tracking.

## Step 2: Tracking Cars

In the second step of the project, we implement a car tracking system that combines the two approaches from the previous step. The system is designed to leverage the strengths of each approach to achieve robust, accurate, and efficient car tracking in various scenarios.

Approach 1: YOLO v8 Object Detection (Every 5 Frames)
In the first tracking approach, we use YOLO v8 for car detection every 5 frames. This approach provides speed and efficiency as YOLO can process frames quickly. However, it comes at the cost of temporarily losing tracking information between the frames. During the non-detection frames, the tracking system maintains the last known state of each car.

Approach 2: YOLO v8 with Background Subtraction (Every 5 Frames)
To address the issue of information loss between YOLO detections, we combine YOLO with background subtraction during the 5 frames intervals when YOLO detection is not performed. This hybrid approach aims to reduce the information loss by using background subtraction to identify moving objects even when YOLO is not actively detecting cars. Any objects identified by background subtraction are associated with their corresponding cars from the previous YOLO detection frame.

### Object Tracking and Class ID

To maintain and track information about each car, we utilize an object tracking system. Each car is assigned a unique Class ID, and this ID is used to store information about the car's properties, such as its position, direction, and other relevant data. The Class ID helps in connecting the car's state across frames, even when there is a brief absence of YOLO detection.

This combined tracking approach ensures that we minimize information loss and provide a more complete and reliable tracking system. The Class ID facilitates the association of cars between different frames, enabling us to monitor their movements accurately.

As a result, our car tracking system is capable of not only detecting cars but also following their trajectories and collecting essential data about their behavior. It also allows us to count the number of cars that go in each direction.

## Step 3: Visualizing Car Tracking

In this step, we focus on visualizing the results of our car tracking system. The output of our system is saved in an output file, typically an output video. This video not only displays the tracked cars but also includes visual indicators for tracking direction and direction counting.

The output video is a visual representation of the car tracking process. It features the following elements:

Tracked Cars: Each car is outlined with a bounding box to visually indicate its position in the frame. The color of the bounding box often corresponds to the car's Class ID for easy reference.

Direction Counting Lines: In the video, lines are drawn across the road or relevant paths. These lines serve as reference points for tracking the direction of the cars. When a car crosses one of these lines, its direction is recorded and visualized.

Direction Indicators: For each tracked car, we provide direction indicators, such as "up," "down," "left," or "right." These indicators are displayed alongside the car's bounding box and are updated as the car changes direction.

By including these elements in the output video, we offer a comprehensive visualization of the car tracking data. This makes it easier to interpret the movement patterns of the tracked cars, such as understanding traffic flow, counting vehicles entering or exiting specific areas, or monitoring lane changes.

## Requirements

- Python 3.7 or higher
- OpenCV
- YOLO v8

## Setup

1. Clone the repository to your local machine:	`git clone https://github.com/Bicaru20/PSIV-Car_tracking`

## Dataset

The dataset used for training and testing consists of recorded videos from the UAB parking lot. These videos vary in size and complexity, providing a diverse set of scenarios for evaluating the car tracking system.

## Contributing

We welcome contributions to this project. If you find any issues, have suggestions for improvements, or would like to add new features, please feel free to open an issue or submit a pull request.