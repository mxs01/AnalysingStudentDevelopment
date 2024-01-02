# Description: Constants used in the code
import os

BASE_DIR = os.path.abspath("/Users/maxschnitt/Documents/AnalysingStudentDevelopment")
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRADUATES_DIR = os.path.join(PROJECT_DIR, "data/graduates_germany.csv")
PLOT_DIR = os.path.join(BASE_DIR, "plots")
