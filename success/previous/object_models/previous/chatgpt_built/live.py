

# يشتغل ولاكن سيء
#
#

import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained EfficientDet model
model = tf.saved_model.load("/Users/saud/Desktop/findingbuddy/artificial_objects/chatgpt_built/efficientdet_d0_coco17_tpu-32/saved_model")  # Download from: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md

# Define class names

class_names = [
    'bicycle', 'person', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'spoon', 'wine glass', 'cup', 'fork', 'knife', 'bottle', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'bot', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
    'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven',
    'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush',
    'hair brush', 'umbrella', 'sunglasses', 'banner', 'blanket', 'bridge', 'cabinet',
    'cage', 'cardboard', 'carpet', 'cloth', 'clothes', 'clouds', 'counter', 'cupboard',
    'curtain', 'dirt','fence', 'flower',  'fruit', 'grass', 'gravel', 
    'house', 'mud', 'napkin', 'net', 'paper',
     'pillow', 'road', 'rug', 'salad',  'shelf', 'snow', 'stairs',
    'straw', 'table', 'tent', 'towel', 'tree', 'vegetable',
]

def detect_objects_from_webcam():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (640, 640))
        input_tensor = tf.convert_to_tensor([img_resized], dtype=tf.uint8)

        detections = model(input_tensor)

        boxes = detections['detection_boxes'][0].numpy()
        classes = detections['detection_classes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()

        # Display bounding boxes for specific classes with confidence > 0.5
        for i in range(len(boxes)):
            if scores[i] > 0.5:
                h, w, _ = frame.shape
                ymin, xmin, ymax, xmax = boxes[i]
                xmin = int(xmin * w)
                xmax = int(xmax * w)
                ymin = int(ymin * h)
                ymax = int(ymax * h)

                class_id = int(classes[i])
                class_name = class_names[class_id]

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name}: {scores[i]:.2f}", (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_objects_from_webcam()
