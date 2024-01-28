"""Utilities to load data into a pandas DataFrame."""

import pandas as pd
import numpy as np
from .constants import GRADUATES_PATH, STUDENTS_PATH, SALARY_PATH, INFLATION_PATH, SEMESTERS
import os 


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

    graduatesInBW = pd.read_csv(GRADUATES_PATH,
                                sep=";",
                                thousands=".",
                                skiprows=1,
                                header=[0, 1],
                                skipfooter=10,
                                index_col=0,
                                na_values=["."],
                                engine="python")
    # Flatten data anamoly due to shift from G9 to G8 in 2012
    newVal = (graduatesInBW.loc[2011, ('Abiturienten insg', 'Anzahl')] + graduatesInBW.loc[2013, ('Abiturienten insg', 'Anzahl')]) / 2
    diff = graduatesInBW.loc[2012, ('Abiturienten insg', 'Anzahl')] - newVal
    graduatesInBW.loc[2012, ('Abiturienten insg', 'Anzahl')] = newVal + diff / 4
    graduatesInBW.loc[2013, ('Abiturienten insg', 'Anzahl')] += diff / 4
    graduatesInBW.loc[2014, ('Abiturienten insg', 'Anzahl')] += + diff / 4
    graduatesInBW.loc[2015, ('Abiturienten insg', 'Anzahl')] += + diff / 4
    return graduatesInBW


def getSalaries() -> pd.DataFrame:
    """Load salary data from csv file into a pandas DataFrame."""

    salaries = pd.read_csv(
        SALARY_PATH,
        encoding="ISO-8859-1",
        sep=";",
        decimal=",",
        skiprows=5,
        header=[0, 1, 2, 3],
        skipfooter=4,
        index_col=[1, 2, 3],
        engine="python")
    return salaries.drop(salaries.columns[0], axis=1)


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


def getBruttoSalary(sector) -> np.array:
    salaries = getSalaries()    
    SALARY_YEARS = salaries.index.levels[1]
    QUARTALS = ['1. Quartal', '2. Quartal', '3. Quartal', '4. Quartal']

    bruttoSalaryNP = salaries.loc[(sector, SALARY_YEARS, QUARTALS), ('Insgesamt', 'Insgesamt', 'Durchschnittliche Bruttomonatsverdienste', 'EUR')].to_numpy(dtype=int) # noqa: E501
    bruttoSalaryMeanForYears = bruttoSalaryNP.reshape(-1, 2).mean(axis=1)
    bruttoSalary = bruttoSalaryMeanForYears.reshape(-1,30).mean(axis=0)
    return bruttoSalary


def getGraduatesInBwFor(years: list) -> np.array:
    graduates = getGraduates()
    graduatesInBW = graduates.loc[years, ('Abiturienten insg', 'Anzahl')].to_numpy()
    return graduatesInBW.astype(float)


def getAllGraduatesYears() -> list[str]:
    graduates = getGraduates()
    return graduates.index.tolist()


def getInflationAdjustedBruttoSalary(sector) -> np.array:
    inflation = getInflation()
    inflation = inflation.loc[:, ('Veränderungsrate zum Vorjahr', 'Prozent')].to_numpy(dtype=float)

    bruttoSalary = getBruttoSalary(sector)

    cummulativeInflation = np.cumprod(1 + inflation / 100)
    print('Create cummulative inflation:')
    for a, b in zip(inflation, cummulativeInflation):
        print(f'{a} -> {b}')

    print('\nAdjust salary for inflation:')
    bruttoInflationSalary = bruttoSalary / cummulativeInflation.repeat(2)
    for a, b in zip(bruttoSalary, bruttoInflationSalary):
        print(f'{a} -> {b}')
    return bruttoInflationSalary


def getInflationAdjustedBruttoSalaries(sectors: list) -> np.array:
    inflation = getInflation()
    inflation = inflation.loc[:, ('Veränderungsrate zum Vorjahr', 'Prozent')].to_numpy(dtype=float)
    
    cummulativeInflation = np.cumprod(1 + inflation / 100)
    print('Create cummulative inflation:')
    for a, b in zip(inflation, cummulativeInflation):
        print(f'{a} -> {b}')

    # Initialize an array to store the sum of salaries for all sectors
    sum_bruttoInflationSalary = np.zeros_like(cummulativeInflation).repeat(2)

    # Iterate over each sector and sum the inflation-adjusted salaries
    for sector in sectors:
        bruttoSalary = getBruttoSalary(sector)
        bruttoInflationSalary = bruttoSalary / cummulativeInflation.repeat(2)
        sum_bruttoInflationSalary += bruttoInflationSalary  # Sum the salaries
        print('\nAdjust salary for inflation:')
        for a, b in zip(bruttoSalary, bruttoInflationSalary):
            print(f'{a} -> {b}')

    # Calculate the average inflation-adjusted salary
    avg_bruttoInflationSalary = sum_bruttoInflationSalary / len(sectors)

    return avg_bruttoInflationSalary




