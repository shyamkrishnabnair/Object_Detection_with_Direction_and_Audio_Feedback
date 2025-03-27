# Object Detection with Audio Feedback

## Overview
This project is an object detection system with audio feedback. It uses a YOLOv5 model to detect objects in real-time via a webcam, providing spoken alerts about detected objects and their positions. The system also includes a simple GUI for ease of use.

## Features
- **Real-time Object Detection:** Uses YOLOv5 to detect objects in a webcam feed.
- **Audio Feedback:** Converts detected object information into speech using `pyttsx3`.
- **GUI Interface:** Built with Tkinter for easy interaction.
- **Text Output:** Saves detected objects with timestamps and directions in a `detected_objects.txt` file.
- **Persistent Object Tracking:** Alerts users about objects that remain in the frame for a prolonged period.

## Installation
### Prerequisites
Ensure you have Python installed (preferably 3.8+). Then install the required dependencies:
```sh
pip install torch torchvision torchaudio
pip install opencv-python
pip install pyttsx3
pip install pillow
```

## Usage
### Running the Object Detection System
1. Run the GUI interface:
   ```sh
   python gui_interface.py
   ```
2. Click the `Detect` button to start object detection.
3. Detected objects will be displayed on the video feed, announced via speech, and logged in `detected_objects.txt`.
4. Click `Quit` to close the application.

Alternatively, you can run object detection without the GUI:
```sh
python object_detection_audio.py
```
Press `q` to exit the detection window.

## File Structure
- `gui_interface.py` - The graphical interface for the object detection system.
- `object_detection_audio.py` - Core script for object detection and audio feedback.
- `detected_objects.txt` - Stores detected objects along with their timestamps and locations.
- `bg.jpg` - Background image for the GUI (replace with your own if needed).

## Customization
- Modify the confidence threshold in `object_detection_audio.py`:
  ```python
  model.conf = 0.50  # Adjust threshold as needed
  ```
- Change speech output frequency:
  ```python
  speech_interval = 5  # Seconds between speech alerts
  ```

## Future Enhancements
- Add support for additional languages in audio feedback.
- Implement object tracking across frames for more precise updates.
- Enhance the GUI with more interactive features.

## License
This project is licensed under the MIT License.

