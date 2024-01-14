import os
import subprocess
import matplotlib.pyplot as plt
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from exp import RandomForestRegressor as rfg


# Generate figures using python scripts 
def generate_figures():
    rfg.RandomForestRegressorPrediction()

# Compile LaTeX paper into PDF (if applicable)
def compile_paper():
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paper_tex_path = os.path.join(PROJECT_DIR,"doc/DataLiteracyStudentProject/samplePaper.tex")
    paper_pdf_path = os.path.join(PROJECT_DIR,"doc/DataLiteracyStudentProject/samplePaper.pdf")

    subprocess.run(['pdflatex', '-output-directory', os.path.dirname(paper_pdf_path), paper_tex_path])

if __name__ == "__main__":
    # Generate and save figures
    generate_figures()
    compile_paper()
