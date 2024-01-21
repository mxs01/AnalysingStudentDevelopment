# Analysing Student Development

This project utilizes a Vector Autorregressive Model (VAR) to predict the amount of students enrolled at the [University of Tübingen](https://uni-tuebingen.de) for specified courses, based on three different time-series datasets:
- [past enrolled students](https://uni-tuebingen.de/einrichtungen/verwaltung/iv-studierende/studierendenabteilung/statistiken/) at Eberhard Karls University Tuebingen
- [salary expectations](https://www.statistik-bw.de/BildungKultur/SchulenAllgem/LRt0302.jsp) in certain sectors
- [high-school graduates in BW](https://www-genesis.destatis.de/genesis//online?operation=table&code=62321-0001&bypass=true&levelindex=0&levelid=1702307320529#abreadcrumb)

## Get started
### Overview
The project uses the following structure.
```
.
├── dat
│   └── <Raw data>
├── doc
│   └── DataLiteracyStudentProject
│       ├── paper.pdf
│       └── paper.tex
├── exp
│   └── <Experiments notebooks>
├── src
│   └── <Small helper functions>
├── README.md
├── conda_env.yml
├── install_env.sh
└── run_notebooks.py
```

### Installation
To get started follow these steps:
#### 1. Install conda
This project uses [conda](https://conda.io/projects/conda/en/latest/index.html) as the package manager. Make sure you have conda installed on your system.
You can verify that by running `conda -V` in your terminal. It should print your current version installed.
```sh
% conda -V
conda 23.11.0
```
If the comand fails, please install conda using this [guide](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).


#### 2. Install environment
To set up the environment needed, run the `install_env.sh` script in your terminal. This process can take a while.
When the script finishes you should see this in your terminal.
```sh
% ./install_env.sh
...
done
#
# To activate this environment, use
#
#     $ conda activate data_literacy
#
# To deactivate an active environment, use
#
#     $ conda deactivate
```

#### 3. Activate environment
All that's left is activating the environment.
```sh
% conda activate data_literacy
```
You are now all set 🚀.

#### Notes
To deactivate the environemnt, use: `conda deactivate`.

If you want to delete the added conda environment from your system, you can run `conda remove -n data_literacy --all`.

`conda env list` lists all your environments. Note the `*` symbol next to the currently active env.

## tbd