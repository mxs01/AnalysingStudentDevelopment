import os
import re
import pandas as pd
from typing import List, Tuple, Set
import openpyxl
from itertools import chain
import constants

class Parser:
    def __init__(self, outputFile) -> None:
        self.output_file = outputFile
        # directory paths
        self.BASEDIR = constants.PROJECT_DIR
        self.DATA = os.path.join(self.BASEDIR, "code","")
        self.OUT_PATH = os.path.join(self.BASEDIR, "data", self.output_file)
        
        self.pandasDataAsDict = dict()
        # MultiIndex 
        self.HEADER_FIRST_LEVEL = ["", "", *list(chain(*[[year for _ in range(len(constants.SEMESTERS))] for year in constants.YEARS]))]
        self.HEADER_SECOND_LEVEL = ["", "HF/NF", *list(chain(*[["Fachsemester" for _ in range(len(constants.SEMESTERS))] for _ in range(len(constants.YEARS))]))]
        self.HEADER_THIRD_LEVEL = ["Subject", "", *list(chain(*[constants.SEMESTERS for _ in range(len(constants.YEARS))]))]
        self.HEADER = [self.HEADER_FIRST_LEVEL, self.HEADER_SECOND_LEVEL,self.HEADER_THIRD_LEVEL]

    def __createMultiIndex(self,):
        """creates MultiIndex for pandas frame

        Returns:
            pd.MultiIndex: MultiIndex for pandas frame
        """
        return pd.MultiIndex.from_arrays(self.HEADER)
   
    def __preprocessData(self,fileAsStr: str) -> List[str]:
        """ removes unwanted data from the file

        Args:
            fileAsStr (str): csv file as string

        Returns:
            List[str]: data for different faculties
        """
        formattedData = []
        removeEmptyLines = re.sub(constants.EMPTY_LINE_PATTERN, "", fileAsStr)
        removePageNumbers = re.sub(constants.PAGE_NUMBER_PATTERN, "", removeEmptyLines)
        removeUniversityData = re.sub(constants.REMOVE_PATTERN, "", removePageNumbers)
        splittedData = re.split(constants.DELIMETER_PATTERN, removeUniversityData)
        splittedData = [re.sub(constants.DELIMETER_PATTERN, "", data) for data in splittedData]
        
        for split in splittedData:
            formattedData.append(split)
        return formattedData[1:]

    def __cleanDataForFaculties(self,preprocessedData: List[str]) -> List[List[str]]:
        """ removes unwanted patterns in faculty specific data 

        Args:
            preprocessedData (List[str]): preprocessed faculty data which needs to be cleaned

        Returns:
            List[List[str]]: cleaned faculty data 
        """
        cleanedData = []
        for facultyData in preprocessedData:
            facultyData = re.sub(constants.MULTIPLE_BLANKS_PATTERN," " ,facultyData)
            facultyData = re.sub(constants.PAGE_NUMBER_PATTERN , "",facultyData)
            facultyData = re.sub(constants.FACHSEMESTER_PATTERN,"Fachsemester",facultyData)
            splittedData = [data for data in facultyData.split("\n") if not re.fullmatch(r'(?:\"|\s")', data)]
            cleanedData.append(splittedData)
        return cleanedData

    def __prefillWithAllSubjects(self,subjects: Set,preprocessedData: List[str]):
        """fills self.pandasDataAsDict dictionary with keys

        Args:
            subjects (Set): all subjects
            preprocessedData (List[str]): cleaned faculty data
        """
        for data in preprocessedData:
            subject = data[0]
            subjects.add(subject)
        for subject in subjects:
            if subject not in self.pandasDataAsDict.keys():  
                self.pandasDataAsDict[subject] = [[subject,"HF"],[subject,"NF"], False]
    
    def __checkIfElementsAdded(self, subject):
        """_summary_

        Args:
            subject (str): a university subject
        """
        majorData, minorData, changed = self.pandasDataAsDict[subject]
        noData = [0 for _ in range(14)]
        assert len(noData) == 14
        if not changed:
            majorData.extend(noData)
            minorData.extend(noData)
        self.pandasDataAsDict[subject][2]=False
        
                
    def __addElementsToPandaDataAsDict(self,subject,minor, major):
        """fills self.pandasDataAsDict with data

        Args:
            subject (str): subject name
            minor (List): minor data
            major (List): major data
        """
        majorData, minorData, _ = self.pandasDataAsDict[subject]
        self.pandasDataAsDict[subject][2]=True
        majorData.extend(major)
        minorData.extend(minor)
        
    def __createPandasStructureSingleFaculty(self,subjectData:List[str]) -> Tuple[List[str], List[str]]:
        """build list structure which represents minor and major row in data

        Args:
            subjectData (List[str]): data of a faculty as list

        Returns:
            Tuple[List[str], List[str]]: list which represents one row in pandas data frame
        """
        subject = subjectData[0]
        # only extract the numerical values 
        totalMainSubject = list(chain.from_iterable([data.split(" ")[1:] for data in subjectData if re.match(constants.HF_PATTERN, data)]))[0:-1]
        totalMinorSubject = list(chain.from_iterable([data.split(" ")[1:] for data in subjectData if re.match(constants.NF_PATTERN, data)]))[0:-1]
        
        if "HF" in totalMainSubject:
            totalMainSubject = totalMainSubject[1:]
        if "NF" in totalMinorSubject:
            totalMinorSubject = totalMinorSubject[1:]
        
        #check for empty main and minor subject
        if totalMainSubject == None or len(totalMainSubject) == 0:
            totalMainSubject = ["0" for _ in range(len(constants.SEMESTERS))]
        if totalMinorSubject == None or len(totalMinorSubject) == 0:
            totalMinorSubject = ["0" for _ in range(len(constants.SEMESTERS))]
            
        if len(totalMainSubject) != 14:
            totalMainSubject.insert(0,"0")
        if len(totalMinorSubject) != 14:
            totalMinorSubject.insert(0,"0")
            
        # each row has to have length 14
        assert len(totalMainSubject) == 14 and len(totalMinorSubject) == 14   
        
        self.__addElementsToPandaDataAsDict(subject,totalMinorSubject,totalMainSubject)
        
        return [subject, "HF", *totalMainSubject], [subject, "NF", *totalMinorSubject]
        

    def __createPandasStructureAllFaculties(self,preprocessedData: List[str])->List[List[str]]:
        """create 2d array which contains HF/NF data for each faculty

        Args:
            preprocessedData (List[str]): cleaned faculty data

        Returns:
            List[List[str]]: array which contains hf/nf data for all faculties
        """
        # stores rows for pandas dataframe
        pandasFrameStructures = []
        for data in preprocessedData:
            # create row data for each subject
            mainSubjectFrame, minorSubjectFrame = self.__createPandasStructureSingleFaculty(data)
            pandasFrameStructures.append(mainSubjectFrame)
            pandasFrameStructures.append(minorSubjectFrame)
        return pandasFrameStructures
        
    def __constructRowDataFromPandasDataFromDict(self):
        """creates 2d array from self.pandasDataFromDict

        Returns:
            List[List]: 2d list of row data for pandas
        """
        pandasRowData = []
        for major,minor,change in self.pandasDataAsDict.values():
            pandasRowData.append(major)
            pandasRowData.append(minor)
        return pandasRowData       
            
    def parseSubsetData(self, files:List[str], output_sheet:str) :
        """ parses buggy csv as text and extracts data to excel

        Args:
            output_sheet (str): name of excel sheet
        """
        subjects = set()
        for file in files:
            filename = file.replace("/", "-") + ".csv"
            self.DATA = os.path.join(self.BASEDIR, "data", "csvFiles", filename)            
            multiIndex = self.__createMultiIndex()
            with open(self.DATA, "r") as file:
                dataAsString = file.read()
                preprocessedData = self.__preprocessData(dataAsString)
                cleanedFacultyData = self.__cleanDataForFaculties(preprocessedData)
                self.__prefillWithAllSubjects(subjects,cleanedFacultyData)
        
        for file in files:
            filename = file.replace("/", "-") + ".csv"
            self.DATA = os.path.join(self.BASEDIR, "data", "csvFiles", filename)            
            multiIndex = self.__createMultiIndex()
            with open(self.DATA, "r") as file:
                dataAsString = file.read()
                preprocessedData = self.__preprocessData(dataAsString)
                cleanedFacultyData = self.__cleanDataForFaculties(preprocessedData)
                self.__createPandasStructureAllFaculties(cleanedFacultyData)
            for subject in subjects:
                self.__checkIfElementsAdded(subject)
        
        
        for values in list(self.pandasDataAsDict.values()):
            assert len(values[0]) == 520
            assert len(values[1]) == 520
            
        # create pandas frame
        pandasFrame = pd.DataFrame(self.__constructRowDataFromPandasDataFromDict(), columns=multiIndex)
        pandasFrame.to_excel(self.OUT_PATH, sheet_name=output_sheet)
        
            
if __name__ == "__main__":
    csvFilePath = os.path.abspath("/Users/maxschnitt/Documents/AnalysingStudentDevelopment/data/csvFiles")
    output_file = "student_data_per_subject.xlsx"
    filenames = constants.YEARS
    #os.listdir(csvFilePath)
    
    myParser = Parser(output_file)
    myParser.parseSubsetData(filenames, "Sheet1")