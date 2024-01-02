import os
import re
import pandas as pd
from typing import List, Tuple
import openpyxl
from itertools import chain
import constants

class Parser:
    def __init__(self, outputFile) -> None:
        self.output_file = outputFile
        # directory paths
        self.BASEDIR = os.path.abspath("/Users/maxschnitt/Documents/AnalysingStudentDevelopment/")
        self.DATA = os.path.join(self.BASEDIR, "Parser" ,"statistik-ws-20232024-2.csv")
        self.OUT_PATH = os.path.join(self.BASEDIR, "data", self.output_file)
        
        self.loaded_data = self.dataLoader()
        
        # MultiIndex 
        self.HEADER_FIRST_LEVEL = ["", "", *["WiSe 2005/2006" for _ in range(len(constants.SEMESTERS))]]
        self.HEADER_SECOND_LEVEL = ["", "HF/NF", *["Fachsemester" for _ in range(len(constants.SEMESTERS))]]
        self.HEADER_THIRD_LEVEL = ["Subject", "", *constants.SEMESTERS]
        self.HEADER = [self.HEADER_FIRST_LEVEL, self.HEADER_SECOND_LEVEL,self.HEADER_THIRD_LEVEL]

    def __createMultiIndex(self):
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
            # facultyData = re.sub(HF_PATTERN, "",facultyData)
            splittedData = [data for data in facultyData.split("\n") if not re.fullmatch(r'(?:\"|\s")', data)]
            cleanedData.append(splittedData)
        return cleanedData


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
        
        #check for empty main and minor subject
        if totalMainSubject == None or len(totalMainSubject) == 0:
            totalMainSubject = [0 for _ in range(len(constants.SEMESTERS))]
        if totalMinorSubject == None or len(totalMinorSubject) == 0:
            totalMinorSubject = [0 for _ in range(len(constants.SEMESTERS))]
            
        if len(totalMainSubject) != 14:
            totalMainSubject.insert(0,0)
        if len(totalMinorSubject) != 14:
            totalMinorSubject.insert(0,0)
            
        
        assert len(totalMainSubject) == 14 and len(totalMinorSubject) == 14   
            
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
        
        
    def __clean_excel_sheet(self, sheet:str):
        """ remove all data from excel sheet

        Args:
            sheet (str): name of excel sheet
        """
        excel_workbench = openpyxl.load_workbook(self.OUT_PATH)
        try:
            excel_workbench.remove(excel_workbench[sheet])
        except KeyError:
            pass
        finally:
            excel_workbench.create_sheet(sheet)
            excel_workbench.save(self.OUT_PATH)

            
    def parseSubsetData(self, file:str, output_sheet:str) :
        """ parses buggy csv as text and extracts data to excel

        Args:
            output_sheet (str): name of excel sheet
        """
        
        self.DATA = os.path.join(self.BASEDIR, "data", "csvFiles", file)
        
        multiIndex = self.__createMultiIndex()
        
        #self.__clean_excel_sheet(output_sheet)

        with open(self.DATA, "r") as file:
            dataAsString = file.read()
            preprocessedData = self.__preprocessData(dataAsString)
            cleanedFacultyData = self.__cleanDataForFaculties(preprocessedData)
            pandasData = self.__createPandasStructureAllFaculties(cleanedFacultyData)
            pandasFrame = pd.DataFrame(pandasData, columns=multiIndex)
            pandasFrame.to_excel(self.OUT_PATH, sheet_name=output_sheet)
        
            
if __name__ == "__main__":
    csvFilePath = os.path.abspath("/Users/maxschnitt/Documents/AnalysingStudentDevelopment/data/csvFiles")
    output_file = "student_data_per_subject.xlsx"
    filenames = os.listdir(csvFilePath)
    
    myParser = Parser(output_file)
    for number, file in enumerate(filenames):
        print("#######################################")
        print(f"Currently at file: {file}")
        sheet = f"Sheet{number}"
        myParser.parseSubsetData(file, sheet)
        print("#######################################")
    #myParser.parseSubsetData("ss-2006.csv", "Sheet1")