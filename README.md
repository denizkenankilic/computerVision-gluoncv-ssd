# computerVision-gluoncv-ssd
Finetune a Pretrained SSD Detection Model with GluonCV

In this repository, there are Python codes to finetune a pretrained SSD (single shot detector) model with GluonCV library (mxnet). The "changeJsonStructureSsd.py" script can be used to change the Json structure of ground truths (here bounding box) to be useable for SSD. It changes the following struture

      "class": "0",
      "height": "25",
      "idx": "88",
      "isModified": "true",
      "width": "19",
      "x": "461",
      "y": "1995"

to the structure below

      "class": "0",
      "idx": "193",
      "isModified": "true",
      "x_min": "330",
      "y_min": "0",
      "x_max": "356",
      "y_max": "17"
      
The example data folder which stands in the repository contains the updated Json files. The main "finetune_detection.py" code requires a ".rec" file and ".lst" file need to be created to form ".rec" file. Therefore we use the "createLstFile.py" is used to create ".lst" file firstly. It uses images and ground truths in updated Json format. After creating ".lst" file below command can be used for creating .rec file:

      python im2rec.py lst_file_name relative_root_to_images --pass-through --pack-label

Finally, "finetune_detection.py" is used to train model and find predicted ground truths in the test folder. The "resultsToTxtSsd.py" script converts the pickle results, that are outputs of "finetune_detection.py", to the txt format.
