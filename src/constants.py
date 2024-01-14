# Description: Constants used in the code
import os
import re

# paths
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "dat")
GRADUATES_PATH = os.path.join(DATA_DIR, "graduates_germany.csv")
SALLARY_PATH = os.path.join(DATA_DIR, "sallary_per_sector.csv")
STUDENTS_PATH = os.path.join(DATA_DIR, "student_data_per_subject.xlsx")
INFLATION_PATH = os.path.join(DATA_DIR, "inflation_germany.csv")


# REGEX Patterns
DELIMETER_PATTERN = re.compile(r".*\s*Studienfachbelegung nach Abschlusszielen")
REMOVE_PATTERN = re.compile(
    r'(?:\s*"EBERHARD KARLS UNIVERSITÄT"\s*|\s*"72074 Tübingen"\s*)|"Stand der Datenerhebung: \d{2}.\d{2}.\d{4}"|"Wintersemester \d{4} / \d{4}"|"ST.NR.S‐\d{3}‐\d{1,3}"')  # noqa: E501
EMPTY_LINE_PATTERN = re.compile(r'""\n')
PAGE_NUMBER_PATTERN = re.compile(r'" ‐ \d{0,3} ‐"')
MULTIPLE_BLANKS_PATTERN = re.compile(r"\s{2,}")
FACHSEMESTER_PATTERN = re.compile(r'Fachsemesterzahlen .+')
HF_PATTERN = re.compile(r'"(Ges|Summe)(\.|\s)HF.*"')
NF_PATTERN = re.compile(r'"(Ges|Summe)(\.|\s)NF.*"')

# Constants
SEMESTERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", ">12"]
YEARS = [
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
    "SoSe 2011",
    "WiSe 2011/2012",
    "SoSe 2012",
    "WiSe 2012/2013",
    "SoSe 2013",
    "WiSe 2013/2014",
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

