# Finding Buddy

## Overview
**Finding Buddy** is an innovative assistive device designed to aid visually impaired (VI) individuals in locating specific objects within their environment. By leveraging advanced technologies such as VOSK-API for speech recognition and YOLOv8 for object detection, Finding Buddy offers a user-friendly solution that enhances the independence and quality of life for VI users. This repository contains the implementation and supporting files for the Finding Buddy system.

## Abstract
Visual impairment affects millions worldwide, making daily activities like object localization challenging, especially for the 253 million visually impaired individuals globally. This project proposes a novel solution, the Finding Buddy, which integrates advanced technologies like VOSK-API for speech recognition and YOLOv8 for object detection into a user-friendly device. Our experiments demonstrate the system's effectiveness and efficiency, addressing a critical gap in assistive technology for the visually impaired. The Finding Buddy aims to improve the independence and quality of life for VI individuals, providing an essential tool for daily object localization.

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
{
    "camera_source": "http://<IP_ADDRESS>:<PORT>/video"
}
    5. Test the connection: Ensure that your computer and smartphone are connected to the same Wi-Fi network. Open a web browser on your computer and navigate to the URL specified in the configuration file to verify the camera stream.

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

## Testing and Validation
The device was tested with four sighted participants blindfolded to simulate the VI user experience. The assessment metrics included searching accuracy and searching speed, with participants performing searches using both the grab method and land method. The results demonstrated high accuracy and user satisfaction, confirming the system's effectiveness.

## Conclusion
The Finding Buddy device represents a significant advancement in assistive technology for the visually impaired. By addressing the specific challenge of locating household items, it fills a critical gap and has the potential to greatly enhance the independence and quality of life for VI individuals.

## References
For a detailed list of references, please refer to the `References` section in the documentation.

## Contact
For questions or support, please contact [Your Name] at [Your Email].

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**Video Demonstration**: [YouTube Video Link]

**GitHub Repository**: [GitHub Repository Link]





To use your smartphone's camera as the input for the Finding Buddy device, follow these steps:

Install a streaming app on your smartphone: Download and install a camera streaming app such as "IP Webcam" for Android or "EpocCam" for iOS.
Configure the app: Open the app and configure it to stream video over your local Wi-Fi network. Make a note of the IP address and port number provided by the app.
Update the configuration file: Edit the configuration file (config/camera_config.json) in the repository to include the IP address and port number of your smartphone's camera stream. The configuration file should look something like this:
json
Copy code
{
    "camera_source": "http://<IP_ADDRESS>:<PORT>/video"
}
Test the connection: Ensure that your computer and smartphone are connected to the same Wi-Fi network. Open a web browser on your computer and navigate to the URL specified in the configuration file to verify the camera stream.
