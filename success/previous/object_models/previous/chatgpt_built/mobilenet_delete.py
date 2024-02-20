
# WORKS BUT NO BOUNDING BOXES!!

# Is image classification rather than object detection!

import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights='imagenet')
class_names = ['bottle', 'cup', 'spoon', 'fork', 'tissue', 'trash_can', 'backpack', 'pen', 'pencil', 'marker',
               'door', 'chair', 'couch', 'table', 'sink', 'toilet', 'blind_walking_stick', 'dog', 'cat', 'person',
               'phone', 'towel', 'box', 'jacket', 'shorts', 'shirt', 'socks', 'underwear', 'laptop', 'vest',
               'plate', 'can', 'braille_wording', 'fire_alarm', 'purse']

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def predict_object(image_path):
    img = preprocess_image(image_path)
    
    # Make a prediction
    predictions = model.predict(img)
    
    # Decode the predictions
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)[0]
    
    # Display the top 3 predictions
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions[:3]):
        print(f"{i + 1}: {label} ({score:.2f})")

if __name__ == "__main__":
    # Replace 'your_image.jpg' with the path to your image
    image_path = '/Users/saud/Desktop/findingbuddy/artificial_objects/cat_and_dog.jpg'
    
    # Make a prediction on the image
    predict_object(image_path)
