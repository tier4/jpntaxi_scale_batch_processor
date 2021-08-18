# JapanTaxi (XX1) Scale.AI Data Batch Fixing and Task Creation Tool

Depends on [https://github.com/tier4/jpntaxi_annotation_data_fixer](URL) & [https://github.com/tier4/scale_ai](URL)

`batch_data_fixer.py` - Fixes bag files supplied in a csv and uploads to AWS S3

`scale_batch_task_upload.py` - Creates tasks on Scale AI dashboard from preprocessed list of bag files from the previous step