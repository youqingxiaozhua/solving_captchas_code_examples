from keras.models import load_model

from cv_test import del_noise, image_segment
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle


MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"
CAPTCHA_IMAGE_FOLDER = "captcha_images"


# Load up the model labels (so we can translate model predictions to actual letters)
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

# Load the trained neural network
model = load_model(MODEL_FILENAME)

# Grab some random CAPTCHA images to test against.
# In the real world, you'd replace this section with code to grab a real
# CAPTCHA image from a live website.
captcha_image_files = list(paths.list_images('%s/xuanwu' % CAPTCHA_IMAGE_FOLDER))
captcha_image_files = np.random.choice(captcha_image_files, size=(10,), replace=False)
# captcha_image_files = ('%s/xuanwu/tdyw.jpg' % CAPTCHA_IMAGE_FOLDER,)

# loop over the image paths
for image_file in captcha_image_files:
    image = cv2.imread(image_file)

    thresh = del_noise(image)
    thresh = cv2.copyMakeBorder(thresh, 20, 20, 20, 20, cv2.BORDER_CONSTANT)

    letter_image_regions = image_segment(thresh)

    # Create an output image and a list to hold our predicted letters
    output = cv2.merge([thresh] * 3)
    predictions = []

    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        # letter_image = thresh[y - 2:y + h + 2, x - 2:x + w + 2]
        letter_image = thresh[y:y + h, x:x + w]

        if len(letter_image) == 0:
            if len(letter_image_regions) == 4:
                print('哥你弄啥来？？？')

        # Re-size the letter image to 20x20 pixels to match training data
        letter_image = resize_to_fit(letter_image, 20, 20)

        # Turn the single image into a 4d list of images to make Keras happy
        letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)

        # Ask the neural network to make a prediction
        prediction = model.predict(letter_image)

        # Convert the one-hot-encoded prediction back to a normal letter
        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

        # draw the prediction on the output image
        cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
        cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    # Print the captcha's text
    captcha_text = "".join(predictions)
    print("CAPTCHA text is: {}".format(captcha_text))

    # Show the annotated image
    cv2.imshow("Output", output)
    cv2.waitKey()
