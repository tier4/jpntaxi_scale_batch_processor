#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 10:36:53 2021

@author: nithilan
"""

import os
import sys
import csv
import argparse

#mapping taxi_id and config yamls
taxi_id_config_map = {
		"4941" : 1,
		"1089" : 2,
		"4943" : 3,
		"2190" : 4,
		"4939" : 5,
		"2189" : 7,
		"4940" : 8,
        	"2638" : 9,
		"5030" : 10,                
	}

with open('/home/nithilan/Downloads/train/lidar_cuboid_shiojiri_2hz.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

old_task_ids = [ x[0] for x in data]
bag_file_names = [ x[1] for x in data]
taxi_ids = [ x[2] for x in data]
number_of_frames_list = [ x[3] for x in data]
scale_project_name = "lidar_cuboid_shiojiri_2hz"

yaml_config_path = "/home/nithilan/autoware.proj.jpntaxi/src/autoware/launcher/vehicle_launch/config"
s3_path = "s3://tier4-ml-dev-annotator-japantaxi-extracted-frame"
path = "/home/nithilan/Downloads/train/batch_conversion"
bag_path = "/home/nithilan/Insync/nithilan.karunakaran@tier4.jp/datasets/Lsim_learnDataSet"
failed_bag_files = []
count = 0
original_bag_files = os.listdir(bag_path)
for bag_file_name, taxi_id, old_task_id, number_of_frames in zip(bag_file_names, taxi_ids, old_task_ids, number_of_frames_list):
#    bag_file_name = "da46daf9-ad82-4f49-8efe-5330147cd07f_1610419344_2021-01-12-11-53-21_15"
#    taxi_id = "1089"
    print "bag being processed: " + bag_file_name
    #check if bag data exists in S3
    ret = os.system("python /home/nithilan/scale_ai/CuboidLidarAnnotation_command_line.py %s %s %s %s" % (scale_project_name, bag_file_name, number_of_frames, old_task_id))
    if ret == -1:
        print "Error in creating task for bag %s!! Please check..." % (bag_file_name)
        break
    count = count + 1

print "Number of bags processed: " + str(count) + " , number of csv entries: " + str(len(old_task_ids))