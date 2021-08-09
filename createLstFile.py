# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:11:43 2020

@author: deniz.kilic
"""
import mxnet as mx
import numpy as np
import os
import json

# Function for reading json files
def read_json(json_path, json_file):
    with open(os.path.join(json_path, json_file)) as f:
        data = json.load(f)
    f.close()
    return data

# Script given in
# https://gluon-cv.mxnet.io/build/examples_datasets/detection_custom.html#lst-record-dataset
def write_line(img_path, im_shape, boxes, ids, idx, is_empty):
    h, w, c = im_shape
    # for header, we use minimal length 2, plus width and height
    # with A: 4, B: 5, C: width, D: height
    A = 4
    if is_empty == True:
         B = 0
    else:
         B = 5
    C = w
    D = h
    # concat id and bboxes
    labels = np.hstack((ids.reshape(-1, 1), boxes)).astype('float')
    # normalized bboxes (recommanded)
    labels[:, (1, 3)] /= float(w)
    labels[:, (2, 4)] /= float(h)
    # flatten
    labels = labels.flatten().tolist()
    str_idx = [str(idx)]
    str_header = [str(x) for x in [A, B, C, D]]
    str_labels = [str(x) for x in labels]
    str_path = [img_path]
# =============================================================================
#     if boxes.size == 0:
#          line = '\t'.join(str_idx + str_header + str_path) + '\n'
#     else:
#          line = '\t'.join(str_idx + str_header + str_labels + str_path) + '\n'
# =============================================================================
    # here if is_empty = True than it creates no bbox, if is_empty = False
    # it creates bbox as [-1, -1, -1, -1] and class id as (-1) for images that have no object
    if is_empty == True:
         line = '\t'.join(str_idx + str_header + str_path) + '\n'
    else:
         line = '\t'.join(str_idx + str_header + str_labels + str_path) + '\n'
    return line

image_folder_path = r'AOI_02\Updated_Images_tile_512'
image_list = os.listdir(image_folder_path)
if 'Thumbs.db' in image_list:
    image_list.remove('Thumbs.db')
json_folder_path = r'AOI_02\Updated_GTs_tile_512_ssd'
json_list = os.listdir(json_folder_path)
f = None
i = -1
j = -1
use_images_with_no_object = False ####

# Write all information to .lst file
with open('AOI_02_tile_512.lst', 'w') as fw:
    for json_file in json_list:
        all_boxes = []
        all_ids = []
        i += 1
        if ((os.path.isdir(os.path.join(json_folder_path, json_file)))):
             continue
        if (f != None):
             f.close()
        json_data = read_json(json_folder_path, json_file)
        gt_samples = json_data['samples']
        # if image has at least 1 object
        if not gt_samples == []:
             for sample in gt_samples:
               all_boxes.append([sample['x_min'], sample['y_min'], sample['x_max'], sample['y_max']])
               all_ids.append(sample['class'])

             # use j for lst file which contains only images with objects
             j += 1
             all_boxes_arr = np.array(all_boxes)
             all_ids_arr = np.array(all_ids)
             img = mx.image.imread(image_folder_path + '\\' + image_list[i])
             # for index value here j is used since imgs with no objects are not used,
             # otherwise i value will be used and below else part will be commented out
             if use_images_with_no_object == True: ###
                  line = write_line(image_folder_path + '\\' + image_list[i], img.shape, all_boxes_arr, all_ids_arr, i, False)
             else: ###
                  line = write_line(image_folder_path + '\\' + image_list[i], img.shape, all_boxes_arr, all_ids_arr, j, False)
             #print(line)
             fw.write(line)
        # if image has no object
        if use_images_with_no_object == True and gt_samples == []: ####
             all_boxes.append([-1, -1, -1, -1])
             all_ids.append(-1)
             all_boxes_arr = np.array(all_boxes)
             all_ids_arr = np.array(all_ids)

             img = mx.image.imread(image_folder_path + '\\' + image_list[i])
             # here if is_empty = True than it creates no bbox, if is_empty = False
             # it creates bbox as [-1, -1, -1, -1] and class id as (-1) for images that have no object
             line = write_line(image_folder_path + '\\' + image_list[i], img.shape, all_boxes_arr, all_ids_arr, i, False)
             #print(line)
             fw.write(line)

# After creating .lst file below command can be used for creating .rec file
# python im2rec.py lst_file_name relative_root_to_images --pass-through --pack-label
