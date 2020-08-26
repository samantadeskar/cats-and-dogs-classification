import cv2
import numpy as np
import os
import h5py


# Function for saving loaded images and labels into .h5 format so that it can be used in Google Colab
# Gets called by load_and_save_data function
def save_h5_data(filename, x_data, y_data):
    with h5py.File(filename, "w") as out:
        out.create_dataset("x_data", data=x_data, compression="gzip", compression_opts=9)
        out.create_dataset("y_data", data=y_data, dtype='i8', compression="gzip", compression_opts=9)
    print("H5 file saved!")


# Loading images and image labels into numpy arrays and calling save_h5_data function
def load_and_save_data(path_cat, path_dog, save_name, names, num):
    # Placeholder for images and labels
    images = np.empty((num, 224, 224, 3), dtype=np.float32)
    labels = np.zeros(num, dtype=np.int8)

    # Loading cat images and labels
    for (i, filename) in enumerate(os.listdir(path_cat)):
        images[i] = cv2.imread(os.path.join(path_cat, filename), cv2.IMREAD_COLOR) / 255.0
        for (j, name) in enumerate(names):
            if parseName(filename) == name:
                labels[i] = j

    # Loading dog images and labels
    for (i, filename) in enumerate(os.listdir(path_dog)):
        images[i + 2394] = cv2.imread(os.path.join(path_dog, filename), cv2.IMREAD_COLOR) / 255.0
        for (j, name) in enumerate(names):
            if parseName(filename) == name:
                labels[i + 2394] = j

    print("Done loading images!")
    save_h5_data(save_name, images, labels)


# Function for parsing image name
def parseName(name):
    for (i, letter) in enumerate(name):
        if name[i] == "_" and name[i + 1].isdigit():
            return name[0:i]

    return "error"


# Function for getting animal ID
def getIDs(path_cat, path_dog):
    all_names = []

    # Fetches all cat breeds
    for filename in os.listdir(path_cat):
        all_names.append(parseName(filename))

    # Fetches all dog breeds
    for filename in os.listdir(path_dog):
        all_names.append(parseName(filename))

    #Counts how much of images there is
    count = len(all_names)

    # Gets unique list of breeds and sorts them alphabetically
    all_names = list(set(all_names))
    all_names.sort()

    print(all_names)
    print(count)
    return all_names, count


# Running the functions
species, num = getIDs("resizedimages/cat", "resizedimages/dog")
load_and_save_data("resizedimages/cat", "resizedimages/dog", "data.h5", species, num)
