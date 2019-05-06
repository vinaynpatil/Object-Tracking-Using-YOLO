import pandas as pd
import numpy as np
import math

"""
Handles all functions with regards to computing similarity scores in motion detection.
"""

# Takes two pandas objects and computes similarity scores of all pairs of objects across frames.
def compute_similarity_scores(frame1, frame2, image1, image2):
    num_objs_frame1 = len(frame1)
    num_objs_frame2 = len(frame2)

    similarity_scores = np.zeros([num_objs_frame1, num_objs_frame2])

    # Create histograms of bounding boxes.
    hist_prev = create_histogram(frame1, image1)
    hist_new = create_histogram(frame2, image2)

    bb_prev = get_bounding_boxes(frame1, image1)
    bb_new = get_bounding_boxes(frame2, image2)

    for i in range(num_objs_frame1):
        for j in range(num_objs_frame2):
            hist_score = compute_similarity(hist_prev[i], hist_new[j])
            #print('hist\t'+str(hist_score))
            bb_score = compute_bb_similarity(bb_prev[i], bb_new[j])
            #print('bb\t'+str(bb_score))
            similarity_scores[i][j] = hist_score + bb_score

    return similarity_scores


def get_objects_list(scores, frame2, threshold=5000):
    min_vals = scores.min(axis=1)
    min_inds = scores.argmin(axis=1)

    thresholding = [i for i in range(len(min_vals)) if min_vals[i] < threshold]
    obj_list = min_inds[thresholding]

    return obj_list


# Given a frame, will make a list of all the sizes of the bounding boxes.
def get_bounding_boxes(frame, image):
    sizes = []
    img_width = image.shape[1]
    img_height = image.shape[0]
    for obj in frame:
        rel_coords = obj['relative_coordinates']
        width = rel_coords['width'] * img_width
        height = rel_coords['height'] * img_height
        xCen = rel_coords['center_x'] * img_width
        yCen = rel_coords['center_y'] * img_height
        size = np.array([width, height])
        sizes.append(size)

    return sizes


def compute_bb_similarity(bb1, bb2):
    norm = np.linalg.norm(bb1 - bb2)
    return norm


# Given two objects, compute the similarity score between the two objects.
def compute_similarity_naive(object1, object2):
    if object1['class_id'] == object2['class_id']:
        return object1['confidence'] * object2['confidence']
    else:
        return object1['confidence'] * (1 - object2['confidence'])


# Given two objects, compute the similarity score between the two objects.
def compute_similarity(hist1, hist2):
    red1 = hist1['red'][0]
    green1 = hist1['green'][0]
    blue1 = hist1['blue'][0]
    red2 = hist2['red'][0]
    green2 = hist2['green'][0]
    blue2 = hist2['blue'][0]

    red_norm = np.linalg.norm(red1-red2)
    green_norm = np.linalg.norm(green1-green2)
    blue_norm = np.linalg.norm(blue1-blue2)

    score = red_norm + green_norm + blue_norm
    return score / 1000


def create_histogram(frame, image, bins=200):
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]
    img_width = red.shape[1]
    img_height = red.shape[0]
    if len(frame) == 0:
        return None
    elif len(frame) == 1:
        # Create histogram of one object
        obj = frame[0]
        hists = hist_object(obj, red, green, blue, img_width, img_height, bins)
        return [hists]
    else:
        # Create histogram of one object
        obj = frame[0]
        hists = []
        for obj in frame:
            hist = hist_object(obj, red, green, blue, img_width, img_height, bins)
            hists.append(hist)

        return hists


def hist_object(obj, red, green, blue, img_width, img_height, bins):
    rel_coords = obj['relative_coordinates']
    width = rel_coords['width'] * img_width
    height = rel_coords['height'] * img_height
    xCen = rel_coords['center_x'] * img_width
    yCen = rel_coords['center_y'] * img_height
    xStart = math.floor(xCen - width / 2)
    yStart = math.floor(yCen - height / 2)
    xEnd = math.floor(xCen + width / 2)
    yEnd = math.floor(yCen + height / 2)
    hist_red = np.histogram(red[yStart:yEnd, xStart:xEnd], range=(0, 1), bins=bins)
    hist_green = np.histogram(green[yStart:yEnd, xStart:xEnd], range=(0, 1), bins=bins)
    hist_blue = np.histogram(blue[yStart:yEnd, xStart:xEnd], range=(0, 1), bins=bins)
    hist = {'red': hist_red, 'green': hist_green, 'blue': hist_blue}
    return hist
