# Finding Buddy

## Overview
**Finding Buddy** is an innovative assistive device designed to aid visually impaired (VI) individuals in locating specific objects within their environment. Finding Buddy is leveraging advanced technologies such as VOSK-API for speech recognition and YOLOv8 for object detection, as well as novel methods such as the Hand Relative Directioning System and the Rotated Military Clock Directioning System. Finding Buddy offers a user-friendly solution that enhances the independence and quality of life for VI users. This repository contains the implementation and supporting files for the Finding Buddy system.

## Hand Relative Directioning System
    A novel feature was developed where the program can provide directioning relative to the hand, which is especially useful for smaller objects. The VI user may want to grab a fork, bottle, or toothbrush with their hand, while larger objects do not need hand relative directioning, e.g. bench, bus, or car. This is the first instance of hand relative directioning in VI assistive technology (see Figure 1).
    
![Figure 1](Images/Figure 1?raw=true "Figure 1")


## Installation
To set up Finding Buddy, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/FindingBuddy.git
    cd FindingBuddy
    cd success
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Pre-trained Models**:
    Download the required pre-trained models for VOSK-API and YOLOv8 and place them in the appropriate directories.

   Connect your smartphone's camera as input:
   To use your smartphone's camera as the input for the Finding Buddy device, follow these steps:

    1. Install a streaming app on your smartphone: Download and install a camera streaming app such as "IP Webcam" for Android or "EpocCam" for iOS.
    2. Configure the app: Open the app and configure it to stream video over your local Wi-Fi network. Make a note of the IP address and port number provided by the app.
    3. Update the configuration file: Edit the configuration file (config/camera_config.json) in the repository to include the IP address and port number of your smartphone's camera stream. The configuration file should look something like this:
json
    4. Copy code
   
        ```bash
        http://<IP_ADDRESS>:<PORT>/video
        ```

    6. Test the connection: Ensure that your computer and smartphone are connected to the same Wi-Fi network. Open a web browser on your computer and navigate to the URL specified in the configuration file to verify the camera stream.

6. **Run the Application**:
    ```bash
    python main.py
    ```

## Files
- `main.py`: Main script to run the Finding Buddy application.
- `requirements.txt`: List of required Python packages.
- `vosk_api.py`: Script for speech recognition using VOSK-API.
- `yolo_detection.py`: Script for object detection using YOLOv8.
- `utils.py`: Utility functions for processing and calculations.
- `config/`: Directory containing configuration files.
- `models/`: Directory for storing pre-trained models.

## Usage
1. **Start the Device**:
    Connect the headpiece (bone conduction headset, camera, and microphone) to the Raspberry Pi.
2. **Voice Command**:
    Use voice commands to interact with the device. For example, say "find my keys" to initiate a search for keys.
3. **Audio Guidance**:
    The device will provide audio instructions using the novel rotated military clock directioning system and hand-relative directioning system to guide you to the object.

## Documentation
HERE IS THE DRIVE LINK TO THE PAPER

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**Video Demonstration**: [YouTube Video Link]

{
    "camera_source": "http://<IP_ADDRESS>:<PORT>/video"
}
Test the connection: Ensure that your computer and smartphone are connected to the same Wi-Fi network. Open a web browser on your computer and navigate to the URL specified in the configuration file to verify the camera stream.
