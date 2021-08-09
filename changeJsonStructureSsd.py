# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:30:33 2020

@author: deniz.kilic
"""
import os
import json

def read_json(json_path, json_file):
    with open(os.path.join(json_path, json_file)) as f:
        data = json.load(f)
    f.close()
    return data

def write_to_json(json_file_name,data):
    with open(json_file_name, 'w') as json_file:
        json.dump(data, json_file,indent=2)
    json_file.close()

def append_to_json(json_struct, class_num, idx_num, modified, x_min, y_min, x_max, y_max):
    json_struct['samples'].append({
        'class': class_num,
        'idx': idx_num,
        'isModified': modified,
        'x_min': x_min,
        'y_min': y_min,
        'x_max': x_max,
        'y_max': y_max
    })
    return json_struct

json_folder_path = r'AOI_02\Updated_GTs_tile_512'
modified_json_path = r'AOI_02\Updated_GTs_tile_512_ssd'

json_struct = {
  "samples": [{
    "class" : {"type" : "string"},
    "idx": {"type": "string"},
    "isModified": {"type": "string"},
    "x_min": {"type": "string"},
    "y_min": {"type": "string"},
    "x_max" : {"type" : "string"},
    "y_max" : {"type" : "string"}

  }]
}

if not os.path.exists(modified_json_path):
    os.makedirs(modified_json_path)

json_list = os.listdir(json_folder_path)
f = None
for json_file in json_list:
    if ((os.path.isdir(os.path.join(json_folder_path, json_file)))):
        continue
    if (f != None):
        f.close()

    file_name, file_extension = os.path.splitext(json_file)
    f = open(modified_json_path + '/' + json_file, 'a')

    json_data = read_json(json_folder_path, json_file)
    gt_samples = json_data['samples']

    json_struct['samples'].clear()

    for sample in gt_samples:
        class_num = str(sample['class'])
        idx_num = str(sample['idx'])
        modified = str(sample['isModified'])
        x_min = str((1/1)*int(float(sample['x'])))
        y_min = str((1/1)*int(float(sample['y'])))
        x_max = str((1/1)*(int(float(sample['x'])) + int(float(sample['width'])) - 1))
        y_max = str((1/1)*(int(float(sample['y'])) + int(float(sample['height'])) - 1))
        json_struct = append_to_json(json_struct, class_num, idx_num, modified, x_min, y_min, x_max, y_max)

    write_to_json(os.path.join(modified_json_path, json_file), json_struct)

    f.close()
