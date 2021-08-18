#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 11:54:34 2021

@author: nithilan
"""
import os
import csv

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
#number_of_frames = [ x[3] for x in data]
#scale_project_name = "lidar_cuboid_shiojiri_2hz"

yaml_config_path = "/home/nithilan/autoware.proj.jpntaxi/src/autoware/launcher/vehicle_launch/config"
s3_path = "s3://tier4-ml-dev-annotator-japantaxi-extracted-frame"
path = "/home/nithilan/Downloads/train/batch_conversion"
bag_path = "/home/nithilan/Insync/nithilan.karunakaran@tier4.jp/datasets/Lsim_learnDataSet"
failed_bag_files = []

original_bag_files = os.listdir(bag_path)
count = 0
for bag_file_name, taxi_id in zip(bag_file_names, taxi_ids):
#    bag_file_name = "da46daf9-ad82-4f49-8efe-5330147cd07f_1610419344_2021-01-12-11-53-21_15"
#    taxi_id = "1089"
    print "bag being processed: " + bag_file_name
    #check if bag data exists in S3
    result = os.popen("aws s3 ls %s/train/%s/ --profile ml-dev-jpntaxi" % (s3_path, bag_file_name)).read()
    #check if corresponding original bag file exists
    matching_bags = [s for s in original_bag_files if bag_file_name in s]

    if len(result) > 0 and len(matching_bags) > 0:
        print "Folder \"%s\" exists in S3!" % (bag_file_name)
    else:
        print "Folder \"%s\" is missing. S3: %d, Bag: %d! Skipping bagfile processing..." % (bag_file_name, len(result), len(matching_bags))
        #to be processed individually later
        failed_bag_files.append(bag_file_name)
        break
    #download original data from S3
    os.system("aws s3 sync %s/train/%s/ %s/%s_original --profile ml-dev-jpntaxi" % (s3_path, bag_file_name, path, bag_file_name))
    
    #reupload original bag data renamed as _original to S3
    os.system("aws s3 sync %s/%s_original %s/train/%s_original/ --profile ml-dev-jpntaxi" % (path, bag_file_name, s3_path, bag_file_name))

    #delete original bag data from S3
    os.system("aws s3 rm %s/train/%s/ --recursive --profile ml-dev-jpntaxi" % (s3_path, bag_file_name))
    
    config = str(taxi_id_config_map.get(taxi_id))
    print "Taxi id map for: " + taxi_id + " is " + config
    #unzip bag file
    err = os.system("zstd -d %s/%s.bag.zst -f -o %s/%s.bag" % (bag_path, bag_file_name, path, bag_file_name))
    if err > 0: #error in unzipping bag
        print "Error in unzipping bag!!"
        break
    #fix jsons using scale_data_fix.py
    ret = os.system("python jpntaxi_scale_data_fix.py %s/%s.bag %s/%s/aip_xx1/ %s/%s_original/json/ %s/%s/" % (path, bag_file_name, yaml_config_path, config, path, bag_file_name, path, bag_file_name))
    if ret == -1:
        print "Error in fixing %s bag!! Please check..." % (bag_file_name)
        break
    #upload fixed bag data to S3
    os.system("aws s3 sync %s/%s %s/train/%s/ --profile ml-dev-jpntaxi" % (path, bag_file_name, s3_path, bag_file_name))
    
    #delete unzipped bag file
    os.system("rm -rf %s/%s.bag" % (path, bag_file_name))
    print "Failed bags so far: " + str(failed_bag_files)
