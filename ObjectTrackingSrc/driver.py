import loadImages as li
import similarityScores as ss
import movementScores as ms
import heatmap
import boundingBox as bb
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd
import json
import os
import time

"""
Handles loading information from json and images for performing movement detection.
"""

name = 'Rainy'
capped_images = 500
step = 3

dir_short = ''

start_time = time.time()
# Make directory for output if not made.
if not os.path.exists(name):
    os.makedirs(name)

heatmap_dir_orig = name+'\\Heatmaps_'+name
json_out = name+'\\objects_'+name

print('Loading json: ')
file_name = ""+dir_short+".json"
frame_objs = li.load_json_to_pd(file_name, capped_images, step)

print('Loading images: ')
#file_name = "two_new_videos\\two_new_videos\\"+dir_short+"\\text.txt"
#prefix = "two_new_videos\\two_new_videos\\"+dir_short+"\\"
images = li.load_images_to_pd(file_name, prefix, capped_images, step)

height = images.shape[2]
width = images.shape[1]

print('Calculating scores: ')
obj_frames_s = []
obj_frames_m = []
for i in range(len(frame_objs)-1):
    # Get YOLO object details.
    frame1 = frame_objs[i*step]
    frame2 = frame_objs[(i+1)*step]
    # Get corresponding image frames.
    image1 = images[i]
    image2 = images[i+1]
    # Compute scores
    s_scores = ss.compute_similarity_scores(frame1, frame2, image1, image2)
    m_scores = ms.compute_movement_scores(frame1, frame2, width, height)

    # Threshold similarity scores and movement scores. Thresholds are hyper-parameters that must be predetermined.
    s_obj_list = ss.get_objects_list(s_scores, frame2, threshold=500)
    m_obj_list = ms.get_objects_list(s_obj_list, m_scores, threshold=5)

    # Construct list of objects for both similarity and movement.
    obj_list_s = []
    obj_list_m = []
    for j in s_obj_list:
        obj_list_s.append(frame2[j])
    for j in m_obj_list:
        obj_list_m.append(frame2[j])

    # Save information for each of the two lists.
    obj_frame_s = {}
    obj_frame_s['frame_id'] = i+1
    obj_frame_s['objects'] = obj_list_s
    obj_frames_s.append(obj_frame_s)

    obj_frame_m = {}
    obj_frame_m['frame_id'] = i + 1
    obj_frame_m['objects'] = obj_list_m
    obj_frames_m.append(obj_frame_m)


print('Writing JSON: ')
for i in range(2):
    if i == 0:
        obj_frames = obj_frames_s
        json_out_curr = json_out + '_Similarity'
    else:
        obj_frames = obj_frames_m
        json_out_curr = json_out + '_Movement'

    df = pd.DataFrame(obj_frames)
    with open(json_out_curr, 'w') as outfile:
        df.to_json(outfile)

print('Creating heatmaps: ')
for mode in range(2):
    if mode == 0:
        print('\tSimilarity: ')
        obj_frames = obj_frames_s
        heatmap_dir = heatmap_dir_orig + '_Similarity'
    else:
        print('\tMovement: ')
        obj_frames = obj_frames_m
        heatmap_dir = heatmap_dir_orig + '_Movement'

    # Create heatmap all.
    if not os.path.exists(heatmap_dir + '_all'):
        os.makedirs(heatmap_dir + '_all')
    points = []
    for i in range(len(obj_frames)):
        frame = obj_frames[i]
        obj_list = frame['objects']
        for obj in obj_list:
            points.append(bb.getPoints(obj, width, height))

    if len(points) != 0:
        hm = heatmap.Heatmap()
        img = hm.heatmap(points, dotsize=25, area=((0, 0), (width, height)), size=(height, width))
        img.save(heatmap_dir + '_all\\' + 'all' + '.png')

    # Create heatmap moving.
    size_window = 10
    if not os.path.exists(heatmap_dir+'_moving'):
        os.makedirs(heatmap_dir+'_moving')
    for j in range(len(obj_frames)-1-size_window):
        points = []
        for i in range(size_window):
            frame = obj_frames[i+j]
            obj_list = frame['objects']
            for obj in obj_list:
                points.append(bb.getPoints(obj, width, height))

        if len(points) == 0:
            continue
        hm = heatmap.Heatmap()
        img = hm.heatmap(points, dotsize=25, area=((0, 0), (width, height)), size=(height, width))
        img.save(heatmap_dir+'_moving\\'+str(j*step)+'.png')

    # Create heatmap creation.
    if not os.path.exists(heatmap_dir+'_creation'):
        os.makedirs(heatmap_dir+'_creation')
    for j in range(len(obj_frames) - 1):
        points = []
        for i in range(j+1):
            frame = obj_frames[i]
            obj_list = frame['objects']
            for obj in obj_list:
                points.append(bb.getPoints(obj, width, height))

        if len(points) == 0:
            continue
        hm = heatmap.Heatmap()
        img = hm.heatmap(points, dotsize=25, area=((0, 0), (width, height)), size=(height, width))
        img.save(heatmap_dir + '_creation\\' + str(j*step) + '.png')

print('Time elapsed: '+str(time.time()-start_time))
