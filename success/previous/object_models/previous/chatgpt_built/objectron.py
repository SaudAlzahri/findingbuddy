
# 3D WORKS on 
    # bikes
    # books
    # cameras 
    # cereal boxes
    # chairs
    # cups
    # laptops
    # shoes


#       for more classes, Ask chatgpt to program onepose, trainable version of objectro
import cv2
import mediapipe as mp

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_objectron = mp.solutions.objectron

    # Initialize object detection
    objectron = mp_objectron.Objectron(static_image_mode=False)

    # Open video capture
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to read frame")
            break

        # Convert image to RGB for processing with MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with object detection
        results = objectron.process(image)

        if results.detected_objects:
            for detected_object in results.detected_objects:
                mp_drawing.draw_landmarks(
                    frame, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)

        # Display the resulting frame
        cv2.imshow('Object Recognition Livestream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
