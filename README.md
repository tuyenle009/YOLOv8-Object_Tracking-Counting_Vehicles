# Yolo Vehicle Counter

## Overview
You Only Look Once (YOLO) is a CNN architecture for performing real-time object detection. The algorithm applies a single neural network to the full image, and then divides the image into regions and predicts bounding boxes and probabilities for each region. For more detailed working of YOLO algorithm, please refer to the [YOLO paper](https://pjreddie.com/media/files/papers/YOLOv3.pdf). 

This project aims to count every vehicle (motorcycle, bus, car, cycle, truck, train) detected in the input video using YOLOv8 object-detection algorithm.

## Working 
<p align="center">
![counting_vehicle (1)](https://github.com/tuyenle009/YOLOv8-Object_Tracking-Counting_Vehicles/assets/128459950/2342c55b-a222-4774-becf-179c858d3cd4)
</p>
As shown in the image above, when the vehicles in the frame are detected, they are counted. After getting detected once, the vehicles get tracked and do not get re-counted by the algorithm. 

You may also notice that the vehicles will initially be detected and the counter increments, but for a few frames, the vehicle is not detected, and then it gets detected again. As the vehicles are tracked, the vehicles are not re-counted if they are counted once. 


## Prerequisites

Python packages to be installed
Tested on Python 3.10
```
* Cvzone 1.5.6
* Ultralytics
* OpenCV (4.9.0.80)
* Numpy
```

## Implementation details

### Overview

This script performs object detection and tracking on a video feed using the YOLO (You Only Look Once) model and OpenCV. The goal is to detect specific objects (like cars, trucks, buses, and motorbikes), track them, and count how many times they cross a predefined line in the video.

### Step-by-Step Breakdown

1. **Importing Libraries**:
   - **ultralytics**: For the YOLO model.
   - **cv2**: For video capture, processing, and displaying frames.
   - **cvzone**: Simplifies certain OpenCV tasks.
   - **numpy**: For mathematical operations.

2. **Video Capture Setup**:
   - **Webcam**: Alternative option (commented out).
   - **Video File**: The script captures frames from a specified video file.

3. **Loading the YOLO Model**:
   - The YOLO model is loaded with specific pre-trained weights to detect objects in the video frames.

4. **Defining Class Names**:
   - A list of class names the YOLO model can detect is provided. This helps in identifying the type of object detected (e.g., car, truck, bus, etc.).

5. **Loading Mask and Graphics Images**:
   - **Mask Image**: Used to focus detection on a specific region of interest in the video frames.
   - **Graphics Image**: Overlaid on the video frames for visual enhancement.

6. **Initializing the Tracker**:
   - A tracker object is initialized to keep track of detected objects across frames using Euclidean distance.

7. **Defining Counting Limits**:
   - Coordinates of a line are defined. Objects crossing this line are counted.

8. **List to Keep Track of Counted Objects**:
   - A list is maintained to store IDs of objects that have been counted, preventing double counting.

9. **Processing Video Frames**:
   - The script reads frames from the video feed in a loop.
   - Each frame is processed to apply the mask, overlay graphics, and detect objects using the YOLO model.
   - Detected objects are filtered to focus on specific classes (car, truck, bus, motorbike) and a confidence threshold.
   - Bounding boxes are drawn around detected objects.
   - The tracker updates the positions of detected objects and assigns unique IDs.
   - The script checks if any tracked object crosses the predefined line. If an object crosses the line, it is counted.
   - The total count of objects is displayed on the frame.

10. **Displaying Results**:
    - The processed frame, with annotations and counts, is displayed in a window.
    - The loop continues until the video ends or the user presses the 'q' key to quit.

### Key Functionalities

- **YOLO Model**: Utilized for detecting objects in each frame.
- **Mask**: Focuses detection on a specific region of interest.
- **Overlay**: Adds graphical elements to the video frames for better visualization.
- **Tracker**: Tracks objects over multiple frames and assigns unique IDs.
- **Counting Mechanism**: Detects if an object crosses a predefined line and counts it.

