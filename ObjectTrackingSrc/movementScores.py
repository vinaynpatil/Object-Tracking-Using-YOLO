import pandas as pd
import numpy as np
import math

"""
Handles all functions with regards to computing movement scores in motion detection.
"""

# Takes two pandas objects and computes movement scores of all pairs of objects across frames.
def compute_movement_scores(frame1, frame2, img_width, img_height):
    num_objs_frame1 = len(frame1)
    num_objs_frame2 = len(frame2)

    movement_scores = np.zeros([num_objs_frame1, num_objs_frame2])

    for i in range(num_objs_frame1):
        for j in range(num_objs_frame2):
            score = compute_movement(frame1[i], frame2[j], img_width, img_height)
            movement_scores[i][j] = score

    return movement_scores


def get_objects_list(obj_list_sim, scores, threshold=50):
    #print('New List:')
    obj_list = []
    for i in range(len(obj_list_sim)):
        #print('\t'+str(scores[i][obj_list_sim[i]]))
        if scores[i][obj_list_sim[i]] > threshold and scores[i][obj_list_sim[i]] < 100:
            obj_list.append(obj_list_sim[i])

    return obj_list


# Given two objects, compute the movement score between the two objects.
def compute_movement(object1, object2, img_width, img_height):
    rel_coords1 = object1['relative_coordinates']
    width1 = rel_coords1['width'] * img_width
    height1 = rel_coords1['height'] * img_height
    xCen1 = rel_coords1['center_x'] * img_width
    yCen1 = rel_coords1['center_y'] * img_height

    rel_coords2 = object2['relative_coordinates']
    width2 = rel_coords2['width'] * img_width
    height2 = rel_coords2['height'] * img_height
    xCen2 = rel_coords2['center_x'] * img_width
    yCen2 = rel_coords2['center_y'] * img_height

    obj1_name = object1['name']
    obj2_name = object2['name']

    lambda1 = 1
    lambda2 = 1

    displacement = math.sqrt((xCen1 - xCen2)*(xCen1 - xCen2) + (yCen1 - yCen2)*(yCen1 - yCen2))
    morphing = math.sqrt((width1 - width2)*(width1 - width2) + (height1 - height2)*(height1 - height2))

    # Movement score construction.
    score = lambda1 * displacement - lambda2 * morphing

    return score


# Given a table of movement scores, determine what objects have moved.
def determine_movement(scores):
    max_id = np.argmax(scores, axis=0)
    max_val = np.amax(scores, axis=0)
    result = np.concat([max_id, max_val])

    return result


