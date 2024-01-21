import os
import subprocess
from src.constants import EXP_DIR

# get a list of all notebooks in the experiments directory
notebooks = [f for f in os.listdir(EXP_DIR) if f.endswith('.ipynb')]

# iterate over each notebook and execute it
for notebook in notebooks:
    print(f"\nRunning {notebook}...\n\n")
    subprocess.check_call(["jupyter", "nbconvert", "--execute", "--inplace", os.path.join(EXP_DIR, notebook)])
