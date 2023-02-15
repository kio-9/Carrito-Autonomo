import numpy as np
import pandas as pd
import cv2

# Cargar datos
rawImgData = cv2.VideoCapture('./out.avi')
ret, frame= rawImgData.read()
cv2.imshow('frame',frame)
cv2.waitKey(1)

# Entrenamiento

# training_indices = np.arange(1500)
# testing_indices = np.arange(1500, 2000)

# images_training = data['images'][training_indices, :, :]/255. #Normalize between 0 and 1
# angles_training = data['encoded_angles'][training_indices, :]

# images_testing = data['images'][testing_indices, :, :]/255. #Normalize between 0 and 1
# angles_testing = data['encoded_angles'][testing_indices, :]