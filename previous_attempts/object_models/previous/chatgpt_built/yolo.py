
#
#
#   gives results as numbers, shaking...
#
#

import torch
import cv2

def main():
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5:v6.0', 'yolov5s', pretrained=True)

    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Set model to device
    model.to(device).eval()

    # Open the video stream (you can also use cv2.VideoCapture(0) for webcam)
    capture = cv2.VideoCapture(0)

    while True:
        # Read frame from video stream
        ret, frame = capture.read()

        # Inference
        results = model(frame)

        # Post-process results
        pred = results.xyxy[0].cpu().numpy()

        # Annotate image with bounding boxes and labels
        for x1, y1, x2, y2, conf, cls in pred:
            label = f'Class {int(cls)}: {conf:.2f}'
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display annotated frame
        cv2.imshow('YOLOv5 Object Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) == ord('q'):
            break

    # Release video capture and close windows
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
