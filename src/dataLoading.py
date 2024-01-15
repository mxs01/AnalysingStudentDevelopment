"""Utilities to load data into a pandas DataFrame."""

import pandas as pd
import numpy as np
from .constants import GRADUATES_PATH, STUDENTS_PATH, SALLARY_PATH, INFLATION_PATH, SEMESTERS


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


def getAllCourses() -> list:
    """Get all courses from student data."""

    students = getStudents()
    return students.index.levels[0].tolist()


def getTotalStudentsFor(courses: list, years: list[str]) -> np.array:
    students = getStudents()

    studentsInCourseHF = np.empty((len(courses), 0))

    for year in years:
        data_for_year = students.loc[(courses, 'HF'), (year, SEMESTERS)].to_numpy(dtype=int).sum(axis=1)
        data_for_year = data_for_year.reshape((len(courses), 1))
        studentsInCourseHF = np.hstack((studentsInCourseHF, data_for_year))

    studentsInCourseNF = np.empty((len(courses), 0))

    for year in years:
        data_for_year = students.loc[(courses, 'NF'), (year, SEMESTERS)].to_numpy(dtype=int).sum(axis=1)
        data_for_year = data_for_year.reshape((len(courses), 1))
        studentsInCourseNF = np.hstack((studentsInCourseNF, data_for_year))

    return studentsInCourseHF.sum(axis=0) + studentsInCourseNF.sum(axis=0)


def getBruttoSallary(sector) -> np.array:
    sallaries = getSallaries()
    SALLARY_YEARS = sallaries.index.levels[2]
    QUARTALS = ['1. Quartal', '2. Quartal', '3. Quartal', '4. Quartal']

    bruttoSallary = sallaries.loc[(sector[0], sector[1], SALLARY_YEARS, QUARTALS), ('Insgesamt', 'Insgesamt', 'Durchschnittliche Bruttomonatsverdienste', 'EUR')].to_numpy(dtype=int)  # noqa: E501
    bruttoSallary = bruttoSallary.reshape(-1, 2)
    return bruttoSallary.mean(axis=1)


def getGraduatesInBwFor(years: list) -> np.array:
    graduates = getGraduates()
    graduatesInBW = graduates.loc[('Insgesamt', years), ('Baden-Württemberg', 'Absolventen und Abgänger', 'Anzahl')].to_numpy()
    graduatesInBW = np.where(graduatesInBW == '-', np.nan, graduatesInBW)
    return graduatesInBW.astype(float)


def getAllGraduatesYears() -> list[str]:
    graduates = getGraduates()
    return graduates.index.levels[1].tolist()


def getInflationAdjustedBruttoSallary(sector) -> np.array:
    inflation = getInflation()
    inflation = inflation.loc[:, ('Veränderungsrate zum Vorjahr', 'Prozent')].to_numpy(dtype=float)

    bruttoSallary = getBruttoSallary(sector)

    cummulativeInflation = np.cumprod(1 + inflation / 100)
    print('Create cummulative inflation:')
    for a, b in zip(inflation, cummulativeInflation):
        print(f'{a} -> {b}')

    print('\nAdjust sallary for inflation:')
    bruttoInflationSallary = bruttoSallary / cummulativeInflation.repeat(2)
    for a, b in zip(bruttoSallary, bruttoInflationSallary):
        print(f'{a} -> {b}')
    return bruttoInflationSallary
