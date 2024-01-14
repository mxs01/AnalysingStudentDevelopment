"""Utilities to load data into a pandas DataFrame."""

import pandas as pd
from .constants import GRADUATES_PATH, STUDENTS_PATH, SALLARY_PATH, INFLATION_PATH


def getStudents() -> pd.DataFrame:
    """Load student data from excel file into a pandas DataFrame."""

    students = pd.read_excel(STUDENTS_PATH,
                             sheet_name='Sheet1',
                             index_col=[0, 1, 2],
                             header=[0, 2],)
    students.index = students.index.droplevel(0)
    return students


def getGraduates() -> pd.DataFrame:
    """Load graduates data from csv file into a pandas DataFrame."""

    graduates = pd.read_csv(
        GRADUATES_PATH,
        encoding="ISO-8859-1",
        sep=";",
        decimal=",",
        skiprows=4,
        header=[1, 2, 3],
        skipfooter=3,
        index_col=[0, 1],
        engine="python")
    return graduates


def getSallaries() -> pd.DataFrame:
    """Load sallary data from csv file into a pandas DataFrame."""

    sallaries = pd.read_csv(
        SALLARY_PATH,
        encoding="ISO-8859-1",
        sep=";",
        decimal=",",
        skiprows=5,
        header=[0, 1, 2, 3],
        skipfooter=4,
        index_col=[0, 1, 2, 3],
        engine="python")
    return sallaries


def getInflation() -> pd.DataFrame:
    """Load inflation data from csv file into a pandas DataFrame."""

    inflation = pd.read_csv(
        INFLATION_PATH,
        encoding="ISO-8859-1",
        sep=";",
        decimal=",",
        skiprows=4,
        header=[0, 1],
        index_col=[0],
        skipfooter=3,
        engine="python")
    return inflation
