import cv2

def main():
    # Loop through webcam indices to find the available ones
    for i in range(11):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Webcam index {i} is available.")
            cap.release()
        else:
            print(f"Webcam index {i} is not available.")

    # Choose an available webcam index to open
    chosen_index = int(input("Enter the index of the webcam you want to use: "))

    # Open the chosen webcam
    cap = cv2.VideoCapture(chosen_index)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()