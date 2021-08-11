import os
import pickle

# Result path for txt file
txtResultFolderPath = r'AOI_02\Txt_Results'
# Image path
imageFolderPath = r'AOI_02\Updated_Images_tile_512'
testImagesPath = os.path.basename(imageFolderPath)

picklePathBbox = r'AOI_02\\bboxResults.pickle'
picklePathScore = r'AOI_02\scoreResults.pickle'

def results_to_txt(imageFolderPath, txtResultFolderPath, picklePathBbox, picklePathScore):

     imageNames = os.listdir(imageFolderPath)
     imageNames = [os.path.join(imageFolderPath, images) for images in imageNames]

     if not os.path.exists(txtResultFolderPath):
         os.makedirs(txtResultFolderPath)

     bboxResultsScoreResults = []
     with (open(picklePathBbox, "rb")) as openfile:
          while True:
              try:
                  bboxResultsScoreResults.append(pickle.load(openfile))
              except EOFError:
                  break
     with (open(picklePathScore, "rb")) as openfile:
          while True:
              try:
                  bboxResultsScoreResults.append(pickle.load(openfile))
              except EOFError:
                  break
     bboxResultNames = list(bboxResultsScoreResults[0])
     scoreResultNames = list(bboxResultsScoreResults[1])

     f = open(txtResultFolderPath + '/' + testImagesPath + '.txt', 'a')

     for i in range(len(imageNames)):
        imageName = os.path.split(imageNames[i])
        f.write('Enter Image Path:' + ' ' + str(imageFolderPath + r'\\' + imageName[1] + ':' + ' ') + 'Predicted in xyz milli-seconds.' + '\n')

        for j in range(bboxResultsScoreResults[0][bboxResultNames[i]].shape[1]):
             score_value = bboxResultsScoreResults[1][scoreResultNames[i]][0][j][0].as_np_ndarray().tolist()[0]
             x_min_value = bboxResultsScoreResults[0][bboxResultNames[i]][0][j][0].as_np_ndarray().tolist()[0]
             y_min_value = bboxResultsScoreResults[0][bboxResultNames[i]][0][j][1].as_np_ndarray().tolist()[0]
             width_value = bboxResultsScoreResults[0][bboxResultNames[i]][0][j][2].as_np_ndarray().tolist()[0]-bboxResultsScoreResults[0][bboxResultNames[i]][0][j][0].as_np_ndarray().tolist()[0]+1
             height_value = bboxResultsScoreResults[0][bboxResultNames[i]][0][j][3].as_np_ndarray().tolist()[0]-bboxResultsScoreResults[0][bboxResultNames[i]][0][j][1].as_np_ndarray().tolist()[0]+1

             f.write('car:' + ' ' + str(round(100*score_value)) + '%' + ' ' + '(left_x:' + ' ' + str(x_min_value) + ' ' + 'top_y:' + ' ' + str(y_min_value) + ' ' + 'width:' + ' ' + str(width_value) + ' ' + 'height:' + ' ' + str(height_value) + ')' + '\n')

# inputs are variables that "finetune_detection.py" creates in pickle folder
results_to_txt(imageFolderPath, txtResultFolderPath, picklePathBbox, picklePathScore)
