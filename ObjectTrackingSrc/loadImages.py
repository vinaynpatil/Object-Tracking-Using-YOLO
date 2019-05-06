import json
import numpy as np
import pandas as pd
from matplotlib.image import imread
import time

"""
Handles loading information from json and images for performing movement detection.
"""

# Load the json file into a pandas object.
def load_json_to_pd(file_name, max_images, step=1):
    with open(file_name) as json_file:
        data = pd.io.json.read_json(json_file)

    frame_objs = data.objects

    if len(frame_objs) > max_images:
        frame_objs = frame_objs[:max_images]

    frame_objs = frame_objs[0::step]

    return frame_objs


# Load images from a file to a numpy array.
# Returned object has dimensions (frame, yval, xval, rgb)
def load_images_to_pd(file_name, prefix, max_images, step=1):
    start_time = time.time()
    # Get image names.
    with open(file_name) as f:
        file = f.read()
        img_names = file.split("\n")

    # Assume at least two images.
    img = load_image(prefix+img_names[0])
    img2 = load_image(prefix+img_names[1])

    images = np.stack((img, img2))

    num_images = len(img_names)

    if num_images > max_images:
        num_images = max_images
    inc = int((num_images/step)/20)
    for i in range(int((num_images-2)/step)):
        if i % inc == 0:
            print('\t...'+str((i/inc)*5)+'%... ('+str(time.time()-start_time)+')')
        curr_img = load_image(prefix+img_names[(i*step)+2])
        curr_img = np.expand_dims(curr_img, axis=0)
        images = np.concatenate((images, curr_img), axis=0)

    return images


# Load one image into a numpy array.
def load_image(file_name):
    img = imread(file_name)
    return img



