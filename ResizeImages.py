import cv2
import numpy as np
import os


# Function for resizing images to 224x224 and separating dogs and cats into individual folders
def resize_images(src, destination_cat, destination_dog, grayscale):
    # Looping through every image in folder
    for filename in os.listdir(src):
        if grayscale:
            image = cv2.imread(os.path.join(src, filename), cv2.IMREAD_GRAYSCALE)
            img = np.dstack((image, image, image))
        else:
            # Reading RGB image using cv2.imread() function
            img = cv2.imread(os.path.join(src, filename), cv2.IMREAD_COLOR)

        # In case that the image is NULL skip to the next image
        if (type(img) is np.ndarray):
            filename_without_extension = filename.split(".")

            # Resizing image using cv2.resize()
            resized = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

            # If image name is starting with a uppercase letter then it's image of a cat otherwise it's dog
            if (filename[0].isupper()):
                cv2.imwrite("{}/{}.jpg".format(destination_cat, filename_without_extension[0]), resized)
            else:
                cv2.imwrite("{}/{}.jpg".format(destination_dog, filename_without_extension[0]), resized)

            print("Reszied: {}".format(filename))


resize_images("images/images", "resizedimages/cat", "resizedimages/dog", False)
