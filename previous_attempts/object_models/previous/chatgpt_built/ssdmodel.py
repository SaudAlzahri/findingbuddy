
#
#
#   reorganize object list
#                  even with that its not accurate enough
#
#


import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained SSD MobileNet model
model = tf.saved_model.load("/Users/saud/Desktop/findingbuddy/artificial_objects/chatgpt_built/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model")

# Function to perform object detection and return bounding box coordinates
def detect_objects(frame):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (640, 416))
    input_tensor = tf.convert_to_tensor([img_resized], dtype=tf.uint8)

    detections = model(input_tensor)

    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()

    if classes.size == 0 or scores.size == 0:
        print("No objects detected or scores available.")
        return

    for i in range(len(boxes)):
        if scores[i] > 0.5:
            h, w, _ = frame.shape
            ymin, xmin, ymax, xmax = boxes[i]
            xmin = int(xmin * w)
            xmax = int(xmax * w)
            ymin = int(ymin * h)
            ymax = int(ymax * h)

            # Make sure the class index is within the range of class_names list
            class_index = int(classes[i])
            if 0 <= class_index < len(class_names):
                class_name = class_names[class_index]
            else:
                class_name = 'Unknown'

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name}: {scores[i]:.2f}", (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Object Detection', frame)



if __name__ == "__main__":
    # Define COCO class names
    class_names = ['background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                   'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
                   'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
                   'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
                   'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
                   'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'apple',
                   'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
                   'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                   'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    # Open camera (0 is the default camera index)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detect_objects(frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
