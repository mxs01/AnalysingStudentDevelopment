import os
import re
import pandas as pd
from typing import List, Dict
import openpyxl
from itertools import chain

# directory paths
BASEDIR = os.getcwd()
DATA = os.path.join(BASEDIR, "statistik-ws-20232024-2.csv")

# REGEX Patterns
DELIMETER_PATTERN = re.compile(r".*\s*Studienfachbelegung nach Abschlusszielen")
REMOVE_PATTERN = re.compile(r'(?:\s*"EBERHARD KARLS UNIVERSITÄT"\s*|\s*"72074 Tübingen"\s*)|"Stand der Datenerhebung: \d{2}.\d{2}.\d{4}"|"Wintersemester \d{4} / \d{4}"|"ST.NR.S‐\d{3}‐\d{1,3}"')
EMPTY_LINE_PATTERN = re.compile(r'""\n')
PAGE_NUMBER_PATTERN = re.compile(r'" ‐ \d{0,3} ‐"')
MULTIPLE_BLANKS_PATTERN = re.compile(r"\s{2,}")
FACHSEMESTER_PATTERN = re.compile(r'Fachsemesterzahlen .+')
HF_PATTERN = re.compile(r'"Ges\.HF.*"')
NF_PATTERN = re.compile(r'"Ges\.NF.*"')

# Constants
SEMESTERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ,"10", "11", "12", ">12"]
YEARS  = [
    "WiSe 2005/2006",
    "SoSe 2006",
    "WiSe 2006/2007",
    "SoSe 2007",
    "WiSe 2007/2008",
    "SoSe 2008",
    "WiSe 2008/2009",
    "SoSe 2009",
    "WiSe 2009/2010",
    "SoSe 2010",
    "WiSe 2010/2011",
    "SoSe 2011"
    "WiSe 2011/2012",
    "SoSe 2012",
    "WiSe 2012/2013",
    "WiSe 2013/2014",
    "SoSe 2013",
    "SoSe 2014",
    "WiSe 2014/2015",
    "SoSe 2015",
    "WiSe 2015/2016",
    "SoSe 2016",
    "WiSe 2016/2017",
    "SoSe 2017",
    "WiSe 2017/2018",
    "SoSe 2018",
    "WiSe 2018/2019",
    "SoSe 2019",
    "WiSe 2019/2020",
    "SoSe 2020",
    "WiSe 2020/2021",
    "SoSe 2021",
    "WiSe 2021/2022",
    "SoSe 2022",
    "WiSe 2022/2023",
    "SoSe 2023",
    "WiSe 2023/2024",
]
HEADER_FIRST_LEVEL = ["", "", *["WiSe 2005/2006" for _ in range(len(SEMESTERS))]]
HEADER_SECOND_LEVEL = ["", "HF/NF", *["Fachsemester" for _ in range(len(SEMESTERS))]]
HEADER_THIRD_LEVEL = ["Subject", "", *SEMESTERS]
HEADER = [HEADER_FIRST_LEVEL, HEADER_SECOND_LEVEL,HEADER_THIRD_LEVEL]

def get_columns():
    return pd.MultiIndex.from_arrays(HEADER)

def preprocessData(fileAsStr: str) -> List[str]:
    """ removes unwanted data from the file

    Args:
        fileAsStr (str): csv file as string

    Returns:
        List[str]: data for different faculties
    """
    formattedData = []
    removeEmptyLines = re.sub(EMPTY_LINE_PATTERN, "", fileAsStr)
    removePageNumbers = re.sub(PAGE_NUMBER_PATTERN, "", removeEmptyLines)
    removeUniversityData = re.sub(REMOVE_PATTERN, "", removePageNumbers)
    splittedData = re.split(DELIMETER_PATTERN, removeUniversityData)
    splittedData = [re.sub(DELIMETER_PATTERN, "", data) for data in splittedData]
    
    
    for split in splittedData:
        formattedData.append(split)
    return formattedData[1:]

def cleanDataForFaculties(preprocessedData: List[str]) -> List[List[str]]:
    cleanedData = []
    for facultyData in preprocessedData:
        facultyData = re.sub(MULTIPLE_BLANKS_PATTERN," " ,facultyData)
        facultyData = re.sub(PAGE_NUMBER_PATTERN , "",facultyData)
        facultyData = re.sub(FACHSEMESTER_PATTERN,"Fachsemester",facultyData)
        # facultyData = re.sub(HF_PATTERN, "",facultyData)
        splittedData = [data for data in facultyData.split("\n") if not re.fullmatch(r'(?:\"|\s")', data)]
        cleanedData.append(splittedData)
    return cleanedData


def createPandasStructure(subjectData:List[str]) -> Dict[str, List[str]]:
    subject = subjectData[0]
    # only extract the numerical values 
    totalMainSubject = list(chain.from_iterable([data.split(" ")[1:] for data in subjectData if re.match(HF_PATTERN, data)]))[0:-1]
    totalMinorSubject = list(chain.from_iterable([data.split(" ")[1:] for data in subjectData if re.match(NF_PATTERN, data)]))[0:-1]
    
    #check fo empty Main and Minor subject
    if totalMainSubject == None or len(totalMainSubject) == 0:
        totalMainSubject = [0 for _ in range(len(SEMESTERS))]
    if totalMinorSubject == None or len(totalMinorSubject) == 0:
        totalMinorSubject = [0 for _ in range(len(SEMESTERS))]
        
    return [subject, "HF", *totalMainSubject], [subject, "NF", *totalMinorSubject]
    

def buildPandasDataFrame(preprocessedData: List[str]):
    # stores rows for pandas dataframe
    pandasFrameStructures = []
    for data in preprocessedData:
        # create row data for each subject
        mainSubjectFrame, minorSubjectFrame = createPandasStructure(data)
        
        pandasFrameStructures.append(mainSubjectFrame)
        pandasFrameStructures.append(minorSubjectFrame)
    return pandasFrameStructures
    
    
def __clean_excel_sheet(filename, sheet):
    excel_workbench = openpyxl.load_workbook(filename)
    excel_workbench.remove(excel_workbench[sheet])
    excel_workbench.create_sheet(sheet)
    excel_workbench.save(filename)

        
def parseSubsetData(filename: str, output_file) -> Dict[str, List[str]]:
    data = os.path.join(BASEDIR, filename)
    
    columns = get_columns()
    
    __clean_excel_sheet(output_file, "Sheet1")

    with open(data, "r") as file:
        dataAsString = file.read()
        preprocessedData = preprocessData(dataAsString)
        cleanedFacultyData = cleanDataForFaculties(preprocessedData)
        pandasData = buildPandasDataFrame(cleanedFacultyData)
        pandasFrame = pd.DataFrame(pandasData, columns=columns)
        
        pandasFrame.to_excel(output_file)
    
        
if __name__ == "__main__":
    filename = "statistik-ws-20232024-2.csv"
    parseSubsetData(filename, "output.xlsx")