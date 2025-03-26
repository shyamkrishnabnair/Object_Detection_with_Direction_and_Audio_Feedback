import cv2
import torch
import pyttsx3
import time
from collections import defaultdict

def get_direction(x, y, frame_width, frame_height):
    col = int(3 * x / frame_width)
    row = int(3 * y / frame_height)
    
    directions = [
        ['top-left', 'top-center', 'top-right'],
        ['middle-left', 'center', 'middle-right'],
        ['bottom-left', 'bottom-center', 'bottom-right']
    ]
    
    return directions[row][col]

def run_object_detection():
    # Initialize YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.conf = 0.50  # Set confidence threshold to 0.5

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize variables
    detected_labels = defaultdict(list)
    last_speech_time = 0
    speech_interval = 5  # Minimum time between speech outputs in seconds
    persistent_object_interval = 3  # Interval to check for persistent objects

    # Dictionary to store objects and their first detection time
    object_detection_times = {}

    # Function to write output to file
    def write_to_file(detected_labels):
        with open('detected_objects.txt', 'w') as f:
            for label, detections in detected_labels.items():
                f.write(f"{label}:\n")
                for timestamp, direction in detections:
                    f.write(f"  {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))} - {direction}\n")
                f.write("\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection
        results = model(frame)

        # Get the detected labels with timestamps and directions
        current_time = time.time()
        current_labels = []
        for *xyxy, conf, cls in results.xyxy[0]:
            label = results.names[int(cls)]
            x_center = (xyxy[0] + xyxy[2]) / 2
            y_center = (xyxy[1] + xyxy[3]) / 2
            direction = get_direction(x_center, y_center, frame_width, frame_height)
            current_labels.append((label, current_time, direction))

        # Update the detected_labels dictionary with new detections
        for label, timestamp, direction in current_labels:
            detected_labels[label].append((timestamp, direction))

        # Draw bounding boxes and labels
        for *xyxy, conf, cls in results.xyxy[0]:
            label = f'{results.names[int(cls)]} {conf:.2f}'
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
            cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the frame
        cv2.imshow('Object Detection', frame)

        # Convert new labels to speech
        new_labels = [f"{label} in the {direction}" for label, _, direction in current_labels if len(detected_labels[label]) == 1]
        if new_labels and (current_time - last_speech_time) >= speech_interval:
            speech_text = ", ".join(new_labels)
            timestamp_str = time.strftime('%H:%M:%S', time.localtime(current_time))
            engine.say(f"Detected: {speech_text}")
            engine.runAndWait()
            last_speech_time = current_time

        # Check for persistent objects
        persistent_objects = []
        for label, detection_time in list(object_detection_times.items()):
            if label not in [l for l, _, _ in current_labels]:
                # Object is no longer in frame
                del object_detection_times[label]
            elif current_time - detection_time >= persistent_object_interval:
                direction = next(direction for l, _, direction in current_labels if l == label)
                persistent_objects.append(f"{label} in the {direction}")
                # Reset the detection time for this object
                object_detection_times[label] = current_time

        # Add new objects to the detection times dictionary
        for label, _, _ in current_labels:
            if label not in object_detection_times:
                object_detection_times[label] = current_time

        # Provide audio feedback for persistent objects
        if persistent_objects and (current_time - last_speech_time) >= speech_interval:
            speech_text = ", ".join(persistent_objects)
            timestamp_str = time.strftime('%H:%M:%S', time.localtime(current_time))
            engine.say(f"Still detecting: {speech_text}")
            engine.runAndWait()
            last_speech_time = current_time

        # Write current detections to file
        write_to_file(detected_labels)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    # Final list of all detected objects with timestamps and directions
    print("All detected objects:")
    for label, detections in detected_labels.items():
        print(f"2{label}:")
        for timestamp, direction in detections:
            print(f"  {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))} - {direction}")

if __name__ == "__main__":
    run_object_detection()

