from trainingModel import trainModel
from training_Validation_Insertion import train_validation

path='Training_Batch_Files'

train_valObj = train_validation(path)  # object initialization

train_valObj.train_validation()  # calling the training_validation function

trainModelObj = trainModel()  # object initialization
print("training done")
trainModelObj.trainingModel()  # training the model for the files in the table