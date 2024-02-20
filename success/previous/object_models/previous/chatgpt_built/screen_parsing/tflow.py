import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights='imagenet')
class_names = ['bottle', 'cup', 'spoon', 'fork', 'tissue', 'trash_can', 'backpack', 'pen', 'pencil', 'marker',
               'door', 'chair', 'couch', 'table', 'sink', 'toilet', 'blind_walking_stick', 'dog', 'cat', 'person',
               'phone', 'towel', 'box', 'jacket', 'shorts', 'shirt', 'socks', 'underwear', 'laptop', 'vest',
               'plate', 'can', 'braille_wording', 'fire_alarm', 'purse']

def preprocess_image(frame):
    img = cv2.resize(frame, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def predict_object(frame):
    img = preprocess_image(frame)
    
    # Make a prediction
    predictions = model.predict(img)
    
    # Decode the predictions
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)[0]
    
    # Display the top prediction
    top_prediction = decoded_predictions[0]
    label = top_prediction[1]
    score = top_prediction[2]
    print(f"Prediction: {label} (Score: {score:.2f})")

if __name__ == "__main__":
    # Open the camera (use 0 for the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Perform object prediction
        predict_object(frame)

        # Display the frame
        cv2.imshow('Live Object Prediction', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
