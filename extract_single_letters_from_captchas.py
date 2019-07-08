import os
import os.path
import cv2
import glob
import imutils

from cv_test import del_noise, image_segment

CAPTCHA_IMAGE_FOLDER = ("captcha_images/gen",
                        "captcha_images/xuanwu"
                        )
OUTPUT_FOLDER = "extracted_letter_images"


# Get a list of all the captcha images we need to process
captcha_image_files = []
for i in CAPTCHA_IMAGE_FOLDER:
    a = glob.glob(os.path.join(i, "*"))
    captcha_image_files += a
counts = {}
j = 0

# loop over the image paths
for (i, captcha_image_file) in enumerate(captcha_image_files):
    filename = os.path.basename(captcha_image_file).lower()
    captcha_correct_text = os.path.splitext(filename)[0]

    # Load the image and convert it to grayscale
    image = cv2.imread(captcha_image_file)
    if image is None:
        continue

    thresh = del_noise(image)

    letter_image_regions = image_segment(thresh)

    # If we found more or less than 4 letters in the captcha, our letter extraction
    # didn't work correcly. Skip the image instead of saving bad training data!
    if len(letter_image_regions) != 4:
        print('pass %s, %s' % (filename, len(letter_image_regions)))
        for x, y, w, h in letter_image_regions:
            cv2.rectangle(thresh, (x - 2, y - 2), (x + w + 4, y + h + 4), (255, 0, 0), 1)
        # cv2.imshow(filename, thresh)
        # cv2.waitKey(0)
        j += 1
        continue

    # Sort the detected letter images based on the x coordinate to make sure
    # we are processing them from left-to-right so we match the right image
    # with the right letter
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    # Save out each letter as a single image
    for letter_bounding_box, letter_text in zip(letter_image_regions, captcha_correct_text):
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        # letter_image = thresh[y - 2:y + h + 2, x - 2:x + w + 2]
        letter_image = thresh[y:y + h, x:x + w]

        # Get the folder to save the image in
        save_path = os.path.join(OUTPUT_FOLDER, letter_text)

        # if the output directory does not exist, create it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, letter_image)

        # increment the count for the current key
        counts[letter_text] = count + 1

print(j)
# cv2.waitKey(0)
