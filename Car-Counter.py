import random
from ultralytics import YOLO
import cv2
import cvzone
from tracker import *

# Initialize the webcam (commented out)
# cap = cv2.VideoCapture(0)
# cap.set(3,1280) # Set the width
# cap.set(4,720) # Set the height

# Initialize video capture from a file
cap = cv2.VideoCapture("Images_Videos/vehicles.mp4")

# Load the YOLO model with specific weights
model = YOLO("yolov8n.pt")

# List of class names that the YOLO model can detect
classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush"
]

# Load the mask image for the region of interest
mask = cv2.imread("Images_Videos/mask.png")

# Load the graphics image to overlay on the video frame
imgGraphics = cv2.imread("Images_Videos/carGraphics.png", cv2.IMREAD_UNCHANGED)

# Initialize the tracker for object tracking
tracker = EuclideanDistTracker()

# Define the limits for counting objects crossing a line
limits = [20, 275, 230, 275]

# List to keep track of total counted objects
totalCount = []
colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(10)]
while True:
    # Read a frame from the video
    flag, frame = cap.read()

    # Apply the mask to the frame to focus on the region of interest
    frameRegion = cv2.bitwise_and(frame, mask)

    # Draw a rectangle for displaying the count on the frame
    cv2.rectangle(frame, (0, 0), (180, 50), (255, 255, 255), cv2.FILLED)

    # Overlay the graphics image on the frame
    frame = cvzone.overlayPNG(frame, imgGraphics, (0, 10))

    # Use the YOLO model to detect objects in the region of interest
    results = model(frameRegion, stream=True)

    # Draw a line on the frame for counting objects
    cv2.line(frame, (limits[0], limits[1]), (limits[2], limits[3]), (15, 60, 255), 5)

    # Process each detection result
    for r in results:
        # List to store detections
        detections = []
        obj = r.boxes

        # Extract class, confidence, and bounding box information for each detected object
        for cls, conf, bbox in zip(obj.cls, obj.conf, obj.xywh):
            x, y, w, h = bbox
            x, y, w, h, cls = int(x), int(y), int(w), int(h), int(cls)

            # Round confidence and get the class name
            conf = math.ceil((conf * 100)) / 100
            currentClass = classNames[cls]

            # Draw bounding boxes for specific classes with confidence greater than 0.3
            if currentClass == "car" or currentClass == "truck" or currentClass == "bus" and conf > 0.3:
                detections.append([x, y, w, h])

        # Perform object tracking
        boxes_ids = tracker.update(detections)

        # Annotate the frame with tracking IDs
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            x1, y1 = int(x - w / 2), int(y - h / 2)

            frame = tracker.opacityRectangle(frame, bbox=(x, y, w, h), color=colors[id % len(colors)])
            cvzone.putTextRect(frame, f"{id}", (x, y), scale=1, thickness=2, offset=1)

            # Check if the object crosses the defined line and update the count
            if limits[0] < x < limits[2] and limits[3] - 10 < y < limits[3] + 5:
                if totalCount.count(id) == 0:
                    totalCount.append(id)

    # Display the total count on the frame
    cv2.putText(frame, str(len(totalCount)), (105, 38), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # Show the frame in a window
    cv2.imshow("Image", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(9) == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
