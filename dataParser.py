import os
import re
import pandas as pd
from typing import List, Dict

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
HF_PATTERN = re.compile(r'"Ges\.HF."*')
NF_PATTERN = re.compile(r'"Ges\.NF.*"')

# Constants
HEADER = []
HEADER_FIRST_LEVEL = []
HEADER_SECOND_LEVEL = []


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
        facultyData = re.sub(HF_PATTERN, "",facultyData)
        splittedData = [data for data in facultyData.split("\n") if not re.fullmatch(r'(?:\"|\s")', data)]
        cleanedData.append(splittedData)
    return cleanedData


def createPandasStructure(subjectData:List[str]) -> Dict[str, List[str]]:
    pandasDataFrame = []
    subject = subjectData[0]
    totalMainSubject = [data for data in subjectData if re.match(HF_PATTERN, data)]
    totalMinorSubject = [data for data in subjectData if re.match(NF_PATTERN, data)]
    
    
    return pandasDataFrameStructure

def buildPandasDataFrame(preprocessedData: List[str]):
    pandasFrameStructures = []
    for data in preprocessedData:
        pandasStructure = createPandasStructure(data)
        pandasFrameStructures.append(pandasStructure)
    return

        
def parseSubsetData(filename: str) -> Dict[str, List[str]]:
    data = os.path.join(BASEDIR, filename)

    with open(data, "r") as file:
        dataAsString = file.read()
        preprocessedData = preprocessData(dataAsString)
        cleanedFacultyData = cleanDataForFaculties(preprocessedData)
        buildPandasDataFrame(cleanedFacultyData)
   
       
        
        
if __name__ == "__main__":
    filename = "statistik-ws-20232024-2.csv"
    parseSubsetData(filename)