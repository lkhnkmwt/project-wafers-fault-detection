from  application_logging import logger
from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from DataTransform_Training.DataTransformation import dataTransform
class train_validation:
    def __init__(self,path):
        self.raw_data=Raw_Data_validation(path)
        self.dataTransform=dataTransform()
        self.dBOperation=dBOperation()
        self.file_object=open("Training_Logs/Training_Main_log.txt",'a+')
        self.log_writer = logger.App_Logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files!!')
            #extracting values from prediction schema
            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = self.raw_data.valuesFromSchema()
            #getting the regex defined to validate filename
            regex=self.raw_data.manualRegexCreation()
            #validating  filename of  prediction files
            self.raw_data.validationFileNameRaw(regex,LengthOfDateStampInFile,LengthOfTimeStampInFile)
            #validating column length in files
            self.raw_data.validateColumnLength(noofcolumns)
            #validating if any column has all values  missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object,"Raw Data Validation Complete!!")
            self.log_writer.log(self.file_object,"Starting Data Transformation")
            #replacing blanks in the csv file with null values to insert in the table
            self.dataTransform.replaceMissingWithNull()

            self.log_writer.log(self.file_object,"Data Transformation Completed!!")
            self.log_writer.log(self.file_object,'Creating Training_Database and tables on the basis of given schema')
            #create database with given name, if present, open the connection!
            self.dBOperation.createTableDb('Training',column_names)
            self.log_writer.log(self.file_object,'Table Creation completed!!')
            self.log_writer.log(self.file_object,"Insertion Of Data into  table started")
            #insert  the csv file into table
            self.dBOperation.insertIntoTableGoodData('Training')
            self.log_writer.log(self.file_object,"Insertion into the table completed")
            self.log_writer.log(self.file_object,"Deleting good data folder!!")
            #Delete the good data  folder after loading the files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object,"Good  data Folder deleted")
            self.log_writer.log(self.file_object,"Moving bad files to archive and deleting bad data files")
            #move  the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object,"Bad files moved to archived and bad folder deleted!!")
            self.log_writer.log(self.file_object,"Validating Operation completed")
            self.log_writer.log(self.file_object,"Extracting csv file from table")
            #export  data in table to csv file
            self.dBOperation.selectingDatafromtableintocsv("Training")
            self.file_object.close()

        except Exception as e:
            raise e









