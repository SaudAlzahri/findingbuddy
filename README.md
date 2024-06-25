# Finding Buddy

## Overview
**Finding Buddy** is an innovative assistive device designed to aid visually impaired (VI) individuals in locating specific objects within their environment. Finding Buddy is leveraging advanced technologies such as VOSK-API for speech recognition and YOLOv8 for object detection, as well as novel methods such as the Hand Relative Directioning System and the Rotated Military Clock Directioning System. Finding Buddy offers a user-friendly solution that enhances the independence and quality of life for VI users. This repository contains the implementation and supporting files for the Finding Buddy system.

[**Video Demonstration**](https://www.youtube.com/watch?v=zEVl4kBO3d4)            [**Research Paper**](download link for research paper)

## Rotated Military Clock Directioning System
The format of the audio given directions is perhaps the most vital element of the user experience, because it is the deciding factor for product usability and user receptiveness/precision. However, we are not providing directioning on a 2D plane like most assistive devices currently in the market (e.g. navigation) but rather on a 3D space, because objects may be up and down in addition to forward, back, left and right. For this purpose we had to developed a completely new format for the directioning system, the rotated military clock directioning system, where degrees are given (see Figure 1).

## Hand Relative Directioning System
A novel feature was developed where the program can provide directioning relative to the hand, which is especially useful for smaller objects. The VI user may want to grab a fork, bottle, or toothbrush with their hand, while larger objects do not need hand relative directioning, e.g. bench, bus, or car. This is the first instance of hand relative directioning in VI assistive technology. <img src="images/figure1.png" alt="Figure 1" width="600"/>

<sup>Figure 1: Diagram of the novel directioning system. Shown bigger on the left is the grab mode, and smaller on top right is the land mode. Audio given results are the clock degrees in addition to the forward distance in meters.</sup>



## Installation
To set up Finding Buddy, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/FindingBuddy.git
    cd FindingBuddy
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
- `main.py`: Main script to run the Finding Buddy application, beginning with audio input.
- `object.py`: Function handling visual input and post visual input algorithms.
- `requirements.txt`: List of required Python packages.
- `texttovoice.py`: Script containing gTTS's HTML text to voice function.
- `clock.py`: Algorithm achieving the rotated military clock directioning system.
- `vosk-model-small-en-us-0.15/`: Directory containing VOSK-API's language model.
- `images/`: Directory for storing images used in the READ ME.

## Usage
1. **Run the Application**:
    Run the main file. Wait until initiation is completed in terminal.
    ```bash
    python main.py
    ```
3. **Voice Command**:
    Use voice commands to interact with the system, with all command following the initiation phrase "Finding Buddy." For example, say "Finding Buddy, find my bottle" to begin a search for your water bottle.
5. **Audio Guidance**:
    The device will provide audio instructions using the novel rotated military clock directioning system and forward distance in meters to guide you to the object: "9 o'clock, 2 meters." Were the object to be small (bottle) the novel hand-relative directioning system would provide directioning to move your hand, however were it to be large (couch) it would provide directioning to move your body.

## Documentation
HERE IS THE DRIVE LINK TO THE PAPER

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

